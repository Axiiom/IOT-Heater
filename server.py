import socket, threading, json
from _thread import *

import controller 

# connection info
HOST = json.loads(open("config.json", 'r').read())["host"]
PORT = json.loads(open("config.json", 'r').read())["port"]
LOCK = threading.Lock()

# create socket
sock = socket.socket(
    socket.AF_INET, 
    socket.SOCK_STREAM
)
# bind to port and listen
sock.bind((HOST,PORT))
sock.listen(5)

ctrlr = controller.Controller()
print(f"Server now awaiting connections on {HOST}:{PORT}")
while True:
    print("\nwaiting for connection")
    conn, addr = sock.accept()
    start_new_thread(
        controller.createConnection, 
        (conn,ctrlr,addr,LOCK)
    )

sock.close()