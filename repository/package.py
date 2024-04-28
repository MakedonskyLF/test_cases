from collections.abc import Hashable
from dataclasses import dataclass

from rpm_vercmp import vercmp


@dataclass
class Package:
    """Class for representing package"""

    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str

    def getid(self) -> Hashable:
        """Returns unique package identifier"""
        return (self.name, self.arch)

    def isnewer(self, other_package: "Package") -> bool:
        """Compare package version with version of other package according RPM Package Manager version comparison algorithm

        Args:
            other_package (Package): Other package to compare

        Returns:
            bool: is self newer than other package
        """
        if self.getid() != other_package.getid():
            raise ValueError("Trying to compare version of different packages.")

        if self.version == other_package.version:
            return vercmp(self.release, other_package.release) == 1
        else:
            return vercmp(self.version, other_package.version) == 1
