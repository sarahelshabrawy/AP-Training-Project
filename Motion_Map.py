from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import cv2
import numpy as np


class Ui_MotionMapWindow(QMainWindow):

    def setupUi(self):
        self.setWindowTitle("Motion Map")
        self.setObjectName("MotionMapWindow")
        self.resize(483, 607)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.motionMapLabel = QtWidgets.QLabel(self.centralwidget)
        self.motionMapLabel.setGeometry(QtCore.QRect(20, 20, 441, 501))
        self.motionMapLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.motionMapLabel.setLineWidth(3)
        self.motionMapLabel.setScaledContents(True)
        self.motionMapLabel.setText("")
        self.motionMapLabel.setObjectName("motionMapLabel")
        self.rMotorLabel = QtWidgets.QLabel("R-Motor: Clockwise", self.centralwidget)
        self.rMotorLabel.setGeometry(QtCore.QRect(30, 530, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rMotorLabel.setFont(font)
        self.rMotorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rMotorLabel.setObjectName("rMotorLabel")
        self.lMotorLabel = QtWidgets.QLabel("L-Motor: Clockwise", self.centralwidget)
        self.lMotorLabel.setGeometry(QtCore.QRect(230, 530, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lMotorLabel.setFont(font)
        self.lMotorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lMotorLabel.setObjectName("lMotorLabel")
        self.speedLabel = QtWidgets.QLabel("Current Speed: Lowest", self.centralwidget)
        self.speedLabel.setGeometry(QtCore.QRect(30, 560, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.speedLabel.setFont(font)
        self.speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.speedLabel.setObjectName("speedLabel")
        self.typeLabel = QtWidgets.QLabel("DC", self.centralwidget)
        self.typeLabel.setGeometry(QtCore.QRect(290, 560, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.typeLabel.setFont(font)
        self.typeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.typeLabel.setObjectName("typeLabel")
        self.setCentralWidget(self.centralwidget)
        self.map = np.zeros((520, 520, 3),
                            np.uint8)  # create a black background for the motion map, by creating a numpy array filled with zeros
        self.map = cv2.circle(self.map, (260, 500), radius=3, color=(238, 130, 238),
                              thickness=-1)  # draw a point in the starting point
        qtMap = QtGui.QImage(self.map.data, self.map.shape[1], self.map.shape[0],
                             QtGui.QImage.Format_RGB888).rgbSwapped()  # convert the image to be used with qt label
        pixmap = QtGui.QPixmap.fromImage(qtMap)
        self.motionMapLabel.setPixmap(pixmap)
        self.x = 260
        self.y = 500

        self.motorType = "DC"

        # ---------------------------------------------------------Variables to send to the Arduino-----------------------------------------------------------
        self.motorDirData = "CC"
        self.motorSpeedData = "L"
        self.motorTypeData = "D"

        # ---------------------------------------------------------Variables to send to the MainWindow-----------------------------------------------------------
        Ui_MotionMapWindow.rMotorDirection = "Clockwise"
        Ui_MotionMapWindow.lMotorDirection = "Clockwise"
        Ui_MotionMapWindow.motorSpeed = "Lowest"

    # --------------------------------------------------------function to update the motion map-----------------------------------------------------------
    def update_map(self):
        self.map = cv2.circle(self.map, (self.x, self.y), radius=3, color=(238, 130, 238),
                              thickness=-1)  # draw a point in the starting point, thickness -1 means a filled circle
        qtMap = QtGui.QImage(self.map.data, self.map.shape[1], self.map.shape[0],
                             QtGui.QImage.Format_RGB888).rgbSwapped()  # convert the image to be used with qt label
        pixmap = QtGui.QPixmap.fromImage(qtMap)
        self.motionMapLabel.setPixmap(pixmap)

    # ------------------------------------------------------the responses to different key presses---------------------------------------------------------
    def up_response(self):
        self.y -= 3
        self.update_map()
        self.lMotorLabel.setText("L-Motor: Clockwise")
        self.rMotorLabel.setText("R-Motor: Clockwise")
        self.motorDirData = "CC"
        Ui_MotionMapWindow.rMotorDirection = "Clockwise"
        Ui_MotionMapWindow.lMotorDirection = "Clockwise"

    def down_response(self):
        self.y += 3
        self.update_map()
        self.lMotorLabel.setText("L-Motor: Anti-clockwise")
        self.rMotorLabel.setText("R-Motor: Anti-clockwise")
        self.motorDirData = "AA"
        Ui_MotionMapWindow.rMotorDirection = "Anti-clockwise"
        Ui_MotionMapWindow.lMotorDirection = "Anti-clockwise"

    def left_response(self):
        self.x -= 3
        self.update_map()
        self.lMotorLabel.setText("L-Motor: Stopped")
        self.rMotorLabel.setText("R-Motor: Clockwise")
        self.motorDirData = "SC"
        Ui_MotionMapWindow.rMotorDirection = "Clockwise"
        Ui_MotionMapWindow.lMotorDirection = "Stopped"

    def right_response(self):
        self.x += 3
        self.update_map()
        self.lMotorLabel.setText("L-Motor: Clockwise")
        self.rMotorLabel.setText("R-Motor: Stopped")
        self.motorDirData = "CS"
        Ui_MotionMapWindow.rMotorDirection = "Stopped"
        Ui_MotionMapWindow.lMotorDirection = "Clockwise"

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

        if self.x > 520 or self.x < 0 or self.y < 0 or self.y > 500:
            if self.x < 0:
                self.x = 520
            elif self.x > 520:
                self.x = 0
            if self.y < 0:
                self.y = 500
            elif self.y > 500:
                self.y = 0
        else:
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
