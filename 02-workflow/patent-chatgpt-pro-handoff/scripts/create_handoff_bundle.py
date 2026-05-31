#!/usr/bin/env python3
"""Create a local ChatGPT Pro handoff bundle for Chinese patent workflows."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
RULE_DIR = SKILL_DIR / "references" / "chatgpt-rules"
DEFAULT_MAX_DOCUMENTS = 20
BASE_DOCUMENT_COUNT = 10
TEXT_SOURCE_SUFFIXES = {
    ".csv",
    ".htm",
    ".html",
    ".json",
    ".md",
    ".tex",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
MAX_MERGED_TEXT_BYTES = 1_500_000


COMMON_RULES = ["00_通用处理规则.md", "50_输出格式规则.md"]
TASK_RULES = {
    "claims": ["10_权利要求撰写规则.md"],
    "background": ["21_背景技术规则.md"],
    "invention-content": ["10_权利要求撰写规则.md", "22_发明内容规则.md"],
    "embodiments": ["20_说明书撰写规则.md", "23_具体实施方式规则.md"],
    "specification": [
        "10_权利要求撰写规则.md",
        "20_说明书撰写规则.md",
        "21_背景技术规则.md",
        "22_发明内容规则.md",
        "23_具体实施方式规则.md",
    ],
    "oa-response": ["10_权利要求撰写规则.md", "30_审查意见答复规则.md"],
    "invalidity": ["10_权利要求撰写规则.md", "30_审查意见答复规则.md"],
    "review": ["20_说明书撰写规则.md"],
    "prior-art": ["21_背景技术规则.md", "30_审查意见答复规则.md"],
    "generic": [],
}
FORMULA_RULE = "40_公式与DOCX规则.md"


def safe_slug(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\\s]+", "_", value.strip())
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:80] or "ChatGPT交接"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def selected_rules(task_kind: str, has_formulas: bool) -> list[str]:
    names = list(COMMON_RULES)
    for name in TASK_RULES.get(task_kind, []):
        if name not in names:
            names.append(name)
    if has_formulas and FORMULA_RULE not in names:
        names.append(FORMULA_RULE)
    return names


def is_text_source(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SOURCE_SUFFIXES


def unique_target_path(directory: Path, name: str) -> Path:
    target = directory / name
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    counter = 2
    while True:
        candidate = directory / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def process_sources(
    sources: list[Path],
    material_dir: Path,
    binary_budget: int,
) -> dict[str, object]:
    copied = []
    merged = []
    deferred = []
    merged_blocks = []
    for source in sources:
        source = source.expanduser().resolve()
        if not source.exists():
            deferred.append({"source": str(source), "status": "missing", "reason": "source not found"})
            continue
        if source.is_dir():
            deferred.append({
                "source": str(source),
                "status": "deferred",
                "reason": "directory must be inventoried or extracted into the material digest before web upload",
            })
            continue
        if is_text_source(source) and source.stat().st_size <= MAX_MERGED_TEXT_BYTES:
            try:
                text = read_text(source)
            except UnicodeDecodeError:
                text = source.read_text(encoding="utf-8", errors="replace")
            merged_blocks.append(f"### 源文件：{source.name}\n\n```text\n{text}\n```")
            merged.append({"source": str(source), "status": "merged_into_material_digest"})
            continue
        if is_text_source(source) and source.stat().st_size > MAX_MERGED_TEXT_BYTES:
            deferred.append({
                "source": str(source),
                "status": "deferred",
                "reason": "text source is too large; extract the relevant portions into the material digest",
            })
            continue
        if binary_budget > 0:
            material_dir.mkdir(parents=True, exist_ok=True)
            target = unique_target_path(material_dir, source.name)
            shutil.copy2(source, target)
            copied.append({"source": str(source), "status": "copied", "copied_to": str(target)})
            binary_budget -= 1
        else:
            deferred.append({
                "source": str(source),
                "status": "deferred",
                "reason": "document limit reached; extract or merge this source before web upload",
            })
    return {
        "copied": copied,
        "merged": merged,
        "deferred": deferred,
        "merged_text": "\n\n".join(merged_blocks),
    }


def build_prompt(
    *,
    task_title: str,
    route: str,
    task_kind: str,
    model_target: str,
    has_formulas: bool,
    material_text: str,
    rule_texts: list[tuple[str, str]],
    notes: str,
) -> str:
    formula_line = (
        "本任务包含公式或公式化表达。最终交付必须是一份 DOCX 文档，并且公式应为可编辑公式，不要使用公式截图。"
        if has_formulas
        else "最终交付必须是一份 DOCX 文档。若你发现材料中存在公式，请在 DOCX 中按公式规则处理。"
    )
    rules_block = "\n\n".join(f"## 规则文件：{name}\n\n{text}" for name, text in rule_texts)
    return f"""# 发送给 ChatGPT Pro 的任务

