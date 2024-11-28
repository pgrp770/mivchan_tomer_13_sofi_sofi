from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    latitude: float
    longitude: float
    altitude_meters: float
    accuracy_meters: float
    uuid: Optional[str] = None