"""Reference solutions for chapter 04. Peek only after trying!"""


class Value:
    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.parents = []
        self.local_slopes = []


def mul(a, b, book):
    out = Value(a.data * b.data)
    out.parents = [a, b]
    out.local_slopes = [b.data, a.data]
    book.append(out)
    return out


def add(a, b, book):
    out = Value(a.data + b.data)
    out.parents = [a, b]
    out.local_slopes = [1, 1]
    book.append(out)
    return out


def sub(a, b, book):
    out = Value(a.data - b.data)
    out.parents = [a, b]
    out.local_slopes = [1, -1]
    book.append(out)
    return out


def square(a, book):
    out = Value(a.data * a.data)
    out.parents = [a]
    out.local_slopes = [2 * a.data]
    book.append(out)
    return out


def backward(loss, book):
    loss.grad = 1
    for entry in reversed(book):
        for parent, slope in zip(entry.parents, entry.local_slopes):
            parent.grad = parent.grad + slope * entry.grad


def engine_gradient(w_num, b_num, xs, ys):
    book = []
    w = Value(w_num)
    b = Value(b_num)
    total = Value(0)
    for x, y in zip(xs, ys):
        guess = add(mul(w, Value(x), book), b, book)
        e = sub(guess, Value(y), book)
        total = add(total, square(e, book), book)
    mean = mul(total, Value(1 / len(xs)), book)
    backward(mean, book)
    return w.grad, b.grad
