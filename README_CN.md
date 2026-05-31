# 专利技能备份与整理

> 整理日期：2026-05-30
> 原始目录：`~/.codex/skills/`（未做任何修改）

---

## 一、这个目录是什么

这个目录是对 `~/.codex/skills/` 下所有专利相关 skill 的**完整备份、去重、分类和优化**。

原始 skill 目录完全没有被动过。所有原始文件的副本都保存在 `01-entry/` 到 `09-tools/` 这九个分类文件夹中。`universal/` 文件夹里是经过优化的、可以在 Claude Code 和 Codex 上通用的新版本。

---

## 二、目录结构

```
patent-skills-backup/
│
├── README_CN.md                 ← 你正在看的这个文件
├── DEDUPLICATION-REPORT.md      ← 去重报告（英文）
├── WORKFLOW-CONSTRAINTS.md      ← 流程约束设计（英文）
│
├── universal/                   ← ★ 优化后的通用技能（推荐使用）
│   ├── CLAUDE.md                ← 全局规则文件
│   ├── INSTALL.md               ← 安装说明（英文）
│   ├── install.sh               ← 一键安装脚本
│   ├── patent-cn/               ← 主路由入口
│   ├── patent-cn-draft/         ← 撰写流程编排器
│   ├── patent-cn-response/      ← 答复流程编排器
│   ├── patent-cn-review/        ← 质检流程编排器
│   ├── patent-cn-doctor/        ← 系统健康检查
│   ├── code2patent/             ← 代码转专利
│   └── hooks/                   ← 流程强制执行钩子
│       ├── hooks.json
│       ├── patent_stage_gate.py       ← 阶段门控（阻止跳步）
│       ├── patent_artifact_reminder.py ← 工件注册提醒
│       └── patent_completion_gate.py   ← 完成声明验证
│
├── 01-entry/                    ← 原始入口技能（6个）
├── 02-workflow/                 ← 原始工作流编排器（8个）
├── 03-stage/                    ← 原始阶段专家（10个）
├── 04-method/                   ← 原始方法专利专家（8个）
├── 05-support/                  ← 原始文档支持（6个）
├── 06-qc/                       ← 原始质检（3个）
├── 07-research/                 ← 原始研究分析（2个）
├── 08-doc-output/               ← 原始文档生成（2个）
├── 09-tools/                    ← 原始运行时工具（1个）
└── patent_*.toml                ← 原始 Agent 定义（11个）
```

---

## 三、去重结果

从约 50 个专利相关 skill 中，去重后保留 38 个独立技能，删除/合并了 7 个重复项：

| 去重项 | 保留 | 删除 | 原因 |
|--------|------|------|------|
| Google Patents 下载 | `patent-support-google-patents-pdfs` | `download-google-patents-pdfs` | 前者更通用，后者仅适配 OA 文件夹布局 |
| DOCX 公式支持 | `patent-support-docx-math` | `patent-docx-math` | 前者多一个 `replace_docx_text_preserve_runs.py` 脚本 |
| 顶级路由 | `patent-cn` | `patent-workflow-router` | `patent-cn` 是规范入口，后者是旧版 |
| 课题研究 | `patent-topic-deep-research` | `patent-research-topic` | 前者是超集，包含完整方法论和模板 |
| 交底分析 | 保留两个 | — | `patent-disclosure-agent`（公开）+ `patent-stage-disclosure-analysis`（内部引擎） |
| OA 答复 | 保留两个 | — | `patent-oa-response`（公开）+ `patent-entry-oa-response`（内部引擎） |
| 形式审查 | 保留两个 | — | `cn-patent-formal-check`（公开）+ `patent-qc-cn-formality`（内部） |

---

## 四、分类说明

### 01-entry/（6个）—— 顶级入口

用户直接调用的入口技能。所有专利工作都必须从这里开始。

| 技能 | 用途 |
|------|------|
| `patent-cn` | **主路由**：分析用户意图，分发到正确的流程 |
| `patent-cn-draft` | **撰写编排器**：交底 → 查新 → 重构 → 权利要求 → 说明书 → 质检 |
| `patent-cn-response` | **答复编排器**：审查意见、补正、无效、口审 |
| `patent-cn-review` | **质检编排器**：形式审查、一致性检查、公式检查 |
| `patent-cn-doctor` | **系统检查**：依赖项、工具、模板是否就绪 |
| `code2patent` | **代码转专利**：从代码仓库提取技术交底并生成专利草稿 |

