import Adafruit_DHT


SENSOR = Adafruit_DHT.DHT22
DHT_PIN = int(open("config.json").read()["DHT_PIN")

def get_temperature():
    _, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
    return temperature
