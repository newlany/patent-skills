#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic renderer for Chinese patent method flowcharts.

The renderer intentionally handles only the narrow patent-flowchart case:
ordered rectangular steps arranged top-to-bottom with vertical arrows. Keeping
the geometry simple and explicit prevents the common "floating arrow" and text
overflow failures seen in general-purpose diagram generation.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


SVG_FONT_FAMILY = "Songti SC, SimSun, STSong, serif"

COMMON_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Songti.ttc",
    "/Library/Fonts/SimSun.ttf",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/simsun.ttf",
]


@dataclass
class Style:
    canvas_width: int = 1600
    box_width: int = 1120
    margin_y: int = 120
    padding_x: int = 54
    padding_y: int = 30
    gap: int = 86
    arrow_gap: int = 14
    stroke_width: int = 3
    font_size: int = 34
    line_spacing: int = 12
    min_box_height: int = 120
    arrow_head: int = 18
    png_scale: int = 2

    @property
    def line_height(self) -> int:
        return self.font_size + self.line_spacing

    @property
    def box_x(self) -> int:
        return round((self.canvas_width - self.box_width) / 2)

    @property
    def text_width(self) -> int:
        return self.box_width - self.padding_x * 2


@dataclass
class BoxLayout:
    step: str
    lines: list[str]
    x: int
    y: int
    width: int
    height: int

    @property
    def cx(self) -> int:
        return self.x + round(self.width / 2)

    @property
    def bottom(self) -> int:
        return self.y + self.height


@dataclass
class Layout:
    width: int
    height: int
    boxes: list[BoxLayout]
    style: Style
    font_path: str


class FontLoadError(RuntimeError):
    pass


def load_font(font_arg: str | None, size: int) -> tuple[ImageFont.FreeTypeFont, str]:
    candidates: list[str] = []
    if font_arg:
        candidates.append(font_arg)
    candidates.extend(COMMON_FONT_PATHS)

    tried: list[str] = []
    for candidate in candidates:
        path = Path(candidate).expanduser()
        tried.append(str(path))
        try:
            if path.exists():
                return ImageFont.truetype(str(path), size=size), str(path)
            return ImageFont.truetype(candidate, size=size), candidate
        except OSError:
            continue

    raise FontLoadError(
        "Could not load a Chinese-capable font. Tried:\n  " + "\n  ".join(tried)
    )


def normalize_steps(raw: str) -> list[str]:
    lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
    steps = [line for line in lines if line]
    if not steps:
        raise ValueError("No steps were provided.")
    return steps


