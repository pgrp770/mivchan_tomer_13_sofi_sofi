from typing import List

import pytest
from app.db.models import Device, ConnectRelation, Location
from app.service.service_phone_route import from_json_to_device, from_json_to_connect_relation, from_json_to_location, \
    from_json_to_models


@pytest.fixture(scope="module")
def json():
    return {
        "devices": [
            {
                "id": "88f0d56f-f9b0-4de3-a22c-6cf17bf0501a",
                "name": "Travis",
                "brand": "Mccann and Sons",
                "model": "Arrive Morning",
                "os": "CommonOS 7.2",
                "location": {
                    "latitude": 32.4210795,
                    "longitude": 152.867668,
                    "altitude_meters": 2167,
                    "accuracy_meters": 15
                }
            },
            {
                "id": "76070ff0-16d5-48e7-b009-6ab245c3a4c4",
                "name": "Thomas",
                "brand": "Hall-Wu",
                "model": "Law Represent",
                "os": "WhomOS 4.0",
                "location": {
                    "latitude": 12.7029955,
                    "longitude": -31.983685,
                    "altitude_meters": 563,
                    "accuracy_meters": 48
                }
            }
        ],
        "interaction": {
            "from_device": "88f0d56f-f9b0-4de3-a22c-6cf17bf0501a",
            "to_device": "76070ff0-16d5-48e7-b009-6ab245c3a4c4",
            "method": "NFC",
            "bluetooth_version": "4.3",
            "signal_strength_dbm": -43,
            "distance_meters": 8.08,
            "duration_seconds": 32,
            "timestamp": "1976-03-14T12:34:04"
        }
    }


def test_from_json_to_device(json):
    result = from_json_to_device(json["devices"][0])
    assert isinstance(result, Device)

def test_from_json_to_connect_relation(json):
    result = from_json_to_connect_relation(json["interaction"])
    assert isinstance(result, ConnectRelation)


def test_from_json_to_location(json):
    result = from_json_to_location(json["devices"][0]["location"])
    assert isinstance(result, Location)

def test_from_json_to_models(json):
    result = from_json_to_models(json)
    assert isinstance(result, List)