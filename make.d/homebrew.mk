ifneq (, $(shell which brew))
$(info Homebrew detected)
#. HOMEBREW TARGETS

BREW ?= brew

.PHONY: homebrew-bundle-install
homebrew-bundle-install: #> Install packages from `Brewfile` with Homebrew
	$(BREW) bundle install
endif
