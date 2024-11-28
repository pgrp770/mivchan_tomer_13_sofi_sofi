from dataclasses import dataclass
from typing import Optional


@dataclass
class Device:
    name: str
    brand: str
    model: str
    os: str

    uuid: Optional[str] = None
