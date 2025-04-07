#. WHEEL TARGETS

## Artifacts

artifact_wheel = $(wildcard dist/$(package_id)*.whl)
cmd_name := sode
wheel_timestamp := .wheel-timestamp

.PHONY: wheel
wheel: $(wheel_timestamp) #> Build the wheel
	@:

.PHONY: wheel-contents
wheel-contents: wheel #> Show what's inside the wheel
	$(UNZIP) -l $(artifact_wheel)

# Phony target timestamp, to avoid guessing target name of artifact named with source code version
$(wheel_timestamp): $(sources)
	$(BUILD) --wheel
	@touch $@

## Standard sub-targets

.PHONY: clean-wheel
clean-wheel:
	$(RM) $(wheel_timestamp)

.PHONY: install-editable-wheel
install-editable-wheel: wheel #> Link to the wheel globally with pipx
	$(PIPX) install --editable .

.PHONY: install-wheel
install-wheel: $(requirements_obj) wheel #> Install the wheel and its libraries in a globally-available, pipx-managed venv
	$(PIPX) install --force --python=python .
	$(PIPX) runpip $(cmd_name) install -r $(requirements_obj)

.PHONY: uninstall-wheel
uninstall-wheel:
	$(PIPX) uninstall $(package_id)

## Support sub-targets

.PHONY: check-wheel
check-wheel:
	@type $(cmd_name) &> /dev/null || ( echo "$(cmd_name): not found"; exit 1 )

.PHONY: debug-wheel
debug-wheel:
	$(info Artifacts [wheel]:)
	$(info - artifact_wheel=$(artifact_wheel))
	@:

## Program sub-targets

.PHONY: run-wheel
run-wheel: install-wheel #> Run the program from a (re-)installed wheel
	@echo ""
	@$(cmd_name) --version
