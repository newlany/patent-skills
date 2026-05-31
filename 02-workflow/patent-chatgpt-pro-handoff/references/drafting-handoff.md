# Drafting Handoff Guidance

## Task Kind Mapping

Use `claims` for independent-claim strategy, dependent-claim layering, claim amendment, or claim polishing.

Use `background` when ChatGPT should frame the existing technical problem without overstating the invention.

Use `invention-content` when ChatGPT should draft technical problem, technical solution, and beneficial effects.

Use `embodiments` when ChatGPT should expand concrete implementation, structural relationships, software flow, algorithm steps, or formula-backed examples.

Use `specification` when ChatGPT should draft or revise several specification sections together.

## Drafting Rules To Include

For claims, include:

- common rules;
- claim rules;
- output format rules;
- formula rules if formulas exist.

For background, include:

- common rules;
- background rules;
- output format rules.

For invention content, include:

- common rules;
- invention-content rules;
- claim rules if the technical solution must align with claims;
- output format rules;
- formula rules if formulas exist.

For embodiments, include:

- common rules;
- embodiment rules;
- specification rules;
- output format rules;
- formula rules if formulas exist.

For a full specification handoff, include all drafting section rules.

## Drafting Guardrails

Tell ChatGPT Pro to preserve these boundaries:

- ground every feature in the disclosure, search memo, or user-provided facts;
- distinguish claim limitations from optional embodiments;
- avoid importing limitations from prior art unless the prompt expressly asks for amendment options;
- identify unsupported assumptions instead of silently inventing details;
- keep effects tied to technical means;
- write in Chinese patent style without marketing language;
- avoid dense ideographic-comma chains in prose sections.

For software, AI, algorithm, or data-processing cases, require ChatGPT to separate runtime method steps from offline training, configuration, precondition, and result evaluation unless the user's route intentionally combines them.

For structural cases, require the embodiment to explain physical form, relative position, connection, direction, and cooperation among parts. Do not allow a mere prose copy of the claims.

