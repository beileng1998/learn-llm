"""Exercise checks: run a learner's function against known cases and explain the result.

The same checks run on the lesson page (rendered with `show`) and headless in CI (`run`).
"""

import math
from dataclasses import dataclass
from typing import Any, Callable

from learn_llm.i18n import t

PASS, FAIL, ERROR, TODO = "pass", "fail", "error", "todo"


@dataclass(frozen=True)
class Case:
    """One check: call the learner's function via `call`, expect `expected`.

    `key` names the catalog message describing what the case tests.
    """

    key: str
    call: Callable[[Callable], Any]
    expected: Any
    tolerance: float = 0.0


@dataclass(frozen=True)
class Result:
    case: Case
    status: str
    got: Any = None
    error: str = ""


def _same(got, expected, tolerance) -> bool:
    if tolerance and isinstance(got, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(got, expected, abs_tol=tolerance)
    return got == expected


def run(cases: list[Case], fn: Callable) -> list[Result]:
    results = []
    for case in cases:
        try:
            got = case.call(fn)
        except NotImplementedError:
            results.append(Result(case, TODO))
            continue
        except Exception as e:  # learner code can raise anything; report it, don't crash the page
            results.append(Result(case, ERROR, error=f"{type(e).__name__}: {e}"))
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
    if result.status == ERROR:
        return t("check.case_error", locale, what=what, error=result.error)
    if result.got is None:
        return t("check.case_none", locale, what=what)
    return t(
        "check.case_fail", locale, what=what, got=repr(result.got), expected=repr(result.case.expected)
    )


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
