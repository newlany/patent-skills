# Drafting Route Families

Use this map to classify the disclosure by drafting burden rather than by applicant or folder name.

## Route A: Structural / Device / Product / Material-Structure

Choose the structural default route when:

- the likely independent claim is mainly a device, system, product, assembly, component relation, or material structure
- the hard part is defining structural features, connections, layers, modules, or cooperation relations
- formulas, process windows, and model derivations are present only as secondary support

Typical examples:

- 宏发类具体结构交底
- 科华类具体结构交底
- 具有明确部件、连接关系、层次结构、装配关系的案件

Outcome:

- stay inside `patent-entry-drafting` for the common drafting chain
- use `patent-stage-disclosure-analysis`, `patent-stage-prior-art-search`, `patent-stage-invention-content`, `patent-support-docx-math`, and `patent-qc-application-consistency` as needed

## Route B: Process / Preparation-Heavy Method

Choose `patent-method-process-route` when:

- the technical contribution is mainly the preparation route, treatment route, composition process, parameter window, or test-backed process optimization
- examples, comparative examples, testing, and result tables are central
- the next drafting burden is organizing process steps and retained experimental support

Strong signals:

- raw materials,配方, feed order, temperature, time, concentration, speed, curing, foaming, mixing, or treatment windows
- the user explicitly says `安踏` and `方案重构`, and the file content confirms a process or material-heavy route

## Route C: Formula / Model-Driven Method

Choose `patent-method-formula-model` when:

- formulas, variables, derived parameters, objective functions, constraints, or simulation outputs define the technical route
- the next drafting burden is preserving mathematical meaning and turning it into patent language

Typical examples:

- 厦大模型方法案
- 仿真、优化、反演、敏感度分析、目标函数驱动的交底

## Route D: General Runtime-Chain / Boundary Method

Choose `patent-method-runtime-boundary` when:

- the disclosure is method-type, but the main burden is clarifying runtime steps, step order, state transfer, matching logic, or method boundary
- the case is not dominated by formulas or process examples

## Confidence Gate

- high confidence: one route has multiple strong signals
- medium confidence: mixed signals, but one route still clearly controls the next drafting step
- low confidence: the next drafting output would materially differ depending on the route

At low confidence, stop and ask the user to confirm before continuing.
