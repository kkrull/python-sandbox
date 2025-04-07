import logging
import os
from argparse import Action
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


DefaultArg = TypedDict("DefaultArg", {"default": str})
OptionalArg = TypedDict("OptionalArg", {"required": Literal[False]})
RequiredArg = TypedDict("RequiredArg", {"required": Literal[True]})


## add_argument decorators


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
