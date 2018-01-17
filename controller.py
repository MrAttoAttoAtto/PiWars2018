import xbox

class Controller:
    def __init__(self):
        self.joy = xbox.Joystick()

    def get_values(self):
        values = {}
        values['left_axes'] = self.joy.leftStick()
        values['right_axes'] = self.joy.rightStick()
        values['bumpers'] = (
            self.joy.leftBumper(),
            self.joy.rightBumper()
        )
        values['triggers'] = (
            self.joy.leftTrigger(),
            self.joy.rightTrigger()
        )
        values['button_pad'] = (
            self.joy.A(),
            self.joy.B(),
            self.joy.Y(),
            self.joy.X()
        )
        values['d_pad'] = (
            self.joy.dpadUp(),
            self.joy.dpadDown(),
            self.joy.dpadLeft(),
            self.joy.dpadRight()
        )
        values['control_buttons'] = (
            self.joy.Start(),
            self.joy.Guide(),
            self.joy.Back()
        )
        values['thumbsticks'] = (
            self.joy.leftThumbstick(),
            self.joy.rightThumbstick()
        )

        return values

    def safe_close(self):
        self.joy.close()
