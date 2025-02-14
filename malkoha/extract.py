"""Trace information extraction"""

import inspect
import pkgutil
import os

from functools import partial
from types import ModuleType
from typing import cast, Iterable
from importlib.abc import PathEntryFinder, Loader
from importlib.machinery import ModuleSpec
from pathlib import Path

from malkoha.data import Trace


def filter_objects(mod: ModuleType, x: object):
    """Filters objects that should be tracable"""

    return (
        not inspect.isbuiltin(x)
        and inspect.getmodule(x) == mod
        and (inspect.isclass(x) or inspect.ismodule(x) or inspect.isfunction(x))
    )


def get_traces(path: Path) -> Iterable[Trace]:
    """Get requirement traces from python code"""

    search_path: str = os.path.abspath(path)
    for info in pkgutil.walk_packages(path=[search_path]):
        finder = cast(PathEntryFinder, info.module_finder)
        spec = cast(ModuleSpec, finder.find_spec(info.name))
        loader = cast(Loader, spec.loader)
        mod = loader.load_module(info.name)

        for name, value in inspect.getmembers(mod, partial(filter_objects, mod)):
            try:
                file = inspect.getsourcefile(mod)
                line = inspect.getsourcelines(value)[1]
            except (OSError, TypeError):
                file = None
                line = None
            if hasattr(value, "__malkoha_traced_requirements__"):
                requirements = value.__malkoha_traced_requirements__
                yield Trace(
                    name,
                    file,
                    line,
                    requirements,
                )
            else:
                # This means that the object is missing requirements tracing
                yield Trace(
                    name,
                    file,
                    line,
                    requirements=None,
                )
