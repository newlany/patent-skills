# Method Patent Scene Routing

Use this routing table to classify the case by drafting bottleneck rather than by applicant or source.

## Mandatory Intake Order

When the user has provided disclosure files:

1. read the disclosure content first
2. identify the likely independent-claim main line
3. identify what will be hardest to draft correctly
4. classify by that drafting bottleneck

Do not classify from the file name, applicant, or project folder label alone.

## Route Signals From File Content

Use multiple signals together. One isolated signal is usually not enough.

## Route 1: Preparation / Process-Route Heavy

Choose [$patent-method-process-route](/Users/chrynos/.codex/skills/patent-method-process-route/SKILL.md) when the case is dominated by:

- raw materials, feed order, composition, or treatment sequence
- process windows, temperature/time/concentration/speed ranges
- equipment coordination or processing order
- many examples, comparative examples, testing standards, and retained result tables
- inventive contribution expressed mainly through the process route plus test-backed performance

Strong supporting signals:

- the disclosure spends more effort on process windows, material ratios, equipment cooperation, or treatment conditions than on abstract step logic
- the likely embodiments will center on examples, comparative examples, tests, and performance tables
- the hard part is organizing retained technical effects through experimental design and results

## Route 2: Formula / Model Driven

Choose [$patent-method-formula-model](/Users/chrynos/.codex/skills/patent-method-formula-model/SKILL.md) when the case is dominated by:

- formulas, variables, objective functions, or constraints
- derived parameters, sensitivity analysis, inversion, optimization, or simulation
- result curves, model outputs, or figure-label interpretation
- Word math objects, inline math repair, or formula completeness checks

Strong supporting signals:

- the disclosure depends on equations, variables, derivations, or model outputs to define the technical route
- the likely embodiments will need careful formula restoration, variable consistency, and figure-curve explanation
- the hard part is preserving mathematical content and explaining model-driven technical meaning in patent language

## Route 3: General Runtime-Chain / Boundary Driven

Choose [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md) when the case is dominated by:

- clarifying what belongs to the runtime method chain
- distinguishing preconditions, pre-established resources, and later updates from runtime steps
- aligning claims, invention content, embodiments, abstract, and flowcharts to one step chain
- control, identification, routing, matching, state-transfer, or closed-loop execution logic

Strong supporting signals:

- the disclosure difficulty lies in deciding what belongs inside the method and what belongs outside it
- the likely claim 1 depends more on step order, state transfer, matching logic, or closed-loop handling than on formulas or experiments
- the hard part is keeping claims, invention content, embodiments, and flowcharts aligned to one adopted runtime chain

## Confidence Rule

Use these confidence levels:

- high confidence: one route has multiple strong signals and the others are clearly secondary
- medium confidence: the case is mixed, but one route still dominates the drafting bottleneck
- low confidence: route signals conflict and the next drafting step would change materially depending on the route

When confidence is high or medium, route directly and say why.

When confidence is low:

1. use [$patent-method-runtime-boundary](/Users/chrynos/.codex/skills/patent-method-runtime-boundary/SKILL.md) as the provisional intake route
2. complete the shared baseline analysis through technical problem and key technical means
3. re-evaluate whether the case should stay in the general workflow or hand off to the process-route or formula/model route

## Common Misclassification Traps

Avoid these mistakes:

- a process case with one or two calculation formulas is still a process-route case if the drafting burden is examples, tests, and result tables
- a model case with some preprocessing steps is still a formula/model case if the drafting burden is variables, equations, derivations, and result curves
- a control or closed-loop case with devices and databases is still a general runtime-chain case if the core issue is method-boundary alignment and step interaction
- the presence of equipment does not by itself make the case a process-route case
- the presence of steps does not by itself make the case a general runtime-chain case

## Routing Output Contract

After classification, state:

1. selected skill
2. route confidence
3. file-based evidence for the selection
4. any non-dominant competing signals
5. whether the route is final or provisional

## Tie-Break Rule

If the case fits more than one route, select the route that matches the hardest part to draft correctly.

- hard formulas -> formula/model-driven
- hard process examples and testing -> preparation/process-route-heavy
- hard step-boundary and cross-section alignment -> runtime-chain/boundary-driven
