import logging
import os
from argparse import SUPPRESS, Action
from typing import Literal, TypedDict, Union

import argcomplete

logger = logging.getLogger(__name__)

## argcomplete decorators


def completable_argument(
    completer: argcomplete.completers.BaseCompleter,
    action: Action,
) -> Action:
    """Decorates an argument-parsing action with a completer"""

    action.completer = completer  # type: ignore[attr-defined]
    return action


def completion_choices(choices: list[str] = []) -> argcomplete.completers.ChoicesCompleter:
    """Convenience factory to ignore unavoidable typings warning"""

    return argcomplete.completers.ChoicesCompleter(choices=choices)  # type: ignore[no-untyped-call]


## add_argument decorators

DefaultArg = TypedDict("DefaultArg", {"default": str})
HelplessArg = TypedDict("HelplessArg", {"help": str})
OptionalArg = TypedDict("OptionalArg", {"required": Literal[False]})
OptionalArgWithDefault = TypedDict(
    "OptionalArgWithDefault",
    {
        "default": str,
        "required": Literal[False],
    },
)

RequiredArg = TypedDict("RequiredArg", {"required": Literal[True]})


def carrier_of_secrets() -> HelplessArg:
    """
    Exclude argument from command help text so the advertised means of passing secrets is an
    environment variable.  This is safer on most systems, where other users can often see others'
    command-line arguments to running processes but not their environment variables.

    The argument is still available for use when needed, provided you know what you're doing.
    """

    return {"help": SUPPRESS}


def environ_or_default(
    name: str,
    default: str,
    environ: os._Environ[str] = os.environ,
) -> DefaultArg:
    """An argument that has an overridable default."""

    match environ.get(name):
        case str(override):
            return {"default": override}
        case None:
            return {"default": default}


def environ_or_optional(
    name: str,
    environ: os._Environ[str] = os.environ,
) -> Union[DefaultArg, OptionalArg]:
    """An optional argument that can be passed through an environment variable."""

    match environ.get(name):
        case str(secret_value):
            return {"default": secret_value}
        case None:
            return {"required": False}


def environ_or_required(
    name: str,
    environ: os._Environ[str] = os.environ,
) -> Union[DefaultArg, RequiredArg]:
    """An argument that's only required if it's not passed through an environment variable."""

    match environ.get(name):
        case str(secret_value):
            return {"default": secret_value}
        case None:
            return {"required": True}


def optional_with_default(default: str) -> OptionalArgWithDefault:
    """An optional argument with a default value."""

    return {
        "default": default,
        "required": False,
    }
