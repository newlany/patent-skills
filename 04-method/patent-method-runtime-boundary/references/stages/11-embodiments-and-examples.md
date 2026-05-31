# Stage 11: Embodiments And Examples

## Enter this stage when

- the user asks for stage 11
- the user asks for 具体实施方式, 实施例, or 对比例
- the claim set and invention-content baseline are fixed

## Required baseline

- confirmed claim set
- confirmed invention-content main line
- confirmed final disclosure

## Task focus

- open with the method and the application scene
- after that brief opening, first list the runtime steps from the fixed independent-claim chain
- then explain the steps in order
- do not front-load a glossary paragraph before the step chain unless the user explicitly asks for that format
- state which devices, mappings, formulas, models, libraries, or rule sets already exist before execution in the relevant step explanations or in a short support-resource paragraph that follows the step chain
- integrate dependent features into the relevant step explanations
- if a dependent feature concerns post-run update of a pre-existing support resource, describe it after the main step chain or as an optional paragraph instead of automatically creating a new numbered step
- naturally define custom terms, intermediate quantities, and self-defined process names when they first appear in the detailed step explanation
- if those definitions rely on other terms such as process names, pattern labels, or structure labels, explain those terms there as well and give brief examples when useful
- in Chinese drafting paragraphs, avoid double quotes around self-defined terms by default
- do not repeatedly use one fixed definition lead-in such as `这里所称`; vary the wording naturally, for example with `其中`, direct apposition, or short explanatory follow-on clauses
- if a self-defined quantity or non-routine feature parameter is used, explain how it is measured, extracted, calculated, or represented so that the scheme can be implemented from the text
- for image features, signal features, and state features, explain the source data, the basic processing route, and the resulting feature form
- for any physical device, actuator, sensor, controller, valve, guide, roller, or adjustment mechanism recited in the method, explain how it is arranged and how it concretely carries out the claimed operation in industrial use
- when the method is implemented by a control system, explain the division of work among PLC controllers, industrial control computers, embedded computing modules, sensor interfaces, drives, and actuator mechanisms
- when an execution step changes speed, torque, pressure, position, path length, wrap angle, or similar physical quantities, explain how the control instruction is converted into that physical change
- for preparation-heavy or material-preparation cases, default to `方案详细说明 -> 实施例和对比例 -> 性能测试`
- in the detailed scheme part, first state `本发明提供一种...方法，包括步骤一、步骤二...` and then explain each step in fuller process detail
- if the user asks for no small headings, keep only `实施例1/2/...` and `对比例1/2/...` as local headings, and write the rest as ordinary paragraphs
- in that mode, the opening step-chain paragraphs should directly write out the full independent-claim route with retained parameters and ranges
- before writing `实施例` and `对比例` for preparation-heavy or material-preparation cases, add a raw-materials paragraph or compact raw-materials section unless the user explicitly forbids it
- in the raw-materials text, identify each key raw material by raw-material name, commercial grade or model, and supplier when available, rather than defaulting to a raw-material table
- prefer commercially available domestic Chinese products when they technically fit the disclosure and claim scope
- if supplier and grade/model information is completed from market research, use real web evidence such as a supplier page, TDS, SDS, catalog page, product manual, manufacturer page, or credible marketplace/manufacturer listing; do not invent commercial sources
- keep web-sourced supplier and grade/model information as an embodiment example and add generic fallback wording so the claim scope is not limited to a single commercial source
- when source evidence is missing or ambiguous, use generic technical wording or flag the item for inventor confirmation instead of fabricating a supplier or grade
- for commercial raw materials that support a key claim feature, verify or conditionally state the exact functional property; do not treat `active hydrogen`, `nonvolatile content`, or broad product descriptions as automatic proof of `hydroxyl`, `non-aqueous`, or `low water`
- avoid absolute raw-material facts unless supported by a source or test; prefer operational controls such as `使用前确认/预处理为...` and `控制含水率不高于...`
- for range-defined material cases, default to at least three implementation examples aligned to lower-bound, optimized, and upper-bound parameter sets unless the user asks for a different design
- add concrete examples after the step-by-step detailed explanation
- add comparative examples only when they directly support the inventive main line
- keep comparative examples centered on the inventive key means and write them briefly against one anchor embodiment when that avoids contradiction
- when comparative examples change pigments, color pastes, color masterbatches, fillers, or active additives, define whether the comparison is based on equal effective component amount or equal total addition amount; avoid ambiguous `等量` wording
- in the testing part, write only effect-linked test items and methods, keep the retained data in a results table, and keep the results analysis brief
- if test data are missing from the disclosure, drafted example data may be completed from retained technical logic and field knowledge, but that status must be clear in the response
- do not say the test results prove inventiveness; instead, say which technical means played the key role in the retained effects
- if the user asks to reduce AI-like tone, prefer shorter step sentences and avoid repeated dense `、` stacks unless they are technically necessary

## Deliverable

- embodiments and examples section in specification style

## Guardrails

- do not reintroduce a precondition as a runtime step after the claim chain has already been fixed
- do not continue numbering beyond the independent-claim chain merely because a later dependent claim adds an optional update, writeback, or evaluation feature
- do not leave key self-defined terms or device names unexplained when the embodiment is supposed to teach industrial implementation
- do not use a short `common knowledge` disclaimer as a substitute for explaining key self-defined terms, feature quantities, device actions, or step interfaces
- do not open with standalone terminology lists when the user has asked for claim-step-first drafting
- do not cite claim numbers unless the user specifically asks
- the concrete example should show how the method runs, not how the pre-existing support was historically accumulated

## Stop rule

Stop after the embodiments and examples and wait for confirmation before figures or cleanup.
