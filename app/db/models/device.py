from dataclasses import dataclass
from typing import Optional


@dataclass
class Device:
    brand: str
    model: str
    os: str

    uuid: Optional[str] = None
