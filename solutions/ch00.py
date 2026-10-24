"""Reference solutions for chapter 00. Peek only after trying!"""


def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def total(numbers):
    result = 0
    for n in numbers:
        result = result + n
    return result


def average(numbers):
    return total(numbers) / len(numbers)
