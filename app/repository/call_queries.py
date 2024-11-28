insert_call_query = """
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

connect_devices_query = """
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

get_bluetooth_connection_query = '''
                    MATCH (start:Device)
                    MATCH (end:Device)
                    WHERE start <> end
                    MATCH path = shortestPath((start)-[:CALLED_TO*]->(end))
                    WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
                    WITH path, length(path) as pathLength
                    ORDER BY pathLength DESC
                    LIMIT 1
                    RETURN path
            '''

devices_stronger_than_60_query = '''
                    MATCH (d1:Device) -[rel:CALLED_TO]->(d2:Device)
                    WHERE rel.signal_strength_dbm > -60
                    RETURN d1
            '''

connected_devices_query = '''
                    MATCH (d1:Device) -[rel:CALLED_TO]-> (d2:Device)
                    WHERE d2.uuid = $id
                    RETURN d1
            '''

get_direct_connection_query = '''
                    match (d1:Device) -[rel:CALLED_TO]- (d2:Device) 
                    where d1.uuid = $id_1 and d2.uuid = $id_2
                    return d1, rel, d2
            '''

latest_timestamp_query = '''
                    match (d1) -[rel:CALLED_TO] - (d2)
                    where d1.uuid = $id_1 and d2.uuid= $id_2
                    RETURN max(rel.timestamp)
            '''
