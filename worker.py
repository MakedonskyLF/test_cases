import dataclasses
import json
import typing
from collections import defaultdict

from repository import API_connector, Package


def is_newer(val1: tuple[str, str], val2: tuple[str, str]) -> bool:
    """Lexicographic comparison information about two packages

    Args:
        val1 (tuple[str, str]): Version, release of first package
        val2 (tuple[str, str]): Version, release of second package

    Returns:
        bool: is first newer than second
    """
    return val1 > val2


def generate(
    fname1: str, fname2: str
) -> typing.Dict[str, typing.Dict[str, list[Package]]]:
    """Compare differences between p10 and sisyphus and organize it

    Args:
        fname1 (str): file with information about branch 1
        fname2 (str): file with information about branch 2

    Returns:
        typing.Dict[str, typing.Dict[str, list[Package]]]: for each arch contain three lists
        (only in branch 1, only in branch 2, in branch 1 newer than in branch 2)
    """

    only_b1_name = f'only_{fname1.rsplit("/", 1)[-1].split(".")[0]}'
    only_b2_name = f'only_{fname2.rsplit("/", 1)[-1].split(".")[0]}'
    res: typing.Dict[str, typing.Dict[str, list[Package]]] = defaultdict(
        lambda: {only_b1_name: [], only_b2_name: [], "newer": []}
    )
    branch1 = API_connector.load_package_data(fname1)
    branch2 = API_connector.load_package_data(fname2)
    for key, val in branch1.items():
        arch = res[val.arch]
        p10_val = branch2.pop(key, None)
        if p10_val:
            if is_newer((val.version, val.release), (p10_val.version, p10_val.release)):
                arch["newer"].append(val)
        else:
            arch[only_b1_name].append(val)
    for val in branch2.values():
        res[val.arch][only_b2_name].append(val)
    return res


def to_json(diff_dict: typing.Dict[str, typing.Dict[str, list[Package]]]) -> str:
    """Convert dict with dataclasses to json

    Args:
        diff_dict (typing.Dict[str, typing.Dict[str, list[Package]]]): differences between branches

    Returns:
        str: json serialized string
    """

    class DataclassJSONEncoder(json.JSONEncoder):
        def default(self, val):
            if dataclasses.is_dataclass(val):
                return dataclasses.asdict(val)
            return super().default(val)

    return json.dumps(diff_dict, cls=DataclassJSONEncoder)
