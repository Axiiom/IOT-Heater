from flask import Flask, jsonify, request, abort
from config import Testing as Config
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config.from_object(Config)
version = Config.API_VERSION


def check_state():
    state = []
    for i in Config.PINS:
        status = GPIO.input(i[0]) == 0 and GPIO.input(i[1]) == 0
        state.append(status)

    return {"heater": state[0], "light": state[1]}


@app.errorhandler(404)
def handle_404(e):
    return jsonify({"message": "invalid endpoint"}), 404


@app.errorhandler(405)
def handle_405(e):
    return jsonify({"message": "method not allowed"}), 405


@app.route(f"/api/{version}/state", methods=["GET"])
def get_state():
    return jsonify({"state": check_state()}), 200


@app.route(f"/api/{version}/state", methods=["POST"])
def set_state():
    try:
        state = request.json['state']
        if len(state) != len(Config.PINS):
            return jsonify({"message": "invalid length for state input"}), 400

        for i in range(len(state)):
            for pin in Config.PINS[i]:
                GPIO.output(pin, state[i])

    except KeyError as e:
        return jsonify({"message": "state information not found in json body"}), 400

    return jsonify({"state": check_state()}), 200
