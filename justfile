set shell := ["nu", "-c"]

lint target=".":
	poetry run ruff {{target}}

test target="" show="all" *flags="":
	poetry run coverage run -m pytest -x --ignore=tests/app -p no:warnings --show-capture={{show}} --failed-first --asyncio-mode=auto {{flags}} {{target}}

check: lint test

run *flags="":
	poetry run python -m rtsp {{flags}}
