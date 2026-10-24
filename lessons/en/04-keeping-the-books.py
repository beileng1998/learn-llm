import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="04 · Keeping the books")

with app.setup(hide_code=True):
    import marimo as mo

    from learn_llm import todo
    from learn_llm.checks import check
    from learn_llm.diagrams import one_day
    from learn_llm.plot import chart

    LOCALE = "en"
    temps = [14, 17, 20, 22, 25, 28, 31, 33]
    sales = [63, 90, 137, 148, 193, 234, 257, 288]


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 04 · Keeping the books

    In chapter 03 you worked out the backward steps for Mia's line by hand, then wrote them as
    code in `day_slopes`. That works, but only for that one recipe. Change the recipe (a curve
    instead of a line, a neural network) and you'd have to work out every backward step by hand
    again.

    In this chapter you'll build a small **engine** that does it for you. While a calculation
    runs, the engine writes down every step in a book, like a shopkeeper keeping the books. Then
    it reads the book backwards and hands out the blame by itself, using exactly the rules from
    chapter 03.

    ## What the engine has to do

    Recall the rule from chapter 03. Every box gets a blame (how much the loss moves per unit
    this box moves, for a tiny nudge), and walking backwards:

    > blame of a box = the sum, over every arrow leaving it, of
    > (local slope of that arrow × blame of the box the arrow points to)

    So for every box, the engine must remember three things: its **value**, the boxes it was
    **made from**, and the **local slope** towards each of them. That calls for a new kind of
    Python value.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A new kind of value: classes

    So far you've used numbers, lists and functions. Python lets you invent your own kind of
    value, with named slots for whatever it needs to remember. The recipe for a new kind of value
    is called a **class**. Here is ours:
    """)
    return


@app.class_definition
class Value:
    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.parents = []
        self.local_slopes = []


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Line by line:

    - `class Value:` says "here is the recipe for a new kind of value, called `Value`".
    - `def __init__(self, data):` is the setup function Python runs every time you make a new
      `Value`. The name `__init__` (two underscores on each side, short for *initialise*) is fixed
      by Python. `self` stands for the new value being set up; `data` is the number you give it.
    - `self.data = data` stores the number in a slot called `data`, inside this value. A slot like
      this is called an **attribute**.
    - `self.grad = 0` starts its blame at 0. ("grad" is short for gradient: the blame from
      chapter 03. It starts at 0 because blame is collected later, by adding.)
    - `self.parents = []` and `self.local_slopes = []` start as empty lists: the boxes this one
      was made from, and the local slope towards each, filled in later.

    Making one looks like calling a function. (As in chapter 03, several values separated by
    commas on the last line show up as a numbered list of items, counting from 0.) A dot reads a slot: `v.data` means "the `data`
    slot of `v`".
    """)
    return


@app.cell
def _():
    v = Value(3)
    v.data, v.grad, v.parents
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    You can also store into a slot with the dot: `v.grad = 5` would replace its blame with 5.

    ## The book

    The book is an ordinary list. Every time the engine does one step, it adds the result to the
    end of the book. Lists have a built-in way to do that: `book.append(x)` adds `x` to the end
    of `book`. (The dot again: `append` is a function that belongs to every list.)
    """)
    return


@app.cell
def _():
    shelf = []
    shelf.append(5)
    shelf.append(8)
    shelf
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## One step: multiply

    Here is how the engine multiplies two values. It works out the result like normal maths,
    then fills in the result's memory and writes it in the book:
    """)
    return


