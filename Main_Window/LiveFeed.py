import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog


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
