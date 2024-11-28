from flask import Blueprint, request, jsonify

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200