import dataclasses
import json
import typing
from collections import defaultdict

from .repository import API_connector, Package


class BranchesDiffDict(defaultdict):
    """Class for reporting difference between two branches in json format"""

    class DataclassJSONEncoder(json.JSONEncoder):
        def default(self, val):
            if dataclasses.is_dataclass(val):
                return dataclasses.asdict(val)
            return super().default(val)

    def __str__(self) -> str:
        return json.dumps(self, cls=self.DataclassJSONEncoder)

    def tofile(self, fname: str) -> None:
        json.dump(self, open(fname, "w"), cls=self.DataclassJSONEncoder)


def generate_diff_dict(
    dev_branch_name: str,
    dev_branch: typing.Dict[typing.Any, Package],
    stable_branch_name: str,
    stable_branch: typing.Dict[typing.Any, Package],
) -> BranchesDiffDict:
    """Analyze two dicts with packages and generates BranchesDiffDict

    Args:
        dev_branch_name (str): name of development branch
        dev_branch (typing.Dict[typing.Any, Package]): Development packages dict with Package id as a key
        stable_branch_name (str): name of stable branch
        stable_branch (typing.Dict[typing.Any, Package]): Stable packages dict with Package id as a key

    Returns:
        BranchesDiffDict: for each arch contain three lists (only in development branch,
        only in stable branch, in  development branch newer than in stable branch)
    """
    only_dev_branch_key = f"only_{dev_branch_name}"
    only_stable_branch_key = f"only_{stable_branch_name}"

    res = BranchesDiffDict(
        lambda: {
            only_dev_branch_key: [],
            only_stable_branch_key: [],
            "newer": [],
        }  # default value if missing key
    )

    for id, dev_package in dev_branch.items():
        arch = res[dev_package.arch]
        stable_package = stable_branch.pop(id, None)
        if stable_package:
            if dev_package.isnewer(stable_package):
                arch["newer"].append(dev_package)
        else:
            arch[only_dev_branch_key].append(dev_package)

    for stable_package in stable_branch.values():
        res[stable_package.arch][only_stable_branch_key].append(stable_package)
    return res


def compare(
    apiurl: str, dev_branch_name: str, stable_branch_name: str
) -> BranchesDiffDict:
    """Compare differences between development and stable branches and return it as BranchesDiffDict object

    Args:
        apiurl (str): Address for branches API
        dev_branch_name (str): name of development branch
        stable_branch_name (str): name of stable branch

    Returns:
        BranchesDiffDict: for each arch contain three lists (only in development branch,
        only in stable branch, in  development branch newer than in stable branch)
    """
    api_connector = API_connector(apiurl)
    print(f"requesting branch: {dev_branch_name}")
    dev_branch = api_connector.get_packages(dev_branch_name)
    print("Complete.")
    print(f"requesting branch: {stable_branch_name}")
    stable_branch = api_connector.get_packages(stable_branch_name)
    print("Complete.")

    print("generating report.")
    return generate_diff_dict(
        dev_branch_name, dev_branch, stable_branch_name, stable_branch
    )
