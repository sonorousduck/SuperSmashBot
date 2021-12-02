from melee.enums import Button

class Moveset:
    def __init__(self, controller):
        self.controller = controller
        self.possibleActions = 27

    def moveLeft(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .25, .5)

    def moveRight(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .75, .5)

    def crouch(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)

    def sprintLeft(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, 0, .5)

    def sprintRight(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, 1, .5)

    def jumpRight(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, 1, .5)
        self.controller.press_button(Button.BUTTON_Y)

    def jumpLeft(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, 0, .5)
        self.controller.press_button(Button.BUTTON_Y)

    def jump(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_Y)

    def B(self):
        self.controller.release_all()
        # self.controller.press_button(Button.BUTTON_B)
        self.controller.simple_press(.5, .5, Button.BUTTON_B)

    def BDown(self):
        self.controller.release_all()
        # self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
        # self.controller.press_button(Button.BUTTON_B)
        self.controller.simple_press(.5, 0, Button.BUTTON_B)


    def BLeft(self):
        self.controller.release_all()
        # self.controller.tilt_analog(Button.BUTTON_MAIN, 0, .5)
        # self.controller.press_button(Button.BUTTON_B)
        self.controller.simple_press(.2, .5, Button.BUTTON_B)


    def BRight(self):
        self.controller.release_all()
        # self.controller.tilt_analog(Button.BUTTON_MAIN, 1, .5)
        # self.controller.press_button(Button.BUTTON_B)
        self.controller.simple_press(.8, .5, Button.BUTTON_B)


    def BUp(self):
        self.controller.release_all()
        # self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 1)
        # self.controller.press_button(Button.BUTTON_B)
        self.controller.simple_press(.5, 1, Button.BUTTON_B)

    def A(self):
        self.controller.release_all()
        # self.controller.press_button(Button.BUTTON_A)
        self.controller.simple_press(.5, .5, Button.BUTTON_A)

    def forwardARight(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, 1, .5)

    def forwardALeft(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, 0, .5)

    def tiltLeftA(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .4, .5)
        self.controller.press_button(Button.BUTTON_A)

    def tiltRightA(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .6, .5)
        self.controller.press_button(Button.BUTTON_A)

    def tiltDownA(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .5, .4)
        self.controller.press_button(Button.BUTTON_A)

    def tiltUpA(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_MAIN, .5, .6)
        self.controller.press_button(Button.BUTTON_A)

    def cUp(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, .5, 1)

    def cDown(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, .5, 0)

    def cLeft(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, 1, .5)

    def cRight(self):
        self.controller.release_all()
        self.controller.tilt_analog(Button.BUTTON_C, 0, .5)

    def shield(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_L)

    def dodgeLeft(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_L)
        self.controller.tilt_analog(Button.BUTTON_MAIN, 0, .5)

    def dodgeRight(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_L)
        self.controller.tilt_analog(Button.BUTTON_MAIN, 1, .5)

    def spotDodge(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_L)
        self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)

    def grab(self):
        self.controller.release_all()
        self.controller.press_button(Button.BUTTON_Z)

    def doNothing(self):
        self.controller.release_all()



