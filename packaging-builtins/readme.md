# Python: Dependency Management with `pip`

Uses the built-in `venv` module to set up a separate enviornment for this
project and plain old `pip` to install dependencies.


## Dependency Management

Create a virtual environment once per workspace (i.e. when first cloning this
repository).  **Note that this needs to be redone any time the underlying
directory is renamed**.

```shell
$ python -m venv venv-packaging
$ source ./venv-packaging/bin/activate
```

Install listed dependencies:

```shell
$ pip install -r requirements.txt
```


Install new packages and update requirements, when needed:

```shell
$ pip install ...
$ pip freeze > requirements.txt
```


## Editor (VSCode)

Python needs to be indented with 4 spaces, which differs from my normal settings
I use in VSCode.  Set up a language-specfic setting by adding this to
`settings.json`:

```json
"[python]": {
    "editor.tabSize": 4,
}
```


## Formatting

Format in VSCode as usual, and it will ask you to install a formatting package.
I picked the first choice: `autopep8`, and it can be used directly as follows:

```shell
$ autopep8 -i <file> ...
```


## Running

There's a simple `main.py`.  Run it in either of the following ways:

```shell
$ python main.py #Starts interpreter and runs script with __name__ == '__main__'
$ ./main.py #Uses shebang to do the same thing (including __name__)
```

## Testing

There's a simple unit test using the built-in `unittest` package:

```shell
$ ./test_clock.py
```
