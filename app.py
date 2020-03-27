from flask import Flask, jsonify, request
import threading, queue, time

import routes


# setup app
app = Flask(__name__)


def get_temperature():
    pass


# global temperature sampling thread
def continuous_sample(q):
    while True:
        temperature = get_temperature()
        if not q.empty():
            target, deadzone = q.get()

        if int(temperature) not in range( target-deadzone, target+deadzone ):
            # toggle the thing
            pass

        time.sleep(5)

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

# setup temperature sampler
q = queue.Queue()
with open("state.json") as file:
    file = json.loads(file)
    q.put(( file["climate"]["target"], file["climate"]["deadzone"] ))

sampler = threading.Thread(target=continuous_sample, args=(q, ))
sampler.start()

# routes
@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(routes.get_state(gState))

@app.route("/api/state", methods=["PUT"])
def set_state():
    global gState
    gState = routes.set_state(request, gState)
    q.put( (gState["climate"]["target"], gState["climate"]["deadzone"]) )
    return jsonify({"state": gState})

@app.route("/api/state/climate")
def get_climate():
    return jsonify(routes.get_climate(gState))

@app.route("/api/history")
def get_history():
    return jsonify(routes.get_history(request))

@app.route("/api/history/climate")
def get_history_climate():
    return jsonify(routes.get_history_climate(request))
