#. SOURCE DISTRIBUTION TARGETS

## Artifacts

artifact_sdist = $(wildcard dist/$(package_id)*.tar.gz)
sdist_timestamp := .sdist-timestamp

.PHONY: sdist
sdist: $(sdist_timestamp) #> Build the source distribution
	@:

.PHONY: sdist-contents
sdist-contents: sdist #> Show what's inside the sdist
	$(TAR) tfz $(artifact_sdist)

# Phony target timestamp, to avoid guessing target name of artifact named with source code version
$(sdist_timestamp): $(sources)
	$(BUILD) --sdist
	@touch $@

## Support sub-targets

.PHONY: clean-sdist
clean-sdist:
	$(RM) $(sdist_timestamp)

.PHONY: debug-sdist
debug-sdist:
	$(info Artifacts [sdist]:)
	$(info - artifact_sdist=$(artifact_sdist))
	@:
