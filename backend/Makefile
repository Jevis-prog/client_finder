include .env
export

.PHONY: lint isort style test mypy all

VENV_BIN_PATH ?= .venv\Scripts
PYTHON = $(VENV_BIN_PATH)\python.exe

chats:
	$(PYTHON) -m bot chats

run:
	$(PYTHON) -m bot run

lint:
	$(VENV_BIN_PATH)\flake8.exe

isort:
	$(VENV_BIN_PATH)\isort.exe bot tests

mypy:
	mypy --config-file setup.cfg .

style: lint isort

test:
	$(VENV_BIN_PATH)\pytest.exe

all: style test