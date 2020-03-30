import requests
import json


url="http://192.168.1.12/api/eXbpUKQhYxGRtQRgDKAVlVUzyv0BO8WS5erAYWnu/lights"
resp = requests.get(url)

js = resp.json()
index = None
for i, val in js.items():
    if val["name"] == "Heater":
        index = i
        break

heater = js[index] if index is not None else None
if heater is None:
    print("not found")
    exit()

resp = requests.put(f"{url}/{index}/state", json={"on":False})
print(json.dumps(resp.json()))