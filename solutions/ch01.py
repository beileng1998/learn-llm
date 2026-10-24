"""Reference solutions for chapter 01. Peek only after trying!"""


def predict(w, b, x):
    return w * x + b


def squared_error(guess, truth):
    return (guess - truth) ** 2


def mse(w, b, xs, ys):
    running = 0
    for x, y in zip(xs, ys):
        running = running + squared_error(predict(w, b, x), y)
    return running / len(xs)
