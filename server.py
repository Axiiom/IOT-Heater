import asyncio
import websockets
import json
import random
import time

from _thread import start_new_thread

from state import State

base_state = {
    "temperature": 18,
    "target": 24,
    "deadzone": 0.2,
    "on": True
}

g_state = State(**base_state)

async def update_clients():
    rep = repr(g_state)
    await asyncio.wait( [client.send(rep) for client in g_state.CONNECTIONS] )

async def echo(websocket, path):
    g_state.CONNECTIONS.add(websocket)
    try:
        await websocket.send(repr(g_state))
        while True:
            print("waiting for message")
            data = await websocket.recv()
            js = json.loads(str(data))
            if js["action"] == "update":
                await update_clients()
                print("Updating ... ")
                print(js)
            else:
                print("Sending data ... ")
                print(js)

            await websocket.send(repr(g_state))
    finally:
        g_state.CONNECTIONS.remove(websocket)

async def monitor():
    def get_temperature():
        return random.randint(0,100)

    while True:
        temperature = get_temperature()
        
        if g_state.temperature != temperature:
            await update_clients()
        else:
            g_state.temperature = temperature

        print(f"STATE: {repr(g_state)}")
        time.sleep(1)


# begin listening
start_server = websockets.serve(echo, "localhost", 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(monitor)

asyncio.get_event_loop().run_forever()
