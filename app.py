# flask imports
from flask import Flask, jsonify, request

# python imports
import threading, queue, time 
import requests, json
import Adafruit_DHT

# custom module imports
from config import Config
import routes


# setup app
app = Flask(__name__)
SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# setup climate control system
url = f"http://{(Config.hue_ip)}/api/{(Config.hue_apik)}"
print(url)
heater_url=f"{url}/lights/1/state"
cooler_url=f"{url}/lights/2/state"
system_url=f"{url}/groups/1/action"


# climate control functions #
def get_temperature():
    _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return temperature

def heat():
    color = { "bri": 123, "hue": 64570, "sat": 254 }
    requests.put(system_url, json=color)

def cool():
    color = { "bri": 239, "hue": 42637, "sat": 254 }
    requests.put(system_url, json=color)

def hold():
    color = { "bri": 144, "hue": 7676, "sat": 254 }
    requests.put(system_url, json=color)


# global temperature sampling thread
def continuous_sample(q):
    target, deadzone = q.get()
    while True:
        temperature = get_temperature()
        if temperature is None:
            continue

        target, deadzone = (target, deadzone) if q.empty() else q.get()
        lower_bound = target-deadzone
        upper_bound = target+deadzone

        print("ID:",threading.currentThread().ident)
        print("Temperature:",temperature)
        print(f"Range [{lower_bound} - {upper_bound}]")

        if temperature < lower_bound:
            print("Too cold\n")
            heat()
        elif temperature > upper_bound:
            print("Too warm\n")
            cool()
        else:
            print("Within deadzone\n")
            hold()

        print("")
        time.sleep(4)

# system global state #
gState = {
    "mode": "automatic",
    "climate": {
        "temperature": get_temperature(),
        "target": None,
        "deadzone": None
    }
}

# temperature sampler (climate control thread) #
q = queue.Queue()
sampler = threading.Thread(target=continuous_sample, args=(q, ))
sampler.setDaemon(True)
sampler.start()

# routes #
@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(routes.get_state(gState))

@app.route("/api/state", methods=["PUT"])
def set_state():
    global gState
    gState = routes.set_state(request, gState)

    target = gState["climate"]["target"]
    deadzone = gState["climate"]["deadzone"]
    q.put( (target, deadzone) )

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
