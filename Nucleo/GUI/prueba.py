from EnProgress import *
from PyQt5.QtCore import QTime, QTimer

import time as t

class Ui_init(QtWidgets.QDialog, Encrypt):
    def __init__(self):
        super(Ui_init, self).__init__()

        self.setupUi(self)
        
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.start)
        
    c=0
    def start(self):
        self.timer.start(100)
        while(c<102):
            c=self.step(c)
            self.EnPGB.setValue(c)
            
        self.timer.stop()
        self.close()
    
    def step(self, count):
        return count+1
    
    def progres(self):
        pass


app=QtWidgets.QApplication([])
window = Ui_init()

window.show()
app.exec_()

