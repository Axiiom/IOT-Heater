# db imports
from sqlalchemy import Column, Float, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import as_declarative

# python imports
from datetime import datetime


@as_declarative()
class Base(object):
    pass

class TemperatureHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float, nullable=True)
    target = Column(Float, nullable=True)
    deadzone = Column(Float, nullable=True)
    mode = Column(String, nullable=True)
    dt = Column(DateTime, default=datetime.now(), nullable=True)

    def __init__(self, **kwargs):
        super(TemperatureHistory, self).__init__(kwargs)

    def to_dict(self):
        return {
            "mode": self.mode,
            "climate": {
                "temperature": self.temperature,
                "target": self.target,
                "deadzone": self.deadzone
            },
            "dt": self.dt
        }
