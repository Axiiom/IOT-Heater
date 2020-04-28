import socket,json, time, threading

HOST = json.loads(open("config.json", 'r').read())["host"]
PORT = json.loads(open("config.json", 'r').read())["port"]

def sendMessages(sock):
    message = "old"
    while message != "exit":
        message = input()
        data = json.dumps({"target": message})
        s.sendall(bytes(data, 'utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    sendingThread = threading.Thread(target=sendMessages, args=(s,) )
    sendingThread.start()

    while True:
        data = s.recv(1024)
        print(json.loads(data))
    
    print("Connection closed")