from learn_llm.checking import Case


def _square(x):
    return x * x


def _line(x):
    return 5 * x + 1


def _flat(x):
    return 7


def _bowl(x):
    return (x - 3) * (x - 3)


EXERCISES = {
    "nudge_slope": [
        Case("ch02.nudge_slope.square", lambda f: f(_square, 3), 6, tolerance=1e-3, hint="ch02.nudge_slope.hint"),
        Case("ch02.nudge_slope.line", lambda f: f(_line, 10), 5, tolerance=1e-4, hint="ch02.nudge_slope.hint"),
        Case("ch02.nudge_slope.flat", lambda f: f(_flat, 2), 0, tolerance=1e-9, hint="ch02.nudge_slope.hint"),
        Case("ch02.nudge_slope.negative", lambda f: f(_square, -2), -4, tolerance=1e-3, hint="ch02.nudge_slope.hint"),
    ],
    "step": [
        Case("ch02.step.uphill", lambda f: f(10, 2, 0.5), 9, tolerance=1e-12, hint="ch02.step.hint"),
        Case("ch02.step.downhill", lambda f: f(10, -2, 0.5), 11, tolerance=1e-12, hint="ch02.step.hint"),
        Case("ch02.step.flat", lambda f: f(10, 0, 0.5), 10, tolerance=1e-12),
        Case("ch02.step.small", lambda f: f(1, 100, 0.001), 0.9, tolerance=1e-12),
    ],
    "descend": [
        Case("ch02.descend.none", lambda f: f(_bowl, 0, 0.1, 0), 0, tolerance=1e-12),
        Case("ch02.descend.one", lambda f: f(_bowl, 0, 0.5, 1), 3, tolerance=1e-3, hint="ch02.descend.hint"),
        Case("ch02.descend.many", lambda f: f(_bowl, 0, 0.1, 100), 3, tolerance=1e-3, hint="ch02.descend.hint"),
    ],
    "slope_f": [
        Case("ch02.slope_f.zero", lambda f: f(0), 5, tolerance=1e-9, hint="ch02.slope_f.hint"),
        Case("ch02.slope_f.one", lambda f: f(1), 11, tolerance=1e-9, hint="ch02.slope_f.hint"),
        Case("ch02.slope_f.negative", lambda f: f(-2), -7, tolerance=1e-9, hint="ch02.slope_f.hint"),
        Case("ch02.slope_f.four", lambda f: f(4), 29, tolerance=1e-9, hint="ch02.slope_f.hint"),
    ],
}
