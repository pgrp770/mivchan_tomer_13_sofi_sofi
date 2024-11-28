from operator import itemgetter
from typing import Dict

from app.db.database import driver
from app.db.models import Device, ConnectRelation, Location
import toolz as t

'''
phone_call = {
        "device_1": device, location
        "device_2": device, location
        "connection": connection
    }
'''


# def create_phone_call(phone_call: Dict):
#     device_1: Device = phone_call["device_1"]["device"]
#     location_1: Location = phone_call["device_1"]["location"]
#
#     device_2: Device = phone_call["device_2"]["device"]
#     location_2: Location = phone_call["device_2"]["location"]
#
#     connection: ConnectRelation = phone_call["connection"]
#
#
#     with driver.session() as session:
#         query = """
#         MERGE (d1:Device{
#             name: $name
#             brand: $brand
#             model: $model
#             os: $os
#             uuid: $uuid
#         })
#         MERGE (d2:Device{
#             name: $name
#             brand: $brand
#             model: $model
#             os: $os
#             uuid: $uuid
#         }
#
#         """


def create_device(device: Device, location: Location) -> str:
    with driver.session() as session:
        query = """
        MERGE (d:Device{
            uuid: $uuid,
            name: $name,
            brand: $brand,
            model: $model,
            os: $os,
            latitude:$latitude,
            longitude:$longitude,
            altitude_meters:$altitude_meters,
            accuracy_meters:$accuracy_meters      
        })
        RETURN d.uuid AS id
        """

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
        return t.pipe(
            result,
            dict,
            itemgetter("id")
        )

def create_relation_devices(device_id_1: str, device_id_2:str):


    pass

if __name__ == '__main__':
    print(create_device(Device(name='Mary', brand='Thomas-Brown', model='Memory Air', os='PossibleOS 2.5', uuid='91b235e7'), Location(latitude=-8.259944, longitude=82.834984, altitude_meters=4508, accuracy_meters=27)))