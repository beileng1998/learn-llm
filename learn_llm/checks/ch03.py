from learn_llm.checking import Case

TEMPS = [14, 17, 20, 22, 25, 28, 31, 33]
SALES = [63, 90, 137, 148, 193, 234, 257, 288]

EXERCISES = {
    "day_slopes": [
        Case("ch03.day_slopes.day1", lambda f: f(10, -60, 14, 63), (476, 34), tolerance=1e-9, hint="ch03.day_slopes.hint"),
        Case("ch03.day_slopes.day3", lambda f: f(10, -60, 20, 137), (120, 6), tolerance=1e-9, hint="ch03.day_slopes.hint"),
        Case("ch03.day_slopes.perfect", lambda f: f(2, 1, 3, 7), (0, 0), tolerance=1e-9, hint="ch03.day_slopes.hint"),
        Case("ch03.day_slopes.small", lambda f: f(1, 0, 2, 0), (8, 4), tolerance=1e-9, hint="ch03.day_slopes.hint"),
    ],
    "gradient": [
        Case("ch03.gradient.tiny", lambda f: f(1, 0, [1, 2], [2, 4]), (-5, -3), tolerance=1e-9, hint="ch03.gradient.hint"),
        Case("ch03.gradient.mia", lambda f: f(10, -60, TEMPS, SALES), (-94, 2.5), tolerance=1e-9, hint="ch03.gradient.hint"),
        Case("ch03.gradient.perfect", lambda f: f(2, 1, [0, 1, 2], [1, 3, 5]), (0, 0), tolerance=1e-9, hint="ch03.gradient.hint"),
    ],
    "fit": [
        Case("ch03.fit.none", lambda f: f(0, 0, [0, 1], [1, 3], 0.1, 0), (0, 0), tolerance=1e-12, hint="ch03.fit.hint"),
        Case("ch03.fit.line", lambda f: f(0, 0, [0, 1, 2], [1, 3, 5], 0.1, 2000), (2, 1), tolerance=1e-3, hint="ch03.fit.hint"),
    ],
}
