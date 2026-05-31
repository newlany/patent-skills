# Patent Application Checklists

## Reference Numeral Checklist

- Claims: structure term followed by full-width parentheses, e.g. `槽状流道（110）`.
- Embodiments/specification: structure term followed by digits without parentheses, e.g. `槽状流道110`.
- Keep numerals consistent with `主要附图标记说明`.
- Do not number section names, method steps, effects, or generic functional phrases unless they are drawing signs.
- Check for mixed styles in the same section, e.g. `皮肤基体100` inside claims or `皮肤基体（100）` inside embodiments.
- Check for duplicate labels such as `皮肤基体（100）（100）` or `槽状流道110110`.

## Formatting Checklist

- Duplicate punctuation: `，，`, `。。`, `；；`, `、、`, `：：`, `？？`, `！！`, `，，。`, `。；`.
- Mixed punctuation that looks accidental: `,，`, `.。`, `;；`.
- Suspicious repeated words: `的的`, `所述所述`, `该该`, `和和`, `与与`, `在在`, `上上`, `下下`.
- Extra spaces inside Chinese text, except around English units or formulas.
- Inconsistent full-width/half-width parentheses around Chinese patent numerals.
- Obvious typos should be reported only when high confidence. Otherwise mark as suspected.

## Claim Citation Checklist

- Dependent claim must cite an earlier claim.
- A claim must not cite itself or a later claim.
- If a later claim uses `所述X`, then `X` should appear in the cited earlier claim or the cited claim's dependency chain.
- Prefer checking against known structure terms from the reference-sign mapping to avoid over-capturing long phrases after `所述`.
- Flag missing antecedent basis as: `权利要求N中“所述X”在其引用基础中未找到明确前序基础`.
- Do not flag common statutory phrases such as `所述的一种...` as structural antecedent terms.

## Drawing And Reference Sign Checklist

- `附图说明` should describe every actual drawing: `图1`, `图2`, etc.
- If the document contains `说明书附图` captions or embedded images, compare them with `附图说明`.
- `主要附图标记说明` should list every reference sign used in the text and drawings when available.
- Every listed reference sign should appear at least once in claims or embodiments, unless it is intentionally drawing-only.
- Every numbered structure term used in claims or embodiments should have a corresponding entry in `主要附图标记说明`.

## Specification Drafting Style Checklist

- Embodiment section should first present the total solution: `本实施例提供...，包括A、B、C...`.
- After the total statement, describe each major component in a stable order, normally the order in the total statement.
- When describing a component, finish its composition, position, connection, and optional variants before moving to the next major component.
- Avoid jumping back and forth between components unless the relationship being described requires it.
- Define key terms before using them heavily.
- For patent robustness, describe both a preferred implementation and allowable alternatives without undermining claim scope.