### 02-workflow/（8个）—— 公开工作流

面向用户的完整工作流入口。

| 技能 | 用途 |
|------|------|
| `patent-disclosure-agent` | 交底分析（产出 3 份报告 + 索引） |
| `patent-oa-response` | OA 答复全流程（9 个阶段） |
| `patent-invalidity-hearing-prep` | 无效宣告 + 口审准备 |
| `patent-topic-deep-research` | 专利课题深度研究 |
| `patent-research-records` | 专利档案检索（法律状态、家族、诉讼） |
| `patent-chatgpt-pro-handoff` | 将材料打包交给 ChatGPT Pro 处理 |
| `oa-correction-docx` | 补正处理（下载通知书 → 修改 → 替换页） |
| `patentwang-decision-downloader` | 从 patent.wang 下载无效/复审决定书 PDF |

### 03-stage/（10个）—— 内部阶段专家

由编排器内部调用，用户不应直接使用。

| 技能 | 用途 |
|------|------|
| `patent-entry-drafting` | 核心撰写引擎（13 步链） |
| `patent-stage-disclosure-analysis` | 交底分析引擎 |
| `patent-stage-prior-art-search` | 现有技术检索引擎 |
| `patent-stage-invention-content` | 发明内容撰写 |
| `patent-stage-embodiments` | 具体实施方式撰写 |
| `patent-entry-oa-response` | OA 答复引擎 |
| `patent-entry-invalidity` | 无效流程引擎 |
| `patent-stage-invalidity-hearing-prep` | 口审准备引擎 |
| `patent-analysis-fixed-patent` | 固定专利/对比文件分析 |
| `patent-inventor-questions` | 发明人补充问题清单起草 |

### 04-method/（8个）—— 方法专利专家

针对不同类型方法专利的专门处理。

| 技能 | 用途 |
|------|------|
| `patent-method-route-helper` | 方法专利路由决策 |
| `patent-method-runtime-boundary` | 运行时/步骤链方法 + 共享工作流基础 |
| `patent-method-process-route` | 工艺/材料/配方方法 |
| `patent-method-formula-model` | 公式/模型/仿真方法 |
| `patent-method-boundary-alignment` | 方法边界对齐工具 |
| `patent-cn-software-embodiment-layout` | 软件/AI/算法专利说明书布局 |
| `anta-method-patent-agent` | 安踏专属方法专利流程 |
| `xmu-method-patent-agent` | 厦大专属方法专利流程 |

### 05-support/（6个）—— 文档与工具支持

为各工作流提供文档处理和工具支持。

| 技能 | 用途 |
|------|------|
| `patent-support-google-patents-pdfs` | Google Patents PDF 下载 |
| `patent-support-docx-math` | DOCX 公式安全检查/提取/转换 |
| `patent-support-correction-docx` | 补正通知书处理 + 替换页生成 |
| `cn-patent-invention-content` | 发明内容章节撰写 |
| `patent-drawing-generator` | 专利附图/流程图生成 |
| `patent-external-brief-docx` | 对外沟通文件 DOCX 生成 |

### 06-qc/（3个）—— 质量控制

| 技能 | 用途 |
|------|------|
| `patent-qc-cn-formality` | CNIPA 形式缺陷检查（自动修复） |
| `patent-qc-application-consistency` | 申请文件一致性检查 |
| `patent-application-checker` | 附图标记增删操作 |

### 07-research/（2个）—— 研究分析

| 技能 | 用途 |
|------|------|
| `patent-analysis` | 7 种场景通用分析（杨卫薪律师） |
| `patent-topic-deep-research` | 专利课题深度研究 |

### 08-doc-output/（2个）—— 文档生成

| 技能 | 用途 |
|------|------|
| `patent-application-correction-docx` | 补正替换页生成 |
| `patent-proposal-list` | 专利提案清单生成 |

### 09-tools/（1个）—— 运行时基础设施

| 技能 | 用途 |
|------|------|
| `patent-cn-runtime` | 工具注册表 + JSON 工具调用层 |

---

## 五、Agent 定义（11个 .toml 文件）

这些 agent 定义了一条线性撰写流水线：

```
文件接收 → 交底分析 → 现有技术检索 → 方案重构 → 权利要求撰写 → 说明书撰写 → 最终质检
```

