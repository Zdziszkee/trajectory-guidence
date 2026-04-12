from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip() + "\n",
    }


cells = [
    md(r"""
# Sterowanie trajektorią w modelach generatywnych

Ten notebook jest rozdziałem dydaktycznym. Nie opisuje jednego algorytmu, tylko wspólny sposób myślenia o całej rodzinie metod z `DOCS.md`: guidance, diffusion, DIAMOND, FlowChef i x0-supervision. Główna teza jest prosta: w modelach generatywnych nie steruje się wyłącznie wynikiem końcowym. Steruje się całym przebiegiem generacji, czyli trajektorią.

Najpierw trzeba więc zrozumieć sam pipeline. Dopiero potem można sensownie mówić o sterowaniu. W praktyce pipeline generatywny wygląda jak wieloetapowa linia produkcyjna:

```text
warunek / input
   │
   ├─ tekst, maska, pose, depth, bbox, reward
   │
   ▼
enkoder / adapter / conditioning
   │
   ▼
stan startowy
   │
   ├─ czysty szum x_T
   ├─ zaszumiony obraz x_t
   └─ inny latent zgodny z zadaniem
   │
   ▼
pętla denoisingu / transportu
   │
   ├─ x_T → x_{T-1} → ... → x_0
   └─ w każdym kroku można interweniować
   │
   ▼
dekoder / renderer
   │
   ▼
wynik
```

To właśnie w tej pętli dzieje się wszystko, co najważniejsze. Prompt nie „tworzy obrazu” sam z siebie. Prompt jest tylko jednym z sygnałów, które model czyta podczas kolejnych kroków. Maska nie jest obrazem końcowym. Jest mapą tego, co wolno zmieniać. Reward nie jest wynikiem. Jest wskazaniem, w którą stronę trajektoria ma być odchylona. Z kolei szum początkowy nie jest tylko losowym seedem. Jest punktem startowym całej drogi.

W tym sensie sterowanie trajektorią nie jest jednym mechanizmem. Jest rodziną punktów wpięcia do pipeline’u. Najważniejsze z nich to:

| etap pipeline’u | pytanie | co kontrolujemy |
|---|---|---|
| wejście / conditioning | co model ma wiedzieć? | prompt, maska, pose, depth, reward |
| start trajektorii | skąd model ma ruszyć? | czysty szum, obraz częściowo zaszumiony, latent |
| denoising loop | jak ma iść dalej? | guidance, correction, steering, scheduler |
| uczenie | czego model ma się nauczyć? | epsilon, x0, weighting, supervision |

To rozróżnienie jest kluczowe. Część metod steruje wejściem, część steruje każdym krokiem, a część steruje samym celem uczenia. Dla użytkownika wszystko może wyglądać jak „lepsza generacja”, ale od strony mechanizmu to zupełnie inne rzeczy. Dlatego w dalszej części notebooka najpierw rozbijamy pipeline na intuicyjne elementy, a dopiero potem przechodzimy do CFG, SDE, DIAMOND, FlowChef i x0-supervision.

Najprostsza intuicja brzmi tak: wczesne kroki budują strukturę globalną, późne kroki dopracowują szczegóły. Jeżeli model ma dobrze ustawić obiekty w scenie, to sterowanie musi działać wcześnie. Jeżeli ma tylko poprawić drobny fragment, to sterowanie może być lokalne. Jeżeli ma respektować obserwację, to trajektoria musi być częściowo zakotwiczona. Jeżeli ma unikać artefaktów, to trzeba reagować zanim artefakt się utrwali. Wszystkie omawiane metody są odpowiedziami na to samo pytanie: gdzie w pipeline’ie należy wprowadzić kontrolę, żeby nie zniszczyć priory modelu, a jednocześnie uzyskać dokładnie to, czego chcemy.
"""),
    md(r"""
## 2. Classifier-free guidance i SDE: dwa fundamenty myślenia o sterowaniu

Jeżeli pipeline jest linią produkcyjną, to CFG jest kierownicą, a SDE jest samą drogą, po której jedziemy. CFG mówi, jak mocno odchylić trajektorię w stronę warunku. SDE mówi, dlaczego trajektoria w ogóle ma postać stopniowego odszumiania i skąd bierze się jej wieloetapowy charakter. Te dwie idee są fundamentem całego dalszego notebooka.

### 2.1 CFG: guidance jako sterowanie kierunkiem

Najważniejsza intuicja w classifier-free guidance jest bardzo prosta. Ten sam model potrafi odpowiedzieć na pytanie „co generować?” w dwóch wersjach: z warunkiem i bez warunku. W czasie samplingu nie wybieramy jednej z nich. Mieszamy je, wzmacniając różnicę między nimi. W zapisie praktycznym:

$$
\hat\epsilon_{cfg} = \epsilon_{uncond} + \gamma\, (\epsilon_{cond} - \epsilon_{uncond}).
$$

To nie jest nowy model. To jest reguła prowadzenia tego samego modelu. Gdy `\gamma` rośnie, model bardziej „słucha” warunku. Gdy `\gamma` maleje, model wraca do własnego prioru. CFG jest więc najprostszą formą sterowania trajektorią: każdemu krokowi przypisujemy większą lub mniejszą siłę odchylającą.

Najlepiej myśleć o tym jak o jeździe z mapą. Bez CFG model jedzie „na wyczucie” własnego rozkładu. Z CFG dostaje mapę, która wskazuje kierunek. Jeśli mapa jest zbyt słaba, cel może zostać tylko częściowo osiągnięty. Jeśli jest zbyt silna, ruch staje się sztywny i mniej naturalny. W praktyce widać to natychmiast: przy wyższym guidance prompt jest lepiej respektowany, ale obraz bywa mniej różnorodny i bardziej podatny na przeostrzenie.

To dlatego CFG jest tak ważne pedagogicznie. Pokazuje, że kontrola trajektorii nie jest subtelnym dodatkiem. Jest realnym wektorem siły dodanym do denoisingu. I pokazuje też pierwszy wielki kompromis: zgodność z warunkiem kontra swoboda generacji.

Typowy przykład to text-to-image. Jeżeli prosimy o „czerwone krzesło przy oknie”, to przy niskim guidance model może wygenerować poprawny styl, ale zgubić dokładną lokalizację. Przy wysokim guidance lepiej trzyma się instrukcji, ale może zacząć nadmiernie upraszczać albo zbyt mocno dociążać scenę jednym rozwiązaniem. Dokładnie to samo dzieje się przy kontrolach strukturalnych, tylko bardziej wyraźnie: maska, pose czy segmentation map wymagają, by trajektoria od początku szła we właściwych granicach.

W formie obrazkowej wygląda to tak:

```text
      model bez warunku
            ────────────────┐
                             │
                             ▼
                        mieszanie
                             ▲
                             │
      model z warunkiem
      ───────────────────────┘
                         │
                         ▼
                 następny krok trajektorii
```

### 2.2 SDE: dlaczego generacja jest procesem, a nie skokiem

SDE wyjaśnia, skąd bierze się sama trajektoria. W diffusion nie zaczynamy od gotowego obrazu. Zaczynamy od stanu zaszumionego i stopniowo odtwarzamy strukturę. Najprostszy zapis to

$$
x_t = \alpha_t x_0 + \sigma_t \epsilon.
$$

To równanie warto czytać bez nadmiaru formalizmu. `x_0` to czysta próbka, `\epsilon` to szum, `\alpha_t` mówi, ile czystego sygnału jeszcze zostało, a `\sigma_t` mówi, ile chaosu zostało dodane. Gdy `t` rośnie, sygnał zanika. Gdy `t` maleje, sygnał wraca. Reverse process jest po prostu próbą przejścia z powrotem od stanu trudnego do stanu czytelnego.

W języku ciągłym zapis wygląda jak SDE:

$$
dx_t = f(x_t,t)\,dt + g(t)\,dW_t.
$$

Ważne jest jednak nie samo równanie, lecz intuicja: model nie „rysuje obrazu od razu”. Model idzie przez serię stanów pośrednich. Każdy stan jest trochę mniej chaotyczny niż poprzedni. Każdy krok usuwa część niepewności. To dlatego diffusion jest naturalnym środowiskiem dla sterowania trajektorią. Skoro sam proces jest wieloetapowy, można do niego wprowadzać kontrolę po drodze.

SDEdit jest tu najlepszym przykładem. Jeśli chcemy edytować obraz, nie musimy go niszczyć i odtwarzać od zera. Możemy zrobić coś bardziej subtelnego: dodać do niego kontrolowaną ilość szumu, tak aby zniknęły lokalne defekty, ale globalna struktura została zachowana. Potem uruchamiamy denoising i pozwalamy modelowi odzyskać szczegóły. To działa dlatego, że trajektoria zaczyna się już blisko sensownego punktu w przestrzeni stanów.

Można to zapisać jako bardzo prosty mentalny diagram:

```text
czysty obraz → dodanie szumu → stan pośredni → odszumianie → edycja / rekonstrukcja
```

Z tego wynika najważniejsza lekcja: SDE nie jest tylko formalizmem matematycznym. Jest sposobem myślenia o edycji i kontroli. Jeżeli masz możliwość rozpoczęcia trajektorii w odpowiednim miejscu, możesz już na starcie ustawić, jak dużo struktury ma zostać zachowane. Jeżeli masz możliwość wpływania na kolejne kroki, możesz sterować nie tylko semantyką, ale także stabilnością i naturalnością generacji.

CFG i SDE razem tworzą fundament. CFG mówi, jak sterować kierunkiem. SDE mówi, dlaczego ten kierunek jest rozłożony w czasie i dlaczego można nim zarządzać krok po kroku. To wystarcza, aby zrozumieć, czemu późniejsze metody są możliwe: one po prostu wybierają inne miejsce w pipeline’ie, w którym da się wprowadzić dodatkową wiedzę.
"""),
    md(r"""
## 3. DIAMOND: sterowanie trajektorią po to, by nie wejść w obszar artefaktów

Po zrozumieniu CFG i SDE łatwo zobaczyć, dlaczego DIAMOND jest logicznym kolejnym krokiem. W flow matching i rectified flow trajektoria bywa prostsza niż w diffusion, ale to nie znaczy, że jest wolna od błędów. Przeciwnie: jeśli model zacznie odchylać się w złą stronę, błąd może utrwalić się bardzo wcześnie i później wręcz „zamrozić” w wyniku końcowym. W obrazach oznacza to artefakty: zniekształcone dłonie, nieprawidłową anatomię, powtarzające się struktury, nienaturalne tekstury albo błędne relacje przestrzenne.

DIAMOND odpowiada na ten problem bardzo konkretnie: zamiast naprawiać wynik po zakończeniu generacji, kieruje inferencję w trakcie drogi. To ważna różnica. Post-hoc filtering widzi już tylko gotowy rezultat. DIAMOND widzi trajektorię, czyli moment, w którym błąd dopiero zaczyna się formować. Dzięki temu można odchylić ruch zanim problem się utrwali.

Intuicja jest następująca. Na każdym kroku mamy stan `x_t`. Z tego stanu można zbudować estymatę czystej próbki `\hat x_0`. Ta estymata nie musi być idealna, ale jest wystarczająco dobra, by ocenić ryzyko. Jeśli `\hat x_0` wygląda na zbliżające się do obszaru artefaktów, kolejny krok powinien zostać zmodyfikowany. Innymi słowy: nie czekamy na katastrofę na końcu, tylko korygujemy kierunek w środku drogi.

W bardzo uproszczonym obrazie wygląda to tak:

```text
x_t → estymata x_0 → ocena jakości → korekta kierunku → x_{t-1}
```

DIAMOND jest więc metodą directed inference. Nie chodzi o to, by zmieniać model po treningu. Nie chodzi o to, by budować nowy decoder. Nie chodzi nawet o dodatkową optymalizację całego obrazu. Chodzi o to, by użyć istniejącego modelu bardziej świadomie. To jest dokładnie ten sam duch, który stoi za guidance, ale tu nacisk pada na jakość lokalnej trajektorii, a nie na zgodność semantyczną.

To rozróżnienie jest bardzo ważne pedagogicznie. W guideance pytamy: „czy model podąża w stronę właściwego warunku?”. W DIAMOND pytamy: „czy model nie wchodzi w obszar, z którego trudno się wydostać?”. To są dwa różne pytania. Pierwsze dotyczy pożądanej treści. Drugie dotyczy jakości samej drogi. Oba są konieczne, bo generacja może być semantycznie poprawna, a zarazem wizualnie zła.

W praktyce DIAMOND jest szczególnie sensowny tam, gdzie model już jest mocny semantycznie, ale nadal produkuje artefakty. Wtedy retrening nie zawsze jest najlepszą odpowiedzią. Jeśli problem jest inferencyjny, najlepsza poprawka też powinna być inferencyjna. Z tej perspektywy DIAMOND jest bardzo elegancki: wykorzystuje gotowy prior i tylko prowadzi go ostrożniej.

W całym notebooku DIAMOND pełni więc rolę pomostu. Pokazuje, że sterowanie trajektorią nie służy wyłącznie do „bardziej posłusznej” generacji. Służy też do ochrony jakości. To naturalnie prowadzi do FlowChef, gdzie sterowanie przestaje być tylko obroną przed artefaktami, a staje się narzędziem do rozwiązywania konkretnych zadań edycyjnych i inverse problems.
"""),
    md(r"""
## 4. FlowChef: gdy trajektoria ma respektować obserwację, a nie tylko prompt

FlowChef idzie o krok dalej niż DIAMOND. DIAMOND chroni trajectory quality. FlowChef używa tej samej idei do sterowania zadaniem. W repozytorium metoda jest opisana jako steering rectified flow models in the vector field for controlled image generation. Najważniejsze słowa to tutaj: inversion-free, gradient-free i training-free. Oznacza to, że nie musimy odwracać całego procesu przez osobny optimization loop, nie musimy liczyć gradientów względem obrazu i nie musimy trenować nowej sieci dla każdej nowej instrukcji.

To jest szczególnie ważne w image editing i inverse problems, gdzie użytkownik nie chce po prostu „ładnej próbki”. Chce próbki zgodnej z obserwacją. Czasem chce zachować część obrazu i zmienić tylko lokalny region. Czasem chce odtworzyć obraz z niepełnych danych. Czasem chce poprawić rozdzielczość, usunąć rozmycie albo uzupełnić brakujący fragment. W każdym z tych zadań model musi jednocześnie respektować ograniczenie i korzystać z własnego prioru.

Najlepiej myśleć o FlowChef jako o prowadzeniu trajektorii po korytarzu. Jedna ściana korytarza to obserwacja: maska, pomiar, input image, sygnał częściowo zachowany. Druga ściana to prior generatywny: wszystko to, czego model nauczył się o naturalnych obrazach. FlowChef ma przeprowadzić trajektorię między tymi ścianami tak, aby wyjście było zarówno realistyczne, jak i zgodne z zadaniem.

W uproszczonym diagramie wygląda to tak:

```text
obserwacja / maska / pomiar
          │
          ▼
   kotwica trajektorii
          │
          ▼
sterowanie polem wektorowym
          │
          ▼
uzupełnienie braków / edycja / rekonstrukcja
```

To od razu pokazuje, czym FlowChef różni się od zwykłego generowania. Zwykły sampler nie wie, które fragmenty obrazu mają pozostać takie same. FlowChef prowadzi trajektorię tak, by ta wiedza była zachowana. Dzięki temu dobrze pasuje do inpaintingu, super-resolution, deblurring i podobnych zadań. To nie jest tylko „lepszy prompt”. To jest kontrola strukturalna.

Dobrym punktem odniesienia jest SDEdit. Tam zaczynamy od częściowo zaszumionego obrazu i pozwalamy modelowi go odtworzyć. FlowChef idzie dalej, bo nie polega tylko na odpowiednim punkcie startu. Prowadzi cały wektor przepływu, a więc może reagować w trakcie drogi. To oznacza większą elastyczność przy zachowaniu wysokiej jakości priory.

Na tle `DOCS.md` warto też pamiętać o Diff2Flow. Ten kierunek pokazuje, że diffusion i flow matching można ze sobą spiąć przez odpowiednie rescaling timestepów i alignment interpolantów. Dla tego notebooka to ważna lekcja, bo oznacza, że język trajectory steering nie jest specyficzny dla jednego modelu. Jest wspólny dla diffusion, flow matching i rectified flow. FlowChef korzysta właśnie z tej wspólnej geometrii.

W praktyce można podsumować to tak: DIAMOND mówi „nie wchodź w obszar artefaktów”. FlowChef mówi „utrzymaj obserwację i dojedź do rozwiązania”. Jeden chroni jakość drogi. Drugi wykorzystuje drogę do spełnienia zadania. Oba jednak opierają się na tym samym założeniu: jeśli model ma mocny prior, to najlepiej sterować jego trajektorią, a nie wymyślać wszystko od nowa.
"""),
    md(r"""
## 5. x0-supervision: czego model ma się naprawdę nauczyć

Ostatni temat dotyczy treningu, nie samej inferencji. To ważne, bo sterowanie trajektorią nie zaczyna się dopiero w samplerze. Zaczyna się już w tym, co model uznaje za dobry sygnał uczenia. Papier o x0-supervision pokazuje, że w controllable generation często lepiej jest nadzorować czysty obraz `x_0` niż sam szum `\epsilon`. To z pozoru niewielka zmiana, ale w praktyce wpływa na szybkość zbieżności i na to, jak model uczy się globalnej struktury.

W diffusion stan pośredni ma postać

$$
x_t = \alpha_t x_0 + \sigma_t \epsilon.
$$

Z tej relacji da się odtworzyć czysty obraz z predykcji szumu:

$$
\hat x_0 = \frac{x_t - \sigma_t\,\epsilon_\theta(x_t,t)}{\alpha_t}.
$$

Ale istota problemu nie leży w algebrze, tylko w ważeniu gradientów. Epsilon-loss automatycznie osłabia sygnał z kroków o niskim SNR, a to właśnie te kroki odpowiadają za globalny układ sceny. Można to zapisać jako zależność między lossami:

$$
\mathcal L^{\epsilon}_\theta \propto \frac{\alpha_t^2}{\sigma_t^2}\,\mathcal L^{x_0}_\theta.
$$

W praktyce oznacza to, że przy dużym poziomie szumu model słabiej uczy się tego, co powinno być najważniejsze w controllable generation: layoutu, geometrii, rozmieszczenia obiektów i stabilnej kompozycji. X0-supervision poprawia ten stan rzeczy, bo bezpośrednio premiuje odtworzenie czystej próbki, a więc dokładnie tego, co na końcu chcemy odzyskać.

To jest szczególnie ważne w metodach kontrolowanych przez strukturę, takich jak ControlNet, T2I-Adapter, OminiControl czy podobne systemy. Jeżeli warunek mówi o układzie przestrzennym, to trening powinien kłaść nacisk właśnie na te kroki, w których układ powstaje. W przeciwnym razie model będzie uczył się wolniej i mniej stabilnie. X0-supervision usuwa tę niezgodność między zadaniem a losssem.

Pedagogicznie można to ująć jednym zdaniem: jeśli chcesz sterować trajektorią w czasie inferencji, musisz najpierw nauczyć modelu, co jest prawidłowym celem w czasie treningu. X0-supervision robi dokładnie to. Dlatego kończymy na nim ten notebook. Jest to bowiem naturalny kontrapunkt dla CFG, SDE, DIAMOND i FlowChef: nie tylko pytanie „jak prowadzić trajektorię?”, ale też pytanie „czego trajektoria ma się nauczyć być poprawnym wynikiem?”.

### Krótkie podsumowanie roli metod

| metoda | co kontroluje | kiedy działa |
|---|---|---|
| CFG | kierunek denoisingu | w czasie samplingu |
| SDE / SDEdit | korupcję i odtwarzanie stanu | w trakcie procesu generacji |
| DIAMOND | wejście w obszary artefaktów | podczas inferencji |
| FlowChef | zgodność trajektorii z obserwacją | podczas inferencji dla edit/inverse problems |
| x0-supervision | to, co model uznaje za właściwy sygnał | w czasie treningu |

To podsumowanie dobrze pokazuje wspólny rdzeń notebooka. Wszystkie metody są o trajektorii, ale każda w innym miejscu pipeline’u. Jedne sterują kierunkiem. Inne sterują punktem startu. Jeszcze inne chronią jakość, respektują obserwację albo zmieniają loss tak, aby model uczył się właściwego priorytetu. Razem tworzą jedną spójną teorię praktycznego sterowania generacją.
"""),
]


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.14",
            "mimetype": "text/x-python",
            "codemirror_mode": {"name": "ipython", "version": 3},
            "pygments_lexer": "ipython3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def main() -> None:
    out = Path("sterowanie_trajektoria_od_podstaw.ipynb")
    out.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
