"""Malkoha CLI"""

import sys
import json


from argparse import ArgumentParser, Namespace
from dataclasses import asdict

from malkoha.extract import get_traces


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
    """Writes traces to JSON stream"""

    with open("malkoha.json", "w", encoding="utf-8") as f:
        for trace in get_traces(args.path):
            json.dump(asdict(trace), f)
            f.write("\n")
