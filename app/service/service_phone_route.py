from typing import List, Dict
import toolz as t

from app.db.models import Device, ConnectRelation, Location


def from_json_to_device(device: dict) -> Device:
    new_device = {
        "uuid": device["id"],
        "name": device["name"],
        "brand": device["brand"],
        "model": device["model"],
        "os": device["os"]
    }
    return Device(**new_device)


def from_json_to_connect_relation(relation: dict) -> ConnectRelation:
    new_relation = {
        "from_device": relation["from_device"],
        "to_device": relation["to_device"],
        "method": relation["method"],
        "bluetooth_version": relation["bluetooth_version"],
        "signal_strength_dbm": relation["signal_strength_dbm"],
        "distance_meters": relation["distance_meters"],
        "duration_seconds": relation["duration_seconds"],
        "timestamp": relation["timestamp"]
    }
    return ConnectRelation(**new_relation)


def from_json_to_location(location: dict) -> Location:
    new_location = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "altitude_meters": location["altitude_meters"],
        "accuracy_meters": location["accuracy_meters"]
    }
    return Location(**new_location)


def from_json_to_device_and_location(device) -> Dict:
    return {"device":from_json_to_device(device), "location":from_json_to_location(device["location"])}


def from_json_to_models(json: dict) -> Dict:
    devices = t.pipe(
        json["devices"],
        t.partial(map, from_json_to_device_and_location),
        list
    )
    connection = from_json_to_connect_relation(json["interaction"])
    full_phone_call = {
        "device_1": devices[0],
        "device_2": devices[1],
        "connection": connection
    }
    print(full_phone_call)
    return full_phone_call

if __name__ == '__main__':
    json = {
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

    print(from_json_to_connect_relation(json["interaction"]))