| Agent | 角色 |
|-------|------|
| `patent_drafting_orchestrator` | 撰写流水线总调度 |
| `patent_file_intake_specialist` | 文件接收 + 公式保护 |
| `patent_disclosure_analyst` | 交底分析专家 |
| `patent_prior_art_searcher` | 现有技术检索专家 |
| `patent_solution_reconstructor` | 方案重构专家 |
| `patent_claim_drafter` | 权利要求撰写专家 |
| `patent_spec_writer` | 说明书撰写专家 |
| `patent_application_qc` | 最终质检专家 |
| `patent_oa_responder` | OA 答复专家（并行） |
| `patent_invalidity_strategist` | 无效策略专家（并行） |
| `patent_topic_researcher` | 课题研究专家（并行） |

---

## 六、如何使用

### 方式一：一键安装（推荐）

```bash
cd /Users/chrynos/.codex/patent-skills-backup/universal
./install.sh all
```

这会为 Claude Code、Codex、Cursor 同时创建符号链接。

也可以只安装某个平台：
```bash
./install.sh claude    # 只装 Claude Code
./install.sh codex     # 只装 Codex
./install.sh cursor    # 只装 Cursor
```

### 方式二：手动安装

#### Claude Code

```bash
# 复制技能到 Claude Code 全局技能目录
mkdir -p ~/.claude/skills
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-draft ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-response ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-review ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/patent-cn-doctor ~/.claude/skills/
cp -r /Users/chrynos/.codex/patent-skills-backup/universal/code2patent ~/.claude/skills/

# 复制全局规则
cp /Users/chrynos/.codex/patent-skills-backup/universal/CLAUDE.md ~/.claude/CLAUDE.md
```

#### OpenAI Codex

```bash
# 创建符号链接
CODEX_SKILLS="/Users/chrynos/.codex/skills"
UNIVERSAL="/Users/chrynos/.codex/patent-skills-backup/universal"

for skill in patent-cn patent-cn-draft patent-cn-response patent-cn-review patent-cn-doctor code2patent; do
  ln -sfn "$UNIVERSAL/$skill" "$CODEX_SKILLS/$skill"
done

# 复制钩子
cp "$UNIVERSAL/hooks/hooks.json" "/Users/chrynos/.codex/hooks/hooks.json"
```

---

## 七、流程约束机制（5 层防护）

这套优化版本的核心价值在于**强制 agent 按步骤执行**，不会跳步或遗漏。

### 第 1 层：SKILL.md 前置约束

每个 skill 的 YAML frontmatter 定义了：
- `allowed-tools`：限制该 skill 可以使用的工具
- `description`：精确的触发词，避免调错 skill
- `user-invocable: true`（仅入口技能）/ `false`（内部技能）

### 第 2 层：阶段门控（硬阻止）

hook 脚本 `patent_stage_gate.py` 在每次写文件前检查：
- 如果要写「权利要求」，但「现有技术检索」未完成 → **阻止写入**
- 如果要写「说明书」，但「权利要求」未完成 → **阻止写入**
- 依此类推，严格按 `交底 → 查新 → 重构 → 权利要求 → 说明书 → 质检` 顺序

### 第 3 层：工件注册提醒

hook 脚本 `patent_artifact_reminder.py` 在每次写 `输出/` 目录后提醒：
- "请通过 `patent_workflow.py add-artifact` 将工件注册到 manifest.json"

### 第 4 层：完成声明验证

hook 脚本 `patent_completion_gate.py` 在 agent 声明完成时检查：
- 如果 agent 说了"filing-ready"或"drafting-complete"但没提到"validate" → **阻止停止**

### 第 5 层：CLAUDE.md 全局规则

这些规则对所有专利 skill 生效，不可被覆盖：

1. **阶段顺序强制**：交底 → 查新 → 重构 → 权利要求 → 说明书 → 质检，不可跳过
2. **编排器优先**：所有工作必须从 `patent-cn` 进入，禁止直接调用内部 skill
3. **Manifest 即真相**：所有工件必须注册到 `manifest.json`
4. **模板合规**：意见陈述必须用指定模板，申请文件必须用 `专利撰写模板文件.docx`
5. **验证后才能完成**：不运行 `patent_workflow.py validate` 就不能声明完成
6. **中文命名**：人类可读文件用中文命名
7. **懒创建目录**：只在写文件时才创建该文件的父目录
8. **不确定就停下**：路由信心低时问一个问题，不要猜

