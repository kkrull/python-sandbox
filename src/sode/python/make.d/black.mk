#. PYTHON SUPPORT TARGETS [BLACK]

.PHONY: black-check
black-check: #> Check sources with black
	$(PIPENV) run black-check

.PHONY: black-format
black-format: #> Format sources with black
	$(PIPENV) run black-format
