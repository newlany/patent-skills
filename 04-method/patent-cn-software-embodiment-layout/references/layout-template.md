# Layout Template For Method + System + Device + Storage-Medium Cases

## Quick Pattern

Use `method thick, system mapped, carrier concise`.

- Method: full executable route, sub-processes, example, variants.
- System/device: module names, module inputs/outputs, mapping to steps.
- Electronic device: processor, memory, program instructions, deployment.
- Storage medium/program product: stored instructions, execution of method, non-limiting medium examples.

## Section Order

### 1. General Implementation Statement

State that the embodiments are illustrative, may be implemented by software, hardware, or software-hardware combination, and may be executed by a terminal, server, workstation, cloud platform, or distributed system.

Avoid limiting language such as `必须由服务器执行` unless the claim requires it.

### 2. Term Definitions

For complex software/AI cases, define terms before the method flow. Use prose, not an inventor-note glossary, if the final application style prefers natural paragraphs.

For each custom term, cover as many of these as needed:

- data source or input;
- generation or calculation route;
- representation form, such as matrix, vector, mask, label map, text field, design file, confidence score, or threshold;
- role in model input, rule matching, validation, feedback, or output;
- example values only when useful, marked as examples.

High-priority terms usually include:

- raw data object;
- design coordinate or alignment space;
- functional region or semantic region;
- mask, label map, constraint map, control condition;
- structured prompt or rule field;
- trained or fine-tuned model;
- candidate result;
- validation score, consistency check, functional constraint;
- feedback, frozen region, local regeneration;
- output file and derived engineering artifact.

### 3. System Or Application Environment

Before the step flow, give a short overview of the execution architecture:

- data acquisition side;
- processing side;
- model/rule side;
- validation/output side;
- optional client/server or cloud deployment.

This helps support both method and system claims.

### 4. Preparation Stage

Use a separate preparation paragraph when the invention depends on previously established resources:

- training samples;
- model training or fine-tuning;
- rule library or template library;
- coordinate template;
- reference database;
- parameter calibration.

Write clearly that the preparation may be performed before the current method execution, periodically, or by a different device, unless the claim requires preparation inside the method.

### 5. Main Method Flow

Follow the independent claim order. For each step:

1. identify the input;
2. describe the operation;
3. name the output;
4. explain how the output is used by the next step;
5. add optional implementation choices;
6. add a concrete example if it makes enablement clearer.

Use step labels such as `S110` only when they match the drawings and claims.

### 6. Key Sub-Process Embodiments

If the method has an inventive bottleneck, give it extra paragraphs after the main flow or inside the relevant step. Typical bottlenecks:

- data registration or coordinate conversion;
- rule-template matching and conflict resolution;
- model input construction;
- model training/fine-tuning;
- result validation;
- feedback correction and local regeneration;
- output transformation into engineering files.

### 7. End-To-End Example

Use one complete scenario to connect all steps. Keep it within the claim breadth:

- start from a real task input;
- walk through key intermediate results;
- show rule/model cooperation;
- show validation or feedback;
- finish with output artifacts.

Do not let the example replace the general method paragraphs.

### 8. System Or Device Embodiment

Map modules to method steps:

- data obtaining module -> input step;
- processing module -> transformation step;
- rule or model module -> generation step;
- validation/output module -> checking and output step.

Include a sentence that modules may be implemented as software modules, hardware circuits, firmware, processors executing instructions, or combinations, and that module division is logical.

### 9. Electronic Device Embodiment

Use concise carrier wording:

`在至少一个实施例中，电子设备包括处理器和存储器，存储器中存储有计算机程序或指令，处理器执行所述程序或指令时实现前述任一方法实施例中的步骤。该电子设备可以为...`

Optionally add communication interface, input/output interface, accelerator, or graphics processor when supported by the method.

### 10. Storage Medium Or Program Product Embodiment

Use concise support wording:

`在至少一个实施例中，计算机可读存储介质中存储有计算机程序或指令，所述程序或指令被处理器执行时实现前述方法实施例。所述存储介质可以包括...`

Avoid over-listing media unless needed.

## Common Pitfalls

- Repeating the claim language without explaining implementation.
- Defining terms only after they have already been used many times.
- Treating optional model training as a mandatory runtime method step.
- Writing system modules as unsupported physical hardware when the invention is software logic.
- Repeating the full method under electronic device and storage medium, making the section bloated.
- Letting the concrete example narrow the general method.
- Leaving validation and feedback loops as black-box labels.
