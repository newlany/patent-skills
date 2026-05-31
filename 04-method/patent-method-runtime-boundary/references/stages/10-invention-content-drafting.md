# Stage 10: Invention-Content Drafting

This is the shared invention-content drafting standard for this family of method-patent skills.

## Enter this stage when

- the user asks for stage 10
- the user asks for 发明内容 or 技术效果
- the claims and main technical route are fixed

## Required baseline

- confirmed claim set
- confirmed final disclosure
- confirmed inventive-step main line

## Task focus

- use the same drafting cadence as [$patent-stage-invention-content](/Users/chrynos/.codex/skills/patent-stage-invention-content/SKILL.md), adapted to method cases
- draft the purpose paragraph so it corresponds to the prior-art phenomena stated in background
- draft a natural `申请人发现` opening that explains why the prior-art phenomena arise in actual use
- draft the main solution paragraph in claim order
- draft the first effect paragraphs around step-to-step information or state transfer, key inventive means, and their interaction
- draft preferred-feature paragraphs aligned with dependent claims
- when a dependent claim only narrows a post-run support-resource update, keep the preferred-feature paragraph in that same update register and do not expand it into an extra independent-step narrative

## Method-style drafting rules

- by default, use the opening order `phenomenon correspondence -> cause attribution -> main solution -> main effect`
- let the main solution paragraph begin directly with `在至少一个实施例中公开了...方法`
- do not use label-only openings such as `技术方案一`
- let the opening `申请人发现` part explain why the prior-art phenomena arise; do not leave that analysis in background by default
- for material, formulation, preparation, foaming, dispersion, or compounding cases, make that cause analysis physical: phase compatibility, viscosity and shear history, particle migration, interface wetting, water-isocyanate side reaction, gas generation, cell nucleation, heat or mass transfer, residence time, and additive distribution are better anchors than abstract labels alone
- in the first effect paragraph, explain the runtime chain through `step feature -> intermediate mechanism/process -> technical consequence`
- if the effect depends on step interaction, explain how the output of one step becomes the input or basis of the next step
- when the inventive point lies in layered or additive improvement, explain how the earlier step or control layer solves one issue and how the later step or control layer addresses the further issue that remains
- make the main effect paragraph explain not only what phenomenon is improved, but also how the case's key inventive means actually take effect
- in material-process cases, connect the effect to the material or process state that changes, such as pigment distribution before foaming, moisture influence on foam stability, reactive-carrier incorporation into the polymer system, or melt mixing state before injection
- when multiple technical means jointly matter, explicitly write the cooperation among target setting, state recognition, prediction or compensation, and execution-level adjustment instead of listing them side by side
- keep the main effect paragraph within the scope of the independent claim
- when a dependent feature is drafted as `resource updated by writeback`, mirror that wording in invention content instead of rewriting it as a broader `writeback for later correction/update use` story
- use `申请人还发现` only when a dependent feature solves a meaningful further problem
- avoid dense `、` lists as the main writing style; prefer natural causal sentences
- if the user wants a less AI-like style, prefer direct definitions and restrained technical-effect wording
- if the user wants a less AI-like style, also split long effect or attribution chains into shorter sentences where possible; do not compress the whole effect path into one oversized sentence

## Deliverable

- invention-content section ready for the specification

## Guardrails

- do not let the main effect paragraph depend on features outside the independent claim
- do not reduce the main effect to a generic problem-solving sentence; explain the effect path of the inventive key means
- avoid inventory-style effect writing or dense `、` lists as the main style
- avoid long stacked sentences in the opening attribution and main effect paragraphs when the same point can be stated in two or three shorter sentences
- do not let invention-content wording drift away from the adopted claim chain or method boundary

## Stop rule

Stop after the invention-content section and wait for confirmation before embodiments.
