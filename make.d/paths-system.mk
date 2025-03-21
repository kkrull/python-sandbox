
prefix ?= /usr/local
exec_prefix ?= $(prefix)

## Executable programs that users can run (including symlinks)

bindir := $(exec_prefix)/bin

## Executable programs to be run by other programs, in a subdirectory thereof

libexecdir := $(exec_prefix)/libexec
libexecdirpkg := $(libexecdir)/sode

## Read-only architecture-independent data files, in a subdirectory thereof

datarootdir := $(prefix)/share

datadir := $(datarootdir)
datadirpkg := $(datadir)/sode
$(datadirpkg):
	mkdir -p $(datadirpkg)

mandir := $(datarootdir)/man
man1dir := $(mandir)/man1
man7dir := $(mandir)/man7

.PHONY: debug-system-paths
debug-system-paths:
	$(info Paths:)
	$(info - prefix: $(prefix))
	$(info - exec_prefix: $(exec_prefix))

	$(info - bindir: $(bindir))

	$(info - libexecdir: $(libexecdir))
	$(info - libexecdirpkg: $(libexecdirpkg))

	$(info - datarootdir: $(datarootdir))
	$(info - datadir: $(datadir))
	$(info - datadirpkg: $(datadirpkg))
	@:
