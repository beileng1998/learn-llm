# learn-llm

**English** · [简体中文](README.zh-CN.md)

Go from almost no maths or programming to building your own large language model, then
serving it the way production systems do. Everything happens on one page in your browser.

> **Status: early.** Chapters 00–04 are ready: from your first line of Python to a working
> backprop engine. Chapter 05 (many numbers at once) is next.
> See the [full chapter map](SCOPE.md).

## Start

You need a computer running macOS, Linux or Windows, and an internet connection the first
time. No GPU, no accounts, no Python install needed.

1. Download this repository ([Code → Download ZIP](../../archive/refs/heads/main.zip)) and unzip it,
   or `git clone` it.
2. Start the course:
   - **Windows:** double-click `start.cmd`.
   - **macOS / Linux:** open a terminal in the folder and run `./start.sh`.
3. Your browser opens the course. Pick your language and begin with chapter 00.

The first start installs [uv](https://docs.astral.sh/uv/), which downloads the right Python
and everything the course needs into this folder. It takes a few minutes, once.
Later starts take seconds.

Your work is saved in `my-work/`, your own copy of every lesson. Updating the course never
overwrites it. To restart a chapter from scratch, delete its file in `my-work/` and start
again.

Each chapter has shared **Previous chapter / Course index / Next chapter** navigation.
The start script adds its navigation cell to new and existing learner copies without
rewriting your lesson text or answers. Before adding it, it keeps a copy of the original
in `my-work/.navigation-backups/`. Starting again does not add duplicate navigation cells.
This navigation is installed by the course launcher; directly editing the source lessons
with `marimo edit lessons/...` does not install it.
If the editor blocks navigation while edits are pending, let autosave finish or save
the notebook before switching chapters.

## How it's different

This course covers the knowledge of Stanford CS231n, CS224N and CS336 and the
[tiny-llm](https://github.com/skyzh/tiny-llm) serving course, rebuilt as one continuous path:

- **Prerequisites when you need them.** No maths unit up front. Each idea is taught on the
  page that uses it.
- **Each topic taught once.** Backprop, attention and transformers each get one chapter,
  and later chapters build on it.
- **Nothing to set up.** One start command; the checks for every exercise run on the page.
- **No jumping around.** Everything you need is in the course. Links are optional extras.
- **One growing project.** The code you write early is still running in the last chapter.

It is original material, not copied lecture notes or assignments, and it is not affiliated
with Stanford or the tiny-llm authors.

## Support

This is a personal, best-effort project with no guaranteed response times. Bug reports and
questions are welcome as GitHub issues.

## License

Code: [MIT](LICENSE). Lesson text: [CC BY 4.0](LICENSE-CONTENT).
