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
