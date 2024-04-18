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


def generate() -> typing.Dict[str, typing.Dict[str, list[Package]]]:
    """Compare differences between p10 and sisyphus and organize it

    Returns:
        typing.Dict[str, typing.Dict[str, list[Package]]]: for each arch contain three lists
        (only in p10, only in sisyphus, in sisyphus newer than in p10)
    """
    res = defaultdict(lambda: {"only_p10": [], "only_sisyphus": [], "newer": []})
    sisyphus = API_connector.load_package_data("sisyphus.json")
    p10 = API_connector.load_package_data("p10.json")
    for key, val in sisyphus.items():
        arch = res[val.arch]
        p10_val = p10.pop(key, None)
        if p10_val:
            if is_newer((val.version, val.release), (p10_val.version, p10_val.release)):
                arch["newer"].append(val)
                print((val.version, val.release), (p10_val.version, p10_val.release))
        else:
            arch["only_sisyphus"].append(val)
    for val in p10.values():
        res[val.arch]["only_p10"].append(val)
    return res


generate()
# print(generate())
