import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="00 · 你的第一个程序")

with app.setup(hide_code=True):
    import marimo as mo

    from learn_llm import todo
    from learn_llm.checks import check

    LOCALE = "zh-CN"


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 00 · 你的第一个程序

    欢迎！学完这门课，你会亲手从零搭建一个自己的语言模型，也就是聊天机器人背后的那种程序。
    而这一切，都从这里的几行 Python 代码开始。

    你现在什么都不需要会。每当需要一个新概念，页面就会在用到它的地方当场讲清楚。

    ## 这个页面怎么用

    这个页面是一个**笔记本**（notebook），由一个个**单元格**（cell）组成。有的单元格是文字，
    比如这一个；有的单元格是 Python 代码，代码的运行结果就显示在它的下方。

    - **运行**代码单元格：点进单元格，按 **Shift + Enter**，或者点它旁边的 ▶ 按钮。
    - 你运行一个改过的单元格后，所有依赖它的单元格都会**自动重新运行**，不用自己记着还要重跑哪些。
    - 你的修改会自动保存在你自己的那份课程副本里。课程不会被你弄坏，放心大胆地试。
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 把 Python 当计算器

    下面的单元格里是一个很小的 Python 程序：`2 + 3`，结果显示在它下方。
    改改数字，再运行一次试试。
    """)
    return


@app.cell
def _():
    2 + 3
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Python 会做常见的算术，只是有些符号和纸上写法不同：

    | 纸上写法 | Python 写法 | 含义 | 结果 |
    |---|---|---|---|
    | 7 × 6 | `7 * 6` | 乘 | `42` |
    | 10 ÷ 4 | `10 / 4` | 除 | `2.5` |
    | 2¹⁰ | `2 ** 10` | 乘方 | `1024` |

    在下面的单元格里多试几个。括号的用法和数学里一样：`(1 + 2) * 3` 等于 `9`。
    """)
    return


@app.cell
def _():
    7 * 6
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 给值起个名字

    同一个数反复输入很累。你可以给一个值起个**名字**，之后用名字代替它。
    有值的名字叫作**变量**（variable）。

    `price = 12` 的意思是“从现在起，`price` 就代表 12”。这里的 `=` 意思是*存进去*，
    而不是*等于*。
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
    把上面那个单元格里的 `price` 改成 `15`，再按 **Shift + Enter**。结果会自己更新，因为它用到了 `price`。

    /// note | 这个笔记本的一条规则
    每个名字只能在**一个**单元格里赋值。如果你在另一个单元格里再写 `price = 20`，
    笔记本会提示这个名字已经被占用了。换个新名字（比如 `new_price`），或者直接改原来的单元格。
    ///
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 函数：有名字的菜谱

    **函数**（function）就像一份小菜谱：你给它一些输入，它按步骤做完，交回一个答案。
    下面是一个把数翻倍的函数：

    ```python
    def double(x):
        return x * 2
    ```

    逐行来看：

    - `def double(x):` 表示“我要定义一份叫 `double` 的菜谱，它的输入叫 `x`”。
    - 下一行往右缩进了四个空格（**缩进**，indent）。Python 靠缩进知道这一行属于这份菜谱。
    - `return x * 2` 表示“答案是 `x * 2`”。`return`（返回）会把答案**交回**给使用这个函数的人。

    使用函数叫作**调用**（call）它：`double(5)` 就是让菜谱在 `x = 5` 时运行一遍。
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
    ## 练习 1：摄氏度转华氏度

    轮到你了。世界上大多数地方用摄氏度（°C）表示温度，美国用华氏度（°F）。换算规则是：

    > 摄氏温度乘以 9，再除以 5，最后加上 32。

    在下面的单元格里写出函数 `to_fahrenheit`：把 `todo()` 这一行换成一行做换算的
    `return` 语句。按 **Shift + Enter** 运行代码，下方的检查结果每次都会更新。
    """)
    return


@app.function
def to_fahrenheit(celsius):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell
def _():
    check("00", "to_fahrenheit", to_fahrenheit, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    temperature = mo.ui.slider(-40, 100, value=20, label="摄氏度", show_value=True)
    return (temperature,)


@app.cell(hide_code=True)
def _(temperature):
    try:
        _answer = f"**{temperature.value} °C = {to_fahrenheit(temperature.value):g} °F**"
    except Exception:
        _answer = "*先完成练习 1，再拖动滑块试试你的函数。*"
    mo.hstack([temperature, mo.md(_answer)], justify="start", gap=2)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 一次处理很多值：列表

    **列表**（list）按顺序装着好几个值，写在方括号里：`[3, 1, 4, 1, 5]`。
    在这门课后面，一串串数字会变成图片、词语，甚至整本书。
    用 `len` 可以让 Python 告诉你列表有多长：
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
    ## 对每个值做同一件事：循环

    **循环**（loop）会对列表里的每一个值各执行一遍同样的步骤。
    下面这个循环数一数有几个分数大于 2：

    ```python
    for s in scores:
        ...
    ```

    意思是“依次取出 `scores` 里的每个值，叫它 `s`，然后运行缩进的那几行”。
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
    `_big = _big + 1` 当成数学式子看很奇怪，但别忘了 `=` 的意思是*存进去*：
    “先算出 `_big + 1`，再把结果存回 `_big`”。所以每次 `_big` 都会加一。
    （以 `_` 开头的名字只属于它所在的单元格，别的单元格可以重复使用。）

    ## 练习 2：把列表加起来

    写出 `total(numbers)`，它返回列表里所有数的和。

    提示：先让一个累计值从 `0` 开始，循环遍历每个数，把它加到累计值上，循环结束后再
    `return` 这个累计值。注意缩进：`return` 要写在循环**之后**，不要写在循环里面。
    """)
    return


@app.function
def total(numbers):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell
def _():
    check("00", "total", total, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 练习 3：平均数

    /// admonition | 🧰 工具箱：平均数（均值）
    一组数的**平均数**，也叫**均值**（mean），就是它们的总和除以个数。
    2、4、9 的平均数是 (2 + 4 + 9) ÷ 3 = 5。下一章会经常用到均值。
    ///

    写出 `average(numbers)`。最难的部分你已经做完了：函数可以调用别的函数，
    所以用上你写的 `total` 和 Python 自带的 `len` 就行。
    """)
    return


@app.function
def average(numbers):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell
def _():
    check("00", "average", average, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 你现在会做的事

    - 运行 Python 代码并看懂结果
    - 把值存进变量
    - 写出接收输入、用 `return` 返回答案的函数
    - 用列表装很多值，并用循环逐个处理

    这些已经足够开始教计算机了。在**第 01 章**里，你会用的正是这些工具：
    让程序从数据里学出规律，再去预测它从没见过的数。

    ---

    <!-- go-deeper -->
    **深入阅读（可选，学这门课用不到）：**官方
    [Python 教程](https://docs.python.org/zh-cn/3/tutorial/) 对这些概念讲得更详细。
    """)
    return


if __name__ == "__main__":
    app.run()
