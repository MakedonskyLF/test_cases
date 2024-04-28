import typing

import requests

from repository.package import Package


class API_connector:
    def __init__(self, URL: str) -> None:
        self._API_url = URL

    def get_packages(self, branch: str) -> typing.Dict[typing.Any, Package]:
        """Get packages data for branch from API

        Args:
            branch (str): branch name

        Returns:
            typing.Dict[typing.Any, Package]: Packages dict with Package id as a key
        """
        res = {}
        with requests.get(f"{self._API_url}{branch}", stream=True) as r:
            r.raise_for_status()
            for package_json in r.json()["packages"]:
                package = Package(**package_json)
                res[package.getid()] = package
        return res
