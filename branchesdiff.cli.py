#! /usr/bin/env python3
# to make executable: chmod +x branchesdiff.cli.py

import argparse
import os
import sys

from branchesdiff import *

__version__ = "2.0.1"


class HiddenPrints:
    """Help class for with statement to abort printing"""

    def __init__(self, verbose: bool = False) -> None:
        self._verbose = verbose

    def __enter__(self):
        if not self._verbose:
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._verbose:
            sys.stdout.close()
            sys.stdout = self._original_stdout


def main(args):
    parser = argparse.ArgumentParser(
        description="Report differences between development branch and stable branch in json format",
        epilog=f"Version {__version__}",
    )

    parser.add_argument("-f", "--file", type=str, help="output to file FILE")
    parser.add_argument("-v", "--verbose", action="store_true", help="print work log")
    parser.add_argument(
        "--dev", type=str, default=cnf.DEV_BRANCH, help="development branch name"
    )
    parser.add_argument(
        "--stable", type=str, default=cnf.STABLE_BRANCH, help="stable branch name"
    )

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(args)

    with HiddenPrints(args.verbose):
        diff = compare(args.dev, args.stable)

    if args.file:
        diff.tofile(args.file)
    else:
        print(diff)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        sys.exit(str(e))
