
class Config():
    API_VERSION = "v1"

class Testing(Config):
    DEBUG = True
    TESTING = True
    HOST = "0.0.0.0"
    PORT = 5000
    
    PINS = [(7,11),(8,12)]