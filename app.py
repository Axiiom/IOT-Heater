# flask imports
from flask import Flask, jsonify, request

# python imports
import threading, queue 

# custom module imports
from config import Config
import util, routes

# setup app
app = Flask(__name__)

# system global state #
gState = {
    "mode": ["automatic", "heat"],
    "climate": {
        "temperature": util.get_temperature(),
        "target": None,
        "deadzone": None
    }
}

# temperature sampler (climate control thread) #
q = queue.Queue()
sampler = threading.Thread(target=util.continuous_sample, args=(q, ))
sampler.setDaemon(True)

# routes #
@app.route("/api/state", methods=["GET"])
def get_state():
    gState["climate"]["temperature"] = util.get_temperature()
    return jsonify({"state": gState})

@app.route("/api/state", methods=["PUT"])
def set_state():
    global gState
    gState = routes.set_state(request, gState)
    q.put( gState )
    return jsonify({"state": gState})

@app.route("/api/history")
def get_history():
    numItems, history = routes.get_history(request)
    return jsonify({ "numItems": numItems, "history": history})
