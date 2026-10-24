"""Checks for each chapter's exercises, shared by every lesson language.

Each chapter module defines `EXERCISES`: exercise function name -> list of Cases.
"""

import importlib


def exercises(chapter: str) -> dict:
    return importlib.import_module(f"learn_llm.checks.ch{chapter}").EXERCISES


def check(chapter: str, name: str, fn, locale: str):
    """Render the checks for one exercise on the lesson page."""
    from learn_llm.checking import show

    return show(exercises(chapter)[name], fn, locale)
