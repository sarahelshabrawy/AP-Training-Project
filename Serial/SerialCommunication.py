import time

import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread

from Motion_Map.motionData import *
from Object_Tracker.ObjectTracker import TrackUI
from Main_Window.MainWindow import Ui_MainWindow
from Spot_The_Diff import SpotTheDiff

class AThread(QThread):
    port = ""
    usbStatus = "Disconnected"
    arduino = None
    def run(self):
        global port
        global usbStatus
        global arduino
        # print("RUNNING")
        arduinoData = motorTypeData + motorSpeedData + motorDirData + str(
       SpotTheDiff.differences) + str(TrackUI.angle).zfill(3)
        print(str(TrackUI.angle))
        differences = 0

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
                        time.sleep(1)

        try:
            incoming = arduino.readline()  # read the sensor data coming from the arduino
            incoming = incoming.decode()
            incoming = incoming.split()
            # print(incoming)
            Ui_MainWindow.voltmeter.setText("Voltmeter: " + incoming[0])
            Ui_MainWindow.current.setText("Current sensor: " + incoming[1])
            Ui_MainWindow.leakage.setText("Leakage sensor: " + incoming[2])
        except:
            # print("Serial error - sensor values")
            pass

        Ui_MainWindow.usbConnectedLabel.setText("USB status: " + usbStatus)
