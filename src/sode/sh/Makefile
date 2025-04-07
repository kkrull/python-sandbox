#. ==sode shell scripts==

.PHONY: default
default: all

include ../../../make.d/help.mk
include ../../../make.d/homebrew.mk

## Environment

### Paths

.PHONY: debug-paths
debug-paths:
	$(info Paths:)
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

sources := $(shell find . -type f -iname '*.sh' | sort)

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
all:
	@:

.PHONY: clean
clean:
	@:

.PHONY: install
install: install-argcomplete install-hint #> Install artifacts
	@:

.PHONY: test
test:
	@:

.PHONY: uninstall
uninstall:
	@:

#. SUPPORT TARGETS

.PHONY: check
check:
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

.PHONY: install-hint
install-hint: #> Tell the user how to install completions
	$(info Completions work by adding this to your shell's local dotfiles:)
	$(info )
	$(info eval "$$(register-python-argcomplete $(package_id))")
	$(info )
	$(info This requires a few things to be true:)
	$(info 1. argcomplete installed as a python package–e.g. pipx install argcomplete.)
	$(info 2. The eval line is called after tab completions–e.g. compinit for zsh–have been initialized.)
	$(info 3. The eval line contains the quotes, as given in the example.)
	@:
