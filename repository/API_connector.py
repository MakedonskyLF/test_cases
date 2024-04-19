import json
import typing

import requests

from repository.package import Package

__API_url__ = "https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
__branches__ = ("sisyphus", "p10")


def download_file(url: str, fname: str) -> None:
    """Save data on specified url to file fname
    raise HTTPError if request failed

    Args:
        url (str): url to download
        fname (str): file name to save
    """

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def download_packages_data(branch: str = "", folder: str = ".") -> list[str]:
    """Download packages data from API and saves to files named: {folder}/{branch}.json
    raise HTTPError if request failed

    Args:
        branch (str, optional): branch for downloading. If not specified download all known branches.
        folder (str, optional): folder to save results. Defaults to ".".

    Returns:
        list[str]: list of created files
    """

    res = []
    if branch:
        download_file(__API_url__.format(branch=branch), f"{folder}/{branch}.json")
        res.append(f"{folder}/{branch}.json")
    else:
        for _branch in __branches__:
            download_file(
                __API_url__.format(branch=_branch), f"{folder}/{_branch}.json"
            )
            res.append(f"{folder}/{_branch}.json")
    return res


def load_package_data(fname: str) -> typing.Dict[tuple[str, str], Package]:
    """Загружает данные пакетов из файла в словарь.
    Ошибки пробрасываются выше

    Args:
        fname (str): имя файла с сохраненными данными о пакетах

    Returns:
        typing.Dict[tuple[str, str], Package]: словарь пакетов. Ключами являются пары (имя, архитектура)
    """

    packages = json.load(open(fname, "r"))
    return {
        (package["name"], package["arch"]): Package(**package)
        for package in packages["packages"]
    }
