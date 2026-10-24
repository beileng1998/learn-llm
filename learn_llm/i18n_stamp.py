"""Track which English version each translated lesson was made from.

Each `i18n/<locale>.lock.json` maps a lesson file to a hash of the English file it matches.
When the English lesson changes, the hash stops matching and the tests flag the translation.

    python -m learn_llm.i18n_stamp zh-CN/00-first-program.py   # after updating that translation
    python -m learn_llm.i18n_stamp                             # every translation (use with care)
"""

import hashlib
import json
import sys
from pathlib import Path

from learn_llm.course import LESSONS, ROOT
from learn_llm.i18n import LOCALES, SOURCE_LOCALE

LOCKS = ROOT / "i18n"


def source_hash(name: str) -> str:
    text = (LESSONS / SOURCE_LOCALE / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


def lock_path(locale: str) -> Path:
    return LOCKS / f"{locale}.lock.json"


def read_lock(locale: str) -> dict[str, str]:
    path = lock_path(locale)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def stale(locale: str) -> list[str]:
    """Translated lessons whose English source changed since they were stamped."""
    lock = read_lock(locale)
    return [
        p.name for p in sorted((LESSONS / locale).glob("*.py"))
        if lock.get(p.name) != source_hash(p.name)
    ]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    targets = [Path(a) for a in argv] or [
        p.relative_to(LESSONS) for loc in LOCALES if loc != SOURCE_LOCALE for p in (LESSONS / loc).glob("*.py")
    ]
    for target in targets:
        locale, name = target.parts[-2], target.name
        lock = read_lock(locale)
        lock[name] = source_hash(name)
        lock_path(locale).write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n", encoding="utf-8")
        print(f"stamped {locale}/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
