# setuptools: flat structure

.PHONY: default
default: all

# Project

package_id := setuptoolsflat
VERSION ?= 0.0.1

# Programs

BREW ?= brew
BUILD ?= $(PIPENV) run python -m build
PIPENV ?= pipenv
TAR ?= tar
UNZIP ?= unzip

.PHONY: debug-programs
debug-programs:
	$(info Programs)
	$(info - BREW=$(BREW))
	$(info - BUILD=$(BUILD))
	$(info - PIPENV=$(PIPENV))
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

#. PYTHON TARGETS

.PHONY: pipenv-install
pipenv-install:
	$(PIPENV) install --dev

.PHONY: sdist-contents
sdist-contents: $(artifact_sdist)
	$(TAR) tfz $(artifact_sdist)

.PHONY: wheel-contents
wheel-contents: $(artifact_wheel)
	$(UNZIP) -l $(artifact_wheel)

$(artifact_sdist): $(sources)
	$(BUILD) --sdist

$(artifact_wheel): $(sources)
	$(BUILD) --wheel

#. STANDARD TARGETS

.PHONY: all
all: $(artifact_sdist) $(artifact_wheel)
	@:

.PHONY: clean
clean:
	$(RM) -r build dist $(package_id).egg-info

.PHONY: test
test:
	@:

#. SUPPORT TARGETS

.PHONY: debug
debug: _debug-prefix debug-artifacts debug-programs debug-sources

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==setuptools: flat structure==)

.PHONY: homebrew-install
homebrew-install:
	$(BREW) bundle install
