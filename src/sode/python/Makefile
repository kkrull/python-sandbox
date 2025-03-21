#. ==sode python==

.PHONY: default
default: all

include ../../../make.d/help.mk
include ../../../make.d/homebrew.mk
include ../../../make.d/paths-system.mk

## Sources

# NB: the wildcard function is not recursive: https://stackoverflow.com/a/2483203/112682
source_bins := $(shell find bin -type f -name '*.py' | sort)
source_libs := $(shell find lib -type f -name '*.py' | sort)
source_main := sode.py
source_version := version
sources := $(shell find . -type f -name '*.py' | sort)

.PHONY: debug-sources
debug-sources:
	$(info Sources:)
	$(info - source_bins: $(source_bins))
	$(info - source_libs: $(source_libs))
	$(info - source_main: $(source_main))
	$(info - source_version: $(source_version))
	$(info - sources: $(sources))
	@:

## Artifacts

executable := sode.py

.PHONY: debug-artifacts
debug-artifacts:
	$(info Artifacts:)
	$(info - executable: $(executable))
	@:

## Paths

.PHONY: debug-paths
debug-paths:
	$(info Paths:)
	$(info - bindir: $(bindir))
	$(info - datadirpkg: $(datadirpkg))
	$(info - libexecdirpkg: $(libexecdirpkg))
	@:

## Programs

INSTALL ?= install
INSTALLFLAGS := -g 0 -o 0

PIP ?= pip
PIPENV ?= pipenv
PYTHON ?= python

.PHONY: debug-programs
debug-programs:
	$(info Programs:)
	$(info - INSTALL: $(INSTALL))
	$(info - INSTALLFLAGS: $(INSTALLFLAGS))
	$(info - PIP: $(PIP))
	$(info - PIPENV: $(PIPENV))
	$(info - PYTHON: $(PYTHON))
	@:

#. PYTHON TARGETS

.PHONY: pipenv-clean
pipenv-clean: #> Uninstall packages not listed in Pipfile
	$(PIPENV) clean

.PHONY: pipenv-lint-flake8
pipenv-lint-flake8: #> Lint sources with flake8
	$(PIPENV) run lint-flake8

.PHONY: pipenv-main
pipenv-main: #> Run the main script with pipenv
	$(PIPENV) run main

.PHONY: pipenv-setup-check
pipenv-setup-check:
	$(PIPENV) run setup-check

# https://stackoverflow.com/questions/1471994/what-is-setup-py
setup.py: Pipfile Pipfile.lock
	$(PIPENV) run pipenv-setup sync --dev

#. STANDARD TARGETS

.NOTPARALLEL: all
.PHONY: all
all: setup.py
	@:

.PHONY: clean
clean: pipenv-clean
	$(RM) -r build sode.egg-info

.PHONY: install
install: $(sources) setup.py #> Install package and links with pip
	$(PIP) install .

.PHONY: test
test: pipenv-lint-flake8 pipenv-setup-check

.PHONY: uninstall
uninstall: #> Uninstall package with pip
	$(PIP) uninstall -y sode

#. SUPPORT TARGETS

.PHONY: check
check: #> Check if `make install` worked
	@type sode &> /dev/null || ( echo "sode: Not found"; exit 1)

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-artifacts debug-paths debug-programs debug-sources #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==sode python==)
	@:

.PHONY: install-assets
install-assets:
	@:

.PHONY: install-tools
install-tools: homebrew-bundle-install
