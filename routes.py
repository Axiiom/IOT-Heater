from datetime import datetime, timedelta

# GET  |  /api/state
def get_state(gState):
    return gState

# PUT  |  /api/state
def set_state(request, gState):
    data = request.json
    
    climate = dict() if "climate" not in data else data["climate"]
    if "temperature" in climate:
        gState["climate"]["temperature"] = climate["temperature"]
    if "target" in climate:
        gState["climate"]["target"] = climate["target"]
    if "deadzone" in climate:
        gState["climate"]["deadzone"] = climate["deadzone"]

    gState["mode"] = gState["mode"] if "mode" not in data else data["mode"]
    return ( gState, gState )

# GET  |  /api/state/climate
def get_climate(gState):
    return gState["climate"]


# GET  |  /api/history
def get_history(request):
    args = request.args

    limit = 200 if "limit" not in args else args["limit"]
    granularity = "hourly" if "granularity" not in args else \
        args["granularity"]

    dt_start = datetime.now() if "dt_start" not in args else \
        datetime.strptime("PLACEHOLDER", args["dt_start"])
    dt_end = datetime.now() if "dt_end" not in args else \
        datetime.strptime("PLACEHOLDER", args["dt_end"])

    # TODO: get entries from database
    return jsonify({"message": "not implemented"})


# GET  |  /api/history/temperature
def get_history_climate(request):
    data = get_history(request)[0]["history"]
    history = {
        "history": [ h["climate"] for h in data ],
        "count": len(data)
    }
    
    return jsonify({"message": "not implemented"})