import asyncio
import websockets
import json
import time
import threading

from config import Config
from state import State
from temp_ctrlr import get_temperature, cool, heat, hold

g_state = State(temperature=18.0, target=24.5, deadzone=0.2, on=True)
HOST = Config.HOST
PORT = Config.PORT


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


async def server(websocket, _):
    g_state.CONNECTIONS.add(websocket)

    connection = websocket.remote_address[0]
    print(f"[{connection}] connected!")
    try:
        while True:
            data = await websocket.recv()
            print(f"Received message from {connection}")
            try:
                js = json.loads(str(data))
                if "action" in js and js["action"] == "update":
                    await update_state(js)
                else:
                    await websocket.send(repr(g_state))

            except Exception as e:
                print(e)
    except Exception as e:
        print(f"[{connection} disconnected! - {e}")
    finally:
        g_state.CONNECTIONS.remove(websocket)


def climate_controller():
    while True:
        if g_state.on:
            g_state.temperature = get_temperature()

            lower_bound = g_state.target - g_state.deadzone
            upper_bound = g_state.target + g_state.deadzone
            temp_range = f"{lower_bound} - {upper_bound}"

            if g_state.temperature > upper_bound:
                print("%.2f IS TOO HOT, RANGE IS: %s" % (
                    g_state.temperature, temp_range))
                cool()
            elif g_state.temperature < lower_bound:
                print("%.2f IS TOO COLD, RANGE IS: %s" % (
                    g_state.temperature, temp_range))
                heat()
            else:
                print("%.2f IS JUST RIGHT, RANGE IS: %s" % (
                    g_state.temperature, temp_range))
                hold()
        else:
            hold()

        time.sleep(4)


# begin listening
print("Setting up Web Socket Server on port 3001 ... ")
start_server = websockets.serve(server, HOST, PORT)
print("Server running")

controller = threading.Thread(target=climate_controller)
controller.daemon = True
controller.start()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
