"""Traces data clases"""

from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    """Location"""

    name: str
    file: str | None
    line: int | None


@dataclass
class Trace:
    """Trace"""

    location: Location
    requirements: List[str] | None

    def __init__(self, name, file, line, requirements):
        self.location = Location(name, file, line)
        self.requirements = requirements
