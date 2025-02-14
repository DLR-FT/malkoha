"""Check that tracing does something"""

from importlib import resources

from malkoha import get_traces

from tests import res


def test_read_traces():
    """Read test traces from an example package"""

    project = resources.files(res).joinpath("test_package")
    for r in get_traces(project):
        match r.location.name:
            case "A":
                assert r.requirements == ["Req123", "Re234"]
            case "B":
                assert r.requirements == ["Re234", "Re5"]
            case "Untraced":
                assert r.requirements is None
