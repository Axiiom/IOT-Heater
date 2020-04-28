import json, time, threading, random
from datetime import datetime

class Controller():
    def __init__(self, target=None, on=True):
        self.temperature = 27
        self.target = target
        self.on = on

    def __repr__(self):
        return json.dumps({
            "temperature": self.temperature,
            "target": self.target,
            "on": self.on
        }, indent=4)

def dtstr():
    dt = datetime.now().time()
    return "[%d:%d:%d]" % (dt.hour, dt.minute, dt.second) 

def controlClimate(controller):
    def getTemperature():
        return 0
    
    def hold():
        pass
    
    def warm():
        pass
    
    def cool():
        pass

    while True:
        controller.temperature = getTemperature()
        too_cold = controller.temperature < controller.target - controller.deadzone
        too_warm = controller.temperature > controller.target + controller.deadzone

        if too_cold:
            warm()
        else if too_warm:
            cool()
        else:
            hold()

def createConnection(connection, controller, addr, LOCK):
    addr = "%s:%d" % addr
    print("%s - Client connected: %s" % (dtstr(), addr))

    def sendData(connection, controller, addr):
        try:
            while True:
                print("%s - Sending data to %s" % (dtstr(), addr))
                controller.temperature = random.randint(10,99)
                connection.sendall(bytes(repr(controller), encoding="utf-8"))
                time.sleep(0.05)
        except Exception as e:
            pass

    def recieveData(connection, controller, addr, LOCK):
        while True:
            data = connection.recv(1024)
            if not data:
                break

            print("%s - Recieved data from %s" % (dtstr(), addr))
            try:
                data = json.loads(data)
                with LOCK:
                    controller.target = int(data["target"])
            except:
                continue
    
    incoming = threading.Thread(
        target=sendData, args=(connection, controller, addr))
    try:
        incoming.start()
        recieveData(connection, controller, addr, LOCK) 
    except:
        pass

    connection.close()
    print("%s - Client disconnected: %s" % (dtstr(), addr))
