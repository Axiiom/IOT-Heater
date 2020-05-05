import json
import websockets
import asyncio

HOST = "192.168.50.184"
PORT = 3005


async def client():
    uri = f"ws://{HOST}:{PORT}"
    async with websockets.connect(uri) as ws:
        while True:
            action = input("(S)end / (R)eceive data: ")
            if action in ["r", "R", "receive"]:
                print("retrieving")
                try:
                    await ws.send(json.dumps({"action": "receive"}))
                    msg = await ws.recv()
                    print(msg)
                except asyncio.TimeoutError as e:
                    print("timeout")
                    print(e)
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
