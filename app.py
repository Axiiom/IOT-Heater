import Adafruit_DHT, board

from flask import Flask, jsonify, request
import threading, queue, time, json
from threading import Lock
import routes


# setup app
app = Flask(__name__)
SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def get_temperature():
    _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return temperature


# global temperature sampling thread
def continuous_sample(q):

    target, deadzone = q.get()
    while True:
        temperature = get_temperature()
        if not q.empty():
            target, deadzone = q.get()
        
        print(int(temperature))
        print(list(range(target-deadzone,target+deadzone)))
        if int(temperature) not in range( target-deadzone, target+deadzone ):
            print("NOT IN RANGE")
            # toggle the thing
        else:
            print("IN RANGE")

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
'''with open("state.json") as file:
    file = json.loads(file)
    q.put(( file["climate"]["target"], file["climate"]["deadzone"] ))
'''
q.put((23, 2))
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
    with threading.Lock():
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
