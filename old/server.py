'''import socket, threading, json
from _thread import *

import controller 

# connection info
with open("config.json") as file:
    js = json.loads(file.read())
    HOST = js["host"]
    PORT = js["port"]


# create and setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))

# setup climate control thread 
LOCK = threading.Lock()
ctrlr = controller.Controller()
climateController = threading.Thread(
    target=controller.controlClimate,
    args=(ctrlr,)
)
climateController.start()

sock.listen(5)
print(f"Server now awaiting connections on {HOST}:{PORT}")

while True:
    print("\nwaiting for connection")
    conn, addr = sock.accept()
    start_new_thread(
        controller.createConnection, 
        (conn,ctrlr,addr,LOCK)
    )

sock.close()'''
import asyncio
import json
import logging
import websockets
import time
import random
from _thread import start_new_thread

STATE = {"value": 0}
USERS = set()

def state_event():
    return json.dumps({"type": "state", **STATE})


async def notify_users():
    message = state_event()
    await asyncio.wait([u.send(message) for u in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    print("client connected")
    await register(websocket)
    try:
        while True:
            await websocket.send(state_event())
            async for message in websocket:
                STATE["value"] = message
                await notify_users()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await unregister(websocket)

start_server = websockets.serve(counter, "localhost", 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
