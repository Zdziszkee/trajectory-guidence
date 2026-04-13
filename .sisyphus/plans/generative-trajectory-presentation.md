# Wstęp do notebooka o trajektoriach modeli generatywnych

## TL;DR
> **Summary**: Zbudować 60-minutowy notebook dydaktyczny z komórkami markdown i code, który prowadzi od intuicji trajektorii do konkretnych metod: CFG + SDEdit → DIAMOND + x0 supervision → FlowChef + rectified flow.
> **Deliverables**: spójna narracja, source whitelist oparta o `DOCS.md`, wyraźne przykłady wizualne, mało wzorów, jasne przejścia między sekcjami, kilka krótkich komórek code jako demonstracje.
> **Effort**: Large
> **Parallel**: YES - 3 waves
> **Critical Path**: Time budget → scope lock → opening intuition → CFG/SDEdit → DIAMOND/x0 → FlowChef/rectified flow → notebook cohesion/QA

## Context
### Original Request
Ułożyć plan wstępu do prezentacji o generowaniu trajektorii modeli generatywnych, w prostym technicznym języku, z naciskiem na praktyczne zastosowania, minimalną matematykę i wizualnie odznaczające się przykłady.

### Interview Summary
- Styl ma być podręcznikowy, pragmatyczny i liniowy: każda kolejna część buduje się na poprzedniej.
- Domyślny kształt to notebook dydaktyczny na 60 minut: ok. 50 min treści + 10 min Q&A.
- Należy dodać segmenty dla: `SDEdit + CFG`, `DIAMOND + x0 supervision`, `FlowChef`.
- Źródłem prawdy ma być `DOCS.md`; w repo nie ma lowercase `docs.md`.
- `.sisyphus/plans/` nie ma przykładowych plików, więc styl trzeba oprzeć na istniejącym drafcie.

### Metis Review (gaps addressed)
- Ustalić dokładnie, że `DIAMOND` oznacza `2602.00883` i nie dopuścić do kolizji skrótu.
- Nie wychodzić poza źródła z `DOCS.md`; wyciąć wszystko, co wygląda jak poboczny detour.
- Nie rozdzielać narracji na odrębne mini-tematy: każda sekcja ma kończyć się mostem do następnej.
- Ograniczyć matematykę do maksymalnie 2 krótkich równań w całym wstępie; reszta ma być diagramem i intuicją.
- Notebook ma mieć wyraźny rytm: markdown → code → markdown → code, bez losowego mieszania form.

## Work Objectives
### Core Objective
Przygotować decision-complete plan notebooka o trajektoriach modeli generatywnych, tak aby wykonawca nie musiał podejmować już żadnych istotnych decyzji narracyjnych ani strukturalnych.

### Deliverables
- notebook z komórkami markdown i code
- source whitelist i mapowanie źródeł do sekcji
- wizualny pipeline / diagram trajektorii
- przejścia między: CFG, SDEdit, DIAMOND, x0 supervision, FlowChef, rectified flow
- finalny pass: spójność, kolejność, budżet wzorów, QA narracji
- time budget dla sekcji i komórek code

### Definition of Done (verifiable conditions with commands)
- `grep -nE "CFG|SDEdit|DIAMOND|x0 supervision|FlowChef|rectified flow" .sisyphus/plans/generative-trajectory-presentation.md`
- `grep -n "DOCS.md" .sisyphus/plans/generative-trajectory-presentation.md`
- `grep -nE "proof|derivation|heavy math|appendix" .sisyphus/plans/generative-trajectory-presentation.md`
- `grep -nE "transition|bridge|therefore|next" .sisyphus/plans/generative-trajectory-presentation.md`
- `grep -nE "markdown|code cell|Jupyter|notebook" .sisyphus/plans/generative-trajectory-presentation.md`
- `grep -nE "Diff2Flow|ControlNet|T2I-Adapter|OminiControl" .sisyphus/plans/generative-trajectory-presentation.md` returns no hits