请使用 {model_target} 处理以下中国专利任务。你需要先阅读案件材料，再严格遵守后附规则。

## 任务信息

- 任务名称：{task_title}
- Codex 路由：{route}
- 任务类型：{task_kind}
- 公式处理：{formula_line}
- 输出形式：请生成一份 DOCX 文档作为最终交付，不要仅在对话中输出普通文本或 Markdown。

## 你的工作方式

1. 只依据本交接包中的材料和明确事实进行分析。
2. 不要补造技术特征和实验数据，也不要虚构对比文件内容、审查员观点或法律事实。
3. 如果材料不足，请明确写出“需要确认”，并说明影响范围。
4. 请在 DOCX 中同时保留分析层和可直接使用的成文层。
5. 中文表达要自然，避免在同一句中堆叠过多顿号。

## 补充要求

{notes or "无。"}

## 案件材料

{material_text}

## 处理规则

{rules_block}
"""


def build_web_starter_prompt(
    *,
    task_title: str,
    route: str,
    task_kind: str,
    model_target: str,
    has_formulas: bool,
) -> str:
    formula_instruction = (
        "本任务包含公式。请在 DOCX 中使用可编辑公式，不要使用公式截图，也不要把公式仅作为普通文本处理。"
        if has_formulas
        else "若你在材料中发现公式，请在 DOCX 中按交接包里的公式规则处理。"
    )
    return f"""请使用 {model_target} 处理我提供的中国专利交接包。

任务名称：{task_title}
Codex 路由：{route}
任务类型：{task_kind}

请先阅读我粘贴或上传的《发送全集_可直接粘贴.md》，并以其中的案件材料和规则文件为准。请严格遵守交接包里的权利要求规则、说明书规则以及审查意见答复规则，公式内容按公式处理规则执行。不要补造技术事实和实验数据，也不要虚构对比文件内容、审查员观点或法律事实；材料不足时，请明确标注“需要确认”。

{formula_instruction}

