import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time
from model.process import * 

form_class = uic.loadUiType("gui/main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.rw = volume_worker(interval = '1d')
        self.StartData()

    def StartData(self) :
        try :
            self.rw.stop()
        except :
            print("no worker")
        time.sleep(1)
        self.rw = volume_worker(interval = '1d')
        self.rw.dataSent.connect(self.updateData)
        self.rw.start()

    def StopData(self) :
        self.rw.stop()
        
    def closeEvent(self, event):
        self.rw.close()
    
    def updateData(self, data):
        self.Price1dWidget.updateData(data)
        self.CandleWidget.updateData(data)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()