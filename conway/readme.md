# CodeRetreat Base Project: Python

Base project for python3.  Python 3.8.10, to be exact.


## Requirements

* Python 3 (3.8.10)
* [`pipenv`](https://pipenv.pypa.io/en/latest/): A handy wrapper around other
  python tools, which sets up the environment to use the specified python
  version, sets up a virtual environment for this project, and downloads
  dependencies with `pip`.


## Developer Setup
### Environment variables

Running commands with `pipenv` also sets some additional environment variables
(see the `pipenv` section for details) that are needed when running code (especially tests).


### pipenv

Use [`pipenv`][pipenv-installation] to manage you Python version, virtual
environment, and project-level dependencies.  Install `pipenv` and then use it
to install packages, as follows:

```shell
$ pip install [--user] pipenv #Run once, when setting up development environment
$ pipenv install [--dev] #Run once to install packages, or when packages change
```

`pipenv` also has a handy way to automate common development tasks, with [custom
script shortcuts][pipenv-custom-scripts] that are defined in `Pipfile`:

```shell
$ pipenv scripts #List available scripts
$ pipenv run test #Runs tests, so you don't have to remember how to run pytest
```

`pipenv` will automatically set the environment variables defined in `.env`,
while running any of these scripts.  This automatically sets `PYTHONPATH` to
something compatible with `pytest`, for example, so developers and CI don't have
to set it up manually.

If you are running tests manually–without the benefit of `pipenv` or
`direnv`–you may need to run `pytest` as follows:

```shell
$ PYTHONPATH=src pytest
```

[pipenv-automatic-env]: https://pipenv-fork.readthedocs.io/en/latest/advanced.html#automatic-loading-of-env
[pipenv-custom-scripts]: https://pipenv-fork.readthedocs.io/en/latest/advanced.html#custom-script-shortcuts
[pipenv-installation]: https://pipenv.pypa.io/en/latest/install/#installing-pipenv


## Development

Install dependencies: `pipenv install --dev`

Test with:

* `pipenv` users: `pipenv run test`
* Manually: `PYTHONPATH=src pytest ...`
