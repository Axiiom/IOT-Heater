import Adafruit_DHT


class Config(object):
    __HUE_URL = "http://192.168.1.12/api"
    __BASE_URL = f"{__HUE_URL}/eXbpUKQhYxGRtQRgDKAVlVUzyv0BO8WS5erAYWnu"
    __HEATER_ID = 5
    __LIGHT_ID = 4

    HEATER_URL = f"{__BASE_URL}/lights/{__HEATER_ID}/state"
    LIGHT_URL = f"{__BASE_URL}/lights/{__LIGHT_ID}/state"

    SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4

    HOST = "192.168.50.184"
    PORT = 3005
