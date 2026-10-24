"""Exercise checks: run a learner's function against known cases and explain the result.

The same checks run on the lesson page (rendered with `show`) and headless in CI (`run`).
"""

import math
from dataclasses import dataclass
from typing import Any, Callable

from learn_llm.i18n import t

PASS, FAIL, ERROR, TODO, BLOCKED = "pass", "fail", "error", "todo", "blocked"


@dataclass(frozen=True)
class Case:
    """One check: call the learner's function via `call`, expect `expected`.

    `key` names the catalog message describing what the case tests.
    """

    key: str
    call: Callable[[Callable], Any]
    expected: Any
    tolerance: float = 0.0
    hint: str = ""  # catalog key of an extra tip shown when the answer is wrong


@dataclass(frozen=True)
class Result:
    case: Case
    status: str
    got: Any = None
    error: str = ""
    error_type: str = ""
    waiting_for: str = ""  # for BLOCKED: the unfinished function this one calls


def _same(got, expected, tolerance) -> bool:
    if isinstance(expected, tuple):
        return isinstance(got, (tuple, list)) and len(got) == len(expected) and all(
            _same(g, e, tolerance) for g, e in zip(got, expected)
        )
    if tolerance and isinstance(got, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(got, expected, abs_tol=tolerance)
    return got == expected


def _todo_caller(error: NotImplementedError) -> Any:
    """The code object of the function whose `todo()` raised `error`."""
    frames, tb = [], error.__traceback__
    while tb:
        frames.append(tb.tb_frame)
        tb = tb.tb_next
    return frames[-2].f_code if len(frames) >= 2 else None


def run(cases: list[Case], fn: Callable) -> list[Result]:
    results = []
    for case in cases:
        try:
            got = case.call(fn)
        except NotImplementedError as e:
            caller = _todo_caller(e)
            if caller is None or caller is getattr(fn, "__code__", None):
                results.append(Result(case, TODO))
            else:  # this exercise is written, but it calls another one that isn't yet
                results.append(Result(case, BLOCKED, waiting_for=caller.co_name))
            continue
        except Exception as e:  # learner code can raise anything; report it, don't crash the page
            results.append(Result(case, ERROR, error=f"{type(e).__name__}: {e}", error_type=type(e).__name__))
            continue
        status = PASS if _same(got, case.expected, case.tolerance) else FAIL
        results.append(Result(case, status, got=got))
    return results


def passed(results: list[Result]) -> bool:
    return bool(results) and all(r.status == PASS for r in results)


def explain(result: Result, locale: str) -> str:
    """One line of feedback for a single case, in the learner's language."""
    what = t(result.case.key, locale)
    if result.status == PASS:
        return t("check.case_pass", locale, what=what)
    if result.status == TODO:
        return t("check.case_todo", locale, what=what)
    if result.status == BLOCKED:
        return t("check.case_blocked", locale, what=what, name=result.waiting_for)
    if result.status == ERROR:
        line = t("check.case_error", locale, what=what, error=result.error)
        hint_key = f"error.{result.error_type}"
        if "'Value'" in result.error:  # an engine box used where a number was expected (ch04 on)
            hint_key += ".Value"
        hint = t(hint_key, locale)
        return f"{line} {hint}" if hint != hint_key else line
    if result.got is None:
        return t("check.case_none", locale, what=what)
    line = t("check.case_fail", locale, what=what, got=repr(result.got), expected=repr(result.case.expected))
    return f"{line} {t(result.case.hint, locale)}" if result.case.hint else line


def show(cases: list[Case], fn: Callable, locale: str):
    """Run the checks and render them as a marimo callout on the lesson page."""
    import marimo as mo

    results = run(cases, fn)
    n_pass = sum(r.status == PASS for r in results)
    if passed(results):
        title, kind = t("check.all_pass", locale), "success"
    elif all(r.status == TODO for r in results):
        title, kind = t("check.not_started", locale), "neutral"
    else:
        title, kind = t("check.some_pass", locale, n=n_pass, total=len(results)), "warn"
    lines = "\n".join(f"- {explain(r, locale)}" for r in results)
    return mo.callout(mo.md(f"**{title}**\n\n{lines}"), kind=kind)
