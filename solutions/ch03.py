"""Reference solutions for chapter 03. Peek only after trying!"""


def day_slopes(w, b, t, s):
    p = w * t
    g = p + b
    e = g - s
    blame_e = 2 * e
    blame_g = blame_e
    blame_p = blame_g
    blame_b = blame_g
    blame_w = t * blame_p
    return blame_w, blame_b


def gradient(w, b, xs, ys):
    total_w = 0
    total_b = 0
    for t, s in zip(xs, ys):
        dw, db = day_slopes(w, b, t, s)
        total_w = total_w + dw
        total_b = total_b + db
    return total_w / len(xs), total_b / len(xs)


def fit(w, b, xs, ys, rate, steps):
    for i in range(steps):
        dw, db = gradient(w, b, xs, ys)
        w = w - rate * dw
        b = b - rate * db
    return w, b
