from flask import g

import Adafruit_DHT
import requests
import time
import threading

from config import Config
from db.models import TemperatureHistory

# setup climate control system
url = f"http://{(Config.hue_ip)}/api/{(Config.hue_apik)}"
heater_url=f"{url}/lights/5/state"
light_url=f"{url}/lights/4/state"

# Setup Temperature Sensor #
SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# climate control functions #
def get_temperature():
    _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return temperature

def heat():
    color = { "on": True,  "bri": 239, "hue": 42637, "sat": 254 }
    try:
        requests.put(light_url, json=color)
        requests.put(heater_url, json={"on": True})
    except Exception as e:
        print(e)

def cool():
    color = { "on": True, "bri": 123, "hue": 64570, "sat": 254 }
    try:
        requests.put(light_url, json=color)
        requests.put(heater_url, json={"on": False})
    except Exception as e:
        print(e)

def hold():
    color = { "on": True, "bri": 144, "hue": 7676, "sat": 254 }
    try:
        requests.put(light_url, json=color)
        requests.put(heater_url, json={"on": False})
    except Exception as e:
        print(e)

# global temperature sampling thread
def continuous_sample(q):
    data = None if q.empty() else q.get()

    # initialize data
    target = 72 if data is None else data["climate"]["target"]
    deadzone = 0.5 if data is None else data["climate"]["deadzone"]
    mode = "automatic" if data is None else data["mode"]

    while True:
        if (temperature := get_temperature()) is None:
            continue
        
        data = None if q.empty() else q.get()
        target = target if data is None else data["climate"]["target"]
        deadzone = deadzone if data is None else data["climate"]["deadzone"]
        mode, state = (mode,state) if data is None else data["mode"]

        print("ID:",threading.currentThread().ident)
        print("Temperature:",temperature)
        print(f"Range [{lower_bound} - {upper_bound}]")

        manual_heat = mode == "manual" and state == "heat"
        manual_cool = mode == "manual" and state == "cool"
        if manual_heat or temperature < target-deadzone:
            print("Too cold\n")
            heat()
        elif manual_cool or temperature > target+deadzone:
            print("Too warm\n")
            cool()
        else:
            print("Within deadzone\n")
            hold()

        print("")
        time.sleep(4)
