#. ==(Brode)sode==

.PHONY: default
default: all

include ../../make.d/help.mk ../../make.d/pre-commit.mk

## Sources

## Artifacts

## Paths

## Programs

.PHONY: debug-programs
debug-programs:
	$(info Programs:)
	@:

## Project

# https://stackoverflow.com/a/17845120/112682
SUBDIRS := manual python

.PHONY: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: debug-project
debug-project:
	$(info Project:)
	$(info - SUBDIRS: $(SUBDIRS))
	@:

#. STANDARD TARGETS

.PHONY: all
all: $(SUBDIRS) #> Build all projects

.PHONY: clean
clean: $(SUBDIRS) #> Remove local build files

.PHONY: install
install: $(SUBDIRS) #> Copy artifacts to shared location

.PHONY: test
test: $(SUBDIRS) #> Run tests

.PHONY: uninstall
uninstall: $(SUBDIRS) #> Remove artifacts from shared location

#. SUPPORT TARGETS

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-programs debug-project $(SUBDIRS) #> Show debugging information

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==(Brode)sode==)
	@:

.PHONY: install-assets
install-assets: $(SUBDIRS)

.PHONY: install-tools
install-tools: $(SUBDIRS)
