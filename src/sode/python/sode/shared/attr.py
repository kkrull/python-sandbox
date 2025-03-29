import typing


def ensure_attr[V](obj: object, name: str, init: V) -> V:
    """Get attribute {name} from {obj}.  Set it to {init} first, if not present."""
    if not hasattr(obj, name):
        setattr(obj, name, init)

    return typing.cast(V, getattr(obj, name))
