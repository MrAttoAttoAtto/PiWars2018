import xbox

class Controller:
    def __init__(self):
        self.joy = xbox.Joystick()

    def get_values(self):
        values = {}
        values['left_axes'] = self.joy.leftStick(2000)
        values['right_axes'] = self.joy.rightStick(2000)
        values['bumpers'] = (
            self.joy.leftBumper(),
            self.joy.rightBumper()
        )
        values['triggers'] = (
            self.joy.leftTrigger(),
            self.joy.rightTrigger()
        )
        values['button_pad'] = {
            'A': self.joy.A(),
            'B': self.joy.B(),
            'Y': self.joy.Y(),
            'X': self.joy.X()
        }
        values['d_pad'] = {
            'Up': self.joy.dpadUp(),
            'Down': self.joy.dpadDown(),
            'Left': self.joy.dpadLeft(),
            'Right': self.joy.dpadRight()
        }
        values['control_buttons'] = {
            'Start': self.joy.Start(),
            'Guide': self.joy.Guide(),
            'Back': self.joy.Back()
        }
        values['thumbsticks'] = (
            self.joy.leftThumbstick(),
            self.joy.rightThumbstick()
        )
        return values

    def safe_close(self):
        self.joy.close()
