# OA Checkpoints

Use these checkpoints to separate automatic evidence work from user-confirmed strategic judgments.

## Automatic work

The agent may do these without asking first:

- read and summarize the application
- break down the office action
- verify D1 and Dx against the original text
- organize examples, comparative examples, parameter tables, and raw evidence
- identify possible risks, weaknesses, and candidate paths

## Default confirmation checkpoints

| ID | Checkpoint | Usually after | Must already be fixed | Confirms |
| --- | --- | --- | --- | --- |
| CP-01 | whether to amend claims | Stage 5 | preliminary difference snapshot and amendment options | `amendment_decision` |
| CP-02 | which amendment path to use | Stage 5 | candidate merged features and support/risk analysis | `amendment_path` |
| CP-03 | final amended claim 1 text | Stage 5 | confirmed amendment path | amended claim 1 text |
| CP-04 | final distinguishing features for the current effective claims | Stage 6 pre-lock | current effective claim set | `final_distinguishing_features` |
| CP-05 | actual technical problem for the current effective claims | Stage 6 pre-lock | confirmed distinguishing features | `technical_problem` |
| CP-06 | key wording used in the formal response | Stage 7 or 8 before finalization | main argument path and sensitivity review | final response wording when needed |

## Checkpoint format

At each checkpoint, present:

1. the recommended option
2. why it is recommended
3. any realistic backup option
4. a direct request for confirmation

## Timing rules

- The preliminary current-claim-1-vs-D1 difference snapshot may be prepared before CP-01, but it is not a substitute for CP-04.
- Do not lock CP-05 before the current effective claim set and CP-04 are fixed.
- If the claim set changes after CP-04 or CP-05, reopen those checkpoints and refresh the dependent outputs.
- For drafting-only or QC-only requests, check whether the required checkpoints are already fixed; if not, state the missing checkpoint and risk before continuing.
