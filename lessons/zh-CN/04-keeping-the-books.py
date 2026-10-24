import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="04 · 记账")

with app.setup(hide_code=True):
    import marimo as mo

    from learn_llm import todo
    from learn_llm.checks import check
    from learn_llm.diagrams import one_day
    from learn_llm.plot import chart

    LOCALE = "zh-CN"
    temps = [14, 17, 20, 22, 25, 28, 31, 33]
    sales = [63, 90, 137, 148, 193, 234, 257, 288]


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 04 · 记账

    第 03 章里，你手工推出了米娅那条直线的往回步骤，再把它们写成 `day_slopes` 里的代码。这样行得通，但只适用于那一个算式。
    算式一变（曲线代替直线、神经网络），每一步往回的计算都得重新手工推一遍。

    这一章，你会做一个小**引擎**来替你干这件事。计算进行时，引擎把每一步都记进一本账，就像店主记账一样。
    算完后，它把账本倒着读一遍，自己把责任分下去，用的正是第 03 章的规则。

    ## 引擎要做什么

    回忆第 03 章的规则。每个框都有一个责任（这个框每移动 1 单位，损失移动多少，指微小轻推时的比率），倒着走时：

    > 一个框的责任 = 对从它出发的每一条箭头，求
    > （这条箭头的局部斜率 × 箭头所指那个框的责任），再全部加起来

    所以对每个框，引擎都要记住三样东西：它的**值**、它是由哪些框**算出来的**，以及通往每个来源的**局部斜率**。
    这需要一种新的 Python 值。
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 一种新的值：类

    到目前为止，你用过数字、列表和函数。Python 允许你发明自己的一种值，里面带着有名字的格子，用来存它需要记住的东西。
    制造一种新值的配方叫作**类**（class）。这是我们的类：
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
    逐行来看：

    - `class Value:` 表示“这是一种叫 `Value` 的新值的配方”。
    - `def __init__(self, data):` 是每次新做一个 `Value` 时 Python 都会运行的准备函数。`__init__` 这个名字
      （两边各两个下划线，是 *initialise*，即“初始化”的缩写）是 Python 规定的。`self` 代表正在准备的这个新值；`data` 是你交给它的数。
    - `self.data = data` 把这个数存进这个值内部一个叫 `data` 的格子。这种格子叫作**属性**（attribute）。
    - `self.grad = 0` 让它的责任从 0 开始。（“grad”是 gradient，即梯度的缩写，也就是第 03 章的责任。从 0 开始，是因为责任要在之后一点点加上去。）
    - `self.parents = []` 和 `self.local_slopes = []` 先是空列表：这个框由哪些框算出来，以及通往每个来源的局部斜率，之后再填。

    做一个新值的写法和调用函数一样。（和第 03 章一样，最后一行用逗号隔开的几个值，会显示成从 0 开始编号的列表。）用点号读取格子：`v.data` 的意思是“`v` 的 `data` 格子”。
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
    也可以用点号往格子里存东西：`v.grad = 5` 会把它的责任换成 5。

    ## 账本

    账本就是一个普通的列表。引擎每做一步，就把结果加到账本末尾。列表自带一种做法：`book.append(x)` 把 `x` 加到 `book` 的末尾。
    （又是点号：`append` 是每个列表都带着的一个函数。）
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
    ## 一步：乘法

    引擎是这样把两个值相乘的。它先像平常的数学那样算出结果，再把结果需要记住的东西填好，记进账本：
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
    - `out = Value(a.data * b.data)`：一个新框，装着两个值的乘积。
    - `out.parents = [a, b]`：它是由 `a` 和 `b` 算出来的。
    - `out.local_slopes = [b.data, a.data]`：第 03 章的局部斜率。在 `a × b` 里，轻推 `a`，结果每单位移动 `b`；
      轻推 `b`，结果每单位移动 `a`。顺序和 `parents` 对应：第一个斜率配第一个来源。
    - `book.append(out)`：把这一步记进账本。
    - `return out`：把新框交回去，好让下一步用它。

    试试看：
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
    `z` 装着 12；它的局部斜率是 4（通往 `x`）和 3（通往 `y`）；账本里有一条记录。

    ## 练习 1：加法

    照同样的方式写出 `add(a, b, book)`。先想一想：在 `a + b` 里，`a` 被轻推一点点，结果每单位移动多少？`b` 呢？
    （第 03 章的表格里有答案。）写代码时记得用英文输入法。
    """)
    return


@app.function
def add(a, b, book):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "add", add, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 练习 2：减法

    写出 `sub(a, b, book)`，对应 `a - b`。注意第二个局部斜率：如果 `b` 增加一个很小的 `h`，结果 `a - b` 就**减少** `h`。
    所以 `b` 每增加 1 单位，结果移动 `-1`。
    """)
    return


