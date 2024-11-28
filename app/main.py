from flask import Flask

from app.route.phone_tracker_route import phone_blueprint

app = Flask(__name__)

app.register_blueprint(phone_blueprint, url_prefix="/api/phone_tracker")


if __name__ == '__main__':
    app.run(debug=True)