# Reference Style

## Extracted Cadence From The Pet Case

Use the following sequence as the default drafting rhythm:

1. Purpose paragraph.
- Start with `本申请的目的在于...`.
- Point directly at the defect already identified in `背景技术`.

2. Optional cause-analysis paragraph before the first solution.
- Use `申请人发现，...` when it helps explain why the background technical problem occurs.
- Analyze the cause or mechanism behind the defect, rather than repeating the defect itself.

3. Technical-solution lead-in.
- Use `为达成上述目的，采用如下技术方案：`.

4. Main independent solution block.
- Start with `在至少一个实施例中公开了...`.
- Recite the solution in claim order.

5. Immediate effect explanation.
- Start with `上述设计中，...`.
- Explain the basic function and the first-order technical effect through a visible mechanism chain, not by directly asserting the result.

6. Secondary problem and effect blocks when needed.
- Do not add `申请人还发现，...` by default.
- Use `申请人还发现，现有技术中...` only when, after the first solution and its first technical effect, there is still a further technical problem worth explaining.
- Follow with another `上述设计中，...` paragraph showing why the recited structure solves that pain point.
- Use `进一步地，...` only to deepen the same causal chain.

7. Preferred-feature blocks.
- Use `在至少一个实施例公开的...中，优选地，...`.
- Use `更优选地` for a narrower optimization on top of a prior preferred feature.
- After each preferred feature, write a matching `上述设计中，...` paragraph.

8. Method block.
- Use `在至少一个实施例中公开了...方法，所述方法包括：步骤1...；步骤2...；和步骤3...`.
- Follow with `上述方法...` to explain the process effect.

9. Optional terminology clarifications.
- Add only if the specification repeatedly uses terms that require unified meaning.

## Sentence Patterns

- `本申请的目的在于解决......并公开一种......。`
- `申请人发现，导致上述技术问题的原因在于......。`
- `为达成上述目的，采用如下技术方案：`
- `在至少一个实施例中公开了一种......，所述......包括......；所述......。`
- `上述设计中，由于......，使得......，从而有利于......。`
- `上述设计中，由于......，导致......，进而减小了......的可能性。`
- `上述设计中，基于......形成的......作用，因而改善了......。`
- `申请人还发现，现有技术中......。`
- `进一步地，......。`
- `在至少一个实施例公开的......中，优选地，......。`
- `在至少一个实施例公开的......中，更优选地，......。`
- `在至少一个实施例中公开了......方法，所述方法包括：步骤1......；步骤2......；和步骤3......。`
- `上述方法实现了......，从而体现出前述......对应的技术效果。`

## Reusable Skeleton

```text
本申请的目的在于解决【背景技术中的核心缺陷】，并公开一种【发明名称】，其相较于现有技术【概括核心效果】。

申请人发现，导致上述技术问题的原因在于【对缺陷成因的机制分析】。

为达成上述目的，采用如下技术方案：

在至少一个实施例中公开了【独立方案名称】，所述【独立方案名称】包括【按权利要求顺序列出的核心特征】。

上述设计中，由于【核心特征/特征关系】，使得【中间机理或作用过程】，从而有利于【第一层技术效果】。

申请人还发现，现有技术中【第二缺陷】。

上述设计中，由于【前述特征】，导致【针对第二缺陷的中间机理】，进而有利于【解决第二缺陷的效果】；进一步地，【延伸效果】。

在至少一个实施例公开的【独立方案名称】中，优选地，【从属特征】。

上述设计中，由于【从属特征】，使得【从属机理变化】，从而有利于【从属技术效果】。

在至少一个实施例中公开了【方法名称】，所述方法包括：步骤1【...】；步骤2【...】；和步骤3【...】。

上述方法【实现的过程效果或使用效果】。
```

## What To Emulate

- Alternate `方案段` and `效果段` instead of stacking all effects at the end.
- Add `申请人发现` before the first `方案段` only when the cause analysis helps the reader understand why the first solution is arranged as claimed.
- Keep the narrative tightly tied to the claim structure.
- Use repeated sentence stems to make the section read like a mature patent draft.
- Add `申请人还发现` only when a later paragraph is truly introducing a further problem after the first solution-effect pair.
- Write every effect paragraph as `特征 -> 机理 -> 效果`, not as a bare assertion that the feature "has" a certain effect.

## What To Adapt

- Replace pet-specific comfort language with the actual domain effect in the target case.
- Omit the `申请人发现` paragraph when the cause analysis would be empty, obvious, or repetitive.
- Remove method content if the application has no method claim.
- Remove terminology definitions unless they are genuinely needed for consistency.
- Soften wording when the effect is reasoned from structure or process rather than proven by data.
- Avoid copying the reference case verbatim; reuse only the cadence and drafting logic.
