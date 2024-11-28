from dataclasses import dataclass


@dataclass
class Device:
    name: str
    brand: str
    model: str
    os: str
    uuid: str
