import RPi.GPIO as GPIO
import time

class OilDispenserControl:
    """Control del solenoide d’oli/tomàquet."""
    def __init__(self, pin_solenoid=23, active_time=1.0):
        self.pin = pin_solenoid
        self.active_time = active_time
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def dispense(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(self.active_time)
        GPIO.output(self.pin, GPIO.LOW)