@app.function
def sub(a, b, book):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "sub", sub, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 练习 3：平方

    写出 `square(a, book)`，对应 `a × a`。它只有**一个**来源 `a`（所以 `out.parents = [a]`），只有一个局部斜率：
    第 02 章 `x × x` 的斜率，也就是 `2 × x`。这里的 `x` 就是 `a.data`。
    """)
    return


@app.function
def square(a, book):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "square", square, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 倒着读账本

    现在是引擎的核心。计算结束后，账本按发生的顺序列出了每一步，最后一条就是损失。分配责任的方法是：

    1. 损失对自己的责任是 1：`loss.grad = 1`。
    2. **从最后一条到第一条**过一遍账本。对每一条记录，把责任传给它的每个来源：把（局部斜率 × 这条记录的责任）加到来源的责任上。

    之所以是把责任**加**上去，是因为一个框连到好几条箭头时，责任要加起来（第 03 章）：从这个框出发的每条箭头都会带回自己那一份。

    为什么要从后往前？一个框总是在它的来源**之后**才被记进账本：来源没算出来，它就没法算。所以倒着读时，
    我们总是先遇到所有*用到*某个值的框，然后才遇到这个值本身。等走到一个框时，所有用到它的框都已经把自己那份责任传给了它：
    它的责任已经齐了，可以放心往下传。

    看看顺序反了会出什么错。取 `x × x + x`，`x = 3`。它的斜率是 `2 × 3 + 1 = 7`（`x × x` 的斜率加上 `x` 的斜率）。
    下面的单元格把它记下来，然后**从前往后**读账本：
    """)
    return


@app.cell
def _():
    wrong_book = []
    x3 = Value(3)
    product = mul(x3, x3, wrong_book)
    total3 = add(product, x3, wrong_book)

    total3.grad = 1
    for entry in wrong_book:  # 从前往后：错误的顺序
        for parent, slope in zip(entry.parents, entry.local_slopes):
            parent.grad = parent.grad + slope * entry.grad
    x3.grad
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    （如果这个单元格报错，先完成练习 1：它用到了你的 `add`。）

    结果是 `1`，不是 `7`。从前往后读时，乘法被**先**处理了，而那时乘积的责任还是 0（加法还没把责任传给它）。
    所以 `x` 从乘法那里只得到 `3 × 0 + 3 × 0`，只从加法那里得到 `1`。倒着读正好解决这个问题。

    要从最后一条到第一条遍历一个列表，Python 有 `reversed`：`for entry in reversed(book):`。

    ## 练习 4：反向传播

    写出 `backward(loss, book)`：

    1. `loss.grad = 1`
    2. `for entry in reversed(book):`，在它里面写
       `for parent, slope in zip(entry.parents, entry.local_slopes):`，再在里面写
       `parent.grad = parent.grad + slope * entry.grad`

    它不需要 `return` 任何东西：责任已经存在各个框里了。
    """)
    return


@app.function
def backward(loss, book):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "backward", backward, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 用引擎算米娅的第一天

    这又是第 03 章的第 1 天（`t = 14`，`s = 63`，旋钮 `w = 10`，`b = -60`），这次用你的引擎来写。没人告诉它往回的步骤：
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
            {n: f"责任 {v.grad:g}" for n, v in (("w", w), ("p", p), ("b", b), ("g", g), ("e", e), ("L", L))})
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `w` 是 476，`b` 是 34：和你在第 03 章手工算出的一样，图里每个框都拿到了自己的责任。（如果你看到的是报错，说明上面的练习还没全部通过。）
    数据框 `t` 和 `s` 也是用 `Value` 做的，所以它们也会收到责任；只是这些责任从来用不上，因为数据我们改不了。

    ## 练习 5：整个损失的梯度

    写出 `engine_gradient(w_num, b_num, xs, ys)`：米娅**平均**损失对两个旋钮的斜率，全部由引擎算出。它就是第 03 章的 `gradient`，
    只不过你只需要写往前的计算：

    1. `book = []`，然后把旋钮做成值：`w = Value(w_num)` 和 `b = Value(b_num)`。
    2. 一个本身也是值的累计值：`total = Value(0)`。
    3. 用 `for x, y in zip(xs, ys):` 循环。在里面：`guess = add(mul(w, Value(x), book), b, book)`，
       然后 `e = sub(guess, Value(y), book)`，然后 `total = add(total, square(e, book), book)`。
    4. 循环结束后，平均值就是总和乘以 `1 / len(xs)`：
       `mean = mul(total, Value(1 / len(xs)), book)`。
    5. `backward(mean, book)`，然后 `return w.grad, b.grad`。
    """)
    return


