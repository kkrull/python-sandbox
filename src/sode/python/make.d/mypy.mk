#. PYTHON SUPPORT TARGETS [MYPY]

MYPY ?= $(PIPENV) run mypy-check

.PHONY: clean-mypy
clean-mypy:
	$(RM) -r .mypy_cache

.PHONY: mypy-check
mypy-check: #> Type check sources with mypy
	$(PIPENV) run mypy-check

.PHONY: mypy-watch
mypy-watch: #> Type check sources with mypy (watch mode)
	$(FSWATCH) $(FSWATCHFLAGS) --one-per-batch --recursive -d $(sources_dir) -0 \
		| xargs -0 -I {} $(MYPY) $(sources_dir)
