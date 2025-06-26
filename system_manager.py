import RPi.GPIO as GPIO
import time

from vision_module import VisionModuleLive as VisionModule
from actuator_control import ActuatorControl
from oil_dispenser_control import OilDispenserControl
from config_module import ConfigModule

class SystemManager:
    """Coordina la seqüència completa utilitzant els paràmetres definits a ConfigModule."""

    def __init__(self):
        # --- Configuració de paràmetres ---
        self.cfg = ConfigModule()  # llegeix tots els valors configurables

        # --- LED d'estat ---
        self.led_pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT, initial=GPIO.LOW)

        # --- Mòduls funcionals ---
        self.vision    = VisionModule()
        self.actuators = ActuatorControl()
        self.oil_ctrl  = OilDispenserControl(active_time=self.cfg.oil_active_time)

    # ------------------------------------------------------------
    def run(self):
        """Bucle principal: mou la cinta, detecta torrat, dispensa oli i finalitza."""
        try:
            # 1. LED encès i cinta fins a càmera
            GPIO.output(self.led_pin, GPIO.HIGH)
            print("LED encès. Portant pa sota la càmera…")
            self.actuators.move_conveyor(direction="forward", duration=self.cfg.cam_time)
            self.actuators.stop()

            # 2. Bucle de detecció de torrat
            cicle = 1
            while True:
                print(f"[Cicle {cicle}] Captura i anàlisi")
                image_path = self.vision.capture_image(f"toast_{cicle}.jpg")
                torrat = self.vision.analyze_toast(image_path)

                if torrat is not None:
                    print(f"Grau de torrat retornat: {torrat:.3f}")
                    if torrat >= self.cfg.toasting_level:
                        print("Pa adequadament torrat!")
                        break
                else:
                    print("No s'ha pogut calcular el torrat en aquest cicle.")

                time.sleep(1)
                cicle += 1

            # 3. Mou fins al solenoide i dispensa oli
            print("Movent pa a la zona de l'oli…")
            self.actuators.move_conveyor(direction="forward", duration=self.cfg.oil_time)
            self.actuators.stop()

            print("Activant solenoide d'oli…")
            self.oil_ctrl.dispense()

            # 4. Mou fins al plat i apaga LED
            print("Portant pa fins al plat…")
            self.actuators.move_conveyor(direction="forward", duration=self.cfg.plate_time)
            self.actuators.stop()

            GPIO.output(self.led_pin, GPIO.LOW)
            print("Procés complet! LED apagat.")

        finally:
            self.actuators.cleanup()
            GPIO.cleanup()
            print("GPIO netejat. Programa finalitzat.")
