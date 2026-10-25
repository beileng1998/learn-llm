import ast
import json
import shutil

import pytest

from learn_llm.course import LESSONS, load
from learn_llm.navigation import install_navigation, navigation, navigation_links


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
    first = navigation_links("00", "zh-CN", workspace)
    middle = navigation_links("02", "zh-CN", workspace)
    last = navigation_links("05", "zh-CN", workspace)
    assert [url for url, _ in first] == ["?file=home.py", "?file=zh-CN%2F02-lesson.py"]
    assert [url for url, _ in middle] == [
        "?file=zh-CN%2F00-lesson.py", "?file=home.py", "?file=zh-CN%2F05-lesson.py",
    ]
    assert [url for url, _ in last] == ["?file=zh-CN%2F02-lesson.py", "?file=home.py"]
    assert first[1][1] == "→ 下一章 · zh-CN 02"
    assert navigation_links("99", "en", workspace) == [("?file=home.py", "Course index")]


def test_navigation_returns_to_selected_language_after_english_fallback(workspace):
    (workspace / "zh-CN/02-lesson.py").unlink()
    assert navigation_links("00", "zh-CN", workspace)[-1][0] == "?file=en%2F02-lesson.py"
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
