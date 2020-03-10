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
    return


# GET  |  /api/history/temperature
def get_history_temperature(request):
    return