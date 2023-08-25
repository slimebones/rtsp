export PYTEST_SHOW=all
export t="."

lint:
	poetry run ruff $(t)

test:
	poetry run coverage run -m pytest -x --ignore=tests/app -p no:warnings --show-capture=$(PYTEST_SHOW) --failed-first $(t)

check: lint test
