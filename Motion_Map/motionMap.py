import cv2
import numpy as np
from PyQt5 import QtGui


def update_map(self):
    self.map = cv2.circle(self.map, (self.x, self.y), radius=3, color=(238, 130, 238),
                          thickness=-1)  # draw a point in the starting point, thickness -1 means a filled circle
    qtMap = QtGui.QImage(self.map.data, self.map.shape[1], self.map.shape[0],
                         QtGui.QImage.Format_RGB888).rgbSwapped()  # convert the image to be used with qt label
    pixmap = QtGui.QPixmap.fromImage(qtMap)
    self.motionMapLabel.setPixmap(pixmap)


# ------------------------------------------------------the responses to different key
# presses---------------------------------------------------------
def up_response(self):
    self.y -= 3
    self.update_map()
    self.lMotorLabel.setText("L-Motor: Clockwise")
    self.rMotorLabel.setText("R-Motor: Clockwise")
    self.motorDirData = "CC"
    self.rMotorDirection = "Clockwise"
    self.lMotorDirection = "Clockwise"


def down_response(self):
    self.y += 3
    self.update_map()
    self.lMotorLabel.setText("L-Motor: Anti-clockwise")
    self.rMotorLabel.setText("R-Motor: Anti-clockwise")
    self.motorDirData = "AA"
    self.rMotorDirection = "Anti-clockwise"
    self.lMotorDirection = "Anti-clockwise"


def left_response(self):
    self.x -= 3
    self.update_map()
    self.lMotorLabel.setText("L-Motor: Stopped")
    self.rMotorLabel.setText("R-Motor: Clockwise")
    self.motorDirData = "SC"
    self.rMotorDirection = "Clockwise"
    self.lMotorDirection = "Stopped"


def right_response(self):
    self.x += 3
    self.update_map()
    self.lMotorLabel.setText("L-Motor: Clockwise")
    self.rMotorLabel.setText("R-Motor: Stopped")
    self.motorDirData = "CS"
    self.rMotorDirection = "Stopped"
    self.lMotorDirection = "Clockwise"


def l_response(self):
    self.speedLabel.setText("Current Speed: Lowest")
    self.motorSpeedData = "L"
    self.motorSpeed = "Lowest"


def m_response(self):
    self.speedLabel.setText("Current Speed: Medium")
    self.motorSpeedData = "M"
    self.motorSpeed = "Medium"


def h_response(self):
    self.speedLabel.setText("Current Speed: Highest")
    self.motorSpeedData = "H"
    self.motorSpeed = "Highest"


def s_response(self):  # switch between DC and BL motors
    if self.motorType == "DC":
        self.motorType = "BLDC"
        self.motorTypeData = "B"
        self.typeLabel.setText(self.motorType)
    else:
        self.motorType = "DC"
        self.motorTypeData = "D"
        self.typeLabel.setText(self.motorType)


def c_response(self):
    self.map = np.zeros((500, 500, 3), np.uint8)
    self.update_map()


def keyPressEvent(self, event):  # function that detects keypresses
    UP_KEY = 16777235
    DOWN_KEY = 16777237
    LEFT_KEY = 16777234
    RIGHT_KEY = 16777236
    L_KEY = 76
    M_KEY = 77
    H_KEY = 72
    C_KEY = 67
    S_KEY = 83

    if ((self.x <= 500 and self.x > 0) and (self.y <= 500 and self.y > 0)):

        if event.key() == UP_KEY:
            self.up_response()
        elif event.key() == DOWN_KEY:
            self.down_response()
        elif event.key() == LEFT_KEY:
            self.left_response()
        elif event.key() == RIGHT_KEY:
            self.right_response()
        elif event.key() == L_KEY:
            self.l_response()
        elif event.key() == M_KEY:
            self.m_response()
        elif event.key() == H_KEY:
            self.h_response()
        elif event.key() == S_KEY:
            self.s_response()
        elif event.key() == C_KEY:  # if c key is pressed, clear the map
            self.c_response()

        else:
            print("Invalid Input")

    else:  # reset the map to the starting point
        self.x = 250
        self.y = 480

    mainUI.rMotorState.setText("R-Motor state: " + self.rMotorDirection)
    mainUI.lMotorState.setText("L-Motor state: " + self.lMotorDirection)
    mainUI.motorSpeed.setText("Motor speed: " + self.motorSpeed)
