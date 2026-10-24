import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="02 · 往下坡走")

with app.setup(hide_code=True):
    import marimo as mo

    from learn_llm import todo
    from learn_llm.checks import check
    from learn_llm.plot import chart

    LOCALE = "zh-CN"
    temps = [14, 17, 20, 22, 25, 28, 31, 33]
    sales = [63, 90, 137, 148, 193, 234, 257, 288]
    B_FIXED = -108


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 02 · 往下坡走

    第 01 章最后你看到了：损失像一个山谷，好的旋钮取值就在谷底。你是靠拖动滑块找到谷底的。
    这一章，计算机会自己找到它，而它用到的每一个数，你都会弄明白。

    ## 回顾

    米娅的数据和之前一样：
    `temps = [14, 17, 20, 22, 25, 28, 31, 33]`，`sales = [63, 90, 137, 148, 193, 234, 257, 288]`。

    下面是你在第 01 章写的三个函数，可以直接用：直线的猜测、一次猜测的平方误差、整条线的损失（均方误差）。
    """)
    return


@app.function
def predict(w, b, x):
    return w * x + b


@app.function
def squared_error(guess, truth):
    return (guess - truth) ** 2


@app.function
def mse(w, b, xs, ys):
    running = 0
    for x, y in zip(xs, ys):
        running = running + squared_error(predict(w, b, x), y)
    return running / len(xs)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    先只用一个旋钮，就像第 01 章最后那张山谷图：起始高度固定为 `b = -108`，只改变陡度 `w`。
    这样损失就只取决于 `w`：
    """)
    return


@app.function
def loss_of_w(w):
    return mse(w, -108, temps, sales)


@app.cell
def _():
    loss_of_w(10)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 哪边是下坡？

    想象你站在大雾里的山谷中：看不见谷底，只能看到脚下的地面。有个简单办法判断哪边往下：
    **迈一小步，看看自己是往下走了还是往上走了。**

    对我们的旋钮来说，迈一小步就是把 `w` 改动一点点，比如 `0.0001`，再比较改动前后的损失。
    这一点点改动叫作**微调**（nudge）。移动滑块，比较两个损失：
    """)
    return


@app.cell(hide_code=True)
def _():
    w_here = mo.ui.slider(10, 14, step=0.1, value=10.5, label="w", show_value=True)
    return (w_here,)


@app.cell(hide_code=True)
def _(w_here):
    _w = w_here.value
    _before, _after = loss_of_w(_w), loss_of_w(_w + 0.0001)
    _change = _after - _before
    mo.vstack([
        w_here,
        mo.md(f"""
| | w | 损失 |
|---|---|---|
| 当前位置 | {_w:.4f} | {_before:.4f} |
| 往右微调后 | {_w + 0.0001:.4f} | {_after:.4f} |

损失变化了 **{_change:+.4f}**：往右微调是**{"下" if _change < 0 else "上"}坡**，
所以谷底在**{"右" if _change < 0 else "左"}边**。
"""),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 有多陡？斜率

    损失的变化告诉我们方向。把它和微调的大小比一比，还能知道地面有多陡。

    /// admonition | 🧰 工具箱：比率
    **比率**用一个变化量除以另一个变化量来比较两者。3 千克苹果卖 6 元，价格就是 6 ÷ 3 = **每**千克 2 元。
    做除法，得到的就是“每一份那个，对应多少这个”。
    ///

    这里我们用损失的变化除以 `w` 的变化（也就是微调量）：

    > 斜率 = （微调后的损失 − 微调前的损失）÷ 微调量

    结果就是**斜率**（slope）：就在你站的地方，`w` **每**增加 1，损失变化多少。
    这和第 01 章米娅那条线的陡度 `w` 是同一个意思：那里 `w` 表示每升高一度多卖多少个；
    这里斜率表示 `w` 每多一份，损失多多少。

    这样读斜率：

    - 它的**正负号**给出方向：负数表示“`w` 变大，损失就变小”，正数表示“`w` 变小，损失才变小”；
    - 它的**大小**给出陡峭程度：离谷底远的地方很陡（斜率大），靠近谷底几乎是平的（斜率接近 0）。

    图中的虚线，正好具有大圆点处的斜率：它是在那里恰好贴着曲线的一条直线。
    """)
    return


