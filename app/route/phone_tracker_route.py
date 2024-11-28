from flask import Blueprint, request, jsonify
from app.repository.call_repository import get_all_bluetooth_connection, \
    get_all_devices_with_signal_stronger_than_60, get_latest_timestamp_relation
from app.service.service_phone_route import is_there_connection, insert_phone_call_to_neo4j, \
    get_amount_of_connected_devices

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
    phone_call = request.json
    insert_phone_call_to_neo4j(phone_call)
    return jsonify({"message": "the phone_call was inserted to neo4j"}), 200


@phone_blueprint.route("/bluetooth_connection", methods=["GET"])
def get_bluetooth_connection_endpoint():
    result = get_all_bluetooth_connection()
    return jsonify(result), 200


@phone_blueprint.route("/signal_stronger_than_60", methods=["GET"])
def get_all_devices_with_signal_stronger_than_60_endpoint():
    result = get_all_devices_with_signal_stronger_than_60()
    return jsonify(result), 200


@phone_blueprint.route("/connected_devices/<string:device_id>", methods=["GET"])
def get_amount_connected_devices(device_id):
    result = get_amount_of_connected_devices(device_id)
    return jsonify(result), 200


@phone_blueprint.route("/check_connection/<string:device_id_1>/<string:device_id_2>", methods=["GET"])
def check_connection(device_id_1: str, device_id_2: str):
    result = is_there_connection(device_id_1, device_id_2)
    return jsonify({"there_is_connection": result}), 200


@phone_blueprint.route("/latest_call/<string:device_id_1>/<string:device_id_2>", methods=["GET"])
def latest_call(device_id_1: str, device_id_2: str):
    result = get_latest_timestamp_relation(device_id_1, device_id_2)

    if not result:
        return jsonify(({"message": "there is not calls between those devices"})), 200

    return jsonify({"latest_call": result}), 200
