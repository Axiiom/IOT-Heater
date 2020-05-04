import json
import asyncio


class State():
    def __init__(self, temperature=None, target=None, deadzone=None, on=True):
        self.temperature = temperature
        self.target = target
        self.deadzone = deadzone
        self.on = on

        self.CONNECTIONS = set()
        self.monitor = None

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "target": self.target,
            "deadzone": self.deadzone,
            "on": self.on
        }

    def get_connections(self):
        return [
            conn for conn in self.CONNECTIONS
        ]
