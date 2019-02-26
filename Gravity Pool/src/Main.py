import PyQt5.QtWidgets as qw
import sys
import requests
import time
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


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    s=Screen()
    s.show()
    targetFPS = 60
    sys.exit(app.exec_())
