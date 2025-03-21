"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

# TODO KDK: Compare to https://github.com/kennethreitz/setup.py/blob/master/setup.py
# https://stackoverflow.com/questions/1471994/what-is-setup-py

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "../README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sode",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version="0.0.2",

    # This one-line description corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Hack away at deadly computing-related scenarios",

    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,

    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",

    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url="https://github.com/kkrull/python-sandbox",

    author="Kyle Krull",
    author_email="",  # Optional

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        "Programming Language :: Python :: 3.13",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="",  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(
        exclude=["contrib", "docs", "tests"],
    ),

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.13, <4",

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects. (Optional)
    extras_require={"dev": [
        "attrs==25.3.0; python_version >= '3.8'",
        "cached-property==2.0.1; python_version >= '3.8'",
        "cerberus==1.3.7; python_version >= '3.7'",
        "certifi==2025.1.31; python_version >= '3.6'",
        "chardet==5.0.0; python_version >= '3.6'",
        "charset-normalizer==3.4.1; python_version >= '3.7'",
        "colorama==0.4.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'",
        'distlib==0.3.9',
        "flake8==7.1.2; python_full_version >= '3.8.1'",
        "idna==3.10; python_version >= '3.6'",
        "mccabe==0.7.0; python_version >= '3.6'",
        'orderedmultidict==1.0.1',
        "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pep517==0.13.1; python_version >= '3.6'",
        "pip==25.0.1; python_version >= '3.8'",
        "pip-shims==0.7.3; python_version >= '3.6'",
        "platformdirs==4.3.7; python_version >= '3.9'",
        "plette[validation]==2.1.0; python_version >= '3.7'",
        "pycodestyle==2.12.1; python_version >= '3.8'",
        "pyflakes==3.2.0; python_version >= '3.8'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'",
        "python-dateutil==2.9.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "requests==2.32.3; python_version >= '3.8'",
        "requirementslib==1.6.9; python_version >= '3.7'",
        "setuptools==77.0.3; python_version >= '3.9'",
        "six==1.17.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'",
        "tomlkit==0.13.2; python_version >= '3.8'",
        "urllib3==2.3.0; python_version >= '3.9'",
        "vistir==0.6.1; python_version not in '3.0, 3.1, 3.2, 3.3' and python_version >= '3.7'",
        "wheel==0.45.1; python_version >= '3.8'",
    ]},

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # Sometimes you’ll want to use packages that are properly arranged with
    # setuptools, but are not published to PyPI. In those cases, you can specify
    # a list of one or more dependency_links URLs where the package can
    # be downloaded, along with some additional hints, and setuptools
    # will find and install the package correctly.
    # see https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    #
    dependency_links=[],

    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={"sample": ["package_data.dat"]},  # Optional
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[("my_data", ["data/data_file"])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={"console_scripts": [
        "sode=sode.sode:main"
    ]},

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        "Bug Reports": "https://github.com/kkrull/python-sandbox/issues",
        "Source": "https://github.com/kkrull/python-sandbox/",
    },
)
