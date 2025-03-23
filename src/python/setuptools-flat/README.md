# Setuptools with a flat directory structure

Learn how to use setuptools with one a standardized, flat directory structure.

This tutorial uses [`build`](https://build.pypa.io/en/stable/) to interface with `setuptools`.
`build` can be installed in a variety of ways:

- install with Homebrew and invoke with `pyproject-build`
- install in pipenv-managed virtualenv with `pipenv run pip install --upgrade build` and invoke with
  `pipenv run build ...`.

Source: <https://setuptools.pypa.io/en/latest/userguide/quickstart.html>

## Create package

```shell
pipenv run python -m build
```

or `make`, for short.  Artifacts appear in `dist/`.

## Install package with pipx

The Homebrew-based installation of Python will complain if you try to install packages with `pip`
and instead point you to other homebrew packages and/or virtualenv.  So use `pipx` for this. It
looks analogous to `npx` for Node.js.

Install the package with this:

```shell
pipx install .
```

or

```shell
pipx install <path/to/setuptools-flat>
```

## Install editable package with pipx

Install the package using links instead of copying the package, so that editing sources in the
project gets reflected when you use the package and/or use its scripts in the outside world.

```shell
pipx install --editable .
```

## Run local code with python

```shell
pipenv run python setuptoolsflat/cli.py
```

## Run local code with pipenv script

```shell
pipenv run main-call
```
