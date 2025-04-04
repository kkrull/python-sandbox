import logging
import os
from typing import Literal, TypedDict, Union

logger = logging.getLogger(__name__)

DefaultArg = TypedDict("DefaultArg", {"default": str})
OptionalArg = TypedDict("OptionalArg", {"required": Literal[False]})
RequiredArg = TypedDict("RequiredArg", {"required": Literal[True]})


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