@app.cell(hide_code=True)
def _(w_here):
    _w = w_here.value
    try:
        _s = nudge_slope(loss_of_w, _w)
        _note = f"你的 `nudge_slope` 算出 w = {_w:g} 处的斜率是 **{_s:,.1f}**。"
    except Exception:
        _s = (loss_of_w(_w + 0.0001) - loss_of_w(_w)) / 0.0001
        _note = f"w = {_w:g} 处的斜率是 **{_s:,.1f}**。（完成练习 1 后，这个数会由你自己的函数算出来。）"
    _y = loss_of_w(_w)
    mo.vstack([
        w_here,
        chart((10, 14), (0, 2700), "w（米娅那条线的陡度）", "损失",
              curve=[(10 + i * 0.05, loss_of_w(10 + i * 0.05)) for i in range(81)],
              marker=(_w, _y), segments=[(_w - 0.6, _y - 0.6 * _s, _w + 0.6, _y + 0.6 * _s)]),
        mo.md(_note),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 练习 1：用微调测量斜率

    写出 `nudge_slope(f, x)`：用 `0.0001` 的微调量，测出函数 `f` 在输入 `x` 处的斜率。

    先讲一个新概念。**函数也是一种值**，就像数字或列表一样：可以把它作为输入交给另一个函数。
    在那个函数里面，像调用普通函数一样调用它就行。比如：
    """)
    return


@app.function
def square(x):
    return x * x


@app.function
def call_with_three(f):
    return f(3)


@app.cell
def _():
    call_with_three(square)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `call_with_three(square)` 把函数 `square` 本身交给 `call_with_three`（`square` 后面没有括号：
    交出去的是菜谱，而不是答案）。在里面，`f` 就代表 `square`，所以 `f(3)` 就是 `square(3)`，等于 `9`。

    在 `nudge_slope(f, x)` 里，`f` 就是你想求斜率的那个函数。步骤：

    1. 存下微调量：`h = 0.0001`
    2. 算出 `f(x + h) - f(x)`：`f` 变化了多少
    3. 返回这个变化量除以 `h` 的结果

    可以写成一行 `return`，但括号很重要：必须先做减法再做除法（不加括号的话，`/` 会比 `-` 先算）。
    """)
    return


@app.function
def nudge_slope(f, x):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("02", "nudge_slope", nudge_slope, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 迈出一步

    现在我们知道了哪边是下坡、有多陡。迈一步的规则是：

    > 新的 w = w − 学习率 × 斜率

    为什么是**减号**？因为斜率指向上坡。把所有情况检查一遍：

    | 斜率 | 意思 | − 学习率 × 斜率 | 所以 w…… |
    |---|---|---|---|
    | 负数（比如 −2000） | 下坡在右边 | 正数 | 变大：往右走 ✓ |
    | 正数（比如 +2000） | 下坡在左边 | 负数 | 变小：往左走 ✓ |
    | 接近 0 | 快到谷底了 | 接近 0 | 几乎不动 ✓ |

    为什么要乘以斜率，而不是每次都走同样远？离谷底远的地方很陡，步子就大；靠近谷底很平，步子自然变小，
    快到的时候就慢下来了。

    **学习率**（learning rate）是你选的一个小数，决定步子整体有多大。米娅的损失动不动就是几千，
    所以学习率得非常小，比如 `0.0008`。

    ## 练习 2：走一步

    写出 `step(w, slope, rate)`：返回往下坡走一步之后新的 `w`。
    """)
    return


@app.function
def step(w, slope, rate):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("02", "step", step, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 练习 3：一路走下坡

    一步不够：我们要把同样的两个动作（测斜率、迈一步）重复很多次。这种重复叫作**梯度下降**
    （gradient descent）：一步一步往下坡走。

    要把一件事重复指定的次数，用 `range`：`for i in range(5):` 会把缩进的那几行运行 5 次
    （`i` 依次是 0、1、2、3、4；这里用不到它，只是必须给它起个名字）。

    写出 `descend(f, w, rate, steps)`：从 `w` 出发，重复 `steps` 次：用你的 `nudge_slope` 测出 `f` 在当前 `w` 处的斜率，
    再用你的 `step` 算出新值，并存回 `w`（`w = step(...)`）。循环结束后返回 `w`。先完成练习 1 和 2。
    """)
    return


@app.function
def descend(f, w, rate, steps):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("02", "descend", descend, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 看它走

    下面是你的函数在米娅的山谷里走的路：从 `w = 10` 出发，走 15 步。每个点是一步落脚的地方。
    在菜单里试试不同的学习率：
    """)
    return


@app.cell(hide_code=True)
def _():
    rate_choice = mo.ui.dropdown(
        {"0.0001（小）": 0.0001, "0.0008": 0.0008, "0.0015": 0.0015, "0.0018（大）": 0.0018},
        value="0.0001（小）", label="学习率",
    )
    return (rate_choice,)


@app.cell(hide_code=True)
def _(rate_choice):
    try:
        _path = [10]
        for _i in range(15):
            _path.append(step(_path[-1], nudge_slope(loss_of_w, _path[-1]), rate_choice.value))
        _end = _path[-1]
        _out = mo.vstack([
            rate_choice,
            chart((6, 18), (0, 12000), "w", "损失",
                  curve=[(6 + i * 0.1, loss_of_w(6 + i * 0.1)) for i in range(121)],
                  dots=[(p, loss_of_w(p)) for p in _path if 6 <= p <= 18]),
            mo.md(f"走了 15 步之后：w = **{_end:.3f}**，损失 = **{loss_of_w(_end):,.1f}**。"),
        ])
    except Exception:
        _out = mo.md("*完成练习 1 和 2 后就能看它走了。*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    你应该会看到：

    - **0.0001**：每一步都很稳，但很短；15 步之后还在半路上。
    - **0.0008**：几步就到了谷底。
    - **0.0015**：步子大到越过谷底跳到对面，来回跳，但跳的幅度越来越小，所以最后还是停了下来。
    - **0.0018**：每一跳都落得比上一跳更高，最后飞出了山谷。（跑出图外的点不会画出来。）

    选学习率就是在找平衡：太小走得慢，太大永远到不了。这门课里的每个模型都会遇到这个选择。

    ## 两个旋钮一起调

    米娅的线有两个旋钮。微调对每个旋钮都一样管用：保持 `b` 不动，测出 `w` 方向的斜率；保持 `w` 不动，
    测出 `b` 方向的斜率；然后两个都迈一步。下面的单元格正是用你的 `nudge_slope` 和 `step` 这样做的，
    起点是 `w = 6`、`b = 0`。选一选走多少步：
    """)
    return


@app.cell(hide_code=True)
def _():
    steps_choice = mo.ui.dropdown(["100", "1000", "5000", "20000"], value="100", label="步数")
    return (steps_choice,)


@app.cell(hide_code=True)
def _(steps_choice):
    try:
        _w, _b = 6, 0
        for _i in range(int(steps_choice.value)):
            _sw = nudge_slope(lambda v: mse(v, _b, temps, sales), _w)
            _sb = nudge_slope(lambda v: mse(_w, v, temps, sales), _b)
            _w, _b = step(_w, _sw, 0.001), step(_b, _sb, 0.001)
        _out = mo.vstack([
            steps_choice,
            chart((10, 36), (0, 320), "气温（°C）", "卖出的冰淇淋（个）",
                  dots=list(zip(temps, sales)), lines=[(_w, _b)]),
            mo.md(f"w = **{_w:.2f}**，b = **{_b:.1f}**，损失 = **{mse(_w, _b, temps, sales):,.1f}**"),
        ])
    except Exception:
        _out = mo.md("*完成练习 1 和 2 后才能运行这一段。*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    计算机自己找到了米娅的直线：走 20,000 步后，损失已经接近最好的结果（大约 27）。没有人拖过滑块。

    你可能注意到，`b` 比 `w` 挪得慢得多。损失对 `w` 的反应比对 `b` 强烈得多（每一度都会乘上 `w`），
    所以对 `w` 来说安全的学习率，对 `b` 来说就太胆小了。后面的章节会介绍常用的解决办法；现在多走几步就够了。

    ## 微调的代价

    每用微调测一次斜率，**每个旋钮**都要多算一次损失。两个旋钮，每步多算两次，没问题。
    这门课最后的语言模型有几十亿个旋钮，而且每算一次损失都要读大量文字。每走一步都要多算几十亿次损失，那要算到天荒地老。

    所以我们想要一种不用微调、直接用公式算出**精确**斜率的办法。为此，先仔细看看微调时到底发生了什么，
    从最简单的曲线开始。

    ## x² 的精确斜率

    取 `square(x) = x × x`。把 `x` 微调一个小量 `h`，新的值是 `(x + h) × (x + h)`。
    它比 `x × x` 大了多少？一张图就能回答：边长为 `x + h` 的正方形，由四块组成。
    """)
    return


@app.cell(hide_code=True)
def _():
    _x, _h = 200, 60  # 画图用的尺寸，不是数值
    _o = 20
    mo.Html(f"""
<svg viewBox="0 0 330 330" width="100%" style="max-width:330px" role="img"
     aria-label="边长为 x 加 h 的正方形，分成 x 的平方、两块 x 乘 h 的长方形和 h 的平方"
     xmlns="http://www.w3.org/2000/svg" font-size="16" text-anchor="middle">
  <rect x="{_o}" y="{_o}" width="{_x}" height="{_x}" fill="var(--blue-4, #dbeafe)" stroke="var(--slate-9, #64748b)"/>
  <rect x="{_o + _x}" y="{_o}" width="{_h}" height="{_x}" fill="var(--crimson-4, #fee2e2)" stroke="var(--slate-9, #64748b)"/>
  <rect x="{_o}" y="{_o + _x}" width="{_x}" height="{_h}" fill="var(--crimson-4, #fee2e2)" stroke="var(--slate-9, #64748b)"/>
  <rect x="{_o + _x}" y="{_o + _x}" width="{_h}" height="{_h}" fill="var(--amber-4, #fef3c7)" stroke="var(--slate-9, #64748b)"/>
  <text x="{_o + _x / 2}" y="{_o + _x / 2 + 6}" fill="var(--slate-12, #1e293b)">x × x</text>
  <text x="{_o + _x + _h / 2}" y="{_o + _x / 2 + 6}" fill="var(--slate-12, #1e293b)">x × h</text>
  <text x="{_o + _x / 2}" y="{_o + _x + _h / 2 + 6}" fill="var(--slate-12, #1e293b)">x × h</text>
  <text x="{_o + _x + _h / 2}" y="{_o + _x + _h / 2 + 6}" fill="var(--slate-12, #1e293b)" font-size="13">h × h</text>
  <text x="{_o + _x / 2}" y="{_o + _x + _h + 22}" fill="var(--slate-11, #475569)">x</text>
  <text x="{_o + _x + _h / 2}" y="{_o + _x + _h + 22}" fill="var(--slate-11, #475569)">h</text>
</svg>""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    蓝色大正方形是原来的值 `x × x`。微调多出了两条各为 `x × h` 的长条，外加一个很小的角 `h × h`。所以：

    > 变化量 = 2 × x × h + h × h

    再像 `nudge_slope` 那样除以微调量 `h`，得到斜率：

    > 斜率 = (2 × x × h + h × h) ÷ h = 2 × x + h

    （每一块里都有一个 `h`，所以除以 `h` 就是从每一块里去掉一个 `h`。）

    现在把微调量取得越来越小：`h = 0.1`、`0.001`、`0.0000001`…… `2 × x` 这部分始终不变，
    而多出来的 `+ h` 越缩越小，趋近于零。最后，`x × x` 的斜率恰好是 **`2 × x`**。在 `x = 3` 处就是 `6`。
    和你的 `nudge_slope` 对比一下，它还带着那个小小的 `h`：
    """)
    return


@app.cell(hide_code=True)
def _():
    try:
        _out = mo.md(
            f"`nudge_slope(square, 3)` = **{nudge_slope(square, 3):.6f}**，而公式给出 "
            f"`2 × 3` = **6**。差别就是多出来的那个 `h` = 0.0001。"
        )
    except Exception:
        _out = mo.md("*完成练习 1 后就能对比了。*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    这个精确的斜率有个名字：**导数**（derivative）。数学家这样写：

    > d/dx (x²) = 2x

    读作：“x² 对 x 的导数是 2x”，或者简单说：“x² 在任意 `x` 处的斜率是 `2x`”。`d/dx` 是一种简写，
    意思是“当 `x` 的微调量缩小到没有时的精确斜率”。从现在起，这门课里**斜率**和**导数**是同一个意思。

    ## 更多规则，同样的推法

    下面每条规则都和 `x²` 一样，是从微调推出来的。对每一条，想想微调量 `h` 会让值变化多少：

    | 函数 | 把 x 微调 h，它变化 | 所以斜率是 |
    |---|---|---|
    | 常数，比如 `5` | 不变：0 | **0** |
    | `c × x`，比如 `7 × x` | `c × h` | **c** |
    | `x × x` | `2 × x × h + h × h` | **2 × x** |
    | `c` 乘以某个函数 | `c` 乘以那个函数的变化量 | **c 乘以它的斜率** |
    | 一个函数加另一个函数 | 两个变化量相加 | **两个斜率相加** |

    最后两条可以把前面几条组合起来。比如 `4 × x × x` 的斜率是 `x × x` 斜率的 `4` 倍，也就是 `4 × 2 × x = 8 × x`。

    ## 练习 4：精确的斜率

    取 `f(x) = 3 × x × x + 5 × x + 2`。先在**纸上**用这些规则算出它的斜率：把三部分各自的斜率求出来，再加起来。
    然后写出 `slope_f(x)`，返回这个公式。检查会把它和正确的公式对比；检查下方，你的 `nudge_slope` 会测出同一个斜率，作为第二意见。
    """)
    return


@app.function
def f(x):
    return 3 * x * x + 5 * x + 2


@app.function
def slope_f(x):
    # ← 把下面的 todo() 换成你的代码
    todo()


@app.cell(hide_code=True)
def _():
    check("02", "slope_f", slope_f, LOCALE)
    return


@app.cell(hide_code=True)
def _():
    try:
        _rows = "\n".join(f"| {x} | {slope_f(x):g} | {nudge_slope(f, x):.4f} |" for x in (-2, 0, 1, 4))
        _out = mo.md("| x | 你的公式 | 微调测量 |\n|---|---|---|\n" + _rows)
    except Exception:
        _out = mo.md("*完成练习 1 和 4 后，就能把你的公式和微调测量对比了。*")
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    你的公式和微调测量结果一致（只差微调留下的那一点点），而公式完全不需要额外计算。这正是我们想要的交换。

    ## 还缺什么

    米娅的损失是许多 `(w × 14 + b − 63)²` 这类东西的平均：是平方，但平方的是一个本身又依赖 `w` 的东西。
    我们现有的规则还管不了“一个含有 `w` 的算式的平方”。在**第 03 章**里，你会把这样的算式拆成一个个小步骤，
    求出每一步的斜率，看这些斜率怎样组合起来，把“责任”从损失一路往回分给每个旋钮。

    ## 你现在会做的事

    - 用微调找出下坡的方向和陡峭程度：斜率
    - 用 `新 w = w − 学习率 × 斜率` 往下坡走，并选择学习率
    - 把一个函数交给另一个函数，用 `range` 重复
    - 用微调规则推出精确的斜率（导数），并用微调来验证

    ---

    <!-- go-deeper -->
    **深入阅读（可选）：**在数学教材里，“微调量越来越小”的思想叫作*极限*，微调测斜率的方法叫作*有限差分*。
    """)
    return


if __name__ == "__main__":
    app.run()
