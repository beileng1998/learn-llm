"""Headless checks, for CI and maintainers. Learners see the same checks on the lesson page.

    python -m learn_llm.grade 00                 # the lesson notebooks (or my-work/ if it exists)
    python -m learn_llm.grade --solutions        # the reference solutions, every chapter
"""

import argparse
import sys

from learn_llm.checking import PASS, explain
from learn_llm.course import LESSONS, SOLUTIONS, WORK, chapters, grade
from learn_llm.i18n import LOCALES, SOURCE_LOCALE


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m learn_llm.grade")
    parser.add_argument("chapter", nargs="?", help="two-digit chapter number; all chapters if omitted")
    parser.add_argument("--solutions", action="store_true", help="check solutions/ instead of notebooks")
    parser.add_argument("--lessons", action="store_true", help="check lessons/ even if my-work/ exists")
    args = parser.parse_args(argv)

    base = LESSONS if args.lessons or not WORK.exists() else WORK
    targets = []  # (label, chapter number, path)
    for locale in [SOURCE_LOCALE] if args.solutions else LOCALES:
        for ch in chapters(locale, base):
            if args.chapter and ch.number != args.chapter:
                continue
            if args.solutions:
                targets.append((f"solutions/ch{ch.number}.py", ch.number, SOLUTIONS / f"ch{ch.number}.py"))
            elif not ch.fallback:
                targets.append((str(ch.path.relative_to(base.parent)), ch.number, ch.path))
    if not targets:
        print(f"No chapter {args.chapter!r} found.", file=sys.stderr)
        return 2

    ok = True
    for label, number, path in targets:
        print(label)
        for name, results in grade(number, path).items():
            for r in results:
                ok &= r.status == PASS
                print(f"  {name}: {explain(r, SOURCE_LOCALE)}")
    print("All checks pass." if ok else "Some checks do not pass.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
