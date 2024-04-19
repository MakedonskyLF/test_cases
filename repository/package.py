from dataclasses import dataclass


@dataclass
class Package:
    """class for representing one package"""

    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str
