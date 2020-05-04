import json
import websockets
import time
import asyncio

HOST = json.loads(open("config.json").read())["host"]
PORT = json.loads(open("config.json").read())["port"]


async def client():
    uri = f"ws://{HOST}:{PORT}"
    async with websockets.connect(uri) as ws:
        while True:
            action = input("(S)end / (R)eceive data: ")
            if action in ["r", "R", "receive"]:
                print("retrieving")
                msg = await ws.recv()
                print(msg)
            else:
                target = float(input("Enter a temperature target: "))
                deadzone = float(input("Enter a new temperature deadzone: "))
                data = json.dumps({
                    "action": "update",
                    "target": target,
                    "deadzone": deadzone
                })

                await ws.send(data)

asyncio.get_event_loop().run_until_complete(client())
asyncio.get_event_loop().run_forever()
