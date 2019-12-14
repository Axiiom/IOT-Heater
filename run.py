import RPi.GPIO as GPIO
from config import Testing as config
from app import app

try:
    GPIO.setmode(GPIO.BOARD)
    for pins in Config.PINS:
        GPIO.setup(pin[0], GPIO.OUT)
        GPIO.setup(pin[1], GPIO.OUT)
    
    if __name__ == '__main__':
        app.run(
            host=Config.HOST,
            port=Config.PORT
        )

except KeyboardInterrupt:
    print("Stopping")

finally:
    GPIO.cleanup()