from learn_llm.checking import Case

TEMPS = [14, 17, 20, 22, 25, 28, 31, 33]
SALES = [63, 90, 137, 148, 193, 234, 257, 288]


class Value:
    """Stands in for the learner's Value: the same four slots, and the same name in errors."""

    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.parents = []
        self.local_slopes = []


class _Shown(str):
    """A description that prints without quotes, so feedback reads `[a, a]`, not `'[a, a]'`."""

    __repr__ = str.__str__


def _op(data, parents, slopes, book):
    out = Value(data)
    out.parents, out.local_slopes = parents, slopes
    book.append(out)
    return out


def _step(f, *numbers):
    """Run one learner op on fresh values; describe what it built (None if it gave back nothing)."""
    book = []
    args = [Value(n) for n in numbers]
    out = f(*args, book)
    if out is None:
        return None
    names = {id(a): n for a, n in zip(args, "ab")}
    slopes = out.local_slopes
    return (
        out.data,
        tuple(slopes) if isinstance(slopes, (list, tuple)) else slopes,
        _Shown("[" + ", ".join(names.get(id(p), "something else") for p in out.parents) + "]"),
        len(book) == 1 and book[0] is out,
    )


def _part(i, f, *numbers):
    built = _step(f, *numbers)
    return None if built is None else built[i]


def _x_times_x_plus_x(backward):
    book = []
    x = Value(3)
    total = _op(9 + 3, [_op(9, [x, x], [3, 3], book), x], [1, 1], book)
    backward(total, book)
    return x.grad


def _mia_day(backward):
    book = []
    w, b, t, s = Value(10), Value(-60), Value(14), Value(63)
    p = _op(140, [w, t], [14, 10], book)
    g = _op(80, [p, b], [1, 1], book)
    e = _op(17, [g, s], [1, -1], book)
    loss = _op(289, [e], [34], book)
    backward(loss, book)
    return (w.grad, b.grad, s.grad)


EXERCISES = {
    "add": [
        Case("ch04.add.value", lambda f: _part(0, f, 3, 4), 7, hint="ch04.op.hint"),
        Case("ch04.add.slopes", lambda f: _part(1, f, 3, 4), (1, 1), hint="ch04.add.hint"),
        Case("ch04.op.parents", lambda f: _part(2, f, 3, 4), _Shown("[a, b]"), hint="ch04.op.hint"),
        Case("ch04.op.book", lambda f: _part(3, f, 3, 4), True, hint="ch04.op.hint"),
    ],
    "sub": [
        Case("ch04.sub.value", lambda f: _part(0, f, 3, 4), -1, hint="ch04.op.hint"),
        Case("ch04.sub.slopes", lambda f: _part(1, f, 3, 4), (1, -1), hint="ch04.sub.hint"),
        Case("ch04.op.parents", lambda f: _part(2, f, 3, 4), _Shown("[a, b]"), hint="ch04.op.hint"),
        Case("ch04.op.book", lambda f: _part(3, f, 3, 4), True, hint="ch04.op.hint"),
    ],
    "square": [
        Case("ch04.square.value", lambda f: _part(0, f, -5), 25, hint="ch04.op.hint"),
        Case("ch04.square.slopes", lambda f: _part(1, f, -5), (-10,), hint="ch04.square.hint"),
        Case("ch04.square.parents", lambda f: _part(2, f, -5), _Shown("[a]"), hint="ch04.square.hint"),
        Case("ch04.op.book", lambda f: _part(3, f, -5), True, hint="ch04.op.hint"),
    ],
    "backward": [
        Case("ch04.backward.reuse", _x_times_x_plus_x, 7, hint="ch04.backward.hint"),
        Case("ch04.backward.mia", _mia_day, (476, 34, -34), hint="ch04.backward.hint"),
    ],
    "engine_gradient": [
        Case("ch04.engine_gradient.tiny", lambda f: f(1, 0, [1, 2], [2, 4]), (-5, -3), tolerance=1e-9, hint="ch04.engine_gradient.hint"),
        Case("ch04.engine_gradient.mia", lambda f: f(10, -60, TEMPS, SALES), (-94, 2.5), tolerance=1e-9, hint="ch04.engine_gradient.hint"),
        Case("ch04.engine_gradient.fresh", lambda f: (f(10, -60, TEMPS, SALES), f(10, -60, TEMPS, SALES))[1], (-94, 2.5), tolerance=1e-9, hint="ch04.engine_gradient.fresh_hint"),
    ],
}
