#. ==sode python==

.PHONY: default
default: all

include ../../../make.d/help.mk
include ../../../make.d/homebrew.mk
include ../../../make.d/paths-system.mk

## Environment

### Paths

.PHONY: debug-paths
debug-paths:
	$(info Paths:)
	$(info - bindir: $(bindir))
	$(info - datadirpkg: $(datadirpkg))
	$(info - libexecdirpkg: $(libexecdirpkg))
	@:

### Programs

FSWATCH ?= fswatch
TAR ?= tar
UNZIP ?= unzip

.PHONY: debug-programs
debug-programs:
	$(info Programs)
	$(info - FSWATCH=$(FSWATCH))
	$(info - TAR=$(TAR))
	$(info - UNZIP=$(UNZIP))
	@:

## Project

package_id := sode

.PHONY: debug-project
debug-project:
	$(info Project)
	$(info - package_id=$(package_id))
	@:

### Sources

sources_py := $(shell find sode -type f -iname '*.py' | sort)
sources := Pipfile Pipfile.lock pyproject.toml $(sources_py)

.PHONY: debug-sources
debug-sources:
	$(info Sources:)
	$(info - sources=$(sources))
	$(info - sources_py=$(sources_py))
	@:

### Artifacts

.PHONY: debug-artifacts
debug-artifacts:
	$(info Artifacts:)
	$(info - artifact_sdist=$(artifact_sdist))
	$(info - artifact_wheel=$(artifact_wheel))
	@:

#. STANDARD TARGETS

.PHONY: all
all: sdist wheel #> Build all artifacts
	@:

.PHONY: clean
clean: clean-build clean-pipenv clean-python clean-sdist clean-wheel #> Remove files built from these sources
	@:

.PHONY: install
install: install-wheel #> Install artifacts
	@:

.PHONY: test
test: black-check isort-check mypy-check #> Run checks

.PHONY: uninstall
uninstall: uninstall-wheel #> Uninstall artifacts
	@:

#. SUPPORT TARGETS

.PHONY: check
check: check-wheel #> Check if artifacts were installed correctly
	@:

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-artifacts debug-paths debug-programs debug-project debug-python debug-sources #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==sode python==)
	@:

.PHONY: format
format: black-format isort-format
	@:

#. DEVELOPMENT ENVIRONMENT TARGETS

.PHONY: install-tools
install-tools: homebrew-bundle-install #> Install development tools
	@:

#. PYTHON TARGETS

BUILD ?= $(PIPENV) run python -m build
PIPENV ?= pipenv
PIPX ?= pipx

.PHONY: clean-build
clean-build: #> Remove files from running build
	$(RM) -r build dist $(package_id).egg-info

.PHONY: clean-pipenv
clean-pipenv: #> Uninstall packages not listed in Pipfile
	$(PIPENV) clean

.PHONY: clean-python
clean-python: #> Remove files from running python
	$(RM) -r **/__pycache__

.PHONY: debug-python
debug-python:
	$(info Python)
	$(info - BUILD=$(BUILD))
	$(info - PIPENV=$(PIPENV))
	$(info - PIPX=$(PIPX))
	@:

.PHONY: pipenv-install
pipenv-install: #> Install development dependencies with pipenv
	$(PIPENV) install --dev

#. PYTHON SUPPORT TARGETS

MYPY ?= $(PIPENV) run mypy-check

.PHONY: black-check
black-check: #> Check sources with black
	$(PIPENV) run black-check

.PHONY: black-format
black-format: #> Format sources with black
	$(PIPENV) run black-format

.PHONY: isort-check
isort-check: #> Check sources with isort
	$(PIPENV) run isort-check

.PHONY: isort-format
isort-format: #> Format sources with isort
	$(PIPENV) run isort-format

.PHONY: mypy-check
mypy-check: #> Type check sources with mypy
	$(PIPENV) run mypy-check

.PHONY: mypy-watch
mypy-watch: #> Type check sources with mypy (watch mode)
	$(FSWATCH) $(sources) -0 \
		| xargs -0 -I {} $(MYPY) {}

#. SOURCE DISTRIBUTION TARGETS

artifact_sdist = $(wildcard dist/$(package_id)*.tar.gz)
sdist_timestamp := .sdist-timestamp

.PHONY: clean-sdist
clean-sdist:
	$(RM) $(sdist_timestamp)

.PHONY: sdist
sdist: $(sdist_timestamp) #> Build the source distribution
	@:

.PHONY: sdist-contents
sdist-contents: sdist #> Show what's inside the sdist
	$(TAR) tfz $(artifact_sdist)

# Phony target timestamp, to avoid guessing target name of artifact named with source code version
$(sdist_timestamp): $(sources)
	$(BUILD) --sdist
	@touch $@

#. WHEEL TARGETS

artifact_wheel = $(wildcard dist/$(package_id)*.whl)
cmd_name := sode
wheel_timestamp := .wheel-timestamp

.PHONY: check-wheel
check-wheel:
	@type $(cmd_name) &> /dev/null || ( echo "$(cmd_name): not found"; exit 1 )

.PHONY: clean-wheel
clean-wheel:
	$(RM) $(wheel_timestamp)

.PHONY: install-editable-wheel
install-editable-wheel: wheel #> Link to the wheel globally with pipx
	$(PIPX) install --editable .

.PHONY: install-wheel
install-wheel: wheel #> Install the wheel globally with pipx
	$(PIPX) install .

.PHONY: uninstall-wheel
uninstall-wheel:
	$(PIPX) uninstall $(package_id)

.PHONY: wheel
wheel: $(wheel_timestamp) #> Build the wheel
	@:

.PHONY: wheel-contents
wheel-contents: wheel #> Show what's inside the wheel
	$(UNZIP) -l $(artifact_wheel)

# Phony target timestamp, to avoid guessing target name of artifact named with source code version
$(wheel_timestamp): $(sources)
	$(BUILD) --wheel
	@touch $@

#. SODE TARGETS

.PHONY: run-cli
run-cli: run-cli-pipenv run-cli-python run-cli-wheel #> Run the CLI all possible ways
	@:

.PHONY: run-cli-pipenv
run-cli-pipenv: #> Run the program from a pipenv script
	@echo ""
	$(PIPENV) run sode-cli --version

.PHONY: run-cli-python
run-cli-python: #> Run the program from venv-managed python
	@echo ""
	PYTHONPATH=. $(PIPENV) run python ./sode/cli.py --version

.PHONY: run-cli-wheel
run-cli-wheel: wheel #> Run the program from a (re-)installed wheel
	@echo ""
	$(PIPX) install --force --quiet .
	@$(cmd_name) --version
