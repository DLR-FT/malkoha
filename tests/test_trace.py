from malkoha import get_traces
from importlib import resources

from tests import res


def test_read_traces():
    project = resources.files(res).joinpath("test_package")
    traces = [r.requirement_id for r in get_traces(project)]

    assert traces.sort() == ["Req123", "Re234", "Re234", "R5"].sort()
