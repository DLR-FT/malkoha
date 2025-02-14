"""Decorator implementation"""


def trace_requirements(*traced_requirements):
    """Traces an object to a list of requirements"""

    if not list(traced_requirements):
        raise ValueError(
            "Usage of trace_requirements must spefify at least one requirement ID"
        )

    def fun(obj):
        setattr(obj, "__malkoha_traced_requirements__", list(traced_requirements))

        return obj

    return fun
