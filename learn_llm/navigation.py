"""Shared chapter navigation, installed once in each learner notebook at startup.

The cell sits at the end of the notebook. It shows two things: a card after the
chapter's last section with the previous and next chapters by name, and a small
bar fixed in the corner for moving between chapters from anywhere on the page.
Everything is plain HTML and CSS, so it works offline.
"""

import ast
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import urlencode

from learn_llm.course import WORK, chapters
from learn_llm.i18n import LOCALES, SOURCE_LOCALE, t


@dataclass(frozen=True)
class Neighbour:
    number: str
    title: str
    url: str


def neighbours(number: str, locale: str, base: Path = WORK) -> tuple[Neighbour | None, Neighbour | None]:
    """The chapters before and after `number`, in `locale` (English where untranslated)."""
    available = chapters(locale, base)
    index = next((i for i, ch in enumerate(available) if ch.number == number), None)
    if index is None:
        return None, None

    def neighbour(i):
        if not 0 <= i < len(available):
            return None
        ch = available[i]
        return Neighbour(ch.number, ch.title, "?" + urlencode({"file": ch.path.relative_to(base).as_posix()}))

    return neighbour(index - 1), neighbour(index + 1)


def _locale(number: str, page_locale: str, base: Path) -> str:
    """The page's own language, unless the page is English standing in for an untranslated
    chapter: then the learner's chosen language, so the next chapter is in it again."""
    try:
        chosen = json.loads((base / ".settings.json").read_text(encoding="utf-8")).get("locale")
    except (OSError, ValueError, AttributeError):
        chosen = None
    if page_locale == SOURCE_LOCALE and chosen in LOCALES and chosen != SOURCE_LOCALE:
        if not any((base / chosen).glob(f"{number}-*.py")):
            return chosen
    return page_locale


def _card(item: Neighbour | None, side: str, locale: str) -> str:
    key = "nav.previous" if side == "previous" else "nav.next"
    if item is None:
        if side == "previous":
            return '<div class="lln-card lln-card--empty"></div>'
        return f'<div class="lln-card lln-card--later"><span class="lln-card__title">{escape(t("nav.later", locale))}</span></div>'
    arrow = "←" if side == "previous" else "→"
    caption = f"{arrow} {t(key, locale)}" if side == "previous" else f"{t(key, locale)} {arrow}"
    return (
        f'<a class="lln-card lln-card--{side}" href="{escape(item.url, quote=True)}">'
        f'<span class="lln-card__caption">{escape(caption)}</span>'
        f'<span class="lln-card__title">{escape(item.title)}</span></a>'
    )


def _bar_button(item: Neighbour | None, side: str, locale: str) -> str:
    key = "nav.previous" if side == "previous" else "nav.next"
    arrow = "←" if side == "previous" else "→"
    if item is None:
        label = t(key, locale)
        return f'<span class="lln-bar__button" aria-disabled="true" aria-label="{escape(label, quote=True)}">{arrow}</span>'
    label = t("nav.destination", locale, action=t(key, locale), title=item.title)
    text = f"{arrow} {item.number}" if side == "previous" else f"{item.number} {arrow}"
    attrs = f'aria-label="{escape(label, quote=True)}" title="{escape(label, quote=True)}"'
    return f'<a class="lln-bar__button" href="{escape(item.url, quote=True)}" {attrs}>{escape(text)}</a>'


def navigation(number: str, default_locale: str, base: Path = WORK):
    """Render the end-of-chapter card and the corner bar."""
    import marimo as mo

    locale = _locale(number, default_locale, base)
    previous, following = neighbours(number, locale, base)
    home = escape(t("nav.home", locale))
    css = Path(__file__).with_name("navigation.css").read_text(encoding="utf-8")
    label = escape(t("nav.label", locale), quote=True)
    return mo.Html(
        f"<style>{css}</style>"
        f'<nav class="lln-end" aria-label="{label}">'
        f'<div class="lln-end__cards">{_card(previous, "previous", locale)}{_card(following, "next", locale)}</div>'
        f'<a class="lln-end__home" href="?file=home.py">{home}</a>'
        "</nav>"
        f'<nav class="lln-bar" aria-label="{label}">'
        f"{_bar_button(previous, 'previous', locale)}"
        f'<a class="lln-bar__button lln-bar__home" href="?file=home.py">{home}</a>'
        f"{_bar_button(following, 'next', locale)}"
        "</nav>"
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


def _is_main_guard(node) -> bool:
    return (isinstance(node, ast.If) and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__")


def install_navigation(path: Path, base: Path = WORK) -> bool:
    """Add one standard cell at the end of the notebook, without changing any learner text.

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
    lines = text.splitlines(keepends=True)
    guard = next((node for node in tree.body if _is_main_guard(node)), None)
    if guard is not None:
        at = guard.lineno - 1  # just before `if __name__ == "__main__":`
    else:
        at = len(lines)
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += newline
        cell = newline * 2 + cell.rstrip("\r\n") + newline
    updated = ("".join(lines[:at]) + cell + "".join(lines[at:])).encode("utf-8")
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
