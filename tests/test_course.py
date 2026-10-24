import ast
import re
import string
import subprocess
import sys

import pytest

from learn_llm.checking import PASS, TODO, run
from learn_llm.checks import exercises
from learn_llm.course import LESSONS, SOLUTIONS, chapters, grade, load
from learn_llm.i18n import LOCALES, SOURCE_LOCALE, catalog
from learn_llm.i18n_stamp import stale

CHAPTERS = [ch.number for ch in chapters(SOURCE_LOCALE)]
NOTEBOOKS = [ch.path for loc in LOCALES for ch in chapters(loc) if not ch.fallback]


def ids(paths):
    return [str(p.relative_to(LESSONS)) for p in paths]


@pytest.mark.parametrize("number", CHAPTERS)
def test_solutions_pass(number):
    for name, results in grade(number, SOLUTIONS / f"ch{number}.py").items():
        assert all(r.status == PASS for r in results), name


@pytest.mark.parametrize("path", NOTEBOOKS, ids=ids(NOTEBOOKS))
def test_stubs_are_not_started(path):
    """Untouched exercises must not pass, or the checks prove nothing."""
    for name, results in grade(path.name[:2], path).items():
        assert all(r.status == TODO for r in results), name


@pytest.mark.parametrize("path", NOTEBOOKS, ids=ids(NOTEBOOKS))
def test_code_is_the_same_in_every_language(path):
    """Only prose and comments are translated; exercise code must match the English notebook."""
    def functions(p):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        return {n.name: ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name != "_"}

    assert functions(path) == functions(LESSONS / SOURCE_LOCALE / path.name)


@pytest.mark.parametrize("locale", [loc for loc in LOCALES if loc != SOURCE_LOCALE])
def test_translations_are_complete_and_current(locale):
    assert not [ch.path.name for ch in chapters(locale) if ch.fallback], "missing translations"
    assert not stale(locale), "English changed since translation; update it, then `make i18n-stamp`"


@pytest.mark.parametrize("locale", LOCALES)
def test_catalogs_match_english(locale):
    def fields(text):
        return {f for _, f, _, _ in string.Formatter().parse(text) if f}

    english, other = catalog(SOURCE_LOCALE), catalog(locale)
    assert set(other) == set(english)
    for key, text in other.items():
        assert fields(text) == fields(english[key]), key


@pytest.mark.parametrize("number", CHAPTERS)
def test_every_check_has_a_message(number):
    keys = {case.key for cases in exercises(number).values() for case in cases}
    assert keys <= set(catalog(SOURCE_LOCALE))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=ids(NOTEBOOKS))
def test_no_required_external_links(path):
    """Everything needed lives in the course; links only in the optional "go deeper" part."""
    required = path.read_text(encoding="utf-8").split("<!-- go-deeper -->")[0]
    assert not re.findall(r"https?://", required)


def test_marimo_check_is_clean():
    out = subprocess.run(
        [sys.executable, "-m", "marimo", "check", "--strict", str(LESSONS)],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stdout + out.stderr


def test_checks_report_common_mistakes():
    def forgot_return(numbers):
        sum(numbers)

    def crashes(numbers):
        return numbers[10]

    cases = exercises("00")["total"]
    assert {r.status for r in run(cases, forgot_return)} == {"fail"}
    assert all(r.got is None for r in run(cases, forgot_return))
    assert {r.status for r in run(cases, crashes)} == {"error"}


def test_notebooks_import_without_running_cells():
    module = load(LESSONS / SOURCE_LOCALE / "00-first-program.py")
    assert module.double(4) == 8
