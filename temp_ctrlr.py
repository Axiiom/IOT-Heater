import Adafruit_DHT
import requests
import json

js = json.loads(open("config.json").read())
BASE_URL = "%s/%s" % (js["HUE_URL"], js["HUE_APIK"])
HEATER_URL = "%s/%d/state" % (BASE_URL, js["HEATER_ID"])
LIGHT_URL = "%s/%d/state" % (BASE_URL, js["LIGHT_ID"])

SENSOR = Adafruit_DHT.DHT22
DHT_PIN = int(json.loads(
    open("config.json").read()
)["DHT_PIN"])


def get_temperature():
    _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return temperature


def heat():
    color = { "on": True,  "bri": 239, "hue": 42637, "sat": 254 }
    try:
        requests.put(LIGHT_URL, json=color)
        requests.put(HEATER_URL, json={"on": True})
    except Exception as e:
        print(e)


def cool():
    color = { "on": True, "bri": 123, "hue": 64570, "sat": 254 }
    try:
        requests.put(LIGHT_URL, json=color)
        requests.put(HEATER_URL, json={"on": False})
    except Exception as e:
        print(e)


def hold():
    color = { "on": True, "bri": 144, "hue": 7676, "sat": 254 }
    try:
        requests.put(LIGHT_URL, json=color)
        requests.put(HEATER_URL, json={"on": False})
    except Exception as e:
        print(e)
