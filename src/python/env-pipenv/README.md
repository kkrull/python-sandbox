# Python: Dependency Management with `pipenv` (More Turtles!)

Try using `pipenv` to manage dependencies in a manner like any sane programming language would do,
without getting hopelessly tangled in a web of shims, environment managers, virtual environments,
and package managers.

## Learnings

`pipenv` seems to handle just about everything, without the need to separately configure `pyenv` or
any kind of virtual environment.

* `pipenv install` should be able to do all the work for installing packages.
* `pipenv shell` and `pipenv run` handle running in the correct environment, with the correct Python
  and the packages listed in `Pipfile`.

Use `python -m site` to display helpful information about the directories from which python will
load packages (`sys.path`).

## Topology

**TL;DR - there are a couple of distinct responsibilities that are managed by several tools, but
`pipenv` rules them all.**

There are two, distinct stacks of tooling with separate–but closely related–responsibilities: the
Python distribution (comprised of the interpreter, tools, and built-in libraries) and the packages
that run on those distributions.

The Python distribution itself of course contains `python` binaries for the interpreter, as well as
a few related tools (`idle`, `pip`, `pydoc`, `wheel`). How does the right version of the Python
interpreter get started when you type `python` or use a shebang at the top of a script?

Starting at the top of the tool chain:

1. Use [`pyenv`](https://github.com/pyenv/pyenv) to install specific versions of Python, in a
   location that will not be affected by system updates.
   * It works by building shims that read the nearest available `pyenv` configuration and load the
     appropriate version of `python` on-the-fly. This works, so long as the shims appear earlier in
     your `$PATH` than the system Python.
   * **It may not be necessary to use `pyenv` to run `python` when using `pipenv`**.  The use of a
     virtual environment seems to cover the Python binaries as well as its libraries and scripts.
1. MacOS has a system installation of Python which will probably remain on version 2.x until the end
   of time and therefore be hopelessly outdated. Its use is frowned upon because it can be upgraded
   out from under you by your OS, and there's always the potential that adding to `site-packages`
   pollutes (breaks) something else really important on your system.

It's also helpful to manage distinct sets of Python packages, instead of putting each projects'
dependencies in a the same, global location.  What defines which versions of which packages will be
available when you `import` modules or run scripts?

Starting at the top of the chain:

1. [`pipenv`](https://pipenv.pypa.io/en/latest/) is the top-level environment manager for Python. It
   appears to be a wrapper around the following tools:
   * `virtualenv` (no mention of using the standard `venv` module?) make and activate virtual
     environments, which:
     * contain links to `python` binaries, reconfiguring your shell to load the intended binary
       instead of the system Python.
     * maintains a distinct directory for just the packages that are used in your project,
       reconfiguring your shell so that `pip` installs packages to that directory and `import` loads
       from it.
   * `pyenv`: If `pyenv` is installed, `pipenv` will use it to install any missing Pythons.
   * `pip` installs the actual packages.  It would put them in `site-packages` or `~/.local/...` and
     affect the entire Python's environment when run outside of a virtual environment, but `pipenv`
     and `virtualenv` ensure that packages are installed to a distinct directory that is unique to
     that environment.
   * A plain environment manager, like `direnv`: it will load `.env` files for you.
