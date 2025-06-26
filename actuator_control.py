import time
from gpiozero import PWMOutputDevice

class ActuatorControl:
    """Control del motor de la cinta mitjançant dos pins PWM."""
    def __init__(self, rpwm_pin=18, lpwm_pin=19, default_speed=0.15):
        self.rpwm = PWMOutputDevice(rpwm_pin)
        self.lpwm = PWMOutputDevice(lpwm_pin)
        self.default_speed = default_speed
        self.stop()

    # -------------------- moviments --------------------
    def move_conveyor(self, direction="forward", duration=None, speed=None):
        """Mou la cinta en la direcció indicada; si s’especifica duration, s’atura en acabar."""
        speed = speed if speed is not None else self.default_speed
        if direction == "forward":
            self.rpwm.value = 0            # rodet dret aturat
            self.lpwm.value = speed        # rodet esquerre gira
        elif direction == "backward":
            self.rpwm.value = speed
            self.lpwm.value = 0
        else:
            raise ValueError("direction must be 'forward' or 'backward'")

        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.rpwm.value = 0
        self.lpwm.value = 0

    def cleanup(self):
        self.stop()
