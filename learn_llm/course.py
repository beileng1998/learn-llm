"""Where the lessons live, and how far a learner has got in each one."""

import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from learn_llm.checking import PASS, TODO, run
from learn_llm.checks import exercises
from learn_llm.i18n import SOURCE_LOCALE

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
SOLUTIONS = ROOT / "solutions"
WORK = ROOT / "my-work"

DONE, IN_PROGRESS, NOT_STARTED = "done", "in_progress", "not_started"


@dataclass(frozen=True)
class Chapter:
    number: str  # "00", "01", ...
    title: str
    path: Path
    fallback: bool  # True when shown in English because this locale has no translation yet


def _title(path: Path) -> str:
    match = re.search(r'app_title="([^"]+)"', path.read_text(encoding="utf-8"))
    return match.group(1) if match else path.stem


def chapters(locale: str, base: Path = LESSONS) -> list[Chapter]:
    """Every chapter in `locale`, using the English notebook where a translation is missing."""
    result = []
    for source in sorted((base / SOURCE_LOCALE).glob("[0-9][0-9]-*.py")):
        translated = base / locale / source.name
        path = translated if translated.exists() else source
        result.append(Chapter(source.name[:2], _title(path), path, path == source and locale != SOURCE_LOCALE))
    return result


def load(path: Path):
    """Import a notebook (or solutions file) as a module, without running its cells."""
    name = f"_learn_llm_{abs(hash(str(path)))}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        del sys.modules[name]
    return module


def grade(number: str, path: Path) -> dict:
    """Check results for every exercise of chapter `number`, using the functions in `path`."""
    module = load(path)
    return {name: run(cases, getattr(module, name)) for name, cases in exercises(number).items()}


def progress(number: str, path: Path) -> str:
    try:
        results = [r for rs in grade(number, path).values() for r in rs]
    except Exception:  # a half-typed notebook may not even import
        return IN_PROGRESS
    if all(r.status == PASS for r in results):
        return DONE
    if all(r.status == TODO for r in results):
        return NOT_STARTED
    return IN_PROGRESS
