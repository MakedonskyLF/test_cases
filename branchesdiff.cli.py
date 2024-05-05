#! /usr/bin/env python3
# to make executable: chmod +x branchesdiff.cli.py

import argparse
import os
import sys
from configparser import ConfigParser, SectionProxy

from branchesdiff import *

__version__ = "2.0.4"

__CONFIG_FILE_NAME__ = "config.ini"


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


def load_config(config_file_name: str) -> SectionProxy:
    """Loads configuration parameters for program branchesdiff.cli

    Args:
        config_file_name (str): name of config file

    Returns:
        SectionProxy: dictionary like object with parameters for branchesdiff.cli
    """
    config = ConfigParser()
    config["branchesdiff"] = {"API_URL": "", "DEV_BRANCH": "", "STABLE_BRANCH": ""}
    config.read(config_file_name)
    return config["branchesdiff"]


def set_file_arg_for_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-f", "--file", type=str, help="output to file FILE")


def set_verbose_arg_for_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-v", "--verbose", action="store_true", help="print work log")


def set_dev_arg_for_parser(parser: argparse.ArgumentParser, default: str) -> None:
    parser.add_argument(
        "--dev",
        help="development branch name",
        required=not bool(default),
        type=str,
        default=default,
    )


def set_stable_arg_for_parser(parser: argparse.ArgumentParser, default: str) -> None:
    parser.add_argument(
        "--stable",
        help="stable branch name",
        required=not bool(default),
        type=str,
        default=default,
    )


def set_api_arg_for_parser(parser: argparse.ArgumentParser, default: str) -> None:
    parser.add_argument(
        "--api",
        help="URL for API requests",
        type=str,
        default=default,
        required=not bool(default),
    )


def set_arguments_for_parser(parser: argparse.ArgumentParser, args: list[str]) -> None:
    """Sets up listed arguments for parser according it defaults

    Args:
        parser (argparse.ArgumentParser): parser for setup
        args (list[str]): list of arguments for setting up
    """
    cfg = load_config(__CONFIG_FILE_NAME__)

    if "file" in args:
        set_file_arg_for_parser(parser)
    if "verbose" in args:
        set_verbose_arg_for_parser(parser)
    if "dev" in args:
        set_dev_arg_for_parser(parser, cfg["DEV_BRANCH"])
    if "stable" in args:
        set_stable_arg_for_parser(parser, cfg["STABLE_BRANCH"])
    if "api" in args:
        set_api_arg_for_parser(parser, cfg["API_URL"])


def main(args):
    parser = argparse.ArgumentParser(
        description="Report differences between development branch and stable branch in json format",
        epilog=f"Version {__version__}",
    )

    set_arguments_for_parser(parser, ["file", "verbose", "dev", "stable", "api"])

    args = parser.parse_args(args)

    with HiddenPrints(args.verbose):
        diff = compare(args.api, args.dev, args.stable)

    if args.file:
        diff.tofile(args.file)
    else:
        print(diff)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        sys.exit(str(e))
    else:
        sys.exit(0)
