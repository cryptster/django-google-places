.PHONY: check test test-all

check:
	pre-commit run --all-files $(CHECK)

test:
	python load_tests.py

test-all:
	tox
