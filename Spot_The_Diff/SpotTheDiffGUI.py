from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from Spot_The_Diff.SpotTheDiff import *

class Ui_DifferencesWindow(QMainWindow):
    def setupUi(self):
        self.setObjectName("DifferencesWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.picture1 = QtWidgets.QLabel(self.centralwidget)
        self.picture1.setGeometry(QtCore.QRect(80, 140, 251, 351))
        self.picture1.setFrameShape(QtWidgets.QFrame.Box)
        self.picture1.setLineWidth(3)
        self.picture1.setScaledContents(True)
        self.picture1.setObjectName("picture1")
        self.picture2 = QtWidgets.QLabel(self.centralwidget)
        self.picture2.setGeometry(QtCore.QRect(450, 140, 251, 351))
        self.picture2.setFrameShape(QtWidgets.QFrame.Box)
        self.picture2.setLineWidth(3)
        self.picture2.setScaledContents(True)
        self.picture2.setObjectName("picture2")
        self.title = QtWidgets.QLabel(
            "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Spot the differences Game</span></p></body></html>",
            self.centralwidget)
        self.title.setGeometry(QtCore.QRect(200, 40, 371, 81))
        self.title.setObjectName("title")
        self.picture1_btn = QtWidgets.QPushButton("Picture 1", self.centralwidget)
        self.picture1_btn.setGeometry(QtCore.QRect(140, 510, 93, 28))
        self.picture1_btn.setObjectName("picture1_btn")
        self.picture2_btn = QtWidgets.QPushButton("Picture 2", self.centralwidget)
        self.picture2_btn.setGeometry(QtCore.QRect(520, 510, 93, 28))
        self.picture2_btn.setObjectName("picture2_btn")
        self.spotdiff_btn = QtWidgets.QPushButton("Spot Differences", self.centralwidget)
        self.spotdiff_btn.setGeometry(QtCore.QRect(320, 510, 131, 28))
        self.spotdiff_btn.setObjectName("spotdiff_btn")
        self.number = QtWidgets.QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt;\">Number of differnces </span></p></body></html>",
            self.centralwidget)
        self.number.setGeometry(QtCore.QRect(250, 550, 151, 21))
        self.number.setObjectName("number")
        self.numbervalue = QtWidgets.QLabel(
            "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">0</span></p></body></html>",
            self.centralwidget)
        self.numbervalue.setGeometry(QtCore.QRect(410, 550, 91, 21))
        self.numbervalue.setObjectName("numbervalue")
        self.setCentralWidget(self.centralwidget)
        self.im1 = None
        self.im2 = None
        self.picture1_btn.clicked.connect(readpic1)
        self.picture2_btn.clicked.connect(readpic2)
        self.spotdiff_btn.clicked.connect(spot_diff)
        QtCore.QMetaObject.connectSlotsByName(self)
