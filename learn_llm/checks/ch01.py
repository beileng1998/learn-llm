from learn_llm.checking import Case

TEMPS = [14, 17, 20, 22, 25, 28, 31, 33]
SALES = [63, 90, 137, 148, 193, 234, 257, 288]

EXERCISES = {
    "predict": [
        Case("ch01.predict.simple", lambda f: f(2, 1, 3), 7),
        Case("ch01.predict.mia", lambda f: f(12, -110, 25), 190),
        Case("ch01.predict.flat", lambda f: f(0, 5, 100), 5),
        Case("ch01.predict.order", lambda f: f(3, 10, 0), 10),
    ],
    "squared_error": [
        Case("ch01.squared_error.over", lambda f: f(10, 7), 9, hint="ch01.squared_error.hint"),
        Case("ch01.squared_error.under", lambda f: f(7, 10), 9),
        Case("ch01.squared_error.exact", lambda f: f(5, 5), 0),
        Case("ch01.squared_error.big", lambda f: f(20, 10), 100),
    ],
    "mse": [
        Case("ch01.mse.tiny", lambda f: f(1, 0, [1, 2], [2, 4]), 2.5, tolerance=1e-9, hint="ch01.mse.hint"),
        Case("ch01.mse.perfect", lambda f: f(2, 1, [0, 1, 2], [1, 3, 5]), 0, tolerance=1e-9, hint="ch01.mse.hint"),
        Case("ch01.mse.mia", lambda f: f(10, -60, TEMPS, SALES), 177.5, tolerance=1e-9, hint="ch01.mse.hint"),
    ],
}
