# flask imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# python imports
import threading, queue 
import Adafruit_DHT

# custom module imports
from config import Config
import util, routes


# setup app
app = Flask(__name__)

# system global state #
gState = {
    "mode": "automatic",
    "climate": {
        "temperature": util.get_temperature(),
        "target": None,
        "deadzone": None
    }
}

# temperature sampler (climate control thread) #
q = queue.Queue()
sampler = threading.Thread(target=util.continuous_sample, args=(q, ))
sampler.setDaemon(True)

@app.before_request
def create_local_db_session():
    g.db_session = Session()


@app.after_request
def destroy_local_db_session(resp):
    try:
        g.db_session.commit()
    except BaseException:
        g.db_session.rollback()
        raise
    finally:
        Session.remove()
        return resp

# routes #
@app.route("/api/state", methods=["GET"])
def get_state():
    gState["climate"]["temperature"] = util.get_temperature()
    return jsonify({"state": gState})

@app.route("/api/state", methods=["PUT"])
def set_state():
    gState = routes.set_state(request, gState)

    target = gState["climate"]["target"]
    deadzone = gState["climate"]["deadzone"]
    q.put( (target, deadzone) )

    return get_state()

@app.route("/api/history")
def get_history():
    return jsonify(routes.get_history(request))
