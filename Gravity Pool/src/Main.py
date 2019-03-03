import PyQt5.QtWidgets as qw
import sys
import math
import requests
import time
import asyncio
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QIntValidator


class MainWindow(qw.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.resize(250, 250)
        self.move(300, 300)
        self.setWindowTitle('Pool controller')
        
        self.fpsLabel = qw.QLabel('Target FPS', self)
        self.fpsLabel.move(0, 50)
        
        self.fpsField = qw.QLineEdit('60', self)
        self.fpsField.setValidator(QIntValidator(1, 1000))
        self.fpsField.move(60, 50)
        self.fpsField.editingFinished.connect(self.setFPS)
 
        self.quitBtn = qw.QPushButton('Quit', self)
        self.quitBtn.move(50, 200)
        self.quitBtn.clicked.connect(self.close)
        
    @pyqtSlot()
    def setFPS(self):
        targetFPS = int(self.fpsField.text())
        print(targetFPS)


class Screen(qw.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.move(600, 300)
        self.setWindowTitle('Gravity Pool')


class Trajectory():

    def __init__(self, x, y, vX, vY, t, g):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.t = t
        self.g = g
        self.getPosition = lambda t: {x:(self.x + self.vX * (t - self.t)), y:(self.y + self.vY * (t - self.t) - self.g * (t - self.t) ** 2), vX:self.vX, vY:self.vY - self.g * (t - self.t)}
        self.nextRebound = min(self.t + (((self.vY - self.vX) + math.sqrt((self.vY - self.vX) ** 2 - 4 * g * (self.x - self.y))) / (2 * self.g)), self.t + (((self.vY + self.vX) + math.sqrt((self.vY + self.vX) ** 2 + 4 * g * (self.x + self.y))) / (2 * self.g)))
        print(f"Current trajectry:{self.getPosition}")

    def calculateNextRebound(self):
        reboundPosition = self.getPosition(self.t + self.nextRebound)
        if(reboundPosition.x >= 0):
            self.__init__(self, reboundPosition.x, reboundPosition.y, reboundPosition.vY, reboundPosition.vX, self.t + self.nextRebound, self.g)
        else:
            self.__init__(self, reboundPosition.x, reboundPosition.y, -reboundPosition.vY, -reboundPosition.vX, self.t + self.nextRebound, self.g)


if __name__ == '__main__':

    # @asyncio.coroutine
    async def drawCycle():
        global lastFrame
        print("tick")
        curTime = time.time()
        if(lastFrame + 1 / targetFPS < curTime):
            return
        drawFrame()
        lastFrame = time.time()
    
    def drawFrame():
        curTime = time.time()
        while currentTrajectory.nextRebound > curTime:
            currentTrajectory.calculateNextRebound()
    
    app = qw.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    s = Screen()
    s.show()
    targetFPS = 60
    currentTrajectory = Trajectory(x=0, y=10, vX=10, vY=0, t=0, g=9.8)
    lastFrame = time.time()
    # loop = asyncio.get_event_loop()
    asyncio.run(drawCycle())
    sys.exit(app.exec_())
    
