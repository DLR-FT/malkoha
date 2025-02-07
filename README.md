# Malkoha

Yet another utility for tracing source code to requirements. Traces are written as a stream of JSON objects.

## Usage

Annotate parts of your code with requirement IDs.

```python
from malkoha import trace_requirements


@trace_requirements("Req123", "Re234")
def a():
    pass


@trace_requirements("Re234", "Re5")
class B:
    pass
```

Then run `malkoha` to generate `malkoha.json`.
