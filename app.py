# import Adafruit_DHT

from flask import Flask, jsonify, request
import threading, queue, time, json, requests
from threading import Lock
import routes


# setup app
app = Flask(__name__)
# SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def get_temperature():
    # _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return 10

def turn_on():
    url="http://192.168.1.12/api/eXbpUKQhYxGRtQRgDKAVlVUzyv0BO8WS5erAYWnu/lights/1/state"
    requests.put(url, json={"on": True})

def turn_off():
    url="http://192.168.1.12/api/eXbpUKQhYxGRtQRgDKAVlVUzyv0BO8WS5erAYWnu/lights/1/state"
    requests.put(url, json={"on": False})

# global temperature sampling thread
def continuous_sample(q):
    target, deadzone = q.get()
    while True:
        if (temperature := get_temperature()) is None:
            continue

        temperature = int(temperature)
        target, deadzone = (target, deadzone) if q.empty() else q.get()
        rng = list(range(target-deadzone,target+deadzone+1))

        print("ID:",threading.currentThread().ident)
        print("Temperature:",temperature)
        print("Range:",rng)
        if temperature not in rng:
            print("NOT IN RANGE")
            turn_off()
        else:
            print("IN RANGE")
            turn_on()

        print("")
        time.sleep(4)

# global state
gState = {
    "mode": "automatic",
    "climate": {
        "temperature": get_temperature(),
        "target": None,
        "deadzone": None
    }
}

# setup temperature sampler
q = queue.Queue()
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
