# Learners only need `make start` (or ./start.sh, or start.cmd on Windows).
# Everything else is for maintainers and CI.

CH ?=

.PHONY: start smoke check check-solutions test lint i18n-stamp

start:
	./start.sh

smoke:  ## start the server, check it answers, stop it
	./start.sh --smoke

check:  ## learner work (my-work/, else the lesson stubs) against the checks; CH=00 for one chapter
	uv run python -m learn_llm.grade $(CH)

check-solutions:  ## reference solutions against the checks
	uv run python -m learn_llm.grade --solutions $(CH)

test:  ## everything CI runs except the smoke test
	uv run pytest -q

lint:
	uv run marimo check lessons

i18n-stamp:  ## after updating a translation: record which English version it matches
	uv run python -m learn_llm.i18n_stamp
