.PHONY: setup check typecheck lint format clean

setup: .venv/bin/python
	.venv/bin/python -m pip install -e .[cli,dev]
check: typecheck lint
typecheck: .venv/bin/mypy
	.venv/bin/mypy --strict src
lint: .venv/bin/black
	.venv/bin/black --check .
format: .venv/bin/black
	.venv/bin/black .
build: .venv/bin/build
	.venv/bin/python -m build .
build-check: .venv/bin/twine
	.venv/bin/twine check dist/*
publish-testpypi: .venv/bin/twine
	.venv/bin/twine upload --repository testpypi dist/*
publish: .venv/bin/twine
	.venv/bin/twine upload dist/*
clean:
	rm -rf dist build .venv
.venv/bin/mypy: .venv/bin/python
	.venv/bin/pip install mypy
.venv/bin/build: .venv/bin/python
	.venv/bin/pip install build
.venv/bin/black: .venv/bin/python
	.venv/bin/pip install black
.venv/bin/twine: .venv/bin/python
	.venv/bin/pip install twine
.venv/bin/python:
	python -m venv --system-site-packages .venv
context:
	@echo "# README.md"
	@cat README.md
	@echo ""
	@echo ""
	@echo "# pyproject.toml"
	@cat pyproject.toml
	@echo ""
	@echo ""
	@for f in $$(find src -type f -name "*.html"); do echo "# $$f"; cat $$f; echo; echo; done
	@echo ""
	@echo ""
	@for f in $$(find src -type f -name "*.py"); do echo "# $$f"; cat $$f; echo; echo; done
