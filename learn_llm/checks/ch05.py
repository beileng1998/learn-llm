import numpy as np

from learn_llm.checking import Case

TEMPS = [14, 17, 20, 22, 25, 28, 31, 33]
RAIN = [0, 1, 0, 1, 0, 0, 1, 0]
WEEKEND = [0, 0, 1, 0, 0, 1, 0, 0]
SALES = [63, 90, 137, 148, 193, 234, 257, 288]
ROWS = [[t, r, k] for t, r, k in zip(TEMPS, RAIN, WEEKEND)]
GUESSES = [63, 91, 139, 151, 195, 235, 259, 291]  # at w = [12, -8, 4], b = -105


def _plain(value):
    """NumPy results as plain numbers and lists, so feedback reads like the lesson."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (tuple, list)):
        return type(value)(_plain(v) for v in value)
    return value


def _np(f, rows, w, *rest):
    return _plain(f(np.array(rows, dtype=float), np.array(w, dtype=float), *rest))


def _mia_np(f, w, b):
    return _plain(f(np.array(ROWS, dtype=float), np.array(SALES, dtype=float), np.array(w, dtype=float), b))


EXERCISES = {
    "dot": [
        Case("ch05.dot.small", lambda f: f([1, 2, 3], [4, 5, 6]), 32, tolerance=1e-9, hint="ch05.dot.hint"),
        Case("ch05.dot.day", lambda f: f([12, -8, 4], [25, 0, 1]), 304, tolerance=1e-9, hint="ch05.dot.hint"),
        Case("ch05.dot.one", lambda f: f([3], [7]), 21, tolerance=1e-9, hint="ch05.dot.hint"),
    ],
    "predict_all": [
        Case("ch05.predict_all.small", lambda f: f([[1, 2], [3, 4]], [1, 1], 0), [3, 7], tolerance=1e-9, hint="ch05.predict_all.hint"),
        Case("ch05.predict_all.mia", lambda f: f(ROWS, [12, -8, 4], -105), GUESSES, tolerance=1e-9, hint="ch05.predict_all.hint"),
    ],
    "predict_np": [
        Case("ch05.predict_np.small", lambda f: _np(f, [[1, 2], [3, 4]], [1, 1], 0), [3, 7], tolerance=1e-9, hint="ch05.predict_np.hint"),
        Case("ch05.predict_np.mia", lambda f: _np(f, ROWS, [12, -8, 4], -105), GUESSES, tolerance=1e-9, hint="ch05.predict_np.hint"),
    ],
    "mse_np": [
        Case("ch05.mse_np.line", lambda f: _mia_np(f, [10, 0, 0], -60), 177.5, tolerance=1e-9, hint="ch05.mse_np.hint"),
        Case("ch05.mse_np.close", lambda f: _mia_np(f, [12, -8, 4], -105), 4, tolerance=1e-9, hint="ch05.mse_np.hint"),
    ],
    "gradient_np": [
        Case("ch05.gradient_np.tiny", lambda f: _plain(f(np.array([[1.0], [2.0]]), np.array([2.0, 4.0]), np.array([1.0]), 0)), ([-5], -3), tolerance=1e-9, hint="ch05.gradient_np.hint"),
        Case("ch05.gradient_np.line", lambda f: _mia_np(f, [10, 0, 0], -60), ([-94, 6.25, -2.75], 2.5), tolerance=1e-9, hint="ch05.gradient_np.hint"),
        Case("ch05.gradient_np.close", lambda f: _mia_np(f, [12, -8, 4], -105), ([90.5, 1.5, 0.75], 3.5), tolerance=1e-9, hint="ch05.gradient_np.hint"),
    ],
}
