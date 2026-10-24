"""Reference solutions for chapter 02. Peek only after trying!"""


def nudge_slope(f, x):
    h = 0.0001
    return (f(x + h) - f(x)) / h


def step(w, slope, rate):
    return w - rate * slope


def descend(f, w, rate, steps):
    for i in range(steps):
        w = step(w, nudge_slope(f, w), rate)
    return w


def slope_f(x):
    return 6 * x + 5
