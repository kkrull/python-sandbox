#. PYTHON SUPPORT TARGETS [ISORT]

ISORT ?= $(PIPENV) run isort-format

.PHONY: isort-check
isort-check: #> Check sources with isort
	$(PIPENV) run isort-check

.PHONY: isort-format
isort-format: #> Format sources with isort
	$(PIPENV) run isort-format

.PHONY: isort-watch
isort-watch: #> Format sources with isort (watch mode)
	$(FSWATCH) $(FSWATCHFLAGS) --one-per-batch --recursive -d $(sources_dir) -0 \
		| xargs -0 -I {} $(ISORT) $(sources_dir)
