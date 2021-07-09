# Pytest structure: Discussion with Christoph


## Discussion

I’m not a fan of having to “install” my code before running tests so I usually
run `python -m pytest` which will find your tests for you (looking for files
starting with `test_` and such). The command above is usually behind a pipenv
command so that I can just run pipenv run test.

I described my python skeleton here as well
https://vanilla-project.guide/python/command-line/

Ah I also forgot the detail of adding a `pytest.ini` config file, so that it
will automatically look inside the tests directory for me

```ini
[pytest]
addopts = --capture=no -vv tests
```

`--capture=no` configures it to not hide any print output from the code (to also
help debugging) and `-vv` increases the verbosity levels of the failure
messages.

Yeah, I prefer the `python -m pytest` option too for much the same reason.

pytest will also auto-detect `_test.py` by the way (a naming convention that I
tend to prefer so that it's easy to see the mirrored file names).

Christoph's Python skeleton page does a good job of explaining how you can avoid
the `import src.my_package` pattern.