@app.function
def mul(a, b, book):
    out = Value(a.data * b.data)
    out.parents = [a, b]
    out.local_slopes = [b.data, a.data]
    book.append(out)
    return out


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    - `out = Value(a.data * b.data)`: a new box holding the product of the two values.
    - `out.parents = [a, b]`: it was made from `a` and `b`.
    - `out.local_slopes = [b.data, a.data]`: the local slopes from chapter 03. In `a × b`, nudging
      `a` moves the result by `b` per unit, and nudging `b` moves it by `a` per unit. The order
      matches `parents`: the first slope goes with the first parent.
    - `book.append(out)`: write the step in the book.
    - `return out`: hand back the new box, so it can be used in the next step.

    Try it:
    """)
    return


@app.cell
def _():
    shop_book = []
    x = Value(3)
    y = Value(4)
    z = mul(x, y, shop_book)
    z.data, z.local_slopes, len(shop_book)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `z` holds 12; its local slopes are 4 (towards `x`) and 3 (towards `y`); the book has one entry.

    ## Exercise 1: add

    Write `add(a, b, book)` the same way. Think first: in `a + b`, if `a` gets a tiny nudge, how
    much does the result move per unit? And for `b`? (Chapter 03's table has the answer.)
    """)
    return


@app.function
def add(a, b, book):
    # ← replace todo() below with your code
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "add", add, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Exercise 2: subtract

    Write `sub(a, b, book)` for `a - b`. Careful with the second local slope: if `b` grows by a
    tiny `h`, the result `a - b` **shrinks** by `h`. So per unit of `b`, the result moves by `-1`.
    """)
    return


@app.function
def sub(a, b, book):
    # ← replace todo() below with your code
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "sub", sub, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Exercise 3: square

    Write `square(a, book)` for `a × a`. It has only **one** parent, `a` (so `out.parents = [a]`),
    and one local slope: chapter 02's slope of `x × x`, which is `2 × x`. Here `x` is `a.data`.
    """)
    return


@app.function
def square(a, book):
    # ← replace todo() below with your code
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "square", square, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Reading the book backwards

    Now the heart of the engine. After the calculation, the book lists every step in the order it
    happened, and the last entry is the loss. To hand out blame:

    1. The loss blames itself 1: `loss.grad = 1`.
    2. Go through the book **from the last entry to the first**. For each entry, pass blame to each
       of its parents: add (local slope × this entry's blame) to the parent's blame.

    We **add** to the parent's blame because blames add up when a box feeds several arrows
    (chapter 03): each arrow out of a box brings its own share.

    Why from last to first? A box is always written in the book **after** the boxes it was made
    from: it can't be worked out before them. So when we read backwards, we reach every box that
    *uses* a value before we reach the value itself. By the time we get to a box, all its users
    have already passed their share of blame to it: its blame is complete, and it's safe to pass
    it on.

    Here is what goes wrong in the other order. Take `x × x + x` at `x = 3`. Its slope is
    `2 × 3 + 1 = 7` (slope of `x × x` plus slope of `x`). The cell below records it, then reads the
    book **front to back** instead:
    """)
    return


@app.cell
def _():
    wrong_book = []
    x3 = Value(3)
    product = mul(x3, x3, wrong_book)
    total3 = add(product, x3, wrong_book)

    total3.grad = 1
    for entry in wrong_book:  # front to back: the wrong order
        for parent, slope in zip(entry.parents, entry.local_slopes):
            parent.grad = parent.grad + slope * entry.grad
    x3.grad
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    (If this cell shows an error, finish Exercise 1 first: it uses your `add`.)

    It says `1`, not `7`. Front to back, the multiplication was handled **first**, while the
    product's blame was still 0 (the addition hadn't passed any blame to it yet). So `x` got
    `3 × 0 + 3 × 0` from the multiplication, and only `1` from the addition. Reading backwards
    fixes exactly this.

    To go through a list from last to first, Python has `reversed`: `for entry in reversed(book):`.

    ## Exercise 4: backward

    Write `backward(loss, book)`:

    1. `loss.grad = 1`
    2. `for entry in reversed(book):`, and inside it,
       `for parent, slope in zip(entry.parents, entry.local_slopes):`, and inside that,
       `parent.grad = parent.grad + slope * entry.grad`

    It doesn't need to `return` anything: the blames are stored in the boxes themselves.
    """)
    return


@app.function
def backward(loss, book):
    # ← replace todo() below with your code
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "backward", backward, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mia's first day, through the engine

    Here is chapter 03's day 1 again (`t = 14`, `s = 63`, knobs `w = 10`, `b = -60`), this time
    written with your engine. Nobody tells it the backward steps:
    """)
    return


@app.cell
def _():
    day_book = []
    w = Value(10)
    b = Value(-60)
    t = Value(14)
    s = Value(63)
    p = mul(w, t, day_book)
    g = add(p, b, day_book)
    e = sub(g, s, day_book)
    L = square(e, day_book)
    backward(L, day_book)
    w.grad, b.grad
    return L, b, e, g, p, s, t, w


@app.cell(hide_code=True)
def _(L, b, e, g, p, s, t, w):
    one_day({"w": w.data, "t": t.data, "p": p.data, "b": b.data, "g": g.data, "s": s.data, "e": e.data, "L": L.data},
            {n: f"blame {v.grad:g}" for n, v in (("w", w), ("p", p), ("b", b), ("g", g), ("e", e), ("L", L))})
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    476 for `w` and 34 for `b`: the same numbers you found by hand in chapter 03, and every box
    in the picture got its blame. (If you see an error instead, the exercises above aren't all
    passing yet.) The data boxes `t` and `s` were made with `Value` too, so they collect blame as
    well; it's simply never used, because we can't change the data.

    ## Exercise 5: the gradient of the whole loss

    Write `engine_gradient(w_num, b_num, xs, ys)`: the slopes of Mia's **mean** loss for both
    knobs, computed entirely by the engine. It's chapter 03's `gradient`, but you only write the
    forward calculation:

    1. `book = []`, then the knobs as values: `w = Value(w_num)` and `b = Value(b_num)`.
    2. A running total that is itself a value: `total = Value(0)`.
    3. Loop with `for x, y in zip(xs, ys):`. Inside: `guess = add(mul(w, Value(x), book), b, book)`,
       then `e = sub(guess, Value(y), book)`, then `total = add(total, square(e, book), book)`.
    4. After the loop, the mean is the total times `1 / len(xs)`:
       `mean = mul(total, Value(1 / len(xs)), book)`.
    5. `backward(mean, book)`, then `return w.grad, b.grad`.
    """)
    return


@app.function
def engine_gradient(w_num, b_num, xs, ys):
    # ← replace todo() below with your code
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "engine_gradient", engine_gradient, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    At `w = 10`, `b = -60` it gives `(-94, 2.5)`, exactly chapter 03's hand-built gradient.

    ## Fresh boxes every time

    One trap. Because `backward` **adds** to each blame, running it twice on the same boxes adds
    the blame twice. The cell below records day 1 once, then reads the book backwards twice:
    """)
    return


@app.cell
def _():
    twice_book = []
    w2 = Value(10)
    loss2 = square(sub(add(mul(w2, Value(14), twice_book), Value(-60), twice_book), Value(63), twice_book), twice_book)
    backward(loss2, twice_book)
    first = w2.grad
    backward(loss2, twice_book)
    first, w2.grad
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The second time, `w`'s blame is 2380, five times 476. On the second pass every box still
    holds its blame from the first pass, and the new shares are added on top of it, box after box
    down the book, so the error grows at every step. That's why `engine_gradient` makes **fresh** `Value` boxes, with a fresh book, every
    time it's called: every blame starts at 0. (Real deep-learning tools have the same rule;
    you'll meet it again with PyTorch.)

    ## The payoff: a new recipe, no new backward steps

    Mia kept selling through a heatwave. Above about 33 °C, sales started to **drop**: it's too hot
    to go out. Here are all 11 days:
    """)
    return


