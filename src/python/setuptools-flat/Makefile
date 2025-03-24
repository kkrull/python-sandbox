# setuptools: flat structure

.PHONY: default
default: all

# Local conventions:
# - Distinguish standard and conventional targets from project-specific ones.
# - Add conventional targets to discover targets and troubleshoot recipes without opening Makefiles.
# - Group non-standard targets by artifact or tool type, starting with the artifact or tool name.
# - Create variables in CAPS with defaults that can be overridden at runtime, for external programs.
# - Create variables in snake_case that are not meant to be overridden at runtime.
# - Put data and variables along with the targets that use them, when possible.
# - Delegate targets to artifact- or tool-specific dependencies that start with the name of the
#   top-level target (e.g. `install` depends upon `install-bin` and `install-lib`).

# Project

package_id := setuptoolsflat
VERSION ?= 0.0.1

.PHONY: debug-project
debug-project:
	$(info Project)
	$(info - package_id=$(package_id))
	$(info - VERSION=$(VERSION))
	@:

# Programs

TAR ?= tar
UNZIP ?= unzip

.PHONY: debug-programs
debug-programs:
	$(info Programs)
	$(info - TAR=$(TAR))
	$(info - UNZIP=$(UNZIP))
	@:

# Sources

sources_py := $(shell find setuptoolsflat -iname '*.py' | sort)
sources := Pipfile Pipfile.lock pyproject.toml $(sources_py)

.PHONY: debug-sources
debug-sources:
	$(info Sources)
	$(info - sources=$(sources))
	$(info - sources_py=$(sources_py))
	@:

# Artifacts

artifact_sdist := dist/$(package_id)-$(VERSION).tar.gz
artifact_wheel := dist/$(package_id)-$(VERSION)-py3-none-any.whl

.PHONY: debug-artifacts
debug-artifacts:
	$(info Artifacts:)
	$(info - artifact_sdist=$(artifact_sdist))
	$(info - artifact_wheel=$(artifact_wheel))
	@:

#. DEVELOPMENT ENVIRONMENT TARGETS

BREW ?= brew

.PHONY: debug-tools
debug-tools:
	$(info Development Environment)
	$(info - BREW=$(BREW))
	@:

.PHONY: install-tools
install-tools: homebrew-install #> Install development tools
	@:

.PHONY: homebrew-install
homebrew-install:
	$(BREW) bundle install

#. STANDARD TARGETS

.PHONY: all
all: $(artifact_sdist) $(artifact_wheel) #> Build all artifacts
	@:

.PHONY: clean
clean: clean-build pipenv-clean #> Remove files built from these sources
	@:

.PHONY: install
install: install-wheel #> Install artifacts
	@:

.PHONY: uninstall
uninstall: uninstall-wheel #> Uninstall artifacts
	@:

.PHONY: test
test:
	@:

#. SUPPORT TARGETS

.PHONY: check
check: check-wheel #> Check if artifacts were installed correctly
	@:

.PHONY: debug
debug: _debug-prefix debug-artifacts debug-programs debug-project debug-python debug-sources debug-tools #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==setuptools: flat structure==)
	@:

# Generate help documentation from Makefiles
# hash-dot NAME => Section titled NAME
# TARGET: hash-greater DESCRIPTION => Target description
# https://stackoverflow.com/a/47107132/112682
.PHONY: help
help: #> Show this help
	@sed -n \
		-e '/@sed/!s/#[.] */_margin_\n/p' \
		-e '/@sed/!s/:.*#> /:/p' \
		$(MAKEFILE_LIST) \
	| column -ts : | sed -e 's/_margin_//'

#. PYTHON TARGETS

BUILD ?= $(PIPENV) run python -m build
PIPENV ?= pipenv
PIPX ?= pipx

.PHONY: clean-build
clean-build: #> Remove files from running build
	$(RM) -r build dist $(package_id).egg-info

.PHONY: debug-python
debug-python:
	$(info Programs)
	$(info - BUILD=$(BUILD))
	$(info - PIPENV=$(PIPENV))
	$(info - PIPX=$(PIPX))
	@:

.PHONY: pipenv-clean
pipenv-clean: #> Uninstall unused packages from virtualenv
	$(PIPENV) clean

.PHONY: pipenv-install
pipenv-install: #> Install development dependencies with pipenv
	$(PIPENV) install --dev

.PHONY: run-local-cli
run-local-cli: #> Run the program directly from the source
	PYTHONPATH=. $(PIPENV) run python ./setuptoolsflat/cli.py

#. PYTHON SOURCE DISTRIBUTION TARGETS

.PHONY: sdist
sdist: $(artifact_sdist) #> Build the source distribution
	@:

.PHONY: sdist-contents
sdist-contents: $(artifact_sdist) #> Show what's inside the sdist
	$(TAR) tfz $(artifact_sdist)

$(artifact_sdist): $(sources)
	$(BUILD) --sdist

#. PYTHON WHEEL TARGETS

.PHONY: check-wheel
check-wheel:
	@type marvin &> /dev/null || ( echo "marvin: not found"; exit 1 )

.PHONY: install-editable-wheel
install-editable-wheel: $(artifact_wheel) #> Link to the wheel globally with pipx
	$(PIPX) install --editable .

.PHONY: install-wheel
install-wheel: $(artifact_wheel) #> Install the wheel globally with pipx
	$(PIPX) install .

.PHONY: uninstall-wheel
uninstall-wheel:
	$(PIPX) uninstall $(package_id)

.PHONY: wheel
wheel: $(artifact_wheel) #> Build the wheel
	@:

.PHONY: wheel-contents
wheel-contents: $(artifact_wheel) #> Show what's inside the wheel
	$(UNZIP) -l $(artifact_wheel)

$(artifact_wheel): $(sources)
	$(BUILD) --wheel
