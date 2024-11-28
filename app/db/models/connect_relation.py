from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ConnectRelation:

    from_device: str
    to_device: str
    method: str
    bluetooth_version: str
    signal_strength_dbm: float
    distance_meters: float
    duration_seconds: float
    timestamp: str

