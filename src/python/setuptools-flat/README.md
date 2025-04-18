# Setuptools with a flat directory structure

Learn how to use setuptools with one a standardized, flat directory structure.

This tutorial uses [`build`](https://build.pypa.io/en/stable/) to interface with `setuptools`.
`build` can be installed in a variety of ways:

- install with Homebrew and invoke with `pyproject-build`
- install in pipenv-managed virtualenv with `pipenv run pip install --upgrade build` and invoke with
  `pipenv run build ...`.

Source: <https://setuptools.pypa.io/en/latest/userguide/quickstart.html>

## Code structure

This tutorial is using the "flat layout", such as in this example:

```shell
project_root_directory
├── pyproject.toml  # AND/OR setup.cfg, setup.py
├── ...
└── mypkg/
    ├── __init__.py
    ├── ...
    ├── module.py #contains run_main function
    ├── subpkg1/
    │   ├── __init__.py
    │   ├── ...
    │   └── module1.py
```

Specifically:

- `pyproject.toml` et al live in the project's root directory
- Each package (a directory containing `__init__.py`) is in its own directory just beneath the
  project root.  Note that packages are generally named all lowercase without dashes, to avoid
  incompatible syntax (e.g. `-` gets interpreted as the minus function).
- Modules are source files within each package, containing functions, classes, etc...
- Scripts and entrypoints refer to these with "entrypoint syntax": `package.module:function`.  In
  this example, it would be `dothething = "mypkg.module:run_main"`.

Source: <https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#flat-layout>

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
