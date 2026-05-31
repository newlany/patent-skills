---
name: cn-patent-invention-content
description: Draft or rewrite the 发明内容 section of a Chinese patent application in a structured, effect-linked style. Use when Codex needs to write 发明内容, 技术方案, 有益效果, 优选方案, or section-level rewrites from claims, technical disclosures, background defects, or a reference case, especially for requests such as “写发明内容”, “补发明内容”, “重写发明内容”, or “按某案件的写法改写发明内容”.
---

# CN Patent Invention Content

## Overview

Use this skill to draft the `发明内容` section for a Chinese patent application by following the cadence in the reference pet-case specification: purpose paragraph, technical-solution lead-in, independent solution block, effect explanation block, preferred-feature blocks, and optional method block.

Prefer product or apparatus content first and method content second unless the case is method-centered.

## Workflow

1. Gather the drafting inputs.
- Extract the invention title, the core technical problem, the independent claim features, the key dependent features, and whether a method claim exists.
- Reconstruct a provisional feature chain from the disclosure only when claims are absent, and state that the draft is claim-aligned only to the extent supported by the disclosure.

2. Build the section frame.
- Start with one purpose paragraph beginning with `本申请的目的在于...`.
- When the background already acknowledges a known technical route, add a short transition paragraph before `申请人发现，...` that fairly states what the known route can do and where its focus stops. Keep this route-agnostic: identify the known route's output or solved aspect, then identify the remaining break between that output and the claimed downstream processing.
- Before the first technical solution, add one cause-analysis paragraph beginning with `申请人发现，...` when the case benefits from explaining why the background defect arises.
- Use that paragraph to analyze the mechanism, operating scene, or process reason that causes the technical problem identified in `背景技术`, not to restate the defect in different words.
- Make the `申请人发现` paragraph sound like a natural field observation. Avoid piling up several parallel short phrases separated by `、`; prefer complete sentences that explain how the problem arises in actual use.
- Keep the `申请人发现` paragraph tightly aligned with the independent claim. Do not introduce problems that only a dependent claim or an unclaimed later update step can solve.
- Follow immediately with `为达成上述目的，采用如下技术方案：`.
- Default order: purpose paragraph, optional `申请人发现` cause-analysis paragraph, independent product or apparatus solution, main effect explanation, high-value preferred features, method solution, optional terminology clarifications.

3. Draft the main independent solution paragraph.
- Start with `在至少一个实施例中公开了...`.
- Follow the feature order of the independent claim instead of the order that is easiest to narrate.
- Keep terminology identical to the claim set. Do not rename components mid-section.
- Pack the technical features into one coherent paragraph unless readability clearly requires a split.
- Do not introduce label-only paragraphs such as `技术方案一：`, `基于技术方案一的技术方案二：`, or similar numbering captions before the方案段. Let the方案段 begin directly with `在至少一个实施例...`.

4. Draft the first effect paragraph immediately after the main solution.
- Start with `上述设计中，...`.
- Explain the chain `技术手段 -> 中间机理/作用过程 -> 技术效果`, not just `技术手段 -> 技术效果`.
- Name at least one intermediate principle when possible, such as force transmission, limiting relationship, contact state, motion path, flow path, sealing state, electrical connection, control timing, heat transfer path, or material interaction.
- Prefer `由于...，使得...，从而...` or `由于...，导致...，进而有利于...` to connect feature, principle, and effect.
- Frame the effect as a principle-based consequence within the disclosure, not as an unsupported conclusion.
- Do not write generic praise such as `效果好` or `体验佳` without identifying the responsible feature.
- Avoid direct assertions such as `具备...效果`、`具有显著...效果`、`能够大幅...` unless the disclosure or data expressly supports that level of certainty.
- Prefer restrained expressions such as `有利于...`、`从而减小...的可能性`、`从而改善...`、`从而提高...的稳定性/便利性` when the effect is inferred from mechanism rather than experimentally proven.
- For the main independent solution, the first effect block may use two or three natural paragraphs when needed: one paragraph explaining how the independent-claim features pass the relevant object, state, parameter, signal, position, or decision from one step to the next; one paragraph explaining why the features are cooperative rather than merely juxtaposed; and, when useful, one paragraph explaining the layered improvement path. Keep all three paragraphs anchored to independent-claim features only.
- Avoid an AI-like inventory style in effect paragraphs. Do not write long strings such as `A、B、C、D` or repeated noun phrases merely listing effects. Write the operating process in natural sentences and let each sentence show what the recited feature changes and what that enables next.
- When discussing inventive contribution in the effect block, explain it through the claimed step interaction and data path, not through slogans such as `协同闭环` unless the mechanism has been described.

5. Add additional problem-effect paragraphs only when the case needs them.
- Do not treat `申请人还发现，...` as mandatory.
- Use `申请人还发现，现有技术中...` only when, after the first technical solution and its first effect paragraph, there remains a further technical problem that the same solution or a later preferred solution can continue to address.
- Follow with `上述设计中，...` to show how the already-recited features solve that secondary pain point.
- Add `进一步地，...` only when the extra effect is a true extension of the same feature set.
- For dependent features, add `申请人还发现，...` only when the dependent feature solves a meaningful new problem that is not already fully explained by the independent solution. Use it before the dependent方案段, then write the dependent方案段 and its matching效果段.
- Do not add `申请人还发现` before every dependent feature. If the dependent feature merely narrows or specifies an implementation detail, write only the方案段 and效果段.

