from flask import Blueprint, request, jsonify

from app.repository.call_repository import create_device, connect_devices, get_all_bluetooth_connection, \
    get_all_devices_with_signal_stronger_than_60
from app.service.service_phone_route import from_json_to_models, from_json_to_connect_relation

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
    phone_call = request.json
    create_device(from_json_to_models(phone_call)["device_1"]["device"],
                  from_json_to_models(phone_call)["device_1"]["location"])
    create_device(from_json_to_models(phone_call)["device_2"]["device"],
                  from_json_to_models(phone_call)["device_2"]["location"])
    connection = from_json_to_connect_relation(phone_call["interaction"])
    print(connection)
    connect_devices(connection)
    return jsonify({}), 200


@phone_blueprint.route("/bluetooth_connection", methods=["GET"])
def get_bluetooth_connection_endpoint():
    result = get_all_bluetooth_connection()
    return jsonify(result), 200


@phone_blueprint.route("/signal_stronger_than_60", methods=["GET"])
def get_all_devices_with_signal_stronger_than_60_endpoint():
    result = get_all_devices_with_signal_stronger_than_60()
    return jsonify(result), 200
