# setuptools: flat structure

.PHONY: default
default: all

# Project

package_id := setuptoolsflat
VERSION ?= 0.0.1

# Programs

BREW ?= brew
BUILD ?= $(PIPENV) run python -m build
PIP ?= pip
PIPENV ?= pipenv
TAR ?= tar
UNZIP ?= unzip

.PHONY: debug-programs
debug-programs:
	$(info Programs)
	$(info - BREW=$(BREW))
	$(info - BUILD=$(BUILD))
	$(info - PIP=$(PIP))
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
pipenv-install: #> Install development dependencies with pipenv
	$(PIPENV) install --dev

.PHONY: sdist
sdist: $(artifact_sdist) #> Build the source distribution
	@:

.PHONY: sdist-contents
sdist-contents: $(artifact_sdist) #> Show what's inside the sdist
	$(TAR) tfz $(artifact_sdist)

.PHONY: wheel
wheel: $(artifact_wheel) #> Build the wheel
	@:

.PHONY: wheel-contents
wheel-contents: $(artifact_wheel) #> Show what's inside the wheel
	$(UNZIP) -l $(artifact_wheel)

.PHONY: wheel-install
wheel-install: $(artifact_wheel) #> Install the wheel as a regular package
	$(PIP) install .

$(artifact_sdist): $(sources)
	$(BUILD) --sdist

$(artifact_wheel): $(sources)
	$(BUILD) --wheel

#. STANDARD TARGETS

.PHONY: all
all: $(artifact_sdist) $(artifact_wheel) #> Build all artifacts
	@:

.PHONY: clean
clean: #> Remove files built from these sources
	$(RM) -r build dist $(package_id).egg-info

.PHONY: install
install: wheel-install #> Install wheel
	@:

.PHONY: test
test:
	@:

#. SUPPORT TARGETS

.PHONY: check
check: check-bin #> Check if artifacts were installed correctly
	@:

.PHONY: check-bin
check-bin:
	@type marvin &> /dev/null || ( echo "marvin: not found"; exit 1 )

.PHONY: debug
debug: _debug-prefix debug-artifacts debug-programs debug-sources

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==setuptools: flat structure==)

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

.PHONY: install-tools
install-tools: homebrew-install #> Install development tools
	@:

.PHONY: homebrew-install
homebrew-install:
	$(BREW) bundle install
