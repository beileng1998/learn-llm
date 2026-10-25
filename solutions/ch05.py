"""Reference solutions for chapter 05. Peek only after trying!"""

import numpy as np


def dot(ws, xs):
    total = 0
    for w, x in zip(ws, xs):
        total = total + w * x
    return total


def predict_all(rows, ws, b):
    guesses = []
    for row in rows:
        guesses.append(dot(ws, row) + b)
    return guesses


def predict_np(X, w, b):
    return X @ w + b


def mse_np(X, y, w, b):
    e = X @ w + b - y
    return np.mean(e * e)


def gradient_np(X, y, w, b):
    e = X @ w + b - y
    grad_w = (2 * e) @ X / len(y)
    grad_b = np.mean(2 * e)
    return grad_w, grad_b
