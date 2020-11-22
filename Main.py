# ---------------------------------------------------------------Libraries----------------------------------------------------------------
import cv2
import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from Object_tracker import TrackUI
from Motion_Map import Ui_MotionMapWindow
from Spot_the_diff import Ui_DifferencesWindow

port = ""
usbStatus = "Disconnected"
arduino = None


# ---------------------------------------------------------------Constants-----------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------Main window code--------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

class Ui_MainWindow(QMainWindow):
    def setupUi(self):
        self.setWindowTitle("MainWindow")
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.screenshot = QtWidgets.QPushButton("Take a screenshot", self.centralwidget)
        self.screenshot.setGeometry(QtCore.QRect(150, 470, 171, 23))
        self.screenshot.setObjectName("screenshot")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(570, 110, 101, 41))
        self.lcdNumber.setObjectName("lcdNumber")
        self.pause = QtWidgets.QPushButton("Pause", self.centralwidget)
        self.pause.setGeometry(QtCore.QRect(570, 230, 75, 23))
        self.pause.setObjectName("pause")
        self.stop = QtWidgets.QPushButton("Stop", self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(650, 230, 75, 23))
        self.stop.setObjectName("stop")
        self.start = QtWidgets.QPushButton("Start", self.centralwidget)
        self.start.setGeometry(QtCore.QRect(490, 230, 75, 23))
        self.start.setObjectName("start")
        self.usbConnectedLabel = QtWidgets.QLabel("USB status: ", self.centralwidget)
        self.usbConnectedLabel.setGeometry(QtCore.QRect(600, 400, 181, 16))
        self.usbConnectedLabel.setObjectName("usbConnectedLabel")
        self.voltmeter = QtWidgets.QLabel("Voltmeter : N/A", self.centralwidget)
        self.voltmeter.setGeometry(QtCore.QRect(600, 420, 191, 20))
        self.voltmeter.setObjectName("voltmeter")
        self.current = QtWidgets.QLabel("Current sensor: N/A", self.centralwidget)
        self.current.setGeometry(QtCore.QRect(600, 440, 191, 20))
        self.current.setObjectName("current")
        self.leakage = QtWidgets.QLabel("Leakage sensor: N/A", self.centralwidget)
        self.leakage.setGeometry(QtCore.QRect(600, 460, 171, 20))
        self.leakage.setObjectName("leakage")
        self.rMotorState = QtWidgets.QLabel("R-Motor state: Clockwise", self.centralwidget)
        self.rMotorState.setGeometry(QtCore.QRect(600, 480, 191, 20))
        self.rMotorState.setObjectName("rMotorState")
        self.lMotorState = QtWidgets.QLabel("L-Motor state: Clockwise", self.centralwidget)
        self.lMotorState.setGeometry(QtCore.QRect(600, 500, 181, 20))
        self.lMotorState.setObjectName("lMotorState")
        self.motorSpeed = QtWidgets.QLabel("Motor speed: Lowest", self.centralwidget)
        self.motorSpeed.setGeometry(QtCore.QRect(600, 520, 171, 20))
        self.motorSpeed.setObjectName("motorSpeed")
        self.camera = QtWidgets.QLabel("Camera", self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(50, 30, 351, 391))
        self.camera.setFrameShape(QtWidgets.QFrame.Box)
        self.camera.setLineWidth(2)
        self.camera.setObjectName("camera")
        self.secondsBox = QtWidgets.QSpinBox(self.centralwidget)
        self.secondsBox.setGeometry(QtCore.QRect(620, 190, 42, 22))
        self.secondsBox.setObjectName("secondsBox")
        self.minutesBox = QtWidgets.QSpinBox(self.centralwidget)
        self.minutesBox.setGeometry(QtCore.QRect(500, 190, 42, 22))
        self.minutesBox.setObjectName("minutesBox")
        self.minutesLabl = QtWidgets.QLabel("Minutes", self.centralwidget)
        self.minutesLabl.setGeometry(QtCore.QRect(560, 190, 47, 13))
        self.minutesLabl.setObjectName("minutesLabl")
        self.secondsLabel = QtWidgets.QLabel("Seconds", self.centralwidget)
        self.secondsLabel.setGeometry(QtCore.QRect(680, 190, 47, 13))
        self.secondsLabel.setObjectName("secondsLabel")
        self.motionMapButton = QtWidgets.QPushButton("Motion Map", self.centralwidget)
        self.motionMapButton.setGeometry(QtCore.QRect(470, 300, 291, 28))
        self.motionMapButton.setObjectName("motionMapButton")
        self.diffButton = QtWidgets.QPushButton("Spot the difference", self.centralwidget)
        self.diffButton.setGeometry(QtCore.QRect(470, 340, 141, 28))
        self.diffButton.setObjectName("diffButton")
        self.trackingButton = QtWidgets.QPushButton("Object Tracking", self.centralwidget)
        self.trackingButton.setGeometry(QtCore.QRect(620, 340, 141, 28))
        self.trackingButton.setObjectName("trackingButton")
        self.setCentralWidget(self.centralwidget)
        self.start.clicked.connect(self.readTimer)
        self.timer = QTimer()
        self.timer.timeout.connect(self.setTimer)
        self.screenshot.clicked.connect(self.save)
        self.stop.clicked.connect(self.stopFun)
        self.pause.clicked.connect(self.pauseFun)
        self.camera.setScaledContents(True)
        self.cap = cv2.VideoCapture(0)
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.showCamera)
        self.timer1.start(20)
        self.startTimer = True
        QtCore.QMetaObject.connectSlotsByName(self)

    # Show a live feed of the webcam
    def showCamera(self):
        _, self.img = self.cap.read()
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.camera.setPixmap(QtGui.QPixmap.fromImage(qImg))
        cv2.waitKey(20)

    # Save a snapshot of the live feed
    def save(self):
        savedframe = self.img
        name, _ = QFileDialog.getSaveFileName()
        cv2.imwrite(name + ".png", savedframe)

    # ------------------------------------------------------------------Timer Code-----------------------------------------------------------------
    def readTimer(self):
        if self.startTimer or self.seconds == 0:
            self.seconds = self.minutesBox.value() * 60 + self.secondsBox.value()
        self.lcdNumber.display(str(self.seconds))
        self.timer.start(1000)

    def setTimer(self):
        self.startTimer = False
        if self.seconds > 0:
            self.seconds -= 1
        self.secondString = str(self.seconds)
        self.lcdNumber.display(self.secondString)

    def pauseFun(self):
        self.timer.stop()

    def stopFun(self):
        self.timer.stop()
        self.seconds = 0
        self.lcdNumber.display("00")


