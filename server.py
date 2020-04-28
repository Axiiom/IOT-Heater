import socket, threading, json
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

sock.close()