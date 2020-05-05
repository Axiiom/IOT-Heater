import asyncio
import websockets
import json
import time
import threading

from state import State
from temp_ctrlr import get_temperature, cool, heat, hold

base_state = {
    "temperature": 18,
    "target": 24,
    "deadzone": 0.2,
    "on": True
}

g_state = State(**base_state)
HOST = json.loads(open("config.json").read())["host"]
PORT = int(json.loads(open("config.json").read())["port"])


async def update_clients():
    rep = repr(g_state)
    await asyncio.wait([client.send(rep) for client in g_state.CONNECTIONS])


async def update_state(js):
    if "temperature" in js:
        g_state.temperature = js["temperature"]
    if "target" in js:
        g_state.target = js["target"]
    if "deadzone" in js:
        g_state.deadzone = js["deadzone"]
    if "on" in js:
        g_state.on = js["on"]


async def server(websocket, path):
    connection = websocket.remote_address[0]
    ws_path = f"ws://{HOST}:{PORT}{path}"

    g_state.CONNECTIONS.add(websocket)
    try:
        while True:
            print("waiting for message")
            data = await websocket.recv()
            print("received message")
            try:
                js = json.loads(str(data))
                if "action" in js and js["action"] == "update":
                    await update_state(js)
                    print("[%s] - %s\n\t%s" % (connection, ws_path, json.dumps(js)))
                else:
                    print("[%s] - %s" % (connection, ws_path))
                    await websocket.send(repr(g_state))

            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    finally:
        g_state.CONNECTIONS.remove(websocket)


def climate_controller():
    while True:
        if g_state.on:
            temperature = get_temperature()
            g_state.temperature = temperature
            too_hot = temperature > g_state.target + g_state.deadzone
            too_cold = temperature < g_state.target - g_state.deadzone
            temp_range = "%.2f - %.2f" % (g_state.temperature - g_state.deadzone, 
                g_state.temperature + g_state.deadzone)

            if too_hot:
                print("%.2f IS TOO HOT, RANGE IS: %s" % ( temperature, repr(temp_range) ))
                cool()
            elif too_cold:
                print("%.2f IS TOO COLD, RANGE IS: %s" % ( temperature, repr(temp_range) ))
                heat()
            else:
                print("%.2f IS JUST RIGHT, RANGE IS: %s" % ( temperature, repr(temp_range) ))
                hold()
        else:
            hold()

        time.sleep(4)


# begin listening
print("Setting up Websocket Server on port 3001 ... ")
start_server = websockets.serve(server, HOST, PORT)
print("Server running")


controller = threading.Thread(target=climate_controller)
controller.daemon = True
controller.start()


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
