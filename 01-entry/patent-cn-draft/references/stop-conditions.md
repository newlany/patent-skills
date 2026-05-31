# Stop Conditions

Stop and ask the user only when continuing would risk a wrong legal or drafting choice.

## Always Stop

- route confidence is low
- closest prior art changes the inventive concept or claim scope
- the disclosure lacks a critical technical fact for enablement/support
- a formula, parameter range, experiment, sequence, or model cannot be safely interpreted
- the user must choose between broad claim scope and safer fallback scope
- inventor/applicant/priority/secrecy/filing-channel facts are required
- validation reports a hard fail that cannot be fixed mechanically

## Do Not Stop

Do not stop just to report normal progress. Instead:

- write the stage memo
- register artifacts
- log the event
- continue if the next step is deterministic

## Stop Message

Use this compact format:

```text
需要确认一个会影响后续撰写方向的问题：
- blocker: <one sentence>
- safest default: <what I would do if allowed>
- why it matters: <claim scope / support / filing / route impact>
- question: <one focused question>
```