def read_steps(args: argparse.Namespace) -> list[str]:
    if args.steps:
        return normalize_steps(args.steps)
    if args.steps_file:
        return normalize_steps(Path(args.steps_file).expanduser().read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        return normalize_steps(sys.stdin.read())
    raise ValueError("Provide --steps, --steps-file, or pipe steps through stdin.")


def text_width(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, text: str) -> int:
    if not text:
        return 0
    left, _, right, _ = draw.textbbox((0, 0), text, font=font)
    return right - left


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if buf:
            tokens.append("".join(buf))
            buf.clear()

    for ch in text:
        if ch.isspace():
            flush()
            if not tokens or tokens[-1] != " ":
                tokens.append(" ")
        elif ch.isascii() and re.match(r"[A-Za-z0-9_./:%+\-#]+", ch):
            buf.append(ch)
        else:
            flush()
            tokens.append(ch)
    flush()
    return tokens


def break_long_token(
    token: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    parts: list[str] = []
    current = ""
    for ch in token:
        candidate = current + ch
        if current and text_width(draw, font, candidate) > max_width:
            parts.append(current)
            current = ch
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts


def wrap_text(
    text: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    tokens = tokenize(re.sub(r"\s+", " ", text.strip()))
    lines: list[str] = []
    current = ""
    closing_punctuation = set("，。；：、？！）】》”’』」,.!?;:)]}")

    for token in tokens:
        candidate = current + token
        if not current:
            if text_width(draw, font, token) <= max_width:
                current = token.lstrip()
            else:
                broken = break_long_token(token, draw, font, max_width)
                lines.extend(broken[:-1])
                current = broken[-1] if broken else ""
            continue

        if text_width(draw, font, candidate) <= max_width:
            current = candidate
            continue

        if token in closing_punctuation:
            trimmed = current.rstrip()
            if len(trimmed) > 1:
                previous_line = trimmed[:-1]
                next_line = trimmed[-1] + token
                if (
                    text_width(draw, font, previous_line) <= max_width
                    and text_width(draw, font, next_line) <= max_width
                ):
                    lines.append(previous_line)
                    current = next_line
                    continue
            lines.append(trimmed)
            current = token
        else:
            lines.append(current.rstrip())
            stripped = token.lstrip()
            if text_width(draw, font, stripped) <= max_width:
                current = stripped
            else:
                broken = break_long_token(stripped, draw, font, max_width)
                lines.extend(broken[:-1])
                current = broken[-1] if broken else ""

    if current.strip():
        lines.append(current.strip())
    return lines or [text]


def build_layout(steps: list[str], style: Style, font: ImageFont.FreeTypeFont, font_path: str) -> Layout:
    meter = Image.new("RGB", (10, 10), "white")
    draw = ImageDraw.Draw(meter)
    boxes: list[BoxLayout] = []
    y = style.margin_y

    for step in steps:
        wrapped = wrap_text(step, draw, font, style.text_width)
        text_block_height = len(wrapped) * style.line_height - style.line_spacing
        height = max(style.min_box_height, text_block_height + style.padding_y * 2)
        boxes.append(BoxLayout(step, wrapped, style.box_x, y, style.box_width, height))
        y += height + style.gap

    height = boxes[-1].bottom + style.margin_y if boxes else style.margin_y * 2
    return Layout(style.canvas_width, height, boxes, style, font_path)


def svg_text_block(box: BoxLayout, style: Style) -> str:
    start_y = box.y + box.height / 2 - (len(box.lines) - 1) * style.line_height / 2
    tspans = []
    for idx, line in enumerate(box.lines):
        y = start_y + idx * style.line_height
        tspans.append(
            f'<tspan x="{box.cx}" y="{y:.1f}">{html.escape(line)}</tspan>'
        )
    return (
        f'<text font-family="{SVG_FONT_FAMILY}" font-size="{style.font_size}" '
        f'fill="#000" text-anchor="middle" dominant-baseline="middle">'
        + "".join(tspans)
        + "</text>"
    )


def render_svg(layout: Layout) -> str:
    style = layout.style
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{layout.width}" height="{layout.height}" viewBox="0 0 {layout.width} {layout.height}">',
        "<defs>",
        f'<marker id="arrow" markerWidth="{style.arrow_head}" markerHeight="{style.arrow_head}" refX="{style.arrow_head - 1}" refY="{style.arrow_head / 2}" orient="auto" markerUnits="userSpaceOnUse">',
        f'<path d="M0,0 L{style.arrow_head},{style.arrow_head / 2} L0,{style.arrow_head} Z" fill="#000"/>',
        "</marker>",
        "</defs>",
        f'<rect x="0" y="0" width="{layout.width}" height="{layout.height}" fill="#fff"/>',
    ]

    for idx, box in enumerate(layout.boxes):
        parts.append(
            f'<rect x="{box.x}" y="{box.y}" width="{box.width}" height="{box.height}" '
            f'fill="#fff" stroke="#000" stroke-width="{style.stroke_width}"/>'
        )
        parts.append(svg_text_block(box, style))
        if idx < len(layout.boxes) - 1:
            nxt = layout.boxes[idx + 1]
            y1 = box.bottom + style.arrow_gap
            y2 = nxt.y - style.arrow_gap
            parts.append(
                f'<line x1="{box.cx}" y1="{y1}" x2="{nxt.cx}" y2="{y2}" '
                f'stroke="#000" stroke-width="{style.stroke_width}" '
                f'stroke-linecap="butt" marker-end="url(#arrow)"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def scaled_style(style: Style, scale: int) -> Style:
    data = asdict(style)
    for key in data:
        if key != "png_scale":
            data[key] = int(data[key] * scale)
    data["png_scale"] = scale
    return Style(**data)


def render_png(layout: Layout, output: Path, font_arg: str | None) -> None:
    scale = max(1, layout.style.png_scale)
    png_style = scaled_style(layout.style, scale)
    font, _ = load_font(font_arg or layout.font_path, png_style.font_size)
    scaled_layout = build_layout([box.step for box in layout.boxes], png_style, font, layout.font_path)

    image = Image.new("RGB", (scaled_layout.width, scaled_layout.height), "white")
    draw = ImageDraw.Draw(image)
    style = scaled_layout.style

    for idx, box in enumerate(scaled_layout.boxes):
        draw.rectangle(
            [box.x, box.y, box.x + box.width, box.y + box.height],
            outline="black",
            width=style.stroke_width,
            fill="white",
        )
        start_y = box.y + box.height / 2 - (len(box.lines) - 1) * style.line_height / 2
        for line_idx, line in enumerate(box.lines):
            draw.text(
                (box.cx, start_y + line_idx * style.line_height),
                line,
                fill="black",
                font=font,
                anchor="mm",
            )

        if idx < len(scaled_layout.boxes) - 1:
            nxt = scaled_layout.boxes[idx + 1]
            x = box.cx
            y1 = box.bottom + style.arrow_gap
            y2 = nxt.y - style.arrow_gap - style.arrow_head
            draw.line([x, y1, x, y2], fill="black", width=style.stroke_width)
            head_y = nxt.y - style.arrow_gap
            half = round(style.arrow_head * 0.46)
            draw.polygon(
                [
                    (x, head_y),
                    (x - half, head_y - style.arrow_head),
                    (x + half, head_y - style.arrow_head),
                ],
                fill="black",
            )

    if scale > 1:
        image = image.resize((layout.width, layout.height), Image.Resampling.LANCZOS)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def validate_layout(layout: Layout, font: ImageFont.FreeTypeFont) -> list[str]:
    meter = Image.new("RGB", (10, 10), "white")
    draw = ImageDraw.Draw(meter)
    warnings: list[str] = []

    for idx, box in enumerate(layout.boxes, 1):
        for line in box.lines:
            width = text_width(draw, font, line)
            if width > layout.style.text_width:
                warnings.append(
                    f"Step {idx} line exceeds text width: {width}px > {layout.style.text_width}px"
                )
        if idx < len(layout.boxes):
            nxt = layout.boxes[idx]
            if nxt.y - box.bottom <= layout.style.arrow_head + layout.style.arrow_gap * 2:
                warnings.append(f"Step {idx} arrow gap is too small.")
    return warnings


def write_layout_json(layout: Layout, output: Path) -> None:
    data = {
        "width": layout.width,
        "height": layout.height,
        "font_path": layout.font_path,
        "style": asdict(layout.style),
        "boxes": [
            {
                "step": box.step,
                "lines": box.lines,
                "x": box.x,
                "y": box.y,
                "width": box.width,
                "height": box.height,
            }
            for box in layout.boxes
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def default_png_path(svg_path: Path) -> Path:
    return svg_path.with_suffix(".png")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a filing-style Chinese patent method flowchart as deterministic SVG/PNG.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--steps", help="Newline-separated method steps, e.g. $'S1、...\\nS2、...'")
    parser.add_argument("--steps-file", help="UTF-8 text file containing one method step per line.")
    parser.add_argument("--out", required=True, help="Output SVG path. Use --png to also write PNG.")
    parser.add_argument("--png", nargs="?", const=True, help="Optional PNG path. If omitted after flag, use --out with .png.")
    parser.add_argument("--layout-json", help="Optional JSON layout dump for debugging or workflow reuse.")
    parser.add_argument("--font", help="Chinese-capable TTF/TTC font path or installed font name.")
    parser.add_argument("--canvas-width", type=int, default=Style.canvas_width)
    parser.add_argument("--box-width", type=int, default=Style.box_width)
    parser.add_argument("--font-size", type=int, default=Style.font_size)
    parser.add_argument("--margin-y", type=int, default=Style.margin_y)
    parser.add_argument("--padding-x", type=int, default=Style.padding_x)
    parser.add_argument("--padding-y", type=int, default=Style.padding_y)
    parser.add_argument("--gap", type=int, default=Style.gap)
    parser.add_argument("--stroke-width", type=int, default=Style.stroke_width)
    parser.add_argument("--png-scale", type=int, default=Style.png_scale)
    parser.add_argument("--quiet", action="store_true", help="Suppress summary output.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        steps = read_steps(args)
        style = Style(
            canvas_width=args.canvas_width,
            box_width=args.box_width,
            margin_y=args.margin_y,
            padding_x=args.padding_x,
            padding_y=args.padding_y,
            gap=args.gap,
            stroke_width=args.stroke_width,
            font_size=args.font_size,
            png_scale=args.png_scale,
        )
        font, font_path = load_font(args.font, style.font_size)
        layout = build_layout(steps, style, font, font_path)
        warnings = validate_layout(layout, font)

        out = Path(args.out).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_svg(layout), encoding="utf-8")

        png_path: Path | None = None
        if args.png:
            png_path = default_png_path(out) if args.png is True else Path(args.png).expanduser()
            render_png(layout, png_path, args.font)

        if args.layout_json:
            write_layout_json(layout, Path(args.layout_json).expanduser())

        if not args.quiet:
            print(f"Wrote SVG: {out}")
            if png_path:
                print(f"Wrote PNG: {png_path}")
            if args.layout_json:
                print(f"Wrote layout JSON: {Path(args.layout_json).expanduser()}")
            print(f"Steps: {len(steps)}")
            print(f"Canvas: {layout.width} x {layout.height}")
            print(f"Font: {font_path}")
            if warnings:
                print("Warnings:", file=sys.stderr)
                for warning in warnings:
                    print(f"  - {warning}", file=sys.stderr)
        return 0 if not warnings else 2
    except Exception as exc:  # noqa: BLE001 - CLI should return a readable error.
        print(f"patent_flowchart.py: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