### Must Have
- source whitelist wyłącznie z `DOCS.md`
- cała narracja zbudowana jako łańcuch: intuicja → sterowanie → metoda → ograniczenie → następna metoda
- notebook ma wyraźnie oznaczone komórki markdown jako narrację i code jako demonstracje, nie odwrotnie
- segment `CFG + SDEdit` jako jeden ciągły blok
- segment `DIAMOND + x0 supervision` jako jeden ciągły blok
- segment `FlowChef` z krótkim mostem do `rectified flow`
- wizualne przykłady różniące się od siebie (pipeline, steering, noise-then-denoise, correction loop, corridor/observation)
- maks. 2 krótkie równania w całym wstępie; preferowane diagramy zamiast wyprowadzania

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- żadnych źródeł spoza `DOCS.md`
- żadnych dodatkowych rodzin metod typu `Diff2Flow`, `ControlNet`, `T2I-Adapter`, `OminiControl`
- żadnych długich wyprowadzeń ani ciężkiej matematyki
- żadnych losowych komórek code bez celu dydaktycznego
- żadnych oderwanych bulletów, które nie budują poprzedniej sekcji
- żadnych „samodzielnych” mini-wykładów o diffusion/flow poza potrzebnym mostem

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: tests-after + narrative QA
- QA policy: każdy task ma scenariusz happy path i failure path
- Primary tool: Bash na notebook outline / rendered notebook; Playwright tylko jeśli notebook jest renderowany w przeglądarce
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 4 tasks per wave; <3 per wave only in the final wave.
> Extract shared dependencies early so późniejsze sekcje mogą pracować równolegle.

Wave 1: time budget + scope lock + opening frame + notebook scaffold + CFG
Wave 2: SDEdit + CFG/SDEdit bridge + DIAMOND + x0 supervision
Wave 3: DIAMOND/x0 bridge + FlowChef + rectified flow bridge + final notebook cohesion/QA

