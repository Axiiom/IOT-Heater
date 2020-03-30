from flask import g

import Adafruit_DHT
import requests
import time

from model import TemperatureHistory

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
    requests.put(light_url, json=color)
    requests.put(heater_url, json={"on": True})

def cool():
    color = { "on": True, "bri": 123, "hue": 64570, "sat": 254 }
    requests.put(light_url, json=color)
    requests.put(heater_url, json={"on": False})

def hold():
    color = { "on": True, "bri": 144, "hue": 7676, "sat": 254 }
    requests.put(light_url, json=color)
    requests.put(heater_url, json={"on": False})


# global temperature sampling thread
def continuous_sample(q):
    target, deadzone = q.get()
    lastState = "hold"
    while True:
        if (temperature := get_temperature()) is None:
            continue

        target, deadzone = (target, deadzone) if q.empty() else q.get()
        lower_bound = target-deadzone
        upper_bound = target+deadzone

        g.db_session.add(TemperatureHistory({
            "temperature": temperature,
            "target": target,
            "deadzone": deadzone,
            "mode": None,
        }))

        print("ID:",threading.currentThread().ident)
        print("Temperature:",temperature)
        print(f"Range [{lower_bound} - {upper_bound}]")

        if temperature < lower_bound and lastState != "heat":
            lastState = "heat"
            print("Too cold\n")
            heat()
        elif temperature > upper_bound and lastState != "cool":
            print("Too warm\n")
            lastState = "cool"
            cool()
        else if lastState != "hold":
            print("Within deadzone\n")
            lastState = "hold"
            hold()

        print("")
        time.sleep(4)