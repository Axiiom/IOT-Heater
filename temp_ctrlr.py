import Adafruit_DHT
import requests
import json

# retrieve settings
with open("config.json") as file:
    settings = json.loads(file.read())
    BASE_URL = "%s/%s" % (settings["HUE_URL"], settings["HUE_APIK"])
    HEATER_URL = "%s/lights/%d/state" % (BASE_URL, settings["HEATER_ID"])
    LIGHT_URL = "%s/lights/%d/state" % (BASE_URL, settings["LIGHT_ID"])

    SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = int(settings["DHT_PIN"])


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
