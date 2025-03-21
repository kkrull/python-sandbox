# Python: Testing with `pytest`

Trying out [`pytest`](https://docs.pytest.org/en/6.2.x/) to see how it works.

## Python Environment

The Python virtual environment is created and managed by `pipenv`, using `pipenv
--python 3.9`.

## Runtime Environment

[`pipenv` also uses
`python-dotenv`](https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env)
to load data at runtime from a `.env` file, which is useful for keeping secrets
out of source control.

Use `pipenv run init-env` to initialize the file with a template that you can
fill in with your own secrets.

## Testing

Run `pytest` and it does the rest.  Or forget the details and just say `pipenv
run test` (`pipenv scripts` if you forget even the name of the script, which I
am bound to do).

There's a test that makes sure you created an `.env` file.  You can get started
by copying a template, by running `pipenv run init-env` and the modifying `.env`
to fill in your own data.
