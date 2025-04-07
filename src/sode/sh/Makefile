#. ==sode shell scripts==

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

.PHONY: debug-programs
debug-programs:
	$(info Programs)
	@:

## Project

package_id := sode

.PHONY: debug-project
debug-project:
	$(info Project)
	$(info - package_id=$(package_id))
	@:

### Sources

sources := ''

.PHONY: debug-sources
debug-sources:
	$(info Sources:)
	$(info - sources=$(sources))
	@:

### Artifacts

.PHONY: debug-artifacts
debug-artifacts:
	$(info Artifacts:)
	@:

#. STANDARD TARGETS

.PHONY: all
all: #> Build all artifacts
	@:

.PHONY: clean
clean: #> Remove files built from these sources
	@:

.PHONY: install
install: #> Install artifacts
	@:

.PHONY: test
test: #> Run checks
	@:

.PHONY: uninstall
uninstall: #> Uninstall artifacts
	@:

#. SUPPORT TARGETS

.PHONY: check
check: #> Check if artifacts were installed correctly
	@:

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-artifacts debug-paths debug-programs debug-project debug-python debug-sources #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==sode shell scripts==)
	@:

#. DEVELOPMENT ENVIRONMENT TARGETS

.PHONY: install-tools
install-tools: homebrew-bundle-install #> Install development tools
	@:

#. PYTHON TARGETS

PIPX ?= pipx

.PHONY: debug-python
debug-python:
	$(info Python)
	$(info - PIPX=$(PIPX))
	@:

.PHONY: install-argcomplete
install-argcomplete: #> Install argcomplete in its own virtualenv
	@type activate-global-python-argcomplete >/dev/null || $(PIPX) install argcomplete

.PHONY: install-global-completions
install-global-completions: install-argcomplete #> Install a global shell completions function for argcomplete
	activate-global-python-argcomplete

#. SHELL COMPLETION TARGETS
