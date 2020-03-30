import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    hue_ip = "192.168.1.12"
    hue_apik = "eXbpUKQhYxGRtQRgDKAVlVUzyv0BO8WS5erAYWnu"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db", "db.db")