# `sode`

That's 'sode', as in [BRODESODE](https://youtu.be/Cx8sl2uC46A?si=6hLK3-kPXTf-7owI).  If you know,
you know.

`sode` is a wrapper providing one-stop shopping for all my hacking needs.  It's structured like Git,
but with references to healthier recreational activities.  Thusly when you find yourself confronted
by deadly (computing-related) scenarios, _take out your BRODE SODE_...and hack away.

For a more enlightening-if dull-description: This is a top-level command that I can use to invoke
other commands that do various things I'm experimenting with.

Scripts proving to be sufficiently useful may later graduate to–or re-spawn–in other repositories.
So this is an incubator for stuff I think may be worth automating, but that doesn't merit its own
repository just yet.

## Run like a developer (e.g. from local sources)

### pipenv script

```shell
pipenv run sode-cli
```

### python invocation

```shell
pipenv run python ./sode/cli.py
```

## Run like a user (e.g. from installed package)

```shell
# from this directory
pipx install [--force] .
sode
```

## Setup

### Install argcomplete

I haven't thought of a good way to automate this yet, but do this to get tab completion to work:

```shell
# some directory that is *not* here; e.g. outside of the virtualenv
pip install argcomplete
activate-global-python-argcomplete --user
```

Then tab completion works for `sode` as an installed wheel and also for `./sode/cli/main.py` or
`python ./sode/cli/main.py`.

### Use `pipenv`

Remember to use `pipenv shell` to set up the python interpreter.  This appears to happen
automatically with the use of a local `.envrc`.

Pipenv automatically loads the contents of `.env` as environment variables when running anything
with pipenv.  This capability is used to add the project directory to `PYTHONPATH`, so that `sode`
can find its own sources when running from local sources.

### Activate virtual environment

`direnv` should automatically activate the virtualenv for this project.  If it doesn't, use

```shell
pipenv shell
```

### Install packages

```shell
pipenv install --dev
```
