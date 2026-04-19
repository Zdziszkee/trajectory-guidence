Bartosz Dziuba BMD223 hehe4616
Kacper Kuchta Zdziszkee Zdziszkee

# miniproject - Sterowanie trajektorią w modelach generatywnych

Celem dzisiejszych zajęć jest poznanie metod sterowania trajektorią w procesie generacji dla modeli dyfuzyjnych oraz opartych na Flow Matching. Podczas zajęć zapoznamy się z klasycznymi i nowymi podejściami do modyfikacji powstawania obrazu i redukcji artefaktów.

Repozytorium zawiera pliki:
- `wstep.ipynb` -- teoretyczne wprowadzenie do problematyki sterowania trajektorią, roli wieloetapowego procesu odszumiania oraz podstawowych technik (m.in. CFG, SDEdit).
- `geoguide.ipynb` -- opis zasady działania algorytmu GeoGuide (Geometryczne Sterowanie Trajektorią).
- `diamond.ipynb` -- omówienie DIAMOND do unikania zniekształceń anatomicznych i wizualnych w najnowszych modelach typu Flow Matching.
- `requirements.txt` -- zestaw potrzebnych bibliotek do uruchomienia kodu.

Projekt wykorzystuje również dodatkowe repozytoria pobierane bezpośrednio wewnątrz notatników:
- [GeoGuide](https://github.com/mateuszpoleski/geoguide) (klonowane w `geoguide.ipynb`)
- [DIAMOND](https://github.com/gmum/DIAMOND) (klonowane w `diamond.ipynb`)

## Konfiguracja środowiska

Aby przygotować środowisko, należy zainstalować niezbędne biblioteki z pliku `requirements.txt`. Zaleca się przygotowanie wcześniej wirtualnego środowiska:

Stwórz środowisko za pomocą `venv`:
```bash
$ python3.9 -m venv .venv
```
lub z użyciem `conda`:
```bash
$ conda create -n .venv python=3.9.9
```

zainstaluj niezbędne biblioteki:
```bash
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Informacje dodatkowe

Zainteresowanym polecamy zapoznać się ze źródłami podanymi w bibliografii poniżej, aby w pełni opanować mechanizmy działania algorytmów SDE, Classifier-Free Guidance oraz metod z obszaru modeli generatywnych.

## Źródła:

Repozytorium zostało stworzone na podstawie oraz warto zwrócić uwagę na:<br/> 
[1] [https://sander.ai/2022/05/26/guidance.html](https://sander.ai/2022/05/26/guidance.html) - podstawy cfg (dostęp: 19.04.2026)<br/>
[2] [https://softwaremill.com/classifier-free-diffusion-model-guidance/](https://softwaremill.com/classifier-free-diffusion-model-guidance/) (dostęp: 19.04.2026)<br/>
[3] [https://sde-image-editing.github.io/](https://sde-image-editing.github.io/) - podstawy sde (dostęp: 19.04.2026)<br/>
[4] [https://arxiv.org/abs/2602.00883](https://arxiv.org/abs/2602.00883) - diamond - sota redukcja artefaktów (dostęp: 19.04.2026)<br/>
[5] [https://arxiv.org/html/2604.05761v1](https://arxiv.org/html/2604.05761v1) - x0 supervision sota training based (dostęp: 19.04.2026)<br/>
[6] [https://github.com/FlowChef/flowchef](https://github.com/FlowChef/flowchef) - sota inference time (dostęp: 19.04.2026)<br/>
[7] [https://www.cs.utexas.edu/~lqiang/rectflow/html/intro.html](https://www.cs.utexas.edu/~lqiang/rectflow/html/intro.html) - rectified flow (dostęp: 19.04.2026)<br/> 
