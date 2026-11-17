#!/usr/bin/env python3
"""Render a practical Markdown manual to a portable, hyperlink-free PDF.

See references/renderer.md for the optional brand profile and callout schemas.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import html
import json
import math
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

PAGE_W, PAGE_H = letter
MARGIN = 45
CONTENT_W = PAGE_W - 2 * MARGIN
FRAME_Y, FRAME_H = 49, PAGE_H - 105
DATE_RE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b")
NEUTRAL = {
    "charcoal": "#18242C", "accent": "#BED4DC", "ink": "#25303B",
    "muted": "#5A6872", "light": "#F3F5F6", "line": "#D5DDE1",
}


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


@dataclass
class Theme:
    organization: str
    palette: dict
    fonts: dict
    logo: Path | None = None


def load_theme(profile: Path | None) -> Theme:
    data = read_json(profile) if profile else {}
    palette = {}
    for key, default in NEUTRAL.items():
        value = data.get("colors", {}).get(key, default)
        if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError(f"colors.{key} must be a six-digit #RRGGBB value")
        palette[key] = colors.HexColor(value)
    fonts = {"heading": "Helvetica-Bold", "body": "Helvetica", "bold": "Helvetica-Bold", "mono": "Courier"}
    for key in fonts:
        filename = data.get("fonts", {}).get(key)
        if filename:
            path = (profile.parent / filename).resolve()
            if not path.is_file():
                raise FileNotFoundError(f"Missing fonts.{key}: {path}")
            fonts[key] = f"Manual{key.title()}"
            pdfmetrics.registerFont(TTFont(fonts[key], str(path)))
    pdfmetrics.registerFontFamily(fonts["body"], normal=fonts["body"], bold=fonts["bold"],
                                  italic=fonts["body"], boldItalic=fonts["bold"])
    for key in ("heading", "mono"):
        pdfmetrics.registerFontFamily(fonts[key], normal=fonts[key], bold=fonts[key],
                                      italic=fonts[key], boldItalic=fonts[key])
    logo = (profile.parent / data["logo"]).resolve() if data.get("logo") else None
    if logo and not logo.is_file():
        raise FileNotFoundError(f"Missing logo: {logo}")
    return Theme(str(data.get("organization", "")), palette, fonts, logo)


def normalize(value: str) -> str:
    return value.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")


def plain(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    return re.sub(r"[`*_]", "", normalize(value))


def inline(value: str, theme: Theme) -> str:
    value, tokens = normalize(value), {}
    def token(markup):
        key = f"ZZMANUALTOKEN{len(tokens)}ZZ"
        tokens[key] = markup
        return key
    value = re.sub(r"<br\s*/?>", lambda _: token("<br/>"), value, flags=re.I)
    value = re.sub(r"`([^`]+)`", lambda m: token(
        f'<font name="{theme.fonts["mono"]}" size="9.3">{html.escape(m[1])}</font>'), value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", lambda m: token(html.escape(m[1])), value)
    value = html.escape(value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"__([^_]+)__", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    for key, markup in tokens.items():
        value = value.replace(key, markup)
    return value


def make_styles(theme: Theme) -> dict:
    p, f = theme.palette, theme.fonts
    body = ParagraphStyle("Body", fontName=f["body"], fontSize=10.5, leading=14.2,
                          textColor=p["ink"], spaceAfter=5, allowWidows=0, allowOrphans=0)
    result = {"body": body}
    for name, size, leading in (("title", 28, 32), ("h1", 24, 28), ("h2", 20, 23), ("h3", 13, 16), ("h4", 10.5, 14)):
        result[name] = ParagraphStyle(name, parent=body, fontName=f["heading"] if size >= 20 else f["bold"],
            fontSize=size, leading=leading, spaceBefore=0 if name == "title" else 8,
            spaceAfter=5, keepWithNext=True)
    result["bullet"] = ParagraphStyle("Bullet", parent=body, leftIndent=18, bulletIndent=1,
                                      bulletFontName=f["body"], bulletFontSize=10.5, spaceAfter=4)
    result["cell"] = ParagraphStyle("Cell", parent=body, fontSize=10, leading=13, spaceAfter=0)
    result["header"] = ParagraphStyle("Header", parent=result["cell"], fontName=f["bold"], textColor=colors.white)
    result["caption"] = ParagraphStyle("Caption", parent=body, fontSize=9.3, leading=12,
                                       textColor=p["muted"], alignment=1, spaceAfter=7)
    result["quote"] = ParagraphStyle("Quote", parent=body, backColor=p["light"],
        borderColor=p["accent"], borderWidth=.6, borderPadding=7, leftIndent=8,
        rightIndent=8, spaceBefore=5, spaceAfter=9)
    return result


def coordinate(value, label: str) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{label} must be a finite number from 0 through 1")
    return float(value)


def point(value, label: str) -> tuple:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be [x, y]")
    return tuple(coordinate(part, label) for part in value)


def load_callouts(path: Path | None) -> dict:
    if not path:
        return {}
    entries = read_json(path).get("images", [])
    if not isinstance(entries, list):
        raise ValueError("callouts.images must be an array")
    result = {}
    for entry in entries:
        image = (path.parent / entry["image"]).resolve()
        if image in result:
            raise ValueError(f"Duplicate image callout entry: {image}")
        width = entry.get("width_pt", CONTENT_W)
        if type(width) not in (int, float) or not 40 <= width <= CONTENT_W:
            raise ValueError(f"width_pt must be from 40 through {CONTENT_W}")
        annotations, used = [], set()
        for item in entry.get("callouts", []):
            number, side = item["number"], item["side"]
            if type(number) is not int or not 1 <= number <= 99 or number in used:
                raise ValueError("Callout numbers must be unique integers from 1 through 99 per image")
            if side not in ("left", "right"):
                raise ValueError("Callout side must be left or right")
            target = point(item["target"], "target")
            annotations.append({"number": number, "side": side, "target": target,
                "marker_y": coordinate(item.get("marker_y", target[1]), "marker_y"),
                "route": [point(vertex, "route vertex") for vertex in item.get("route", [])]})
            used.add(number)
        result[image] = {"width_pt": float(width), "callouts": annotations}
    return result


class ManualImage(Flowable):
    def __init__(self, filename: Path, theme: Theme, spec: dict | None = None):
        super().__init__()
        self.filename, self.theme, self.spec = filename, theme, spec or {}
        self.native_w, self.native_h = ImageReader(str(filename)).getSize()
        self.hAlign = "CENTER"

    def wrap(self, available_width, available_height):
        self.rail = 16 if self.spec.get("callouts") else 0
        self.pad = 8 if self.rail else 0
        limit = min(available_width, CONTENT_W)
        self.image_w = min(self.spec.get("width_pt", limit), limit - self.rail * 2)
        self.image_h = self.image_w * self.native_h / self.native_w
        if self.image_h > FRAME_H - 40 - self.pad * 2:
            self.image_w *= (FRAME_H - 40 - self.pad * 2) / self.image_h
            self.image_h = FRAME_H - 40 - self.pad * 2
        self.width, self.height = self.image_w + self.rail * 2, self.image_h + self.pad * 2
        return self.width, self.height

    def draw(self):
        c, p = self.canv, self.theme.palette
        c.saveState()
        c.drawImage(str(self.filename), self.rail, self.pad, width=self.image_w, height=self.image_h, mask="auto")
        def xy(vertex):
            return self.rail + vertex[0] * self.image_w, self.pad + self.image_h * (1 - vertex[1])
        for item in self.spec.get("callouts", []):
            left = item["side"] == "left"
            x, y = (7 if left else self.width - 7), self.pad + self.image_h * (1 - item["marker_y"])
            line = c.beginPath()
            line.moveTo(x + 7.2 if left else x - 7.2, y)
            for vertex in item["route"]:
                line.lineTo(*xy(vertex))
            end = xy(item["target"])
            line.lineTo(*end)
            c.setStrokeColor(p["charcoal"])
            c.setLineWidth(.65)
            c.drawPath(line)
            c.setFillColor(p["charcoal"])
            c.circle(*end, 1.2, fill=1, stroke=0)
            c.setFillColor(p["accent"])
            c.circle(x, y, 7.2, fill=1, stroke=1)
            c.setFillColor(p["charcoal"])
            c.setFont(self.theme.fonts["bold"], 9.5 if item["number"] < 10 else 8.3)
            c.drawCentredString(x, y - 3.2, str(item["number"]))
        c.restoreState()


class WrappedCode(Flowable):
    def __init__(self, lines: list, theme: Theme):
        super().__init__()
        self.raw, self.theme = lines, theme
        self.spaceBefore, self.spaceAfter = 4, 7

    def wrap(self, available_width, available_height):
        self.width, self.lines = available_width, []
        font = self.theme.fonts["mono"]
        for raw in self.raw:
            line = normalize(raw.expandtabs(4))
            while pdfmetrics.stringWidth(line, font, 9.3) > available_width - 20:
                low, high = 1, len(line)
                while low < high:
                    middle = (low + high + 1) // 2
                    if pdfmetrics.stringWidth(line[:middle], font, 9.3) <= available_width - 20:
                        low = middle
                    else:
                        high = middle - 1
                at = line.rfind(" ", 0, low + 1)
                at = at if at > 8 else low
                self.lines.append(line[:at])
                line = line[at:].lstrip()
            self.lines.append(line)
        self.height = 18 + len(self.lines) * 13
        return self.width, self.height

    def split(self, available_width, available_height):
        self.wrap(available_width, available_height)
        count = int((available_height - 18) // 13)
        if count < 1 or count >= len(self.lines):
            return []
        return [WrappedCode(self.lines[:count], self.theme), WrappedCode(self.lines[count:], self.theme)]

    def draw(self):
        c, p = self.canv, self.theme.palette
        c.saveState()
        c.setFillColor(p["light"])
        c.setStrokeColor(p["line"])
        c.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=1)
        c.setFillColor(p["ink"])
        c.setFont(self.theme.fonts["mono"], 9.3)
        for index, line in enumerate(self.lines):
            c.drawString(10, self.height - 17 - 13 * index, line)
        c.restoreState()


def table_cells(line: str) -> list:
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def make_table(rows: list, theme: Theme, styles: dict) -> Table:
    count = len(rows[0])
    if any(len(row) != count for row in rows):
        raise ValueError("Table rows must have the same number of cells as the header")
    scores = []
    for column in range(count):
        lengths = [len(plain(row[column])) for row in rows]
        scores.append(max(10, min(60, sum(min(n, 100) for n in lengths) / len(lengths))))
    widths = [CONTENT_W * score / sum(scores) for score in scores]
    data = [[Paragraph(inline(cell, theme), styles["header" if index == 0 else "cell"])
             for cell in row] for index, row in enumerate(rows)]
    table = Table(data, colWidths=widths, repeatRows=1, splitInRow=1, hAlign="LEFT")
    p = theme.palette
    commands = [("BACKGROUND", (0, 0), (-1, 0), p["charcoal"]), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.3),
        ("LINEBELOW", (0, 0), (-1, 0), .9, p["accent"]), ("LINEBELOW", (0, 1), (-1, -1), .35, p["line"])]
    commands.extend(("BACKGROUND", (0, row), (-1, row), p["light"]) for row in range(1, len(rows), 2))
    table.setStyle(TableStyle(commands))
    return table


def block_start(line: str) -> bool:
    return bool(line == "---" or line.startswith(("#", "|", "```", ">", "![")) or
                re.match(r"^([-*+]|\d+[.)])\s+", line))


def parse_markdown(source: Path, theme: Theme, callouts: dict, title_override: str | None = None) -> list:
    lines, styles, story = source.read_text(encoding="utf-8-sig").splitlines(), make_styles(theme), []
    index, first_title = 0, True
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line == "---":
            while story and isinstance(story[-1], Spacer):
                story.pop()
            if story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", line)
        if heading:
            level, value = len(heading[1]), heading[2]
            is_title = first_title and level == 1
            if is_title and title_override:
                value = title_override
            story.append(Paragraph(inline(value, theme), styles["title" if is_title else f"h{min(level, 4)}"]))
            first_title = False
            index += 1
            continue
        image = re.match(r"^!\[([^]]*)\]\((.+)\)$", line)
        if image:
            if re.match(r"^[a-z]+://", image[2], re.I):
                raise ValueError("Images must be local files; remote URLs are not fetched")
            filename = (source.parent / image[2]).resolve()
            if not filename.is_file():
                raise FileNotFoundError(f"Missing image: {filename}")
            parts = [ManualImage(filename, theme, callouts.get(filename))]
            if image[1]:
                parts.extend([Spacer(1, 3), Paragraph(inline(image[1], theme), styles["caption"])])
            story.append(KeepTogether(parts))
            index += 1
            continue
        if line.startswith("```"):
            code, index = [], index + 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Unclosed fenced code block")
            story.append(WrappedCode(code, theme))
            index += 1
            continue
        if line.startswith("|") and index + 1 < len(lines):
            separator = table_cells(lines[index + 1])
            if separator and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
                rows, index = [table_cells(line)], index + 2
                while index < len(lines) and lines[index].strip().startswith("|"):
                    rows.append(table_cells(lines[index]))
                    index += 1
                story.extend([make_table(rows, theme, styles), Spacer(1, 5)])
                continue
        bullet = re.match(r"^([-*+]|\d+[.)])\s+(.+)$", line)
        if bullet:
            marker, value, index = bullet[1], bullet[2], index + 1
            while index < len(lines) and lines[index].strip() and not block_start(lines[index].strip()):
                value += " " + lines[index].strip()
                index += 1
            label = "\u2022" if marker in "-*+" else re.sub(r"[.)]$", ".", marker)
            story.append(Paragraph(inline(value, theme), styles["bullet"], bulletText=label))
            continue
        if line.startswith(">"):
            quote = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(re.sub(r"^>\s?", "", lines[index].strip()))
                index += 1
            story.append(Paragraph(inline(" ".join(quote), theme), styles["quote"]))
            continue
        paragraph, index = [line], index + 1
        while index < len(lines) and lines[index].strip() and not block_start(lines[index].strip()):
            paragraph.append(lines[index].strip())
            index += 1
        story.append(Paragraph(inline(" ".join(paragraph), theme), styles["body"]))
    while story and isinstance(story[-1], (Spacer, PageBreak)):
        story.pop()
    if not story:
        raise ValueError("Markdown source contains no content")
    return story


def fit_text(value: str, font: str, size: float, width: float) -> str:
    while value and pdfmetrics.stringWidth(value, font, size) > width:
        value = value[:-4].rstrip() + "..." if len(value) > 4 else ""
    return value


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, theme: Theme, metadata: dict, **kwargs):
        super().__init__(*args, **kwargs)
        self.saved_pages, self.theme, self.metadata = [], theme, metadata

    def showPage(self):
        self.saved_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self.saved_pages)
        for state in self.saved_pages:
            self.__dict__.update(state)
            self.saveState()
            p, f, m = self.theme.palette, self.theme.fonts, self.metadata
            self.setFillColor(p["charcoal"])
            self.rect(0, PAGE_H - 43, PAGE_W, 43, fill=1, stroke=0)
            if self.theme.logo:
                width, height = ImageReader(str(self.theme.logo)).getSize()
                ratio = min(100 / width, 23 / height)
                self.drawImage(str(self.theme.logo), MARGIN, PAGE_H - 33,
                               width=width * ratio, height=height * ratio, mask="auto")
            else:
                self.setFillColor(colors.white)
                self.setFont(f["bold"], 9)
                self.drawString(MARGIN, PAGE_H - 24, fit_text(self.theme.organization, f["bold"], 9, 110))
            self.setFillColor(colors.white)
            self.setFont(f["bold"], 9)
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 19, fit_text(m["title"], f["bold"], 9, CONTENT_W - 120))
            self.setFillColor(p["accent"])
            self.setFont(f["body"], 8)
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 32, fit_text(m["subtitle"], f["body"], 8, CONTENT_W - 120))
            self.setStrokeColor(p["accent"])
            self.setLineWidth(.7)
            self.line(MARGIN, 37, PAGE_W - MARGIN, 37)
            self.setFillColor(p["muted"])
            self.setFont(f["body"], 8)
            left = self.theme.organization + (f" / Rev {m['revision']}" if m["revision"] else "")
            self.drawString(MARGIN, 23, fit_text(left.strip(" /"), f["body"], 8, 190))
            self.drawCentredString(PAGE_W / 2, 23, m["date"])
            self.setFont(f["mono"], 8)
            self.drawRightString(PAGE_W - MARGIN, 23, f"{self._pageNumber} / {total}")
            self.restoreState()
            super().showPage()
        super().save()


def metadata(source: Path, args) -> dict:
    text = source.read_text(encoding="utf-8-sig")
    title = re.search(r"^#\s+(.+)$", text, re.M)
    revision = re.search(r"Document\s+Rev(?:ision)?\.?\s+([\w.\-]+)", text, re.I)
    date = DATE_RE.search(text)
    chosen_date = args.date or (date[0] if date else "")
    if chosen_date:
        value = datetime.strptime(chosen_date, "%B %d, %Y")
        chosen_date = f"{value.strftime('%B')} {value.day}, {value.year}"
    return {"title": plain(args.title or (title[1] if title else source.stem)),
            "subtitle": plain(args.subtitle or ""),
            "revision": args.revision or (revision[1] if revision else ""), "date": chosen_date}


def build(args):
    source, output = args.source.resolve(), args.output.resolve()
    if source == output:
        raise ValueError("Source and output paths must differ")
    theme = load_theme(args.profile.resolve() if args.profile else None)
    details = metadata(source, args)
    story = parse_markdown(source, theme, load_callouts(args.callouts.resolve() if args.callouts else None), args.title)
    output.parent.mkdir(parents=True, exist_ok=True)
    document = BaseDocTemplate(str(output), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=56, bottomMargin=49, title=details["title"], author=theme.organization,
        subject=details["subtitle"], creator="make-manual Markdown renderer", pageCompression=1)
    document.addPageTemplates(PageTemplate(id="manual", frames=[Frame(MARGIN, FRAME_Y, CONTENT_W, FRAME_H,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)]))
    document.build(story, canvasmaker=lambda *a, **kw: NumberedCanvas(*a, theme=theme, metadata=details, **kw))
    from pypdf import PdfReader
    reader = PdfReader(output)
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if annotation.get("/Subtype") == "/Link" or annotation.get("/A", {}).get("/S") == "/URI":
                raise RuntimeError("Output contains a prohibited hyperlink annotation")
    print(f"Built {output} ({len(reader.pages)} pages, {output.stat().st_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="UTF-8 Markdown source")
    parser.add_argument("--output", required=True, type=Path, help="Destination PDF")
    parser.add_argument("--profile", type=Path, help="Optional local brand profile JSON")
    parser.add_argument("--callouts", type=Path, help="Optional image/callout JSON")
    for name in ("title", "subtitle", "revision", "date"):
        parser.add_argument(f"--{name}", help="Running/PDF metadata override" + ("; e.g. October 23, 2026" if name == "date" else ""))
    args = parser.parse_args()
    try:
        build(args)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
