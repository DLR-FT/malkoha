"""Decorator implementation"""


def trace_requirements(*traced_requirements):
    """Traces an object to a list of requirements"""

    def fun(obj):
        setattr(obj, "__malkoha_traced_requirements__", list(traced_requirements))

        return obj

    return fun
