from flask import Blueprint, request, jsonify

from app.repository.call_repository import create_device
from app.service.service_phone_route import from_json_to_models

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():

   phone_call = request.json
   create_device(from_json_to_models(phone_call)["device_1"]["device"], from_json_to_models(phone_call)["device_1"]["location"])
   return jsonify({ }), 200