### Dependency Matrix (full, all tasks)
- T1 unlocks T2–T12.
- T2 and T3 can start po T1.
- T4 depends on T1–T3.
- T5 depends on T1–T4.
- T6 depends on T4–T5.
- T7 depends on T1–T6.
- T8 depends on T1–T6.
- T9 depends on T7–T8.
- T10 depends on T1–T9.
- T11 depends on T10.
- T12 depends on T1–T11.

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 4 tasks → `writing`, `visual-engineering`
- Wave 2 → 4 tasks → `writing`, `deep`
- Wave 3 → 4 tasks → `deep`, `unspecified-high`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [ ] 1. Lock scope, audience, notebook budget, and source whitelist

  **What to do**: confirm the notebook is designed for 60 minutes total (50 min treści + 10 min Q&A), lock `DIAMOND` to `2602.00883`, list every allowed source from `DOCS.md`, and write down the explicit out-of-scope list.
  **Must NOT do**: add any source outside `DOCS.md`, treat `docs.md` as a real file, or leave `DIAMOND` ambiguous.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this task is about scope definition and source governance, not visual polish.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `visual-engineering`, `deep` - not needed yet.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: T2–T12 | Blocked By: none

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `DOCS.md:1-9` - source whitelist and exact URL set.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:3-11` - confirmed requirements.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:27-29` - include/exclude boundary.
  - Pattern: `build_trajectory_notebook.py:20-23` - high-level narrative spine.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `grep -n "DOCS.md"` appears in the plan and whitelist is explicit.
  - [ ] `DIAMOND` is tied to `2602.00883` in the plan.
  - [ ] The notebook time budget is stated as 60 min total with 10 min Q&A.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Run `grep -nE "DOCS.md|2602\.00883|60 min|10 min Q&A|notebook" .sisyphus/plans/generative-trajectory-presentation.md`
    Expected: all five anchors are present in the plan text.
    Evidence: .sisyphus/evidence/task-1-scope-whitelist.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Run `grep -nE "docs\.md|Diff2Flow|ControlNet" .sisyphus/plans/generative-trajectory-presentation.md`
    Expected: no lowercase `docs.md` and no forbidden side topics appear.
    Evidence: .sisyphus/evidence/task-1-scope-whitelist-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 2. Draft the opening thesis and pipeline intuition

  **What to do**: open with the core mental model: generative models are trajectories, not single-shot outputs; introduce the pipeline from input/conditioning → state start → denoising/transport loop → result, then show how the notebook will alternate markdown explanation with small code demonstrations.
  **Must NOT do**: jump straight into method-specific details or mathematical notation.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this is a narrative framing task.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep`, `visual-engineering` - not needed yet.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T4–T12 | Blocked By: T1

  **References**:
  - Pattern: `build_trajectory_notebook.py:20-23,52-63` - pipeline explanation and why trajectory matters.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:14-16` - intended flow from intuition to methods.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:27-29` - keep it tight and non-derivational.

  **Acceptance Criteria**:
  - [ ] Opening paragraph defines “trajectory” in plain technical language.
  - [ ] The pipeline is described as a stepwise process with a start, loop, and output.
  - [ ] The opening ends with a bridge to CFG/SDEdit.
  - [ ] The opening states that the notebook will use markdown for narrative and code for demonstrations.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Verify the opening section contains the terms `trajectory`, `pipeline`, `conditioning`, `denoising`, `markdown`, and `code`.
    Expected: the opening sets the shared mental model without equations and states the notebook format.
    Evidence: .sisyphus/evidence/task-2-opening-frame.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Check that the opening does not introduce `DIAMOND` or `FlowChef` too early.
    Expected: those methods are absent from the opening and appear later only.
    Evidence: .sisyphus/evidence/task-2-opening-frame-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 3. Add the master visual package for the trajectory metaphor

  **What to do**: design one reusable diagram family for markdown cells: pipeline boxes, arrows, state transitions, and a simple “where control happens” visual that can be reused across the notebook.
  **Must NOT do**: make visuals decorative only, overloaded, or method-specific before the method is introduced.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` - Reason: this task is about a reusable visual language.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep` - not needed yet.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T4–T12 | Blocked By: T1–T2

  **References**:
  - Pattern: `build_trajectory_notebook.py:24-50` - linear pipeline diagram.
  - Pattern: `build_trajectory_notebook.py:56-63` - table mapping pipeline stage to control question.
  - Pattern: `build_trajectory_notebook.py:88-103,125-129` - minimal ASCII visuals.

  **Acceptance Criteria**:
  - [ ] One master diagram explains the pipeline end-to-end.
  - [ ] One simplified variant can be reused by later notebook sections.
  - [ ] Visual style clearly separates input, control, process, and output.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Confirm the visual spec names a single reusable diagram and a simplified variant.
    Expected: the visual language is consistent across the notebook.
    Evidence: .sisyphus/evidence/task-3-visual-pack.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for repeated use of unrelated icons or a different diagram language per method.
    Expected: no inconsistent visual grammar is introduced.
    Evidence: .sisyphus/evidence/task-3-visual-pack-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 4. Draft the CFG section and its control metaphor

  **What to do**: explain CFG as steering the direction of denoising, emphasize the tradeoff between following the condition and preserving diversity, and keep the explanation lightweight; use a short code cell only if it makes the guidance intuition clearer.
  **Must NOT do**: derive classifier-free guidance mathematically or turn this into a theory section.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: CFG is mainly an explanation task.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep` - not needed unless the wording becomes ambiguous.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: T5–T12 | Blocked By: T1–T3

  **References**:
  - Pattern: `DOCS.md:1` - CFG source.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:19` - existing note about simple CFG explanation.
  - Pattern: `build_trajectory_notebook.py:68-104` - CFG explanation, steering metaphor, and one compact formula.

  **Acceptance Criteria**:
  - [ ] CFG is defined as trajectory steering, not just “better text conditioning”.
  - [ ] The section includes one practical example and one caution about over-guidance.
  - [ ] The section ends with a bridge to SDEdit.
  - [ ] If code appears, it is a tiny demonstration rather than a derivation.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Verify the CFG section mentions conditional vs unconditional behavior and a single steering metaphor.
    Expected: the section is understandable without derivation and any code cell is minimal.
    Evidence: .sisyphus/evidence/task-4-cfg.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Check that the CFG section does not introduce more than one equation.
    Expected: formula budget is respected.
    Evidence: .sisyphus/evidence/task-4-cfg-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 5. Draft the SDEdit section and the noise-then-denoise bridge

  **What to do**: explain SDEdit as controlled corruption followed by denoising, and frame it as a practical editing strategy that preserves global structure while changing local content; if a code cell is used, it should only illustrate the noise-then-denoise pipeline.
  **Must NOT do**: present SDE as a stochastic calculus lesson.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: the task is explanatory and use-case driven.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep` - not needed yet.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T6–T12 | Blocked By: T1–T4

  **References**:
  - Pattern: `DOCS.md:2` - SDEdit source.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:20` - note on noise addition and denoising intuition.
  - Pattern: `build_trajectory_notebook.py:105-133` - SDE explanation and SDEdit bridge.

  **Acceptance Criteria**:
  - [ ] The section shows the sequence clean image → controlled noise → denoise → edit.
  - [ ] It explicitly explains why starting from a partially corrupted state is useful.
  - [ ] The section ends by motivating the shared block with CFG.
  - [ ] Any code cell only demonstrates the corruption/denoising idea.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Confirm the SDEdit section uses a noise-then-denoise diagram and names editing as the goal.
    Expected: the idea is visually and verbally clear, with code only serving the intuition.
    Evidence: .sisyphus/evidence/task-5-sdedit.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for long mathematical derivations or symbols beyond a simple sketch.
    Expected: none are present.
    Evidence: .sisyphus/evidence/task-5-sdedit-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 6. Connect CFG and SDEdit into one contiguous section

  **What to do**: write the transition so CFG and SDEdit read as one chain: CFG tells the path direction, SDEdit explains why the path is stepwise and how editing can start from a controlled corruption point; add a short notebook cell only if it helps connect the two.
  **Must NOT do**: split them into unrelated mini-topics or introduce new methods between them.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this is a transition and cohesion task.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `visual-engineering` - visuals already covered in T3.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T7–T12 | Blocked By: T4–T5

  **References**:
  - Pattern: `build_trajectory_notebook.py:68-133` - CFG and SDE as the two fundamentals.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:14-16,27-29` - chain and boundaries.

  **Acceptance Criteria**:
  - [ ] The CFG and SDEdit parts sit next to each other and share a single conclusion.
  - [ ] One bridging sentence explains why SDEdit follows CFG in the story.
  - [ ] No unrelated method interrupts this pair.
  - [ ] The transition works in markdown without requiring extra exposition in code.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Inspect the combined section for a direct CFG→SDEdit transition sentence.
    Expected: the reader can follow the causal chain without a jump.
    Evidence: .sisyphus/evidence/task-6-cfg-sdedit-bridge.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search the section for a third method or a detour into background theory.
    Expected: nothing beyond CFG/SDEdit appears.
    Evidence: .sisyphus/evidence/task-6-cfg-sdedit-bridge-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 7. Draft DIAMOND as inference-time trajectory correction

  **What to do**: present DIAMOND as correcting the trajectory before artifacts lock in, and keep the focus on inference-time quality rather than post-hoc cleanup; if code is shown, it should be a compact sketch of the correction loop.
  **Must NOT do**: confuse it with any other DIAMOND acronym or explain it as a generic image filter.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: this section needs careful source-backed synthesis and disambiguation.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `visual-engineering` - not needed yet.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T8–T12 | Blocked By: T1–T6

  **References**:
  - Pattern: `DOCS.md:3` - DIAMOND source.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:21` - trajectory correction and artifact reduction note.
  - Pattern: `build_trajectory_notebook.py:136-156` - DIAMOND as directed inference / quality protection.

  **Acceptance Criteria**:
  - [ ] DIAMOND is explicitly linked to trajectory correction and artifact avoidance.
  - [ ] The section says why it is an inference-time intervention.
  - [ ] A visual loop or correction diagram is included.
  - [ ] If code appears, it is a compact correction-loop sketch only.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Verify the DIAMOND section names artifact correction and inference-time steering.
    Expected: the section is method-specific and not generic cleanup, with no long code block.
    Evidence: .sisyphus/evidence/task-7-diamond.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Check that DIAMOND is not presented as the wrong paper or as a training-only method.
    Expected: the identity and role stay correct.
    Evidence: .sisyphus/evidence/task-7-diamond-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 8. Draft x0 supervision as the training-side counterpart

  **What to do**: explain why supervising the clean image `x0` is more direct for the story being told, and show that this is the training-side counterpart to DIAMOND’s inference-side correction; any code cell should be a tiny schematic of target choice, not a training implementation.
  **Must NOT do**: turn the section into a loss-function derivation or a broad survey of control architectures.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this is a conceptual bridge from inference to training.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep` - not needed unless wording needs disambiguation.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: T9–T12 | Blocked By: T1–T7

  **References**:
  - Pattern: `DOCS.md:6` - x0 supervision source.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:22` - direct clean-image target and faster convergence note.
  - Pattern: `build_trajectory_notebook.py:191-217` - x0-supervision as the training-side complement.

  **Acceptance Criteria**:
  - [ ] The section states that x0 is the clean target.
  - [ ] It explains why this helps the model learn global structure.
  - [ ] It explicitly bridges back to DIAMOND.
  - [ ] Any code cell only illustrates target selection at a high level.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Confirm the x0 section contrasts x0 with epsilon and keeps the explanation in plain language.
    Expected: the training-side story is clear and code stays schematic.
    Evidence: .sisyphus/evidence/task-8-x0-supervision.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for long algebra or extra model families not listed in DOCS.md.
    Expected: no derivations or unrelated families appear.
    Evidence: .sisyphus/evidence/task-8-x0-supervision-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 9. Connect DIAMOND and x0 supervision into one contiguous section

  **What to do**: make the transition explicit: DIAMOND is the inference-time quality safeguard, x0 supervision is the training-time way to make the model more structurally reliable; keep the notebook rhythm markdown → code → markdown.
  **Must NOT do**: let the two parts read as separate papers with no shared thesis.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: the section needs a precise conceptual hinge between inference and training.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `visual-engineering` - not needed here.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T10–T12 | Blocked By: T7–T8

  **References**:
  - Pattern: `build_trajectory_notebook.py:136-217` - DIAMOND and x0 as complementary ideas.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:14-16,27-29` - narrative continuity and boundaries.

  **Acceptance Criteria**:
  - [ ] One sentence explains why DIAMOND and x0 belong in the same story.
  - [ ] The transition from inference to training is explicit.
  - [ ] The section closes by motivating FlowChef.
  - [ ] The transition works with the notebook’s markdown/code rhythm.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Inspect the combined section for one shared conclusion and a direct bridge to FlowChef.
    Expected: the reader sees a single conceptual arc.
    Evidence: .sisyphus/evidence/task-9-diamond-x0-bridge.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for duplicated introductory text or a second disconnected mini-essay.
    Expected: the pair stays contiguous and singular.
    Evidence: .sisyphus/evidence/task-9-diamond-x0-bridge-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 10. Draft FlowChef with rectified flow and observation constraints

  **What to do**: explain FlowChef as steering rectified flow under observation, mask, or measurement constraints, and make it clear this is training-free / inference-time control; use code only for a tiny conceptual sketch if needed.
  **Must NOT do**: reduce it to “a better prompt” or drift into other flow-family methods.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: this section combines source reading with a precise control story.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `writing` - the conceptual lift is higher here.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T11–T12 | Blocked By: T1–T9

  **References**:
  - Pattern: `DOCS.md:7-9` - FlowChef and rectified flow sources.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:23-24` - FlowChef as steering rectified flow and the trajectory narrative.
  - Pattern: `build_trajectory_notebook.py:159-188` - observation constraints, corridor metaphor, and controlled generation.

  **Acceptance Criteria**:
  - [ ] FlowChef is defined as trajectory steering under observation constraints.
  - [ ] The section states why it is useful for editing / inverse problems.
  - [ ] Rectified flow appears only as the small bridge needed to understand FlowChef.
  - [ ] Any code cell stays conceptual and short.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Confirm the FlowChef section mentions observation, prior, and inference-time control in one coherent story.
    Expected: the section is specific and practical, with code not turning into implementation.
    Evidence: .sisyphus/evidence/task-10-flowchef.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for a detour into unrelated flow or diffusion variants.
    Expected: no unrelated branch appears.
    Evidence: .sisyphus/evidence/task-10-flowchef-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 11. Add the rectified flow bridge and comparison line

  **What to do**: add a short bridge that positions rectified flow as the geometry behind the FlowChef story, without turning it into a separate theory chapter or code-heavy detour.
  **Must NOT do**: expand into a standalone rectified-flow lecture.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this is a short connector, not a new topic.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `deep` - the core work is already done in T10.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: T12 | Blocked By: T10

  **References**:
  - Pattern: `DOCS.md:8` - rectified flow source.
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:24` - rectified flow narrative note.
  - Pattern: `build_trajectory_notebook.py:186-188` - how rectified flow supports the shared geometry claim.

  **Acceptance Criteria**:
  - [ ] Rectified flow is mentioned only as a bridge that supports FlowChef.
  - [ ] The bridge sentence does not require new math.
  - [ ] The connection to the earlier trajectory language is explicit.
  - [ ] The bridge fits naturally between markdown cells.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Verify the rectified-flow bridge is one short paragraph and not a new section.
    Expected: the flow story remains lightweight and notebook-friendly.
    Evidence: .sisyphus/evidence/task-11-rectified-flow-bridge.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search for a new theorem-style explanation or a formula block.
    Expected: none appears.
    Evidence: .sisyphus/evidence/task-11-rectified-flow-bridge-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

