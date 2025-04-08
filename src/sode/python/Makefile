#. ==sode python==

.PHONY: default
default: all

include ../../../make.d/help.mk
include ../../../make.d/homebrew.mk
include ../../../make.d/pre-commit.mk

include make.d/black.mk
include make.d/isort.mk
include make.d/mypy.mk
include make.d/sdist.mk
include make.d/wheel.mk

## Environment

### Paths

.PHONY: debug-paths
debug-paths:
	$(info Paths:)
	@:

### Programs

BUILD ?= $(PIPENV) run python -m build
FSWATCH ?= fswatch
FSWATCHFLAGS ?= ''
PIPENV ?= pipenv
PIPX ?= pipx
TAR ?= tar
UNZIP ?= unzip

.PHONY: debug-programs
debug-programs:
	$(info Programs:)
	$(info - BUILD=$(BUILD))
	$(info - FSWATCH=$(FSWATCH))
	$(info - FSWATCHFLAGS=$(FSWATCHFLAGS))
	$(info - PIPENV=$(PIPENV))
	$(info - PIPX=$(PIPX))
	$(info - TAR=$(TAR))
	$(info - UNZIP=$(UNZIP))
	@:

## Project

package_id := sode

.PHONY: debug-project
debug-project:
	$(info Project:)
	$(info - package_id=$(package_id))
	@:

### Sources

sources := Pipfile Pipfile.lock pyproject.toml $(sources_py)
sources_dir := sode
sources_py := $(shell find $(sources_dir) -type f -iname '*.py' | sort)

.PHONY: debug-sources
debug-sources:
	$(info Sources:)
	$(info - sources=$(sources))
	$(info - sources_dir=$(sources_dir))
	$(info - sources_py=$(sources_py))
	@:

### Artifacts

.PHONY: debug-artifacts
debug-artifacts: debug-sdist debug-wheel
	@:

#. STANDARD TARGETS

.PHONY: all
all: sdist wheel #> Build all artifacts
	@:

.PHONY: clean
clean: clean-build clean-mypy clean-python clean-sdist clean-wheel #> Remove files built from these sources
	@:

.PHONY: install
install: install-wheel #> Install artifacts
	@:

.PHONY: test
test: black-check isort-check mypy-check pre-commit-run #> Run checks

.PHONY: uninstall
uninstall: uninstall-wheel #> Uninstall artifacts
	@:

#. SUPPORT TARGETS

.PHONY: check
check: check-wheel #> Check if artifacts were installed correctly
	@:

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-artifacts debug-paths debug-programs debug-project debug-sources #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==sode python==)
	@:

#. DEVELOPMENT ENVIRONMENT TARGETS

.PHONY: install-tools
install-tools: homebrew-bundle-install #> Install development tools
	@:

#. PROGRAM TARGETS

.PHONY: run
run: run-pipenv run-python run-wheel #> Run the program all possible ways
	@:

.PHONY: run-pipenv
run-pipenv: #> Run the program from a pipenv script
	@echo ""
	$(PIPENV) run sode-cli --version

.PHONY: run-python
run-python: #> Run the program from venv-managed python
	@echo ""
	PYTHONPATH=. $(PIPENV) run python ./sode/cli/main.py --version

#. PYTHON TARGETS

.PHONY: clean-build
clean-build: #> Remove files from running build
	$(RM) -r build dist $(package_id).egg-info

.PHONY: clean-python
clean-python: # Remove files from running python
	$(shell find . -type d -name '__pycache__' -exec $(RM) -R {} +)
	@:

.PHONY: format
format: black-format isort-format #> Format sources
	@:

.PHONY: pipenv-clean
pipenv-clean: #> Uninstall packages not listed in Pipfile
	$(PIPENV) clean

.PHONY: pipenv-install
pipenv-install: #> Install development dependencies with pipenv
	$(PIPENV) install --dev
