"""Start the course: copy the lessons into my-work/, start marimo, open the browser.

Run by start.sh / start.cmd. `--smoke` starts the server, checks it answers, and stops it (for CI).
"""

import argparse
import json
import locale
import signal
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser

from learn_llm.course import LESSONS, WORK
from learn_llm.i18n import LOCALES, SOURCE_LOCALE
from learn_llm.navigation import install_navigation

SETTINGS = WORK / ".settings.json"


def default_locale() -> str:
    system = (locale.getlocale()[0] or "").replace("_", "-").lower()
    for code in LOCALES:
        if system.startswith(code.lower()) or system.startswith(code.split("-")[0].lower()):
            return code
    return SOURCE_LOCALE


def prepare_workspace() -> None:
    """Copy new lessons; add shared navigation without replacing learner content."""
    WORK.mkdir(exist_ok=True)
    for source in LESSONS.rglob("*.py"):
        target = WORK / source.relative_to(LESSONS)
        if source.name == "home.py":
            shutil.copyfile(source, target)  # not learner work: always take the latest
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    if not SETTINGS.exists():
        SETTINGS.write_text(json.dumps({"locale": default_locale()}), encoding="utf-8")
    for code in LOCALES:
        for path in (WORK / code).glob("[0-9][0-9]-*.py"):
            try:
                install_navigation(path, WORK)
            except (OSError, SyntaxError, UnicodeError, ValueError) as error:
                print(f"Navigation not added to {path}: {error}", file=sys.stderr)


def free_port(start: int) -> int:
    for port in range(start, start + 50):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit(f"No free port found from {start} to {start + 49}.")


def wait_until_up(url: str, server: subprocess.Popen, seconds: float = 120) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if server.poll() is not None:
            raise SystemExit("The course server stopped while starting. See the messages above.")
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.5)
    raise SystemExit(f"The course server did not answer within {seconds:.0f} seconds.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="start")
    parser.add_argument("--port", type=int, default=2718)
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser window")
    parser.add_argument("--smoke", action="store_true", help="start, check the server answers, stop")
    args = parser.parse_args(argv)

    # Turn `kill`/SIGTERM into a normal exit so the `finally` below stops the server too.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    prepare_workspace()
    port = free_port(args.port)
    # No password (the maintainer's choice): the server listens on this computer only.
    server = subprocess.Popen(
        [sys.executable, "-m", "marimo", "edit", str(WORK), "--headless", "--host", "127.0.0.1",
         "--port", str(port), "--no-token", "--skip-update-check", "--no-sandbox"],
    )

    url = f"http://localhost:{port}/?file=home.py"
    try:
        wait_until_up(url, server)
        if args.smoke:
            print("Smoke test: the course server answered.", flush=True)
            return 0
        print(f"\nThe course is running. If no browser window opened, visit:\n  {url}\n")
        print("Keep this window open while you learn. Press Ctrl+C here to stop.\n", flush=True)
        if not args.no_browser:
            webbrowser.open(url)
        return server.wait()
    except KeyboardInterrupt:
        return 0
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    sys.exit(main())
