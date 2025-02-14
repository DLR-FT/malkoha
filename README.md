# Malkoha

Yet another utility for tracing source code to requirements.
Traces are written as a stream of JSON objects.
Every symbol, such as a class or a function, in the namespace of a module will generate a trace event.
If the object related to the symbol has been annotated with a list of requirement IDs, they will be contained in a trace event.

## Example output

The function `run` in `command.py` is missing trace information, while the class `Location` in `data.py` traces to the requirements with IDs `malkoha_req_first` and `Req123`.

```plain
{"location": {"name": "run", "file": "/home/schu_t26/git/github.com/DLR-FT/malkoha/malkoha/command.py", "line": 13}, "requirements": null}
{"location": {"name": "Location", "file": "/home/schu_t26/git/github.com/DLR-FT/malkoha/malkoha/data.py", "line": 6}, "requirements": ["Req123", "malkoha_req_first"]}
```

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

Then run `malkoha .` to generate the trace information for modules found in the working directory.

## Finding symbols with missing trace information

```bash
malkoha . | jq '.requirements = null | .location.name'
```
