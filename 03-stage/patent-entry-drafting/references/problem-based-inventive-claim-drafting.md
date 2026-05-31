# Problem-Based Inventive Claim Drafting

Use this reference when reconstructing inventive contribution, deciding claim scope, drafting claims, or revising claims after prior-art pressure.

## Core Rule

Do not build inventive contribution from a flat list of features. Start from the technical problem and the technical contradictions inside that problem.

Every important claim feature should answer:

1. What technical contradiction does this feature address?
2. What structural or procedural means is used?
3. What direct technical effect follows from that means?
4. Why would the prior art not combine the means for the same contradiction?

If a feature cannot be tied to a contradiction, keep it out of the independent claim unless the user deliberately wants a narrow commercial embodiment claim.

## Analysis Pattern

For each invention, write a short problem chain before drafting claims:

```text
Total technical problem:
<one sentence>

Contradiction 1:
- technical contradiction:
- technical means:
- direct technical effect:
- claim consequence:

Contradiction 2:
- technical contradiction:
- technical means:
- direct technical effect:
- claim consequence:
```

The `claim consequence` should say whether the means belongs in the independent claim, a dependent claim, the specification, or only the inventive-step argument.

## Independent Claim Strategy

The independent claim should close the main contradiction chain, not merely recite the most visible parts.

Include in the independent claim:

- features that create the basic technical boundary or operating route;
- features that resolve the primary conflict between competing requirements;
- features that prevent the main solution from causing a new structural or procedural failure;
- concrete structure or step relationships that distinguish over crowded prior art.

Usually keep out of the independent claim:

- pure technical effects;
- mechanism speculation not directly supported by the disclosure;
- marketing or performance language;
- parameters without support or without necessity;
- broad labels from crowded art when concrete structure is available.

If a support or boundary feature is necessary to make the main technical problem coherent, move it into the independent claim rather than treating it as a late fallback.

## Dependent Claim Strategy

Order dependent claims by the sub-problems they solve, not by drawing order.

Each claim must state a technical solution, not merely introduce a name or relabel a feature already present in an earlier claim. A dependent claim should add at least one substantive structural, positional, dimensional, material, process, control, sequence, or interaction limitation. If a proposed dependent claim only defines terms such as "凸出部" and "收缩部" for already-recited shapes, either delete it, move the terminology explanation to the specification, or rewrite it so the claim adds a concrete relationship, such as how the corresponding portions of adjacent units contact, align, limit, support, seal, guide, or deform.

Useful fallback layers:

- boundary definition or deformation boundary;
- size, proportion, range, or location that balances competing requirements;
- geometry that explains how material is removed while support remains;
- layout, stagger, alternation, grouping, or sequence that prevents weak paths;
- ribs, walls, frames, supports, or connection members that preserve continuity;
- upper/lower layers, plates, housings, carriers, or external components that stabilize the claimed structure;
- material examples and measured data only after the structural fallback layers.

For multiple independent product tiers, such as component and finished product, repeat the core structure in the later independent claim when requested or strategically useful; do not force a dependency if the user wants two independent claims.

## Prior-Art Argument Rule

When comparing prior art, do not stop at "D1 lacks feature X".

Use this frame:

```text
Even if D1 discloses <known feature>, it addresses <different problem>.
It does not start from the contradiction between <requirement A> and <requirement B>.
It therefore does not provide motivation to combine <means 1> and <means 2> in the claimed relationship.
```

This is especially important when the prior art is crowded around a buzzword or functional label.

## High-Quality Reference Style Rule

Before drafting or revising claims and specification sections after Checkpoint A/B, read the search memo's `Reference Drafting Quality` section or `输出/过程/02_现有技术检索/参考文献撰写质量.md` if present.

If a technically relevant comparison document is marked high quality, you may use it as a writing-style reference for:

- term definitions and consistent terminology
- independent-claim boundary phrasing
- dependent-claim fallback layering
- problem-solution framing and effect linkage
- embodiment organization and section transitions

This does not override the problem-based inventive-contribution analysis. Do not copy unsupported technical features, experimental data, claim scope, or long passages; adapt only the drafting technique to the current disclosure and selected invention strategy.

## Structural Drafting Rule

Prefer observable structure over functional labels.

For structural/product cases:

- describe shape, location, boundary, layout, spacing, orientation, grouping, connection, and layer relationship;
- use effects in the specification and inventive-step memo;
- avoid relying on labels such as "负泊松比", "智能", "高弹", "高稳定", or "自适应" as claim limitations when concrete structure can be stated;
- if a crowded label is useful, place it in the specification as optional effect or mechanism, not as the only claim feature.

## Stage Output Rule

When this rule changes claim strategy, create or update:

- `输出/过程/03_方案重构/创造性来源逻辑.md` or equivalent problem-chain memo;
- `输出/过程/04_权利要求/权利要求当前稿.md`;
- `输出/过程/04_权利要求/权利要求撰写策略-*.md` when claim-scope decisions are material;
- a `记录/04_权利要求/报告/*-stage-report.json` stage report.

Run deterministic claim QC after drafting and record the tool run when the workflow case folder exists.
