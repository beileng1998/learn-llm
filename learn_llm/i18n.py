"""Message catalogs for the course's on-screen text (check results, hints, navigation).

Lesson prose is translated per notebook; only short UI strings live here.
"""

import json
from functools import cache
from pathlib import Path

SOURCE_LOCALE = "en"
LOCALES = ["en", "zh-CN"]
LOCALE_NAMES = {"en": "English", "zh-CN": "简体中文"}

_CATALOG_DIR = Path(__file__).parent / "locales"


@cache
def catalog(locale: str) -> dict[str, str]:
    path = _CATALOG_DIR / f"{locale}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def t(key: str, locale: str = SOURCE_LOCALE, **values) -> str:
    """Look up `key` in `locale`, falling back to English, then to the key itself."""
    text = catalog(locale).get(key) or catalog(SOURCE_LOCALE).get(key) or key
    return text.format(**values) if values else text
