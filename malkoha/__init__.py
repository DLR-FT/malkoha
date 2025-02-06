"""Malkoha sourc code to requirement ID tracing"""

import sys


from argparse import ArgumentParser, Namespace
from xml.etree import ElementTree as ET

from malkoha.decorator import trace_requirements
from malkoha.extract import get_traces


__all__ = ["run", "trace_requirements", "get_traces"]


def run():
    """Runs command"""

    parser = ArgumentParser()
    parser.add_argument("path", nargs="?", help="path to process", default=".")
    parser.set_defaults(func=traces_cmd)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


def traces_cmd(args: Namespace):
    """Writes traces to XML file"""

    traces = ET.Element("traces")
    for trace in get_traces(args.path):
        if trace.requirement_id:
            trace_el = ET.SubElement(
                traces, "trace", requirement_id=trace.requirement_id
            )
        else:
            trace_el = ET.SubElement(traces, "trace")
        if trace.location.file:
            line = str(trace.location.line)
            file = trace.location.file
            location = ET.SubElement(
                trace_el,
                "location",
                line=line,
                file=file,
            )
        else:
            location = ET.SubElement(
                trace_el,
                "location",
            )
        name = trace.location.name
        location.text = f"{name}"
    tree = ET.ElementTree(traces)
    with open("malkoha.xml", "wb") as f:
        tree.write(f)
