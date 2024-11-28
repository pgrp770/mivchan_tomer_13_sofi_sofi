from operator import itemgetter

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


def connect_devices(relation: ConnectRelation):
    with driver.session() as session:
        try:
            query = """
                    MATCH
                       (d1: Device{uuid: $from_device}),
                       (d2:Device {uuid: $to_device})
                    CREATE(d1) - [rel: CALLED_TO{
                       method:$method,
                    bluetooth_version:$bluetooth_version,
                       signal_strength_dbm:$signal_strength_dbm,
                       distance_meters:$distance_meters,
                       duration_seconds:$duration_seconds,
                       timestamp:$timestamp

                   }] -> (d2)
                   RETURN rel
                   """
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

            return t.pipe(
                result,
                dict,
                itemgetter("rel"),
                dict
            )
        except Exception as e:
            print(str(e))

#
if __name__ == '__main__':
    a = ConnectRelation(from_device='c0861948-d81c-4ef8-b4f2-a1e7b107e92b', to_device='56acbf2b-ba5e-487b-a073-28153c381869', method='NFC', bluetooth_version='4.3', signal_strength_dbm=-43, distance_meters=8.08, duration_seconds=32, timestamp='1976-03-14T12:34:04')
    print(connect_devices(a))