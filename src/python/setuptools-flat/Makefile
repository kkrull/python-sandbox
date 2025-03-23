.PHONY: default
default: all

# Programs

BREW ?= brew
PIP ?= pip
PIPENV ?= pipenv
PYTHON ?= python

#. PYTHON TARGETS

.PHONY: pipenv-install
pipenv-install:
	$(PIPENV) install --dev

#. STANDARD TARGETS

.PHONY: all
all:
	$(PIPENV) run python -m build

.PHONY: clean
clean:
	@:

.PHONY: test
test:
	@:

#. SUPPORT TARGETS

.PHONY: homebrew-install
homebrew-install:
	$(BREW) bundle install
