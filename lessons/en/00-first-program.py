import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="00 · Your first program")

with app.setup(hide_code=True):
    import marimo as mo

    from learn_llm import todo
    from learn_llm.checks import check

    LOCALE = "en"


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 00 · Your first program

    Welcome! By the end of this course you will have built your own language model, the
    kind of program behind chatbots, from the ground up. Every piece starts here, with a few
    lines of Python.

    You don't need to know anything yet. When a new idea is needed, this page explains it
    right where you need it.

    ## How this page works

    This page is a **notebook**. It is made of **cells**. Some cells hold text, like this one.
    Others hold Python code, with the code's result shown just below.

    - To **run** a code cell, click inside it and press **Shift + Enter**, or click the ▶ button
      next to it.
    - When you run a cell you changed, every cell that depends on it **re-runs by itself**. You
      never have to remember what else to re-run.
    - Your changes are saved automatically, in your own copy of the lesson. You can't break
      the course; experiment freely.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Python as a calculator

    The cell below holds a tiny Python program: `2 + 3`. Its result appears under it.
    Change the numbers and run it again.
    """)
    return


@app.cell
def _():
    2 + 3
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Python knows the usual arithmetic. Some symbols differ from what you write on paper:

    | You write | Python writes | Example | Result |
    |---|---|---|---|
    | 7 × 6 | `7 * 6` | multiply | `42` |
    | 10 ÷ 4 | `10 / 4` | divide | `2.5` |
    | 2¹⁰ | `2 ** 10` | power | `1024` |

    Try a few in the cell below. Parentheses work as in maths: `(1 + 2) * 3` is `9`.
    """)
    return


@app.cell
def _():
    7 * 6
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Giving values a name

    Typing the same number again and again gets tiring. You can give a value a **name**,
    then use the name instead. A name with a value is called a **variable**.

    `price = 12` means "from now on, `price` stands for 12". The `=` here means *store*,
    not *equals*.
    """)
    return


@app.cell
def _():
    price = 12
    count = 3
    return count, price


@app.cell
def _(count, price):
    price * count
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Change `price` to `15` in the cell above the result and press **Shift + Enter**. The result
    updates by itself, because it uses `price`.

    /// note | One rule of this notebook
    Each name is given its value in **one** cell only. If you write `price = 20` in a second
    cell, the notebook tells you the name is already taken. Pick a new name, such as
    `new_price`, or edit the original cell.
    ///
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Functions: a recipe with a name

    A **function** is a small recipe. You give it some input, it follows the steps, and it
    gives back an answer. Here is a function that doubles a number:

    ```python
    def double(x):
        return x * 2
    ```

    Reading it line by line:

    - `def double(x):` says "I'm defining a recipe called `double`. Its input will be called `x`."
    - The next line is pushed to the right (**indented**) with four spaces. That's how Python
      knows the line belongs to the recipe.
    - `return x * 2` says "the answer is `x * 2`". `return` **gives the answer back** to
      whoever used the function.

    Using a function is called **calling** it: `double(5)` runs the recipe with `x = 5`.
    """)
    return


@app.function
def double(x):
    return x * 2


@app.cell
def _():
    double(5)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Exercise 1: Celsius to Fahrenheit

    Your turn. Most of the world measures temperature in degrees Celsius (°C), but the US
    uses Fahrenheit (°F). The rule to convert is:

    > multiply the Celsius temperature by 9, divide by 5, then add 32.

    Write the function `to_fahrenheit` in the cell below. Replace the `todo()` line with
    a `return` line that does the conversion. Press **Shift + Enter** to run your code; the checks
    under it update every time you do.
    """)
    return


@app.function
def to_fahrenheit(celsius):
    # ← replace todo() below with your code
    todo()


@app.cell
def _():
    check("00", "to_fahrenheit", to_fahrenheit, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    temperature = mo.ui.slider(-40, 100, value=20, label="Celsius", show_value=True)
    return (temperature,)


@app.cell(hide_code=True)
def _(temperature):
    try:
        _answer = f"**{temperature.value} °C = {to_fahrenheit(temperature.value):g} °F**"
    except Exception:
        _answer = "*Finish Exercise 1, then drag the slider to try your function.*"
    mo.hstack([temperature, mo.md(_answer)], justify="start", gap=2)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Many values at once: lists

    A **list** holds several values in order, between square brackets:
    `[3, 1, 4, 1, 5]`. Later in this course, lists of numbers become pictures, words and
    entire books. Python can tell you how long a list is with `len`:
    """)
    return


@app.cell
def _():
    scores = [3, 1, 4, 1, 5]
    len(scores)
    return (scores,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Doing something for each value: loops

    A **loop** repeats steps once for every value in a list. This loop counts how many
    scores are bigger than 2:

    ```python
    for s in scores:
        ...
    ```

    means "take each value of `scores` in turn, call it `s`, and run the indented lines".
    """)
    return


@app.cell
def _(scores):
    _big = 0
    for _s in scores:
        if _s > 2:
            _big = _big + 1
    _big
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `_big = _big + 1` looks odd as maths, but remember `=` means *store*: "work out
    `_big + 1`, then store it back in `_big`". So `_big` grows by one each time. (A name
    starting with `_` belongs to its own cell only, so other cells can reuse it.)

    ## Exercise 2: add up a list

    Write `total(numbers)`, which gives back the sum of all the numbers in the list.

    Hint: start a running total at `0`, loop over the numbers, add each one to the running
    total, and `return` it after the loop. Careful with indentation: `return` goes
    **after** the loop, not inside it.
    """)
    return


@app.function
def total(numbers):
    # ← replace todo() below with your code
    todo()


@app.cell
def _():
    check("00", "total", total, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Exercise 3: the average

    /// admonition | 🧰 Toolbox: the average (mean)
    The **average** of some numbers, also called the **mean**, is their total divided by
    how many there are. The average of 2, 4 and 9 is (2 + 4 + 9) ÷ 3 = 5.
    You'll use the mean all the time in the next chapter.
    ///

    Write `average(numbers)`. You've already done the hard part: a function can call another
    function, so use your `total` and Python's `len`.
    """)
    return


@app.function
def average(numbers):
    # ← replace todo() below with your code
    todo()


@app.cell
def _():
    check("00", "average", average, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## What you can do now

    - run Python code and read its result
    - store values in variables
    - write functions that take inputs and `return` an answer
    - hold many values in a list and loop over them

    That is enough to start teaching a computer. In **Chapter 01** you'll use exactly these
    tools to make a program learn a pattern from data, then predict numbers it has
    never seen.

    ---

    <!-- go-deeper -->
    **Go deeper (optional, not needed for the course):** the official
    [Python tutorial](https://docs.python.org/3/tutorial/) covers these ideas in more detail.
    """)
    return


if __name__ == "__main__":
    app.run()
