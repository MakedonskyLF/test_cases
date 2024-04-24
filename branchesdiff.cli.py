#! /usr/bin/env python3
# to make executable: chmod +x branchesdiff.cli.py

import argparse
import sys
from tempfile import gettempdir

from requests import HTTPError

from worker import *

__version__ = "1.1.0"


def get_branches_data() -> None:
    try:
        files = API_connector.download_packages_data(folder=gettempdir())
    except HTTPError as e:
        sys.exit(f"API error. {e}")
    except OSError as e:
        sys.exit(f"File error. {e}")
    print("Update complete")
    sys.exit(0)


def generate_json():
    try:
        print(
            to_json(
                generate(f"{gettempdir()}/sisyphus.json", f"{gettempdir()}/p10.json")
            )
        )
    except OSError as e:
        sys.exit(f"File error. {e}")
    sys.exit(0)


def main(args):
    parser = argparse.ArgumentParser(
        description="Print differences between branches sisyphus and p10 in json format",
        epilog=f"Version {__version__}",
    )
    subparsers = parser.add_subparsers()

    parser_update = subparsers.add_parser("update", help="Update packages metadata")
    parser_update.set_defaults(func=get_branches_data)

    parser_generate = subparsers.add_parser(
        "generate", help="Generate json with differences between branches"
    )
    parser_generate.set_defaults(func=generate_json)

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(args)
    args.func()


if __name__ == "__main__":
    main(sys.argv[1:])
