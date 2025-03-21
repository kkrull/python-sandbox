#. ==sode manuals==

# Guide: https://eddieantonio.ca/blog/2015/12/18/authoring-manpages-in-markdown-with-pandoc/
# man-pages conventions: https://linux.die.net/man/7/man-pages

.PHONY: default
default: all

include ../../../make.d/help.mk
include ../../../make.d/homebrew.mk
include ../../../make.d/paths-system.mk

### Sources

sources := $(shell find . -type f -name '*.md' | sort)
sources_man1 := $(filter %.1.md,$(sources))
sources_man7 := $(filter %.7.md,$(sources))

.PHONY: debug-sources
debug-sources:
	$(info Sources:)
	$(info - sources: $(sources))
	$(info - sources_man1: $(sources_man1))
	$(info - sources_man7: $(sources_man7))
	@:

## Artifacts

objects := $(patsubst %.md,%,$(sources))
objects_man1 := $(patsubst %.md,%,$(sources_man1))
objects_man7 := $(patsubst %.md,%,$(sources_man7))

.PHONY: debug-artifacts
debug-artifacts:
	$(info Artifacts:)
	$(info - objects: $(objects))
	$(info - objects_man1: $(objects_man1))
	$(info - objects_man7: $(objects_man7))
	@:

### Paths

prefix ?= /usr/local
datarootdir := $(prefix)/share

.PHONY: debug-paths
debug-paths:
	$(info Paths:)
	$(info - datarootdir: $(datarootdir))
	$(info - mandir: $(mandir))
	$(info - man1dir: $(man1dir))
	$(info - man7dir: $(man7dir))
	$(info - prefix: $(prefix))
	@:

## Programs

FSWATCH ?= fswatch

INSTALL ?= install
INSTALLFLAGS := -g 0 -o 0

MANDOC ?= mandoc
PANDOC ?= pandoc
PANDOCFLAGS := -f markdown+definition_lists+line_blocks

.PHONY: debug-programs
debug-programs:
	$(info Programs:)
	$(info - FSWATCH: $(FSWATCH))
	$(info - INSTALL: $(INSTALL))
	$(info - INSTALLFLAGS: $(INSTALLFLAGS))
	$(info - MANDOC: $(MANDOC))
	$(info - PANDOC: $(PANDOC))
	$(info - PANDOCFLAGS: $(PANDOCFLAGS))
	@:

#. GROFF TARGETS

.PHONY: preview
preview: #> Render manuals without building or installing
	$(PANDOC) $(sources) $(PANDOCFLAGS) -s -t man \
		| $(MANDOC)

.PHONY: watch
watch: #> Emit rendered manuals when Pandoc sources change
	$(FSWATCH) $(sources) \
		| xargs -I {} echo "$(PANDOC) {} $(PANDOCFLAGS) -s -t man | $(MANDOC)" \
		| sh

%: %.md
	$(PANDOC) $< $(PANDOCFLAGS) -o $@ -s -t man

#. STANDARD TARGETS

artifacts_installed := $(wildcard $(man1dir)/sode* $(man7dir)/sode*)

.PHONY: all
all: $(objects) #> Build manuals
	@:

.PHONY: clean
clean: #> Remove local build files
	$(RM) $(objects)

.PHONY: install
install: install-man1 install-man7 #> Install manuals to $(mandir)

.PHONY: install-man1
install-man1: $(objects_man1)
	$(INSTALL) $(INSTALLFLAGS) -d $(man1dir)
	$(INSTALL) $(INSTALLFLAGS) -m 0644 $(objects_man1) $(man1dir)

.PHONY: install-man7
install-man7: $(objects_man7)
	$(INSTALL) $(INSTALLFLAGS) -d $(man7dir)
	$(INSTALL) $(INSTALLFLAGS) -m 0644 $(objects_man7) $(man7dir)

.PHONY: test
test:
	@:

.PHONY: uninstall
uninstall: #> Uninstall manuals
	$(RM) $(artifacts_installed)

#. SUPPORT TARGETS

.PHONY: debug
.NOTPARALLEL: debug
debug: _debug-prefix debug-artifacts debug-paths debug-programs debug-sources #> Show debugging information
	@:

.PHONY: _debug-prefix
_debug-prefix:
	$(info ==sode manuals==)
	@:

.PHONY: install-assets
install-assets:
	@:

.PHONY: install-tools
install-tools: homebrew-bundle-install
