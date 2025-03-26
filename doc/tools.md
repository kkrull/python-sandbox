# Tools

## [Black](https://black.readthedocs.io/en/stable/index.html)

_The uncompromising code formatter_

- Documentation:
  - Configuration: <https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-via-a-file>
  - Version control integration: <https://black.readthedocs.io/en/stable/integrations/source_version_control.html#version-control-integration>
- Files:
  - `pyproject.toml`: `[tool.black]` section.
- Related tools:
  - [`pre-commit`](#pre-commit)

## [`checkmake`](https://github.com/mrtazz/checkmake)

_checkmake is an experimental tool for linting and checking Makefiles._

- Documentation:
  - pre-commit usage: <https://github.com/mrtazz/checkmake?tab=readme-ov-file#pre-commit-usage>
- Files:
  - `.checkmake-module.ini`
- Related tools:
  - [GNU Make](#gnu-make)
  - [`pre-commit`](#pre-commit)

## [Code Spell Checker](https://cspell.org/) (`cspell`)

_Spell checker_

- Documentation:
  - <https://github.com/streetsidesoftware/vscode-spell-checker>
- Files:
  - `cspell.config.yaml`: configuration file and dictionary
- Related tools:
  - [`pre-commit`](#pre-commit): Runs checks for this tool.
- VS Code extensions:
  - <https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker>

## [`direnv`](https://direnv.net/)

_Integrates environment management with your shell (e.g. `bash` or `zsh`)._

- Documentation:
  - Getting Started: <https://direnv.net/#getting-started>
  - Standard library: <https://direnv.net/man/direnv-stdlib.1.html>
- Files:
  - `.envrc`: loads application settings and any machine-specific settings into your environment.
  - `.envrc.local`: machine-specific settings, which are excluded from source control to avoid
    exposing secrets.
  - `.envrc.local.example`: an example of settings for various operating systems, which can be used
    as a template for creating `.envrc.local`.
- Installation:
  - Homebrew: `brew install direnv`
    **Note: Follow instructions about updating `.bashrc` or `.zshrc`**.

## [EditorConfig](https://editorconfig.org/)

_Defines basic parameters for formatting source files._

- Documentation:
  - Configuration: <https://editorconfig.org/>
  - Formal specification: <https://spec.editorconfig.org/>
- Files:
  - `.editorconfig`: configuration file
- Related tools:
  - [`pre-commit`](#pre-commit): Runs checks for this tool.

## [GNU Make](https://www.gnu.org/software/make/)

_Automates project-related tasks, such as rendering project audio._

- Documentation:
  - Makefile Style Guide: <https://style-guides.readthedocs.io/en/latest/makefile.html>
  - Manual: <https://www.gnu.org/software/make/manual/make.html>
  - Portable Makefiles: <https://www.oreilly.com/openbook/make3/book/ch07.pdf>
- Files:
  - `Makefile`

## [isort](https://pycqa.github.io/isort/index.html)

_isort your imports, so you don't have to._

- Documentation:
  - Options: <https://pycqa.github.io/isort/index.html>
  - Pre-commit integration: <https://pycqa.github.io/isort/docs/configuration/pre-commit.html>
- Files:
  - `pyproject.toml`: `[tool.isort]` section.
- Related tools:
  - [`pre-commit`](#pre-commit)

## [Markdown](https://daringfireball.net/projects/markdown/)

_File format and syntax for documentation._

- Documentation:
  - Syntax: <https://daringfireball.net/projects/markdown/syntax>
- VS Code extensions:
  - <https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one>

## [Markdownlint](https://github.com/DavidAnson/markdownlint-cli2) (`markdownlint-cli2`)

_Checks Markdown files for style or formatting errors._

- Documentation:
  - Rules: <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>
- Files:
  - `.markdownlint-cli2.jsonc`: configuration file
- Related tools:
  - [`pre-commit`](#pre-commit): Runs checks for this tool.
- VS Code extensions:
  - <https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint>

## [`pre-commit`](https://pre-commit.com/)

_A framework for managing and maintaining multi-language pre-commit hooks in Git repositories._

- Documentation:
  - Configuration file format:
    <https://pre-commit.com/index.html#adding-pre-commit-plugins-to-your-project>
  - Supported hooks: <https://pre-commit.com/hooks.html>
- Files:
  - `.pre-commit-config.yaml`: Defines hooks to run and where they come from
  - `scripts/`: Custom pre-commit scripts that fix issues when the project is on a WSL filesystem.

### Installation

- Install `pre-commit` with your favorite package manager:
  - Debian: `apt install pre-commit`
  - Homebrew: `brew install pre-commit`
- `pre-commit install`: Install Git hooks in this repository.

## [Pipenv](https://pipenv.pypa.io/en/stable/index.html)

_a Python virtualenv management tool that supports a multitude of systems and nicely bridges the
gaps between pip, python (using system python, pyenv or asdf) and virtualenv._

- Documentation:
  - Advanced usage: <https://docs.pipenv.org/advanced/>
  - Custom script shortcuts: <https://pipenv.pypa.io/en/latest/scripts.html>
  - Environment configuration: <https://pipenv.pypa.io/en/latest/shell.html>
  - Installation: <https://pipenv.pypa.io/en/stable/installation.html>
- Files
  - `Pipfile`
  - `Pipfile.lock`
- Related:
  - Pipenv is a better way to install [Python](#python-3).
  - Pipenv can use [pyenv](#pyenv) to install Python.

## [Python 3](https://www.python.org/)

_Python is a programming language that lets you work quickly and integrate systems more effectively_

- Documentation:
  - Library reference: <https://docs.python.org/3.13/library/index.html>
- Related:
  - Override the path to the Python executable you want with [`direnv`](#direnv)
  - Automate installation with [Pipenv](#pipenv).
  - Automate installation with [pyenv](#pyenv).

## [pyenv](https://github.com/pyenv/pyenv)

_pyenv lets you easily switch between multiple versions of Python._

- Documentation:
  - Installation: <https://github.com/pyenv/pyenv?tab=readme-ov-file#installation>
- Related:
  - `pyenv` is a better way to install [Python](#python-3).
