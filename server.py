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
    temperature = g_state.temperature if "temperature" not in js else js["temperature"]
    target = g_state.target if "target" not in js else js["target"]
    deadzone = g_state.deadzone if "deadzone" not in js else js["deadzone"]
    on = g_state.on if "on" not in js else js["on"]

    g_state.temperature = temperature
    g_state.target = target
    g_state.deadzone = deadzone
    g_state.on = on


async def server(websocket, addr):
    g_state.CONNECTIONS.add(websocket)
    try:
        # await websocket.send(repr(g_state))
        while True:
            print("waiting for message")
            data = await websocket.recv()
            try:
                js = json.loads(str(data))
                if "action" in js and js["action"] == "update":
                    await update_state(js)
                    print("Recieved an update on %s - %s" %
                          (f"ws://{HOST}:{PORT}{addr}", json.dumps(js)))

                await websocket.send(repr(g_state))

            except Exception as e:
                print("JSON not found in body")

    finally:
        g_state.CONNECTIONS.remove(websocket)


def climate_controller():
    while True:
        if not g_state.on:
            continue

        temperature = get_temperature()
        too_hot = temperature > g_state.target + g_state.deadzone
        too_cold = temperature < g_state.target - g_state.deadzone
        if too_hot:
            print(f"{temperature} IS TOO HOT")
            cool()
        elif too_cold:
            print(f"{temperature} IS TOO COLD")
            heat()
        else:
            print(f"{temperature} IS JUST RIGHT")
            hold()

        time.sleep(1)


# begin listening

print("Setting up Websocket Server on port 3001 ... ")
start_server = websockets.serve(server, HOST, PORT)
print("Server running")


controller = threading.Thread(target=climate_controller)
controller.daemon = True
controller.start()


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
