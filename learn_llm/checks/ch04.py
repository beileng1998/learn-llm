from learn_llm.checking import Case

TEMPS = [14, 17, 20, 22, 25, 28, 31, 33]
SALES = [63, 90, 137, 148, 193, 234, 257, 288]


class _V:
    """Stands in for the learner's Value: the same four slots."""

    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.parents = []
        self.local_slopes = []


def _op(data, parents, slopes, book):
    out = _V(data)
    out.parents, out.local_slopes = parents, slopes
    book.append(out)
    return out


def _step(f, *numbers):
    """Run one learner op on fresh values; describe what it built."""
    book = []
    args = [_V(n) for n in numbers]
    out = f(*args, book)
    return (
        out.data,
        tuple(out.local_slopes),
        tuple(p is a for p, a in zip(out.parents, args)) + (len(out.parents) == len(args),),
        len(book) == 1 and book[0] is out,
    )


def _x_times_x_plus_x(backward):
    book = []
    x = _V(3)
    total = _op(9 + 3, [_op(9, [x, x], [3, 3], book), x], [1, 1], book)
    backward(total, book)
    return x.grad


def _mia_day(backward):
    book = []
    w, b, t, s = _V(10), _V(-60), _V(14), _V(63)
    p = _op(140, [w, t], [14, 10], book)
    g = _op(80, [p, b], [1, 1], book)
    e = _op(17, [g, s], [1, -1], book)
    loss = _op(289, [e], [34], book)
    backward(loss, book)
    return (w.grad, b.grad, s.grad)


EXERCISES = {
    "add": [
        Case("ch04.add.value", lambda f: _step(f, 3, 4)[0], 7, hint="ch04.op.hint"),
        Case("ch04.add.slopes", lambda f: _step(f, 3, 4)[1], (1, 1), hint="ch04.add.hint"),
        Case("ch04.op.parents", lambda f: _step(f, 3, 4)[2], (True, True, True), hint="ch04.op.hint"),
        Case("ch04.op.book", lambda f: _step(f, 3, 4)[3], True, hint="ch04.op.hint"),
    ],
    "sub": [
        Case("ch04.sub.value", lambda f: _step(f, 3, 4)[0], -1, hint="ch04.op.hint"),
        Case("ch04.sub.slopes", lambda f: _step(f, 3, 4)[1], (1, -1), hint="ch04.sub.hint"),
        Case("ch04.op.parents", lambda f: _step(f, 3, 4)[2], (True, True, True), hint="ch04.op.hint"),
        Case("ch04.op.book", lambda f: _step(f, 3, 4)[3], True, hint="ch04.op.hint"),
    ],
    "square": [
        Case("ch04.square.value", lambda f: _step(f, -5)[0], 25, hint="ch04.op.hint"),
        Case("ch04.square.slopes", lambda f: _step(f, -5)[1], (-10,), hint="ch04.square.hint"),
        Case("ch04.square.parents", lambda f: _step(f, -5)[2], (True, True), hint="ch04.square.hint"),
        Case("ch04.op.book", lambda f: _step(f, -5)[3], True, hint="ch04.op.hint"),
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
