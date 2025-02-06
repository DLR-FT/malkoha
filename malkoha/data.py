from dataclasses import dataclass


@dataclass
class Location:
    name: str
    file: str | None
    line: int | None


@dataclass
class Trace:
    location: Location
    requirement_id: str | None

    def __init__(self, name, file, line, requirement_id):
        self.location = Location(name, file, line)
        self.requirement_id = requirement_id
