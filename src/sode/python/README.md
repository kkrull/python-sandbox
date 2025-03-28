# `sode`

That's 'sode', as in [BRODESODE](https://youtu.be/Cx8sl2uC46A?si=6hLK3-kPXTf-7owI).  If you know,
you know.

`sode` is a wrapper providing one-stop shopping for all my hacking needs.  It's structured like Git,
but with references to healthier recreational activities.  Thusly when you find yourself confronted
by deadly (computing-related) scenarios, take out your brode sode and hack away at it until it stops
moving.

For a much more dull–but perhaps more enlightening–description: This is a top-level command that I
can use to invoke other commands that do various things I'm experimenting with.  Scripts proving to
be sufficiently useful may later graduate to–or re-spawn–in other repositories.  So this is an
incubator for stuff I think may be worth automating, but that doesn't merit its own repository just
yet.

## pipenv

Remember to use `pipenv shell` to set up the python interpreter.  This appears to happen
automatically with the use of a local `.envrc`.

Pipenv automatically loads the contents of `.env` as environment variables when running anything
with pipenv.  In this fashion, it adds the project directory to `PYTHONPATH` so that sode can find
its own sources when running from local sources.

I don't think changes to `PYTHONPATH` will be necessary when running from a pipx-installed package,
but we'll find out soon enough.

## Run like a developer (e.g. from local sources)

### pipenv script

```shell
pipenv run sode-cli --version
```

### python invocation

```shell
pipenv run python ./sode/cli.py --version
```

## Run like a user (e.g. from installed package)

```shell
# from this directory
pipx install [--force] .
sode --version
```

## Setup

### Activate virtual environment

`direnv` should automatically activate the virtualenv for this project.  If it doesn't, use

```shell
pipenv shell
```

### Install packages

```shell
pipenv install --dev
```
