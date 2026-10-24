from learn_llm.checking import Case

EXERCISES = {
    "to_fahrenheit": [
        Case("ch00.to_fahrenheit.freezing", lambda f: f(0), 32),
        Case("ch00.to_fahrenheit.boiling", lambda f: f(100), 212),
        Case("ch00.to_fahrenheit.negative", lambda f: f(-40), -40),
        Case("ch00.to_fahrenheit.body", lambda f: f(37), 98.6, tolerance=1e-9),
    ],
    "total": [
        Case("ch00.total.small", lambda f: f([1, 2, 3]), 6),
        Case("ch00.total.single", lambda f: f([5]), 5),
        Case("ch00.total.empty", lambda f: f([]), 0),
        Case("ch00.total.negative", lambda f: f([4, -1, -2]), 1),
    ],
    "average": [
        Case("ch00.average.small", lambda f: f([1, 2, 3]), 2),
        Case("ch00.average.fraction", lambda f: f([1, 2]), 1.5, tolerance=1e-9),
        Case("ch00.average.single", lambda f: f([7]), 7),
    ],
}
