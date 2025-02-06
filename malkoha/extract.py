import inspect
import pkgutil
import os

from typing import cast
from importlib.abc import PathEntryFinder, Loader
from importlib.machinery import ModuleSpec
from typing import Iterable
from pathlib import Path

from malkoha.data import Trace


def get_traces(path: Path) -> Iterable[Trace]:
    """Get requirement traces from python code"""

    search_path: str = os.path.abspath(path)
    for info in pkgutil.walk_packages(path=[search_path]):
        finder = cast(PathEntryFinder, info.module_finder)
        spec = cast(ModuleSpec, finder.find_spec(info.name))
        loader = cast(Loader, spec.loader)
        mod = loader.load_module(info.name)

        for name, value in inspect.getmembers(
            mod,
            lambda x: (not inspect.isbuiltin(x))
            and inspect.getmodule(x) == mod
            and (inspect.isclass(x) or inspect.ismodule(x) or inspect.isfunction(x)),
        ):
            try:
                file = inspect.getsourcefile(mod)
                line = inspect.getsourcelines(value)[1]
            except (OSError, TypeError):
                file = None
                line = None
            if hasattr(value, "__malkoha_traced_requirements__"):
                requirements = value.__malkoha_traced_requirements__
                for requirement_id in requirements:
                    yield Trace(
                        name=name,
                        file=file,
                        line=line,
                        requirement_id=requirement_id,
                    )
            else:
                # This means that the object is missing requirements tracing
                yield Trace(
                    name=name,
                    file=file,
                    line=line,
                    requirement_id=None,
                )