最终输出形式限定为生成一份 DOCX 文档。请不要仅输出 Markdown 或普通聊天正文。DOCX 中应包含结构化结果，保留分析层和可直接使用的成文层，并列出支持依据、风险以及需要 Codex 后续核查的问题。"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a ChatGPT Pro patent handoff bundle.")
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--task-title", required=True)
    parser.add_argument("--route", required=True, choices=["drafting", "review", "response", "research", "support"])
    parser.add_argument(
        "--task-kind",
        required=True,
        choices=[
            "claims",
            "background",
            "invention-content",
            "embodiments",
            "specification",
            "oa-response",
            "invalidity",
            "review",
            "prior-art",
            "generic",
        ],
    )
    parser.add_argument("--material-md")
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--has-formulas", action="store_true")
    parser.add_argument("--max-documents", type=int, default=DEFAULT_MAX_DOCUMENTS)
    parser.add_argument("--model-target", default="ChatGPT 5.5 Pro（网页版）")
    parser.add_argument("--notes", default="")
    parser.add_argument("--out-dir")
    args = parser.parse_args()

    case_dir = Path(args.case_dir).expanduser().resolve()
    if args.max_documents < BASE_DOCUMENT_COUNT:
        parser.error(f"--max-documents must be at least {BASE_DOCUMENT_COUNT}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else case_dir / "输出" / "过程" / "ChatGPT交接" / f"{timestamp}_{safe_slug(args.task_title)}"
    material_dir = bundle_dir / "材料"
    returned_dir = bundle_dir / "回收"

    bundle_dir.mkdir(parents=True, exist_ok=True)
    returned_dir.mkdir(parents=True, exist_ok=True)

    material_text = "【待 Codex 填写案件材料汇编。发送前必须补全。】"
    material_path = None
    if args.material_md:
        material_path = Path(args.material_md).expanduser().resolve()
        if material_path.exists():
            material_text = read_text(material_path)

    binary_budget = args.max_documents - BASE_DOCUMENT_COUNT
    source_result = process_sources([Path(p) for p in args.source], material_dir, binary_budget)
    if source_result["merged_text"]:
        material_text = f"{material_text}\n\n## 已合并的源文件文本\n\n{source_result['merged_text']}"

    rule_names = selected_rules(args.task_kind, args.has_formulas)
    rule_texts = []
    for name in rule_names:
        source = RULE_DIR / name
        rule_texts.append((name, read_text(source)))
    merged_rules_text = "\n\n".join(f"# {name}\n\n{text}" for name, text in rule_texts)

    prompt = build_prompt(
        task_title=args.task_title,
        route=args.route,
        task_kind=args.task_kind,
        model_target=args.model_target,
        has_formulas=args.has_formulas,
        material_text=material_text,
        rule_texts=rule_texts,
        notes=args.notes,
    )
    web_starter_prompt = build_web_starter_prompt(
        task_title=args.task_title,
        route=args.route,
        task_kind=args.task_kind,
        model_target=args.model_target,
        has_formulas=args.has_formulas,
    )

    write_text(bundle_dir / "00_交接包说明.md", f"""# 交接包说明

本文件夹用于把 Codex 本地专利工作流中的一个高质量文本任务交给 ChatGPT 网页版 Pro 模型处理。

- 任务名称：{args.task_title}
- Codex 路由：{args.route}
- 任务类型：{args.task_kind}
- 模型目标：{args.model_target}
- 是否包含公式：{"是" if args.has_formulas else "否"}

发送前请检查 `04_发送前确认.md`。ChatGPT 返回内容后，请放入 `回收/` 文件夹，再由 Codex 整合。
""")
    write_text(bundle_dir / "01_发送给ChatGPT-Pro的提示词.md", prompt)
    write_text(bundle_dir / "02_案件材料汇编.md", material_text)
    copied_sources = source_result["copied"]
    merged_sources = source_result["merged"]
    deferred_sources = source_result["deferred"]
    document_count = BASE_DOCUMENT_COUNT + len(copied_sources)
    ready_for_web_upload = document_count <= args.max_documents and not deferred_sources
    write_text(bundle_dir / "03_材料清单.md", "\n".join([
        "# 材料清单",
        "",
        f"- 网页端文档上限：{args.max_documents}",
        f"- 本交接包文档数：{document_count}",
        f"- 是否可直接发送：{'是' if ready_for_web_upload else '否，存在未合并或未复制的源文件'}",
        f"- 材料汇编来源：{str(material_path) if material_path else '未提供'}",
        "",
        "## 已合并进材料汇编的源文件",
        "",
        *[f"- {item['status']}: {item['source']}" for item in merged_sources],
        "",
        "## 保留为单独附件的源文件",
        "",
        *[f"- {item['status']}: {item['source']} -> {item['copied_to']}" for item in copied_sources],
        "",
        "## 未直接放入网页版发送包的源文件",
        "",
        *[f"- {item['status']}: {item['source']}；原因：{item['reason']}" for item in deferred_sources],
        "",
    ]))
    write_text(bundle_dir / "04_发送前确认.md", f"""# 发送前确认

请确认是否允许把本交接包中的材料发送到 ChatGPT 网页版 Pro 模型。

## 将发送的内容

- `发送全集_可直接粘贴.md`
- `02_案件材料汇编.md`
- `规则_合并版.md`
- `06_网页端启动提示词_可直接粘贴.md`
- `材料/` 中列明的源文件，前提是需要上传附件

本交接包已按 ChatGPT 网页端一次 20 个文档的限制整理。当前文档数：{document_count}。
{"注意：仍有源文件未直接放入本包。请先由 Codex 提取或合并这些源文件，再发送给 ChatGPT。" if not ready_for_web_upload else ""}

## 目的地

ChatGPT 网页版 Pro 模型。

## 公式处理

{"要求 ChatGPT 生成含可编辑公式的 DOCX，不要使用公式截图。" if args.has_formulas else "未标记为公式密集任务；若 ChatGPT 发现公式，仍应在 DOCX 中按公式规则处理。"}

只有在用户明确确认本包可以发送后，Codex 才能协助打开浏览器并填入提示词。
""")
    write_text(bundle_dir / "05_回收与整合说明.md", """# 回收与整合说明

请把 ChatGPT Pro 的返回内容保存到 `回收/` 文件夹。

推荐回收文件名：

- `ChatGPT-Pro返回_权利要求.docx`
- `ChatGPT-Pro返回_说明书.docx`
- `ChatGPT-Pro返回_审查意见答复.docx`
- `ChatGPT-Pro返回_公式版本.docx`

Codex 回收后应检查术语一致性和支持关系，并复核权利要求引用、附图标记以及公式显示。需要生成 DOCX 时，应把公式转换为可编辑公式，并进行渲染检查。
""")
    write_text(bundle_dir / "06_网页端启动提示词_可直接粘贴.md", web_starter_prompt)
    write_text(bundle_dir / "发送全集_可直接粘贴.md", prompt)
    write_text(bundle_dir / "规则_合并版.md", merged_rules_text)

    manifest = {
        "schema": "patent-chatgpt-pro-handoff/v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "case_dir": str(case_dir),
        "bundle_dir": str(bundle_dir),
        "task_title": args.task_title,
        "route": args.route,
        "task_kind": args.task_kind,
        "has_formulas": args.has_formulas,
        "model_target": args.model_target,
        "material_md": str(material_path) if material_path else None,
        "document_limit": args.max_documents,
        "document_count": document_count,
        "ready_for_web_upload": ready_for_web_upload,
        "sources": {
            "copied": copied_sources,
            "merged_into_material_digest": merged_sources,
            "deferred": deferred_sources,
        },
        "rules": rule_names,
        "merged_rules_file": str(bundle_dir / "规则_合并版.md"),
        "send_file": str(bundle_dir / "发送全集_可直接粘贴.md"),
        "web_starter_prompt_file": str(bundle_dir / "06_网页端启动提示词_可直接粘贴.md"),
        "web_starter_prompt": web_starter_prompt,
        "return_dir": str(returned_dir),
    }
    write_text(bundle_dir / "交接包_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print(json.dumps({
        "bundle_dir": str(bundle_dir),
        "document_limit": args.max_documents,
        "document_count": document_count,
        "ready_for_web_upload": ready_for_web_upload,
        "send_file": manifest["send_file"],
        "merged_rules_file": manifest["merged_rules_file"],
        "web_starter_prompt_file": manifest["web_starter_prompt_file"],
        "web_starter_prompt": web_starter_prompt,
        "deferred_sources": deferred_sources,
        "return_dir": str(returned_dir),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
