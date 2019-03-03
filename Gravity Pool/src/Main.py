import PyQt5.QtWidgets as qw
import asyncqt
import sys
import math
import requests
import time
import asyncio
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPainter
from PyQt5.Qt import QIntValidator, QBrush, QPen, QColor, QFont


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
        self.drawBoundaries(qp)
        self.drawTime(qp)
        qp.end()

    def drawBall(self, qp):
        # print("Drawing ball...")
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        # print (currentTrajectory.getPosition)
        # curPhysTime = curTime - startupTime
        # curPos = currentTrajectory.getPosition(curPhysTime)
        r = 1
        # print(f"Drawing ball at ({curX,curY}),while it is at {currentTrajectory.getPosition(curScreenTime)['y']}")
        drawX, drawY = convertCoord(curX, curY)
        # print(f"Drawing at x={drawX},y={drawY}")
        qp.drawEllipse(drawX - r // 2, drawY - r // 2, r, r)
    
    def drawBoundaries(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        
        qp.drawLine(*convertCoord(0, 0), *convertCoord(100, 100))
        qp.drawLine(*convertCoord(0, 0), *convertCoord(-100, 100))

    def drawTime(self, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Times New Roman', 10))
        qp.drawText(50, 50, f"Time:{round(curScreenTime,2)}")


def convertCoord(x, y):
    xMin = -1
    xMax = 1
    yMin = 2
    yMax = 0
    newX = round((x - xMin) / (xMax - xMin) * 500)
    newY = round((y - yMin) / (yMax - yMin) * 500)
    return (newX, newY)


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
            t1 = self.t + (((self.vY - self.vX) + math.sqrt((self.vY - self.vX) ** 2 - 2 * g * (self.x - self.y))) / (self.g))
        except:
            t1 = math.inf
        try:
            t2 = self.t + (((self.vY + self.vX) + math.sqrt((self.vY + self.vX) ** 2 + 2 * g * (self.x + self.y))) / (self.g))
        except:
            t2 = math.inf
        if(t1 < 0):
            t1 = math.inf
        if(t2 < 0):
            t2 = math.inf
        # print(f"t1={t1},t2={t2}")
        self.nextRebound = min(t1, t2)
        # print(f"Current trajectry:{self.getPosition}")
        # print(f"Trajectory set. Current time:{self.t}, rebound at {self.nextRebound}. Current screenTime:{curScreenTime}")
        # print(f"Current position:({self.x,self.y}), on screen:({curX,curY})")

    def calculateNextRebound(self):
        reboundPosition = self.getPosition(self.nextRebound)
        print(f"Rebound position:{reboundPosition} at time {self.nextRebound}")
        if(reboundPosition['x'] > 1e-6 or (abs(reboundPosition['x']) <= 1e-6 and reboundPosition['vX']>0)):
            self.__init__(reboundPosition['x'], reboundPosition['y'], reboundPosition['vY'], reboundPosition['vX'], self.nextRebound, self.g)
        else:
            self.__init__(reboundPosition['x'], reboundPosition['y'], -reboundPosition['vY'], -reboundPosition['vX'], self.nextRebound, self.g)


if __name__ == '__main__':

    async def screenRefresh(curTime):
        lock = asyncio.Lock()
        async with lock:
            global curX, curY, curScreenTime
            curScreenTime = curTime - startupTime
            curPos = currentTrajectory.getPosition(curScreenTime)
            # print(f"Changing positions from {curX},{curY} to {(curPos['x'], curPos['y'])}")
            curX, curY = (curPos['x'], curPos['y'])
            s.repaint()

    # @asyncio.coroutine
    async def drawCycle():
        global lastFrame
        # global loop
        # print("tick")
        curTime = time.time()
        # if(curTime - startupTime >= 10):
        #    closeAll()
        if(lastFrame + 1 / targetFPS < curTime):
            # print("Drawing new frame")
            propagateRebounds(lastFrame + 1 / targetFPS)
            refresh = loop.create_task(screenRefresh(lastFrame + 1 / targetFPS))
            await refresh
            lastFrame = lastFrame + 1 / targetFPS
        await asyncio.sleep(lastFrame + 1 / targetFPS - curTime)
        loop.create_task(drawCycle())
    
    def propagateRebounds(time):
        global curTime
        curTime = time
        while currentTrajectory.nextRebound < curTime - startupTime:
            # print("Calculating new trajectory")
            currentTrajectory.calculateNextRebound()
    
    targetFPS = 60
    startupTime = time.time()
    curScreenTime = 0
    curX, curY = (0, 0)
    currentTrajectory = Trajectory(x=0, y=1, vX=1, vY=0, t=0, g=9.8)
    lastFrame = startupTime
    curX = currentTrajectory.x
    curY = currentTrajectory.y
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
    
