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
    target = None if data is None else data["climate"]["target"]
    deadzone = None if data is None else data["climate"]["deadzone"]
    automatic = None if data is None else data["mode"]["automatic"]
    action = None if data is None else data["mode"]["action"]

    while True:
        data = data if q.empty() else q.get()
        print("getting temperature")
        if (temperature := get_temperature()) is None or data is None:
            print("continuing")
            continue

        target = data["climate"]["target"]
        deadzone = data["climate"]["deadzone"]
        automatic = data["mode"]["automatic"]
        action = data["mode"]["action"]
        
        print("ID:",threading.currentThread().ident)
        print("Temperature:",temperature)
        print("Deadzone:", deadzone)
        # print(f"Range [{lower_bound} - {upper_bound}]")

        manual_heat = not automatic and action == "heat"
        manual_cool = not automatic and action == "cool"
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
        for i in range(1,5):
            print(f"{i}")
            time.sleep(1)
