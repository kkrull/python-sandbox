# Research

## Discussion with Christoph

I’m not a fan of having to “install” my code before running tests so I usually
run `python -m pytest` which will find your tests for you (looking for files
starting with `test_` and such). The command above is usually behind a pipenv
command so that I can just run pipenv run test.

I described my python skeleton here as well
<https://vanilla-project.guide/python/command-line/>

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

## Discussion with Hana

I also wanted to note that namespace packages (available post-3.3) will allow
for distributing subpackages separately if you're following a monorepo pattern:
<https://packaging.python.org/guides/packaging-namespace-packages/>

## Discussion with Pierce

Are there pytest users out there who create `setup.py` and do `pip install -e
.`, so that the tests run against an installed package (that is sym-linked back
to the working copy in the repository)?  The example from here
(<https://docs.pytest.org/en/6.2.x/goodpractices.html#install-package-with-pip>)
says to put this in `setup.py`:

```python
from setuptools import setup, find_packages
setup(name="PACKAGENAME", packages=find_packages())
```

- [x] Read [Practical
      Python](https://github.com/dabeaz-course/practical-python/blob/master/Notes/09_Packages/00_Overview.md)
      on packaging.
- [ ] Try their examples on package structure with library code and main scripts.
- [ ] Read the [Hitchhiker's
      Guide](https://docs.python-guide.org/writing/structure/) on structure.
- [ ] Read up on
      [`setuptools`](https://setuptools.readthedocs.io/en/latest/userguide/index.html)
      and `setup.py`.
- [ ] Create a package inside this project and install it in editable mode.  See
      how changes are mirrored between source and package files and how `import`
      statements are affected by changes in `setup.py`.

I haven’t encountered the methodology of installing a package first before
testing its internal contents, and I could use a hand understanding the merits
of the approach.

This is a pattern I have used. Installing the package in `-e/editable` mode
"only has to be done once" inside a python `venv`. One benefit of using
`setup.py` is that it strips paths for you. So if you have
`src/my_project/__init__.py` ... and you pass a `package_dir` argument to
`setup()`, something like

```python
setup(
  name="mypackage",
  packages=find_packages(where="src"),
  package_dir={"": "src"}
)
```

Then after pip installing, you can `import my_project` instead of `import
src.my_project`.  The same path stripping is relevant for tests.

The alternative would be to set `PYTHONPATH` to your local package
directory(ies).

One gotcha is that after you do `pip install -e` . you can't rely on the output
of pip freeze to capture 3rd party dependencies. But this isn't a problem with
pipenv and `Pipfile/Pipfile.lock`.

## Future research

Demonstrate pytest with test and sources co-located.

- Try `python -m pytest`
- Read about `python -m pytest` vs `pytest`
- Try the `pytest.ini` file