---

## 八、完成声明术语（仅限这些）

| 术语 | 含义 | 前置条件 |
|------|------|----------|
| `drafting-complete` | 所有草稿阶段工件存在，验证无硬失败 | 所有阶段门控通过 |
| `filing-ready` | 最终 DOCX/包存在，验证无硬失败和软失败 | 所有阶段门控 + 最终质检通过 |
| `blocked` | 无法继续，需要用户输入 | 已识别具体阻塞项 |
| `needs-fix` | 质检发现问题，必须修复 | 质检门控失败 |

**禁止使用**：`ready`、`done`、`complete`、`finished`（不带前缀）。

---

## 九、使用示例

### 示例 1：撰写新申请

```
用户：这个交底帮我走流程
↓
patent-cn（路由）→ 识别为"撰写"意图
↓
patent-cn-draft（编排器）
  ├─ 阶段 1：交底分析 → 产出 3 份报告
  ├─ 阶段 2：现有技术检索 → 产出检索报告
  ├─ 阶段 3：方案重构 → 产出撰写策略
  ├─ 阶段 4：权利要求 → 产出权利要求书
  ├─ 阶段 5：说明书 → 产出说明书全文
  └─ 阶段 6：质检 → 产出质检报告
↓
声明 drafting-complete 或 filing-ready
```

### 示例 2：处理审查意见

```
用户：处理这个审查意见
↓
patent-cn（路由）→ 识别为"答复"意图
↓
patent-cn-response（编排器）
  ├─ 阶段 1：OA 分解 → 提取问题 + 识别 D1/Dx
  ├─ 阶段 2：D1/Dx 验证 → 下载对比文件
  ├─ 阶段 3：修改决策 → 决定修改还是争辩
  ├─ 阶段 4：答复撰写 → 产出意见陈述（用模板）
  └─ 阶段 5：替换页 + 质检
↓
声明完成
```

### 示例 3：代码转专利

```
用户：从这个代码仓库生成专利
↓
code2patent（独立流程）
  ├─ 步骤 1：代码分析 → 方案-代码证据映射表
  ├─ 步骤 2：交底生成 → 技术交底书
  ├─ 步骤 3：权利要求布局 → 布局卡片 + 证据矩阵
  └─ 步骤 4：专利草稿 → 说明书 + 权利要求 + 摘要 + 自检表
↓
如需进一步完善，转入 patent-cn-draft
```

---

## 十、常见问题

### Q: 安装后旧的 skill 还能用吗？
A: 能。安装脚本创建的是符号链接，旧目录里的原始 skill 完全不受影响。如果你同时有旧版和新版 skill，Claude Code 会优先加载 `~/.claude/skills/` 下的版本。

### Q: hooks 会不会影响其他非专利 skill？
A: 不会。hooks 只在文件路径包含 `输出/` 或 `记录/` 时触发，这些是专利工作流专用目录。

### Q: 我能只安装某个 skill 吗？
A: 可以。`universal/` 下每个文件夹都是独立的 skill，可以单独复制到 `~/.claude/skills/` 或 `~/.codex/skills/`。

### Q: 原始的 agent .toml 文件需要安装吗？
A: 如果你使用 Codex 的 agent 系统，需要把 `.toml` 文件复制到 `~/.codex/agents/`。如果只用 Claude Code，不需要——Claude Code 使用自己的 agent 格式。

---

## 十一、关键文件快速索引

| 文件 | 用途 |
|------|------|
| `README_CN.md` | 本文件，中文说明 |
| `DEDUPLICATION-REPORT.md` | 去重决策详细报告 |
| `WORKFLOW-CONSTRAINTS.md` | 约束架构设计文档 |
| `universal/CLAUDE.md` | 全局规则（安装到 `~/.claude/CLAUDE.md`） |
| `universal/install.sh` | 一键安装脚本 |
| `universal/hooks/hooks.json` | 钩子配置 |
| `universal/hooks/patent_stage_gate.py` | 阶段门控脚本 |
| `universal/hooks/patent_artifact_reminder.py` | 工件注册提醒脚本 |
| `universal/hooks/patent_completion_gate.py` | 完成验证脚本 |
