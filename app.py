from flask import Flask, jsonify, request
import routes

# global state
gState = {
    "mode": None,
    "action": None,
    "climate": {
        "temperature": None,
        "target": None,
        "deadzone": None
    }
}

app = Flask(__name__)

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(routes.get_state(gState))

@app.route("/api/state", methods=["PUT"])
def set_state():
    global gState
    gState, resp = routes.set_state(request, gState)
    return jsonify(resp)

@app.route("/api/state/climate")
def get_climate():
    return jsonify(routes.get_climate(gState))

@app.route("/api/history")
def get_history():
    return jsonify(routes.get_history(request))

@app.route("/api/history/temperature")
def get_temperature():
    return jsonify(routes.get_history_temperature(request))
