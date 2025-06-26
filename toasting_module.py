'''
CONTROL TORRAT
Decidirà a través de la informació del vision module quan el pà està torrat
A partir d'això moura la cinta cap on toqui, girar el pà...
'''

class ToastingControl:
    def __init__(self, vision, config):
        self.vision = vision
        self.config = config

    def check_toast_status(self, image):
        level = self.config.get_toasting_level()
        progress = self.vision.analyze_toast(image)
        return progress >= level / 5  # suposem nivell de torrat de 1 a 5
