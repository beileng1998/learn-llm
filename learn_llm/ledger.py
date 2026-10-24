"""The concept ledger: which ideas each chapter teaches, and proof that none is used early.

`lessons/ledger.toml` lists, per chapter, the concepts it introduces (with a one-line
definition) and the earlier concepts it uses. Two checks keep it honest:

- declared uses must have been introduced by an earlier chapter;
- the code a learner sees (visible notebook cells) and the code a learner must write
  (the reference solution) may only use Python features whose concept is already taught.
  Prose can't be checked this way; the novice-review gate covers it, using this ledger
  as the reviewer's "already taught" list.
"""

import ast
import builtins
import tomllib
from pathlib import Path

from learn_llm.course import LESSONS, SOLUTIONS
from learn_llm.i18n import SOURCE_LOCALE

LEDGER = LESSONS / "ledger.toml"

# Python features a learner can see or must write, and the concept that explains each.
NODE_CONCEPTS = {
    ast.BinOp: "arithmetic",
    ast.Assign: "variable",
    ast.FunctionDef: "function",
    ast.Return: "return",
    ast.List: "list",
    ast.For: "loop",
    ast.If: "if",
    ast.Compare: "comparison",
    ast.While: "while-loop",
    ast.AugAssign: "augmented-assignment",
    ast.ListComp: "list-comprehension",
    ast.Lambda: "lambda",
    ast.ClassDef: "class",
    ast.Dict: "dict",
    ast.Tuple: "tuple",
    ast.Subscript: "indexing",
    ast.JoinedStr: "f-string",
    ast.Attribute: "attribute",
}
OPERATOR_CONCEPTS = {ast.Pow: "power", ast.Mod: "remainder", ast.FloorDiv: "floor-division", ast.MatMult: "matmul-operator"}
MODULE_CONCEPTS = {"math": "math-module", "random": "random-module", "numpy": "numpy", "torch": "pytorch"}
# Code the course provides on purpose; using it isn't a concept the learner must know yet.
COURSE_NAMES = {"todo": "todo-placeholder", "check": None, "mo": None}


def load() -> dict:
    return tomllib.loads(LEDGER.read_text(encoding="utf-8"))


def _call_concept(name: str) -> str | None:
    if name in COURSE_NAMES:
        return COURSE_NAMES[name]
    if hasattr(builtins, name):
        return f"builtin-{name}"
    return "call"


def concepts_in(tree: ast.AST) -> set[str]:
    found = set()
    for node in ast.walk(tree):
        for kind, concept in NODE_CONCEPTS.items():
            if isinstance(node, kind):
                found.add(concept)
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATOR_CONCEPTS:
            found.add(OPERATOR_CONCEPTS[type(node.op)])
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            found.add(_call_concept(node.func.id))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                found.add(MODULE_CONCEPTS.get(name.split(".")[0], f"module-{name}"))
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            found.add("docstring")
    found.discard(None)
    return found


def _is_hidden(decorator: ast.expr) -> bool:
    return isinstance(decorator, ast.Call) and any(
        k.arg == "hide_code" and isinstance(k.value, ast.Constant) and k.value.value for k in decorator.keywords
    )


def visible_code(notebook: Path) -> list[ast.AST]:
    """The code cells a learner sees on the page (not hidden cells, not the setup block)."""
    tree = ast.parse(notebook.read_text(encoding="utf-8"))
    shown = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or not node.decorator_list:
            continue
        decorator = node.decorator_list[0]
        if _is_hidden(decorator):
            continue
        if isinstance(decorator, ast.Attribute) and decorator.attr == "function":
            shown.append(ast.FunctionDef(**{**node.__dict__, "decorator_list": []}))  # the def, minus marimo's decorator
        else:
            body = [s for s in node.body if not isinstance(s, ast.Return)]  # marimo's own `return`
            shown.append(ast.Module(body=body, type_ignores=[]))
    return shown


def problems() -> list[str]:
    ledger = load()
    defined = ledger.get("concepts", {})
    taught: set[str] = set()
    found = []
    for chapter, entry in sorted(ledger.get("chapters", {}).items()):
        introduces, uses = set(entry.get("introduces", [])), set(entry.get("uses", []))
        for c in sorted(introduces - set(defined)):
            found.append(f"ch{chapter}: introduces '{c}' but [concepts] has no definition for it")
        for c in sorted(introduces & taught):
            found.append(f"ch{chapter}: introduces '{c}', already introduced earlier")
        for c in sorted(uses - taught):
            found.append(f"ch{chapter}: uses '{c}' before any chapter introduced it")
        allowed = taught | introduces

        notebook = next((LESSONS / SOURCE_LOCALE).glob(f"{chapter}-*.py"))
        seen = set().union(*(concepts_in(t) for t in visible_code(notebook)))
        for c in sorted(seen - allowed):
            found.append(f"ch{chapter}: page shows code using '{c}', not taught by ch{chapter} or earlier")
        solution = SOLUTIONS / f"ch{chapter}.py"
        if solution.exists():
            needed = concepts_in(ast.parse(solution.read_text(encoding="utf-8")))
            for c in sorted(needed - allowed - {"docstring"}):
                found.append(f"ch{chapter}: solution needs '{c}', not taught by ch{chapter} or earlier")
        taught |= introduces
    return found


def already_taught(before: str) -> str:
    """The reviewer's "already taught" list: every concept introduced before chapter `before`."""
    ledger = load()
    lines = []
    for chapter, entry in sorted(ledger.get("chapters", {}).items()):
        if chapter >= before:
            break
        for c in entry.get("introduces", []):
            lines.append(f"- {c}: {ledger['concepts'][c]} (ch {chapter})")
    return "\n".join(lines) or "nothing (this is the first lesson)"


if __name__ == "__main__":
    import sys

    # python -m learn_llm.ledger 03   → the "already taught" list for a chapter-03 review
    print(already_taught(sys.argv[1]) if len(sys.argv) > 1 else "\n".join(problems()) or "No gaps.")
