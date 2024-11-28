from flask import Blueprint, request, jsonify

from app.service.service_phone_route import from_json_to_models

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():

   phone_call = request.json
   from_json_to_models(phone_call)
   return jsonify({ }), 200