- [ ] 12. Final cohesion pass: transitions, order, formula budget, QA

  **What to do**: polish the entire notebook so every section transitions into the next, the cell order is stable, the formula budget is respected, and no bullet stands alone.
  **Must NOT do**: add any new content, new methods, or late-stage scope expansion.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: this is editorial QA and narrative coherence work.
  - Skills: `[]` - no extra skill needed.
  - Omitted: `writing` - the content already exists; this is a quality pass.

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: none | Blocked By: T1–T11

  **References**:
  - Pattern: `.sisyphus/drafts/generative-trajectory-presentation.md:7-16,27-29` - narrative order and scope boundaries.
  - Pattern: `build_trajectory_notebook.py:219-229` - method-to-role summary and overall chain.

  **Acceptance Criteria**:
  - [ ] The intro can be summarized as one story: trajectory → control → method → limitation → next method.
  - [ ] All required segments appear in the prescribed order.
  - [ ] The final pass confirms the 60-minute budget, 2-equation max, markdown/code rhythm, and visual-first style.

  **QA Scenarios**:
  ```
  Scenario: Happy path
    Tool: Bash
    Steps: Run a final grep pass for all required method names, transition keywords, and notebook format terms.
    Expected: every required term appears and no orphaned section remains.
    Evidence: .sisyphus/evidence/task-12-cohesion-qa.txt

  Scenario: Failure/edge case
    Tool: Bash
    Steps: Search the plan for any late-added topic not in DOCS.md or any section that could stand alone.
    Expected: none found; cohesion holds.
    Evidence: .sisyphus/evidence/task-12-cohesion-qa-error.txt
  ```

  **Commit**: NO | Message: n/a | Files: `.sisyphus/plans/generative-trajectory-presentation.md`

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [ ] F1. Plan Compliance Audit — oracle
- [ ] F2. Narrative Quality Review — unspecified-high
- [ ] F3. Real Manual QA — unspecified-high
- [ ] F4. Scope Fidelity Check — deep

## Commit Strategy
Plan artifact only. No git commit unless explicitly requested later; keep the source of truth in `.sisyphus/plans/generative-trajectory-presentation.md` and the working notes in `.sisyphus/drafts/` until execution starts.

## Success Criteria
The intro plan is complete when:
- it uses only sources listed in `DOCS.md`
- it keeps the requested chain intact: CFG + SDEdit → DIAMOND + x0 supervision → FlowChef + rectified flow
- it is explicitly structured as a Jupyter notebook with markdown narration and small code demonstrations
- it stays simple, pragmatic, and visual-first
- it caps mathematics at 2 short equations maximum
- it can be executed without any further narrative decisions from the implementer
