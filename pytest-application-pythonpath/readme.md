# `pytest` an application via `PYTHONPATH`

Use `pytest` to test an application that is distributed as top-level code,
setting `PYTHONPATH` to allow test code to locate production code.

Using `pytest` drives reflection on several questions about structure,
packaging, and distribution.


## Summary

|                        | Prod Code               | Test Code                     |
|------------------------|-------------------------|-------------------------------|
| **Sources**            |                         |                               |
| Packaging              | No `__init__.py`        | No `__init__.py`              |
| Distribution           | `.zip` (no `setup.py`)  | N/A                           |
| Import Prod As         | Top-level module        | Top-level module              |
| Import Test            | N/A                     | Top-level module              |
|                        |                         |                               |
| **Dev Environment**    |                         |                               |
| Repository Location    | `src/module.py`         | `tests/test_module.py`        |
| Run With               | `python src/<main.py>`? | `pytest [module_test.py] ...` |
| PYTHONPATH             | `src`?                  | `src`                         |
|                        |                         |                               |
| **Target Environment** |                         |                               |
| Location               | `.` (`$CWD`)            | N/A                           |
| Run With               | `python `               | N/A                           |
| PYTHONPATH             | -                       | N/A                           |


## Discussion
### Production module structure (target environment)

_How will production code be installed on the target environment?_

1. as a distrubtion, with no other code trying to load it as a package?
2. as a package, that other code will `import` as a dependency?

Put another way: _How will others import production code?_

1. as top-level modules: `from <module_name> import <symbol>`
2. as a package: `from <package_name> import <symbol>`

Since this is an example of a top-level application:

* Entrypoint: `python <main module file> [arguments...]`
* Production code location: top-level modules (files), in the current working
  directory
* Production code imports itself as: top-level modules.  For example:

    ```python
    #main.py
    from <some_module> import <symbol>

    #some_module.py
    from <module_name> import <symbol>
    ```


### Production module structure (source repository)

_Where is production code located, in the source code repository?  Is that
location different than where it will be located, in the target environment?_

In this case:

* Location of production code in repository: `src/`
* Location of production code in target environment: `.` (different)
* Form of production code: Modules, not packages.  There are no `__init__.py`
  files or `setup.[cfg|py]` files.


### How test code locates production sources

Tests will import from top-level modules, without installing anything as a
package first.  So use `PYTHONPATH=src` when running `pytest`, so that test code
can load production sources without going through any \[local\] packages or
links.


## Future Work

1. Run some sort of `main.py` to see if the production code can load ok.
1. Can `pytest` run in watch mode?  Looks like it can: https://stackoverflow.com/questions/35097577/pytest-run-only-the-changed-file/35101867
