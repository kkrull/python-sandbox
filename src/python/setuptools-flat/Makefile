# setuptools: flat structure

.PHONY: default
default: all

# Project

package_id := unknown
VERSION ?= 0.0.0

# Programs

BREW ?= brew
PIP ?= pip
PIPENV ?= pipenv
PYTHON ?= python
TAR ?= tar
UNZIP ?= unzip

# Sources

sources := Pipfile Pipfile.lock pyproject.toml

.PHONY: debug-sources
debug-sources:
	$(info Sources)
	$(info - sources=$(sources))
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
	$(PIPENV) run python -m build --sdist

$(artifact_wheel): $(sources)
	$(PIPENV) run python -m build --wheel

#. STANDARD TARGETS

.PHONY: all
all: $(artifact_sdist) $(artifact_wheel)
	@:

.PHONY: clean
clean:
	$(RM) -r dist

.PHONY: test
test:
	@:

#. SUPPORT TARGETS

.PHONY: debug
debug: _debug-prefix debug-artifacts debug-sources

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==setuptools: flat structure==)

.PHONY: homebrew-install
homebrew-install:
	$(BREW) bundle install
