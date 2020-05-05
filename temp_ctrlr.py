import Adafruit_DHT
import requests

from config import Config


def get_temperature():
    # get temperature and convert to fahrenheit
    _, temperature = Adafruit_DHT.read_retry(Config.SENSOR, Config.DHT_PIN)
    return (temperature * (9/5)) + 32


def heat():
    color = {"on": True, "bri": 239, "hue": 42637, "sat": 254}
    try:
        requests.put(Config.LIGHT_URL, json=color)
        requests.put(Config.HEATER_URL, json={"on": True})
    except Exception as e:
        print(e)


def cool():
    color = {"on": True, "bri": 123, "hue": 64570, "sat": 254}
    try:
        requests.put(Config.LIGHT_URL, json=color)
        requests.put(Config.HEATER_URL, json={"on": False})
    except Exception as e:
        print(e)


def hold():
    color = {"on": True, "bri": 144, "hue": 7676, "sat": 254}
    try:
        requests.put(Config.LIGHT_URL, json=color)
        requests.put(Config.HEATER_URL, json={"on": False})
    except Exception as e:
        print(e)
