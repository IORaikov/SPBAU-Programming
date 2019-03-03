import PyQt5.QtWidgets as qw
import asyncqt
import sys
import math
import requests
import time
import asyncio
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPainter
from PyQt5.Qt import QIntValidator, QBrush


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
        self.quitBtn.clicked.connect(closeAll)
        
    @pyqtSlot()
    def setFPS(self):
        targetFPS = int(self.fpsField.text())
        print(targetFPS)


def closeAll():
    loop.stop()


class Screen(qw.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.move(600, 300)
        self.setWindowTitle('Gravity Pool')

    def paintEvent(self, event):
        # print("paintEvent")
        qp = QPainter()
        qp.begin(self)
        self.drawBall(qp)
        # self.drawBoundaries(qp)
        qp.end()

    def drawBall(self, qp):
        # print("Drawing ball...")
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        # print (currentTrajectory.getPosition)
        curPhysTime = curTime - startupTime
        curPos = currentTrajectory.getPosition(curPhysTime)
        r = 5
        drawX = round(50 + curPos['x'] - r / 2) * 10
        drawY = round(curPos['y'] - r / 2) * 10
        print(f"Drawing at x={drawX},y={drawY}")
        qp.drawEllipse(drawX, drawY, r, r)


class Trajectory():

    def getPosition(self, t):
        return {'x':(self.x + self.vX * (t - self.t)), 'y':(self.y + self.vY * (t - self.t) - self.g / 2 * (t - self.t) ** 2), 'vX':self.vX, 'vY':self.vY - self.g * (t - self.t)}

    def __init__(self, x, y, vX, vY, t, g):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.t = t
        self.g = g
        try:
            t1 = self.t + (((self.vY - self.vX) + math.sqrt((self.vY - self.vX) ** 2 - 4 * g * (self.x - self.y))) / (2 * self.g))
        except:
            t1 = math.inf
        try:
            t2 = self.t + (((self.vY + self.vX) + math.sqrt((self.vY + self.vX) ** 2 + 4 * g * (self.x + self.y))) / (2 * self.g))
        except:
            t2 = math.inf
        if(t1 < 0):
            t1 = math.inf
        if(t2 < 0):
            t2 = math.inf
        # print(f"t1={t1},t2={t2}")
        self.nextRebound = min(t1, t2)
        # print(f"Current trajectry:{self.getPosition}")
        print(f"Trajectory set. Current time:{self.t}, rebound at {self.nextRebound}")

    def calculateNextRebound(self):
        reboundPosition = self.getPosition(self.nextRebound)
        # print(f"Rebound position:{reboundPosition} at time {self.nextRebound}")
        if(reboundPosition['x'] >= 0):
            self.__init__(reboundPosition['x'], reboundPosition['y'], reboundPosition['vY'], reboundPosition['vX'], self.nextRebound, self.g)
        else:
            self.__init__(reboundPosition['x'], reboundPosition['y'], -reboundPosition['vY'], -reboundPosition['vX'], self.nextRebound, self.g)


if __name__ == '__main__':

    async def screenRefresh():
        s.update()

    # @asyncio.coroutine
    async def drawCycle():
        global lastFrame
        # global loop
        # print("tick")
        curTime = time.time()
        #if(curTime - startupTime >= 10):
        #    closeAll()
        if(lastFrame + 1 / targetFPS < curTime):
            # print("Drawing new frame")
            drawFrame()
            refresh = loop.create_task(screenRefresh())
            await refresh
            lastFrame = time.time()
        await asyncio.sleep(lastFrame + 1 / targetFPS - curTime)
        loop.create_task(drawCycle())
    
    def drawFrame():
        global curTime
        curTime = time.time()
        while currentTrajectory.nextRebound + startupTime < curTime:
            # print("Calculating new trajectory")
            currentTrajectory.calculateNextRebound()
    
    
    targetFPS = 60
    startupTime = time.time()
    currentTrajectory = Trajectory(x=0, y=10, vX=10, vY=0, t=0, g=9.8)
    lastFrame = startupTime
    
    app = qw.QApplication(sys.argv)
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = MainWindow()
    w.show()
    s = Screen()
    s.show()
    
    
    loop.create_task(drawCycle())
    with loop:
        sys.exit(loop.run_forever())
    # asyncio.run(drawCycle())
    # sys.exit(app.exec_())
    
