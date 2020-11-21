# ---------------------------------------------------------------Libraries
# ----------------------------------------------------------------

from PyQt5 import QtWidgets

# ---------------------------------------------------------------Constants-----------------------------------------------------------------
from Main_Window.MainWindow import Ui_MainWindow
from Object_Tracker.ObjectTracker import TrackUI
from Serial.SerialCommunication import AThread
from Spot_The_Diff.SpotTheDiffGUI import Ui_DifferencesWindow
from Motion_Map.motionMapGUI import Ui_MotionMapWindow

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
