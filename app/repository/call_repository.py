from operator import itemgetter

from app.db.database import driver
from app.db.models import Device, ConnectRelation, Location
import toolz as t

from app.repository.call_queries import insert_call_query, connect_devices_query, get_bluetooth_connection_query, \
    devices_stronger_than_60_query, connected_devices_query, get_direct_connection_query, latest_timestamp_query


def create_device(device: Device, location: Location) -> str:
    with driver.session() as session:
        query = insert_call_query

        params = {
            "uuid": device.uuid,
            "name": device.name,
            "brand": device.brand,
            "model": device.model,
            "os": device.os,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "altitude_meters": location.altitude_meters,
            "accuracy_meters": location.accuracy_meters
        }
        result = session.run(query, params).single()
        print(f"device with id {device.uuid} was created")
        return t.pipe(
            result,
            dict,
            itemgetter("id")
        )


def connect_devices(relation: ConnectRelation):
    with driver.session() as session:
        try:
            query = connect_devices_query
            params = {
                "from_device": relation.from_device,
                "to_device": relation.to_device,
                "method": relation.method,
                "bluetooth_version": relation.bluetooth_version,
                "signal_strength_dbm": relation.signal_strength_dbm,
                "distance_meters": relation.distance_meters,
                "duration_seconds": relation.duration_seconds,
                "timestamp": relation.timestamp
            }
            result = session.run(query, params).single()
            print(f"connection from {relation.from_device} to {relation.to_device} was created")
            return t.pipe(
                result,
                dict,
                itemgetter("rel"),
                dict
            )
        except Exception as e:
            print(str(e))


def get_all_bluetooth_connection():
    with driver.session() as session:
        try:
            query = get_bluetooth_connection_query
            result = session.run(query).data()
            return result
        except Exception as e:
            print(str(e))


def get_all_devices_with_signal_stronger_than_60():
    with driver.session() as session:
        try:
            query = devices_stronger_than_60_query
            result = session.run(query).data()
            return result
        except Exception as e:
            print(str(e))


def get_connected_devices_by_id(device_id: str):
    with driver.session() as session:
        try:
            query = connected_devices_query
            params = {
                "id": device_id
            }
            result = session.run(query, params).data()
            return result
        except Exception as e:
            print(str(e))


def get_direct_connection(device1_id: str, device2_id: str):
    with driver.session() as session:
        try:
            query = get_direct_connection_query
            params = {
                "id_1": device1_id,
                "id_2": device2_id
            }
            result = session.run(query, params).data()
            return result
        except Exception as e:
            print(str(e))


def get_latest_timestamp_relation(device1_id: str, device2_id: str):
    with driver.session() as session:
        try:
            query = latest_timestamp_query
            params = {
                "id_1": device1_id,
                "id_2": device2_id
            }
            result = session.run(query, params).single()
            return t.pipe(
                result,
                dict,
                itemgetter("max(rel.timestamp)"),
            )
        except Exception as e:
            print(str(e))
