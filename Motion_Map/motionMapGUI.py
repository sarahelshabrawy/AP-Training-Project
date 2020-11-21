import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


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
        self.map = np.zeros((500, 500, 3),
                            np.uint8)  # create a black background for the motion map, by creating a numpy array filled with zeros
        self.map = cv2.circle(self.map, (250, 480), radius=3, color=(238, 130, 238),
                              thickness=-1)  # draw a point in the starting point
        qtMap = QtGui.QImage(self.map.data, self.map.shape[1], self.map.shape[0],
                             QtGui.QImage.Format_RGB888).rgbSwapped()  # convert the image to be used with qt label
        pixmap = QtGui.QPixmap.fromImage(qtMap)
        self.motionMapLabel.setPixmap(pixmap)
        self.x = 250
        self.y = 480

        self.motorType = "DC"

