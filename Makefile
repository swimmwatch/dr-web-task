SRC_DIR=src
TESTS_DIR=src/tests
REFERENCES_DIR=docs/references

mypy:
	poetry run mypy --config formatters-cfg.toml $(SRC_DIR)

flake:
	poetry run flake8 --toml-config formatters-cfg.toml $(SRC_DIR)

black:
	poetry run black --config formatters-cfg.toml $(SRC_DIR)

black-lint:
	poetry run black --check --config formatters-cfg.toml $(SRC_DIR)

isort:
	poetry run isort --settings-path formatters-cfg.toml $(SRC_DIR)

format: black isort

lint: flake mypy black-lint

lock:
	poetry lock --no-update

install:
	poetry install --no-root

test:
	poetry run pytest --benchmark-autosave --cov=$(SRC_DIR) --cov-branch --cov-report=xml --numprocesses logical $(SRC_DIR)
