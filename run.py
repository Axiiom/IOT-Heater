from flask import Flask
from sqlalchemy import MetaData

from app import app, sampler, engine
from config import Config

from db.models import *
import routes

if(__name__ == '__main__'):
    app.config.from_object(Config)
    # db = SQLAlchemy(app)

    print("Starting temperature sampling thread ... ")
    sampler.start()
    print("Done")

    # print("Initializing database ... ")
    # db.create_all()
    # print("Done")

    print("Starting application")
    app.run(host="0.0.0.0", port=5000, debug=True)
