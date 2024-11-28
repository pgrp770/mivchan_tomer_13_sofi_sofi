from typing import Dict
import toolz as t

from app.db.models import Device, ConnectRelation, Location
from app.repository.call_repository import get_direct_connection, create_device, connect_devices, \
    get_connected_devices_by_id


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
    return {"device": from_json_to_device(device), "location": from_json_to_location(device["location"])}


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

    return full_phone_call


def is_the_same_person(phone_call: dict) -> bool:
    device_1: Device = t.get_in(["device_1", "device"], from_json_to_models(phone_call))
    device_2: Device = t.get_in(["device_2", "device"], from_json_to_models(phone_call))

    return device_1.uuid == device_2.uuid


def insert_phone_call_to_neo4j(phone_call):
    create_device(
        t.get_in(["device_1", "device"], from_json_to_models(phone_call)),
        t.get_in(["device_1", "location"], from_json_to_models(phone_call))
    )

    create_device(
        t.get_in(["device_2", "device"], from_json_to_models(phone_call)),
        t.get_in(["device_2", "location"], from_json_to_models(phone_call))
    )

    connect_devices(
        from_json_to_connect_relation(phone_call.get("interaction"))
    )


def get_amount_of_connected_devices(device_id: str):
    return len(get_connected_devices_by_id(device_id))


def is_there_connection(d_1, d_2):
    result = get_direct_connection(d_1, d_2)
    return True if result else False
