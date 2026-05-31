# Structural Case Embodiment Drafting

Use this reference when drafting or revising `具体实施方式` / `实施例` for Chinese structural, device, assembly, product, component-relation, or layered-structure patent cases.

## Contents

- [Core Rule](#core-rule)
- [Natural Integration Rule](#natural-integration-rule)
- [Claim-Phrase Elaboration Rule](#claim-phrase-elaboration-rule)
- [Geometric, Layout, And Boundary Terms](#geometric-layout-and-boundary-terms)
- [Coverage Checklist](#coverage-checklist)
- [Recommended Structure](#recommended-structure)
- [Figure and Reference-Numeral Discipline](#figure-and-reference-numeral-discipline)
- [Anti-Patterns](#anti-patterns)
- [Self-Check Before Finalizing](#self-check-before-finalizing)

## Core Rule

For a structural case, embodiments must do more than repeat the claims in prose. They must explain how each claimed structural expression maps to a physical, locatable, implementable structure so that a person skilled in the art can make and use the product after reading the embodiment and figures.

Draft the embodiment as structural explanation, not method narration:

- describe parts, materials, layers, surfaces, edges, directions, relative positions, and finished-state connections
- explain physical forms of abstract terms such as `线路`, `连接部`, `通道`, `支撑件`, `定位部`, `导向部`, `至少部分重合`, `对应`, `叠设`, `背侧`, `间隔设置`, `电连接`
- describe what the connection looks like in the finished product, and how current, force, fluid, heat, light, or signal is transmitted if that cooperation matters
- avoid turning the embodiment into a production process unless the case also claims a method or the structure cannot be understood without limited manufacturing context

## Natural Integration Rule

The coverage requirement is not a license to write a stiff glossary or one paragraph per claim term. The embodiment should read like a natural description of the product while progressively unfolding the structure shown in the figures.

Write in product/figure order, and weave the explanations into that flow:

- introduce a part, then naturally explain its material, physical form, position, and role in the same or adjacent paragraph
- when describing two related parts, explain their alignment, spacing, overlap, connection, or correspondence as part of that relationship
- explain broad terms at the moment they first matter structurally, rather than collecting definitions in isolated paragraphs
- combine related expressions when possible, e.g. explain `触点焊盘`, `连通孔`, `补电焊盘`, `至少部分重合`, and `对应电连接` together while describing the layer-to-layer conductive interface

The finished text should feel like a detailed product embodiment, not a checklist converted into prose. Use the checklist below to audit completeness after drafting, not as the outline itself.

## Claim-Phrase Elaboration Rule

Do not treat an embodiment as a cleaned-up copy of the claims. For each important claim phrase, add the missing structural explanation that a skilled reader needs to locate, visualize, and implement the feature.

Use this three-step expansion:

1. Identify what the phrase points to in the finished product: part, surface, layer, hole, rib, boundary, region, projection, or connection.
2. Explain how to recognize it physically: shape, orientation, position, edge/boundary, neighboring structures, and acceptable variants.
3. Explain how it cooperates with adjacent structures: how force, deformation, support, fluid, heat, electricity, light, or signal passes through or around it.

For example, a claim phrase such as `两端宽中间窄的条形孔` should not be left as that phrase alone. Explain that the hole has a length direction, two enlarged end regions, and a narrowed middle region; state whether the shape is understood in plan projection or section; give acceptable forms such as dumbbell-like, hourglass-like, or enlarged-ended slot-like shapes if supported; and explain why the narrowed middle preserves material around the hole. Likewise, a phrase such as `端部指向相邻孔的中部` should explain that this is a relative layout, not necessarily strict geometric collinearity, contact, or communication between holes.

## Geometric, Layout, And Boundary Terms

Structural embodiments often fail because geometric and relational claim language is copied without interpretation. Expand these terms where they first matter:

- `完整形状`: say whether completeness is judged in plan projection, cross-section, or another view; distinguish a full feature from an edge-truncated or boundary-cut feature; explain where complete units appear and where partial units may appear.
- Shape phrases such as `两端宽中间窄`, `腰形`, `环形`, `弧形`, `锥形`, or `台阶状`: identify the view direction, major/minor dimensions, wide and narrow regions, transitions, and whether exact mathematical contours are required.
- `平滑过渡`: state that the boundary changes continuously without sharp corners, right-angle notches, abrupt necking, or other local stress concentrators, unless the disclosure says otherwise.
- `阵列状布置`: explain rows/columns, repeated units, approximate spacing, and which variations are allowed near product edges, curved outlines, or local high-load areas.
- `相邻`, `依次相邻`, `交错`, `错位`, and `端部指向中部`: describe the local relationship between neighboring units. Clarify whether the relationship means alignment, projection correspondence, facing, offset, non-end-to-end adjacency, or a load-transfer path through retained material.
- `由...围合`, `外周侧`, `边界`, and `区域`: explain whether the feature is an internal region, an open cutout, a closed frame, a retained sidewall, a perimeter band, or another physical boundary.
- Segmented product regions such as foot, hand, garment, panel, blade, shell, or housing regions: distinguish support regions, deformation regions, transition boundaries, and load-bearing regions. Do not assign a function to a segment merely because it is adjacent; explain where the physical split lies and which segment actually deforms or carries load.

When body anatomy or use-state regions matter, be precise. For a shoe sole, for instance, do not write that a toe segment performs the metatarsal bending function if the physical split is behind the toes and the metatarsal-corresponding segment bends during push-off. State that the toe segment supports the toes, the split corresponds to the rear side of the toes, and the segment behind the split bears the metatarsal push-off deformation.

## Coverage Checklist

Use this as a drafting and self-check aid. For each independent-claim feature and important dependent-claim feature, ensure the embodiment naturally includes at least one of:

- **Physical form**: what the feature can be physically made of or look like, e.g. copper foil trace, plated pad, insulating substrate, molded rib, through hole, flexible sheet.
- **Location and orientation**: where it is on the product, which side/surface/layer/edge it belongs to, and what `front`, `back`, `upper`, `lower`, `length`, `width`, or `thickness` means in the case.
- **Relationship to other parts**: how it is connected, overlapped, spaced, supported, received, aligned, exposed, covered, fastened, or electrically/fluidly/mechanically coupled.
- **Implementable variants**: several acceptable forms when the claim uses broad language, without importing unclaimed limitations.
- **Functional cooperation**: how the structural relationship achieves the stated technical effect.

Do this especially for broad or relational expressions:

- `沿...方向延伸`: identify the product direction and whether the structure is continuous, segmented, repeated, or covers multiple units.
- `完整形状` / `完整轮廓`: identify the view where the complete contour is seen, and distinguish central full units from edge-adapted or truncated units.
- `阵列状布置` / `多排多列`: explain repeated rows/columns without requiring perfect mathematical grids unless that limitation is intended.
- `端部指向中部` / `对应中部`: explain the local adjacency and load path; make clear whether contact, communication, or exact center alignment is required.
- `电连接` / `连通` / `导通`: identify conductive/contact regions, connection media, contact surfaces, and separated positive/negative paths.
- `对应`: distinguish polarity correspondence, position correspondence, hole-to-pad correspondence, or one-to-one/many-to-one correspondence.
- `至少部分重合`: define it as projection overlap along the relevant direction; explain center alignment, eccentric overlap, edge overlap, larger-lower-pad overlap, etc.; state that complete contour coincidence is not required unless intended.
- `叠设` / `背侧`: state that the parts are layered in thickness direction rather than side-by-side, and identify the side/surface.
- `间隔设置`: explain the insulation, clearance, anti-short, positioning, or assembly purpose of the interval.
- `宽度小于或等于` / `边缘不超出`: explain which edges are compared and how this preserves the external product profile.
- `输入部` / `连接部` / `焊盘`: explain whether it is a local widened region, exposed conductive region, terminal area, plated region, opening in solder mask, connector region, etc.

## Recommended Structure

Use a product-description sequence like:

1. Define figure orientation and product directions.
2. Describe the whole product and the main parts.
3. Describe each main part's physical makeup.
4. Describe repeated units or segmentation features.
5. Explain geometric terms when the physical shape first appears.
6. Describe connection interfaces and relative-position terms together with the parts that form those interfaces.
7. For arrays or repeated units, explain how units repeat, vary near boundaries, and cooperate through retained material between units.
8. Fold broad relational terms and implementable variants into the relevant structural paragraphs.
9. Explain dependent features such as materials, pad forms, widths, edge constraints, and input/output portions where they arise in the product description.
10. Close with how the assembled structure realizes the technical effect.

## Figure and Reference-Numeral Discipline

Embodiments should cite figures to anchor spatial relationships, e.g. `如图1至图3所示`. Whether to include reference numerals depends on the drafting convention or user instruction.

- If the user says not to introduce reference numerals in the embodiment, use part names only and avoid forms like `灯带线路板10`.
- If reference numerals are used, keep them consistent with `主要附图标记说明` and do not create new numerals in the embodiment text.

## Anti-Patterns

Avoid:

- merely restating every claim sentence with `在一种实施方式中...`
- drafting a rigid term-by-term glossary or one isolated paragraph for every claim expression
- using method-case language such as `首先、然后、再将、步骤`
- leaving broad structural terms unexplained, especially `补电线路`, `连接部`, `至少部分重合`, `对应电连接`
- leaving shape and layout phrases unexplained, especially `完整形状`, `两端宽中间窄`, `阵列状布置`, `依次相邻`, `端部指向中部`
- saying only that a structure `有利于支撑/回弹/稳定` without first explaining the physical load path, retained material path, contact boundary, or deformation boundary
- confusing adjacent product regions with functional regions, e.g. assigning push-off bending to a toe-support segment when the segment behind the toe split actually bends
- adding unverified parts, extra layers, adhesives, holes, clamps, process temperatures, or manufacturing parameters that are not supported by the disclosure
- importing limitations from examples that should remain optional in the claims

## Self-Check Before Finalizing

Ask:

- Can every independent-claim noun phrase be pointed to in the embodiment as a physical structure?
- Can every relational phrase be understood as a finished-product position or connection relationship?
- Can every geometric phrase be visualized in the relevant view, and did you state whether exact contours or approximate forms are intended?
- For arrays or repeated units, did you explain rows/columns, edge variations, neighboring-unit relationships, and the material retained between units?
- For segmented structures, did you identify the physical split location and avoid confusing support, deformation, and load-bearing functions across segments?
- Did the embodiment explain at least one concrete implementable form for each broad expression?
- Did it preserve claim breadth by giving examples without turning them into mandatory limitations?
- Does the text read like a natural product description rather than a claim-term checklist?
- Is the tone structural and descriptive, not procedural?
- Are figure references and reference numerals consistent with the user's requested convention?
