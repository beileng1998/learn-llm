import ast
import json
import shutil

import pytest

from learn_llm.course import LESSONS, load
from learn_llm.navigation import install_navigation, navigation, neighbours


@pytest.fixture
def workspace(tmp_path):
    for locale in ("en", "zh-CN"):
        (tmp_path / locale).mkdir()
        for number in ("00", "02", "05"):
            (tmp_path / locale / f"{number}-lesson.py").write_text(
                f'import marimo\napp = marimo.App(app_title="{locale} {number}")\n'
            )
    return tmp_path


def test_navigation_uses_actual_order_and_has_no_wraparound(workspace):
    first = neighbours("00", "zh-CN", workspace)
    middle = neighbours("02", "zh-CN", workspace)
    last = neighbours("05", "zh-CN", workspace)
    assert first[0] is None and first[1].url == "?file=zh-CN%2F02-lesson.py"
    assert [n.url for n in middle] == ["?file=zh-CN%2F00-lesson.py", "?file=zh-CN%2F05-lesson.py"]
    assert last[0].url == "?file=zh-CN%2F02-lesson.py" and last[1] is None
    assert first[1].title == "zh-CN 02"
    assert neighbours("99", "en", workspace) == (None, None)


def test_navigation_returns_to_selected_language_after_english_fallback(workspace):
    (workspace / "zh-CN/02-lesson.py").unlink()
    assert neighbours("00", "zh-CN", workspace)[1].url == "?file=en%2F02-lesson.py"
    (workspace / ".settings.json").write_text(json.dumps({"locale": "zh-CN"}))
    html = navigation("02", "en", workspace).text
    assert "上一章" in html and "下一章" in html
    assert "zh-CN%2F05-lesson.py" in html


@pytest.mark.parametrize("settings", ["not json", "[]", '{"locale":"missing"}'])
def test_bad_settings_fall_back_to_notebook_language(workspace, settings):
    (workspace / ".settings.json").write_text(settings)
    assert "下一章" in navigation("00", "zh-CN", workspace).text


def test_titles_are_literal_html(workspace):
    (workspace / "en/02-lesson.py").write_text('app_title="<img src=x> & lesson"')
    html = navigation("00", "en", workspace).text
    assert "&lt;img src=x&gt; &amp; lesson" in html
    assert "<img" not in html


def test_navigation_works_offline_and_names_the_neighbours(workspace):
    html = navigation("02", "en", workspace).text
    assert "iconify" not in html and "http" not in html  # nothing loaded from the internet
    assert html.count('class="lln-card lln-card--') == 2  # previous and next cards, by name
    assert ">en 00<" in html and ">en 05<" in html
    assert "position: fixed" in html  # the corner bar
    assert 'aria-label="Next: en 05"' in html


def test_first_and_last_chapters(workspace):
    from html.parser import HTMLParser

    class Bar(HTMLParser):
        def __init__(self):
            super().__init__()
            self.buttons = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if "lln-bar__button" in (attrs.get("class") or ""):
                self.buttons.append((tag, attrs))

    bar = Bar()
    bar.feed(navigation("00", "en", workspace).text)
    assert [tag for tag, _ in bar.buttons] == ["span", "a", "a"]  # nothing before the first chapter
    assert bar.buttons[0][1].get("aria-disabled") == "true"
    assert all(attrs.get("aria-label") or tag == "a" for tag, attrs in bar.buttons)
    assert "More chapters are on the way" in navigation("05", "en", workspace).text


@pytest.mark.parametrize("newline", [b"\n", b"\r\n"])
def test_install_preserves_work_bytes_and_backs_up_once(tmp_path, newline):
    path = tmp_path / "zh-CN/00-first-program.py"
    path.parent.mkdir()
    original = (LESSONS / "zh-CN" / path.name).read_bytes().replace(
        b"    todo()", b"    return celsius * 9 / 5 + 32  # learner's answer", 1
    ).replace(b"\n", newline)
    path.write_bytes(original)
    assert install_navigation(path, tmp_path)
    installed = path.read_bytes()
    tree = ast.parse(installed)
    nav = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
               and any(isinstance(n, ast.ImportFrom) and n.module == "learn_llm.navigation"
                       for n in ast.walk(node)))
    lines = installed.splitlines(keepends=True)
    start = min(d.lineno for d in nav.decorator_list) - 1
    # Remove only the inserted block; every original byte must survive.
    assert b"".join(lines[:start] + lines[nav.end_lineno + 2:]) == original
    backup = tmp_path / ".navigation-backups/zh-CN" / path.name
    assert backup.read_bytes() == original
    assert not install_navigation(path, tmp_path)
    assert path.read_bytes() == installed
    assert backup.read_bytes() == original
    assert load(path).to_fahrenheit(100) == 212
    assert nav is [n for n in tree.body if isinstance(n, ast.FunctionDef)][-1]  # the last cell


def test_editor_save_then_restart_does_not_duplicate_navigation(tmp_path):
    # Round-trip through the same marimo loader/serializer used by the editor.
    from marimo._ast.load import load_app
    from marimo._ast.app import InternalApp
    from marimo._ast.parse import parse_notebook

    path = tmp_path / "en/00-first-program.py"
    path.parent.mkdir()
    shutil.copyfile(LESSONS / "en" / path.name, path)
    install_navigation(path, tmp_path)
    app = load_app(path)
    assert app is not None
    path.write_text(InternalApp(app).to_py())
    saved = path.read_bytes()
    assert not parse_notebook(saved.decode()).violations
    assert not install_navigation(path, tmp_path)
    assert path.read_bytes() == saved


def test_prepare_workspace_migrates_existing_work_and_adds_new_lessons(tmp_path, monkeypatch, capsys):
    from learn_llm import launch

    work = tmp_path / "my-work"
    existing = work / "en/00-first-program.py"
    existing.parent.mkdir(parents=True)
    answer = (LESSONS / "en" / existing.name).read_text().replace("    todo()", "    return 42", 1)
    existing.write_text(answer)
    broken = work / "en/99-broken.py"
    broken.write_text("def broken(:\n")
    monkeypatch.setattr(launch, "WORK", work)
    monkeypatch.setattr(launch, "SETTINGS", work / ".settings.json")
    launch.prepare_workspace()
    first = existing.read_bytes()
    assert "return 42" in first.decode()
    assert "_course_navigation" in first.decode()
    assert "_course_navigation" in (work / "zh-CN/05-many-numbers-at-once.py").read_text()
    assert "Navigation not added" in capsys.readouterr().err
    assert broken.read_text() == "def broken(:\n"
    launch.prepare_workspace()
    assert existing.read_bytes() == first
    assert (work / ".navigation-backups/en" / existing.name).read_text() == answer


def test_install_appends_when_there_is_no_main_guard(tmp_path):
    path = tmp_path / "en/00-first-program.py"
    path.parent.mkdir()
    text = (LESSONS / "en" / path.name).read_text()
    path.write_text(text[: text.index('if __name__ == "__main__":')].rstrip("\n"))
    assert install_navigation(path, tmp_path)
    tree = ast.parse(path.read_text())
    assert "_course_navigation" in ast.unparse(tree.body[-1])
    assert not install_navigation(path, tmp_path)


def test_a_translated_page_keeps_its_own_language(workspace):
    (workspace / ".settings.json").write_text(json.dumps({"locale": "zh-CN"}))
    html = navigation("02", "en", workspace).text  # zh-CN/02 exists, so this English page was chosen
    assert "Next" in html and "下一章" not in html