@app.cell(hide_code=True)
def _():
    hot_temps = temps + [35, 37, 39]
    hot_sales = sales + [280, 262, 236]
    mo.md(f"`temps` = {hot_temps}  \n`sales` = {hot_sales}")
    return hot_sales, hot_temps


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    A straight line can't go up and then come down. A **curve** can:

    > guess = a × x × x + w × x + b

    with three knobs `a`, `w` and `b`. With `a` negative, the curve bends downwards, like a hill.

    One practical detail: here `x` is the temperature measured **from 25 °C, in tens of degrees**:
    `x = (t - 25) / 10`, so 14 °C becomes -1.1 and 39 °C becomes 1.4. In chapter 02 you saw `b`
    crawl because the loss reacted far more strongly to `w` than to `b`. With raw temperatures,
    `x × x` would be in the hundreds and `a` would make that imbalance much worse. Small numbers
    around 0 keep the three knobs on a similar footing, so one learning rate suits all of them.

    For a curve, chapter 03 would have meant working out new backward steps by hand. With your
    engine, you only write the forward recipe. Press the button to fit the curve with 500 steps of
    gradient descent, every gradient computed by your engine:
    """)
    return


@app.cell(hide_code=True)
def _():
    fit_curve = mo.ui.run_button(label="Fit the curve")
    fit_curve
    return (fit_curve,)


@app.cell(hide_code=True)
def _(fit_curve, hot_sales, hot_temps):
    mo.stop(not fit_curve.value, mo.md("*Press **Fit the curve** to start.*"))
    try:
        _xs = [(t - 25) / 10 for t in hot_temps]
        _knobs = [0.0, 0.0, 0.0]
        for _i in range(500):
            _book = []
            _a, _w, _b = Value(_knobs[0]), Value(_knobs[1]), Value(_knobs[2])
            _total = Value(0)
            for _x, _y in zip(_xs, hot_sales):
                _xv = Value(_x)
                _guess = add(add(mul(_a, square(_xv, _book), _book), mul(_w, _xv, _book), _book), _b, _book)
                _total = add(_total, square(sub(_guess, Value(_y), _book), _book), _book)
            _mean = mul(_total, Value(1 / len(_xs)), _book)
            backward(_mean, _book)
            _knobs = [k - 0.1 * v.grad for k, v in zip(_knobs, (_a, _w, _b))]
        _ka, _kw, _kb = _knobs
        _curve = [(t, _ka * ((t - 25) / 10) ** 2 + _kw * (t - 25) / 10 + _kb) for t in range(12, 42)]
        _out = mo.vstack([
            chart((10, 42), (0, 320), "temperature (°C)", "ice creams sold",
                  dots=list(zip(hot_temps, hot_sales)), curve=_curve),
            mo.md(f"a = **{_ka:.1f}**, w = **{_kw:.1f}**, b = **{_kb:.1f}**, loss = **{_mean.data:,.1f}**. "
                  f"(The best possible straight line on these 11 days has loss about 810.)"),
        ])
    except Exception:
        _out = mo.md("*Finish Exercises 1 to 4 to fit the curve.*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The curve rises with the temperature and then turns down in the heatwave, and its loss is far
    lower than any straight line's. You never worked out a backward step for it: the engine kept
    the books and did it.

    ## What's next

    Your engine handles one number at a time: every multiplication is its own box in the book.
    Real models work with thousands or millions of numbers at once, and a book entry per number
    would be far too slow. In **Chapter 05** you'll learn to work with whole lists of numbers in
    one go (vectors and matrices), and then teach the same backward rules to them.

    ## What you can do now

    - define a class with `__init__`, and read and store attributes with a dot
    - add to a list with `append`, and walk it backwards with `reversed`
    - build an engine that records a calculation and backpropagates through it automatically
    - explain why the book must be read backwards, and why each calculation needs fresh boxes
    - fit a new model by writing only its forward recipe

    ---

    <!-- go-deeper -->
    **Go deeper (optional):** this kind of engine is called *automatic differentiation* (reverse
    mode), or *autograd*. The order we get from the book is a *topological order*.
    """)
    return


if __name__ == "__main__":
    app.run()
