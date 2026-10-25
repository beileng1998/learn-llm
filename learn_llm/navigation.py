"""Shared chapter navigation, installed once in each learner notebook at startup."""

import ast
import json
import os
import re
import shutil
import tempfile
from html import escape
from pathlib import Path
from urllib.parse import urlencode

from learn_llm.course import WORK, chapters
from learn_llm.i18n import LOCALES, t


def navigation_links(number: str, locale: str, base: Path = WORK) -> list[tuple[str | None, str]]:
    """Return three stable slots; unavailable chapter links have no destination."""
    available = chapters(locale, base)
    index = next((i for i, ch in enumerate(available) if ch.number == number), None)
    links = [
        (None, t("nav.previous", locale)),
        ("?file=home.py", t("nav.home", locale)),
        (None, t("nav.next", locale)),
    ]

    def chapter_link(ch, key):
        url = "?" + urlencode({"file": ch.path.relative_to(base).as_posix()})
        return url, t("nav.destination", locale, action=t(key, locale), title=ch.title)

    if index is not None and index > 0:
        links[0] = chapter_link(available[index - 1], "nav.previous")
    if index is not None and index + 1 < len(available):
        links[2] = chapter_link(available[index + 1], "nav.next")
    return links


def navigation(number: str, default_locale: str, base: Path = WORK):
    """Render independently of exercise cells, retaining the learner's language."""
    import marimo as mo

    try:
        locale = json.loads((base / ".settings.json").read_text(encoding="utf-8")).get("locale")
    except (OSError, ValueError, AttributeError):
        locale = None
    if locale not in LOCALES:
        locale = default_locale
    # Plain escaped anchors keep chapter titles literal, and use the editor's
    # normal same-origin navigation and unsaved-change handling.
    controls = []
    icons = ("lucide:chevron-left", "lucide:list", "lucide:chevron-right")
    for (url, label), icon in zip(navigation_links(number, locale, base), icons):
        attributes = (
            'class="learn-llm-navigation__button" '
            f'aria-label="{escape(label, quote=True)}" title="{escape(label, quote=True)}"'
        )
        content = mo.icon(icon, size=18).text
        if url is None:
            controls.append(f'<button type="button" {attributes} disabled>{content}</button>')
        else:
            controls.append(f'<a href="{escape(url, quote=True)}" {attributes}>{content}</a>')
    css = Path(__file__).with_name("navigation.css").read_text(encoding="utf-8")
    return mo.Html(
        f'<style>{css}</style>'
        f'<nav class="learn-llm-navigation" aria-label="{escape(t("nav.label", locale))}">'
        + "".join(controls) + "</nav>"
    )


def _is_cell(node) -> bool:
    if not isinstance(node, ast.FunctionDef):
        return False
    for decorator in node.decorator_list:
        call = decorator.func if isinstance(decorator, ast.Call) else decorator
        if (isinstance(call, ast.Attribute) and call.attr == "cell"
                and isinstance(call.value, ast.Name) and call.value.id == "app"):
            return True
    return False


def _has_navigation(cell: ast.FunctionDef) -> bool:
    # Inspect code, not a comment or cell name: marimo can rewrite both on save.
    aliases = {
        alias.asname or alias.name
        for node in ast.walk(cell)
        if isinstance(node, ast.ImportFrom) and node.module == "learn_llm.navigation"
        for alias in node.names if alias.name == "navigation"
    }
    return any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in aliases
        for node in ast.walk(cell)
    )


def install_navigation(path: Path, base: Path = WORK) -> bool:
    """Add one standard cell without reserializing or replacing any learner text.

    Back up the original once, then replace atomically. Invalid notebooks are
    left alone; the launcher reports them so the learner can fix them in marimo.
    """
    relative = path.relative_to(base)
    if not re.fullmatch(r"\d{2}-.+\.py", path.name) or relative.parts[0] not in LOCALES:
        return False
    original = path.read_bytes()
    text = original.decode("utf-8")
    tree = ast.parse(text)
    cells = [node for node in tree.body if _is_cell(node)]
    if any(_has_navigation(cell) for cell in cells):
        return False
    if not cells:
        raise ValueError("no standard marimo cells found")

    newline = "\r\n" if b"\r\n" in original else "\n"
    cell = (
        '@app.cell(hide_code=True)\n'
        'def _():\n'
        '    from learn_llm.navigation import navigation as _course_navigation\n'
        '\n'
        f'    _course_navigation({path.name[:2]!r}, {relative.parts[0]!r})\n'
        '    return\n\n\n'
    ).replace("\n", newline)
    first_line = min(d.lineno for d in cells[0].decorator_list) - 1
    lines = text.splitlines(keepends=True)
    updated = ("".join(lines[:first_line]) + cell + "".join(lines[first_line:])).encode("utf-8")
    ast.parse(updated)

    backup = base / ".navigation-backups" / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(path, backup)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(updated)
        shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return True
