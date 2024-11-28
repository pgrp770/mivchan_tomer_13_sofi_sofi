from operator import itemgetter

from app.db.database import driver
from app.db.models import Device, ConnectRelation, Location
import toolz as t


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
        print(f"device with id {device.uuid} was created")
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
            query = '''
                    MATCH path = (a:Device)-[r:CALLED_TO*]->(b:Device)
                    WHERE ALL(rel IN relationships(path) WHERE rel.method = 'Bluetooth')
                    RETURN path, length(path)
            '''
            result = session.run(query).data()
            return result
        except Exception as e:
            print(str(e))


def get_all_devices_with_signal_stronger_than_60():
    with driver.session() as session:
        try:
            query = '''
                    MATCH (d1:Device) -[rel:CALLED_TO]->(d2:Device)
                    WHERE rel.signal_strength_dbm > -60
                    RETURN d1
            '''
            result = session.run(query).data()
            return result
        except Exception as e:
            print(str(e))


def get_connected_devices_by_id(device_id: str):
    with driver.session() as session:
        try:
            query = '''
                    MATCH (d1:Device) -[rel:CALLED_TO]->(d2:Device)
                    WHERE d2.uuid = $id
                    RETURN d1
            '''
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
            query = '''
                    match (d1:Device) -[rel:CALLED_TO]- (d2:Device) 
                    where d1.uuid = $id_1 and d2.uuid = $id_2
                    return d1, rel, d2
            '''
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
            query = '''
                    match (d1) -[rel:CALLED_TO] - (d2)
                    where d1.uuid = $id_1 and d2.uuid= $id_2
                    RETURN max(rel.timestamp)
            '''
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


if __name__ == '__main__':
    # a = ConnectRelation(from_device='c0861948-d81c-4ef8-b4f2-a1e7b107e92b', to_device='56acbf2b-ba5e-487b-a073-28153c381869', method='NFC', bluetooth_version='4.3', signal_strength_dbm=-43, distance_meters=8.08, duration_seconds=32, timestamp='1976-03-14T12:34:04')
    # print(connect_devices(a))
    print(get_latest_timestamp_relation("2943920f-bde6-499a-ad07-760d1744dd19", "1086d171-8570-43d6-a1ea-e41cc0440b5e"))
