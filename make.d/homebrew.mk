#. HOMEBREW TARGETS

BREW ?= brew

.PHONY: homebrew-bundle-install
homebrew-bundle-install: #> Install packages from `Brewfile` with Homebrew
	@type $(BREW) &> /dev/null || exit 0
	$(BREW) bundle install
