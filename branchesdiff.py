import dataclasses
import json
import typing
from collections import defaultdict

import settings as cnf
from repository import API_connector, Package

api_connector = API_connector(cnf.API_URL)


def generate(
    dev_branch_name: str, stable_branch_name: str
) -> typing.Dict[str, typing.Dict[str, list[Package]]]:
    """Compare differences between p10 and sisyphus and organize it

    Args:
        dev_branch_name (str): name for development branch
        stable_branch_name (str): name for stable branch

    Returns:
        typing.Dict[str, typing.Dict[str, list[Package]]]: for each arch contain three lists
        (only in development branch, only in stable branch, in  development branch newer than in stable branch)
    """

    only_dev_branch = f"only_{dev_branch_name}"
    only_stable_branch = f"only_{stable_branch_name}"
    res: typing.Dict[str, typing.Dict[str, list[Package]]] = defaultdict(
        lambda: {only_dev_branch: [], only_stable_branch: [], "newer": []}
    )
    dev_branch = api_connector.get_packages(dev_branch_name)
    stable_branch = api_connector.get_packages(stable_branch_name)
    for key, val in dev_branch.items():
        arch = res[val.arch]
        p10_val = stable_branch.pop(key, None)
        if p10_val:
            if val.isnewer(p10_val):
                arch["newer"].append(val)
        else:
            arch[only_dev_branch].append(val)
    for val in stable_branch.values():
        res[val.arch][only_stable_branch].append(val)
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
