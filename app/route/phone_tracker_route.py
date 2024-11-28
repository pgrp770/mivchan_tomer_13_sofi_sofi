from flask import Blueprint, request, jsonify
import toolz as t
from app.repository.call_repository import create_device, connect_devices, get_all_bluetooth_connection, \
    get_all_devices_with_signal_stronger_than_60, get_connected_devices_by_id, get_latest_timestamp_relation
from app.service.service_phone_route import from_json_to_models, from_json_to_connect_relation, is_there_connection

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
    phone_call = request.json
    create_device(
        t.get_in(["device_1", "device"], from_json_to_models(phone_call)),
        t.get_in(["device_1", "location"], from_json_to_models(phone_call))
    )

    create_device(
        t.get_in(["device_2", "device"],from_json_to_models(phone_call)),
        t.get_in(["device_2", "location"], from_json_to_models(phone_call))
    )
    connect_devices(
        from_json_to_connect_relation(phone_call.get("interaction"))
    )
    return jsonify({}), 200


@phone_blueprint.route("/bluetooth_connection", methods=["GET"])
def get_bluetooth_connection_endpoint():
    result = get_all_bluetooth_connection()
    return jsonify(result), 200


@phone_blueprint.route("/signal_stronger_than_60", methods=["GET"])
def get_all_devices_with_signal_stronger_than_60_endpoint():
    result = get_all_devices_with_signal_stronger_than_60()
    return jsonify(result), 200


@phone_blueprint.route("/connected_devices/<string:device_id>", methods=["GET"])
def get_connected_devices(device_id):
    result = get_connected_devices_by_id(device_id)
    return jsonify(result), 200


@phone_blueprint.route("/check_connection/<string:device_id_1>/<string:device_id_2>", methods=["GET"])
def check_connection(device_id_1: str, device_id_2: str):
    result = is_there_connection(device_id_1, device_id_2)
    return jsonify(result), 200


@phone_blueprint.route("/latest_call/<string:device_id_1>/<string:device_id_2>", methods=["GET"])
def latest_call(device_id_1: str, device_id_2: str):
    result = get_latest_timestamp_relation(device_id_1, device_id_2)
    if not result:
        return jsonify(({"message": "there is not calls between those devices"})), 200
    return jsonify({"latest_call": result}), 200