6. Draft preferred-feature blocks in alternating pairs.
- Use `在至少一个实施例公开的...中，优选地，...` for normal dependent features.
- Use `更优选地` only when the feature is a narrower or stronger optimization layered on top of a prior preferred feature.
- After each preferred-feature paragraph, add a matching `上述设计中，...` paragraph to explain why that feature is worth claiming.
- Cover only the high-value dependent features by default. Skip trivial manufacturing details unless the user asks for full coverage.

7. Draft the method block when a method claim exists.
- Place it after the product or apparatus blocks unless the user requests otherwise.
- Start with `在至少一个实施例中公开了...方法，所述方法包括：步骤1...；步骤2...；和步骤3...`.
- Follow with `上述方法...` to connect the method steps to the effects of the product or apparatus.
- Add method-specific convenience, stability, or process advantages only when the steps themselves support them.

8. Decide whether to add terminology clarifications.
- Add definition paragraphs only when the same terms recur across the specification and ambiguity would otherwise weaken the drafting.
- Keep definitions stable with the rest of the specification.
- Do not add a terminology block just because the reference case contains one.

## Style Rules

- Maintain the rhythm `方案段 -> 效果段`, especially for the main independent solution and the important preferred features.
- When needed, place one `申请人发现` cause-analysis paragraph before the first `方案段`; do not confuse that paragraph with a later `申请人还发现` paragraph.
- If known prior-art solutions are already present, acknowledge their limited contribution before the `申请人发现` paragraph. Do not pretend the art has no relevant starting point, partial solution, data source, control step, structural element, or process element when the disclosure says otherwise.
- Write effects as technical consequences, not as advertising language.
- Write effects through principle linkage: recite the relevant feature first, then the intermediate mechanism, then the resulting technical consequence.
- Tie every effect to a recited feature, feature relationship, or step arrangement.
- Avoid conclusory or absolute wording when the specification only supports reasoned inference.
- Keep the solution level aligned with the claims. Do not smuggle unclaimed matter into `发明内容`.
- Keep each effect paragraph within the problem-solving scope of the方案段 it follows. Do not use the independent-solution effect paragraph to claim advantages created only by later dependent features.
- Prefer natural Chinese patent prose over checklist prose. Reduce dense `、` lists where a sentence explaining the cause-and-effect relationship would be clearer.
- Preserve relative gradation: `优选地` for useful narrowing, `更优选地` for still narrower optimization.
- Use field-appropriate effects. Replace the pet-case language with the actual effect in the current technology.
- Keep the product-first, method-second ordering unless the application is fundamentally a method invention.

## Technical Effect Drafting

- For each effect paragraph, identify three layers before drafting: the cited feature, the physical or logical mechanism changed by that feature, and the final technical consequence.
- If the mechanism cannot be articulated, narrow the claimed effect instead of stretching the wording.
- Prefer concrete mechanism verbs such as `限位`、`支撑`、`隔离`、`导向`、`分流`、`贴合`、`释放`、`阻断`、`缓冲`、`均压`、`解耦`、`同步`、`减少接触面积`、`缩短传递路径`.
- Where the effect depends on conditions, say so. For example, note that a certain arrangement `更有利于` stability, sealing, or convenience under the disclosed use state, rather than stating that it always achieves that result.
- When several effects are claimed, split them into separate causal clauses if they arise from different mechanisms.
- Do not let one feature paragraph claim every desirable benefit unless each benefit is separately explained.

## Quality Checks

- Check that the opening purpose paragraph answers the defect identified in `背景技术`.
- Check whether the background or disclosure already admits a relevant prior-art route. If yes, include a fair prior-art transition before `申请人发现`.
- Check that any `申请人发现` paragraph analyzes the cause of the defect rather than merely repeating the defect itself.
- Check that `申请人发现` and `上述设计中` paragraphs do not rely on strings of parallel short phrases separated by `、` as the main writing style.
- Check that every major feature in the independent claim appears in the main solution paragraph.
- Check that every preferred feature has a corresponding effect paragraph or a clear reason to omit one.
- Check that any `申请人还发现` before a dependent feature introduces a real further problem and is not boilerplate.
- Check that every effect paragraph states at least one intermediate mechanism or action process between the feature and the final effect.
- Check that no effect overstates certainty beyond the disclosed mechanism.
- Check that conclusory verbs such as `具备`、`实现了显著`、`大幅提高` are removed or backed by explicit support.
- Check that term names, component names, and positional expressions are consistent with the claims and embodiments.
- Check that method steps do not assume operations not present in the method claim or disclosure.

## Reference

Read `references/reference-style.md` for the extracted cadence, sentence patterns, and reusable skeleton derived from the reference pet-case document.