@app.function
def engine_gradient(w_num, b_num, xs, ys):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("04", "engine_gradient", engine_gradient, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    在 `w = 10`、`b = -60` 处，它给出 `(-94, 2.5)`，和第 03 章手工搭出来的梯度一模一样。

    ## 每次都用新盒子

    有一个陷阱。因为 `backward` 是把责任**加**上去的，所以对同一批框运行两次，责任就会加两遍。
    下面的单元格把第 1 天记一次账，然后倒着读两遍：
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
    第二次，`w` 的责任变成了 2380，是 476 的五倍。第二遍时，每个框里还留着第一遍的责任，新的那一份又加在上面，
    一个框接一个框地往账本后面传，所以误差在每一步都在变大。这就是为什么 `engine_gradient` 每次调用都要做**新的** `Value` 盒子、
    用一本新账本：所有责任都从 0 开始。（真正的深度学习工具也有同样的规则；学到 PyTorch 时你还会再遇到它。）

    ## 回报：新算式，不用新的往回步骤

    热浪来了，米娅还在卖。气温超过大约 33 °C 后，销量开始**下降**：太热了，大家都不出门。下面是全部 11 天：
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
    直线没法先上升再下降。**曲线**可以：

    > 猜测 = a × x × x + w × x + b

    有三个旋钮 `a`、`w` 和 `b`。`a` 为负数时，曲线向下弯，像一座小山。

    一个实际的细节：这里的 `x` 是**从 25 °C 算起、以 10 度为单位**的气温：`x = (t - 25) / 10`，所以 14 °C 变成 -1.1，39 °C 变成 1.4。
    第 02 章里你看到过 `b` 挪得很慢，因为损失对 `w` 的反应比对 `b` 强烈得多。如果用原始气温，`x × x` 会是几百那么大，
    `a` 会让这种不平衡严重得多。用 0 附近的小数，三个旋钮的地位就差不多，一个学习率就能适合所有旋钮。

    换成曲线的话，按第 03 章的做法就得手工推一套新的往回步骤。有了你的引擎，你只需要写往前的算式。
    按下按钮，用 500 步梯度下降拟合这条曲线，每一步的梯度都由你的引擎算出：
    """)
    return


@app.cell(hide_code=True)
def _():
    fit_curve = mo.ui.run_button(label="拟合曲线")
    fit_curve
    return (fit_curve,)


@app.cell(hide_code=True)
def _(fit_curve, hot_sales, hot_temps):
    mo.stop(not fit_curve.value, mo.md("*按**拟合曲线**开始。*"))
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
            chart((10, 42), (0, 320), "气温（°C）", "卖出的冰淇淋（个）",
                  dots=list(zip(hot_temps, hot_sales)), curve=_curve),
            mo.md(f"a = **{_ka:.1f}**，w = **{_kw:.1f}**，b = **{_kb:.1f}**，损失 = **{_mean.data:,.1f}**。"
                  f"（在这 11 天上，最好的直线损失大约是 810。）"),
        ])
    except Exception:
        _out = mo.md("*完成练习 1 到 4 后才能拟合曲线。*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    曲线随着气温上升，到了热浪里又往下拐，损失也比任何直线都低得多。你没有为它推过一步往回的计算：引擎记了账，替你做完了。

    ## 下一步

    你的引擎一次处理一个数：每次乘法都是账本里的一个框。真正的模型要同时处理成千上万甚至几百万个数，每个数记一笔账就太慢了。
    在**第 05 章**里，你会学着一次处理整串的数（向量和矩阵），再把同样的往回规则教给它们。

    ## 你现在会做的事

    - 定义一个带 `__init__` 的类，用点号读取和存入属性
    - 用 `append` 往列表里添加东西，用 `reversed` 倒着遍历
    - 做一个能记下计算过程、并自动做反向传播的引擎
    - 说清楚为什么账本必须倒着读，以及为什么每次计算都要用新盒子
    - 只写往前的算式，就能拟合一个新模型

    ---

    <!-- go-deeper -->
    **深入阅读（可选）：**这种引擎叫作*自动微分*（反向模式），也叫 *autograd*。从账本里得到的这种顺序叫作*拓扑序*。
    """)
    return


if __name__ == "__main__":
    app.run()
