from flask import Flask

from app import app, sampler
from config import Config

import routes

if(__name__ == '__main__'):
    app.config.from_object(Config)

    print("Starting temperature sampling thread ... ")
    sampler.start()
    print("Done")

    print("Starting application")
    app.run(host="0.0.0.0", port=5000, debug=True)