# -----------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------Serial communication code-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

class AThread(QThread):

    def run(self):
        global port
        global usbStatus
        global arduino
        # print("RUNNING")
        arduinoData = motionUI.motorTypeData + motionUI.motorSpeedData + motionUI.motorDirData + str(
            diffUI.differences) + str(TrackUI.angle).zfill(3)
        #print(str(TrackUI.angle))
        diffUI.differences = 0

        try:  # check if the usb is conneected or not, then try to reconnect
            arduino.write(arduinoData.encode())
            usbStatus = "Connected"
            print("SENT")
        except:

            usbStatus = "Disconnected"
            port = ""
            if port == "":  # if no arduino port is found
                for i in range(len(list(
                        serial.tools.list_ports.comports()))):  # look through all the elements of the port list
                    # function
                    if "CH340" in list(serial.tools.list_ports.comports()[i])[
                        1]:  # if the arduino bootloader is found in the current index
                        port = list(serial.tools.list_ports.comports()[0])[
                            0]  # assign the found port to the "port" variable
                        print("\nDevice Connected At", port)  # print the found port
                        usbStatus = "Connected"
                        arduino = serial.Serial(port,
                                                9600)  # add a serial config where "port" is the com port for arduino
                        # and 9600 is the baud rate
                        # time.sleep(1)

        try:
            incoming = arduino.readline()  # read the sensor data coming from the arduino
            incoming = incoming.decode()
            incoming = incoming.split()
            # print(incoming)
            mainUI.voltmeter.setText("Voltmeter: " + incoming[0])
            mainUI.current.setText("Current sensor: " + incoming[1])
            mainUI.leakage.setText("Leakage sensor: " + incoming[2])
        except:
            # print("Serial error - sensor values")
            pass
        mainUI.rMotorState.setText("R-Motor state: " + Ui_MotionMapWindow.rMotorDirection)
        mainUI.lMotorState.setText("L-Motor state: " + Ui_MotionMapWindow.lMotorDirection)
        mainUI.motorSpeed.setText("Motor speed: " + Ui_MotionMapWindow.motorSpeed)
        mainUI.usbConnectedLabel.setText("USB status: " + usbStatus)


# -----------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------Main function--------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainUI = Ui_MainWindow()
    mainUI.setupUi()
    mainUI.show()
    diffUI = Ui_DifferencesWindow()
    diffUI.setupUi()
    motionUI = Ui_MotionMapWindow()
    motionUI.setupUi()
    thread = AThread()
    thread.finished.connect(thread.run)
    thread.finished.connect(thread.start)
    thread.start()
    trackUI = TrackUI()
    mainUI.diffButton.clicked.connect(diffUI.show)
    mainUI.motionMapButton.clicked.connect(motionUI.show)
    mainUI.trackingButton.clicked.connect(trackUI.setup)

    app.exec_()
