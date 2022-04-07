# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from Nucleo.GUI.MainWindow import *
from Nucleo.GUI.About import *
from Nucleo.GUI.Selection import *
from Nucleo.GUI.Resume import *
from Nucleo.GUI.EnProgress import Encrypt

"""
import sys
import threading
"""
import time 

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QDesktopWidget, QTableWidgetItem
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from Nucleo.encryptDecrypt import encryptDecrypt
from Nucleo.AES256 import *
from Nucleo.EncryptorOWN import *

class MyThread(QThread):
    change_value=pyqtSignal(int)

    def run(self):
        coun=0
        while (coun<=102):
            self.change_value.emit(coun)
            coun+=0.001


class MainWindow(QtWidgets.QMainWindow, Ui_Encriptador):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        
        self.center()
        #Estableciendo el titulo de la ventana:
        self.setWindowTitle("Encriptador")

        #Estableciendo Icono del Programa:
        self.setWindowIcon(QIcon("Nucleo/GUI/Imagenes/computer-1294045_960_720.png"))
        barProgress=BarWindow(self)
        barProgress.show()

        #Acciones e los Botones de la ventana principal
        self.pushButton.clicked.connect(self.about)
        self.pushButton_7.clicked.connect(self.getAdress)
        self.pushButton_3.clicked.connect(self.destiny)
        self.pushButton_4.clicked.connect(self.encrypt)#Creado por Alejandro, para que se llame al boton encriptar
        self.pushButton_5.clicked.connect(self.decrypt)#Creado por Alejandro, para que se llame al boton encriptar
        

    def getAdress(self):
        content = []
        self.label_2.hide()
        
        """for i in range(len(self.listWidget)):
            content.append(self.listWidget.item(i).text())"""
        
        window = Selection(self, content)
        window.show()

    def destiny(self):
        filePath=QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_4.setText(filePath)

    #Desde la linea 55 hasta la linea 64 fue creado por Alejandro para poder Encriptar y desencriptar.
    def encrypt(self):
        self.hide()
        
        dirs=[]


        for i in range (len(self.listWidget)):
            dirs.append(self.listWidget.item(i).text())
        
        enc = encryptDecrypt()
        vectorI=[]
        matrixI=[]
        
        for i in dirs:
            if i!="":
                vector, matrix=enc.encryptFileOrDir(i, self.lineEdit_4.text(), self.lineEdit_3.text())
                vectorI.append(vector)
                matrixI+=matrix
        cant,time,size=(0,0,0)
        for vector in vectorI:
            c, t, s = vector
            cant+=c
            time+=t
            size+=s
        vectorI=["%s Archivos"%cant, "%s segundos"%time, "%s KB"%size]
        
        self.listWidget.clear()
        self.lineEdit_4.clear()
        self.lineEdit_3.clear()
        self.label_2.show()

        barProgress.close()
        self.show()
        ventana=TableWindow(self, vectorI, matrixI)
        ventana.show()
            
    def decrypt(self):
        dirs=[]

        for i in range (len(self.listWidget)):
            dirs.append(self.listWidget.item(i).text())
        
        enc = encryptDecrypt()
        
        for i in dirs:  
                if i!="":
                    enc.decryptFileOrDir(i, self.lineEdit_4.text(), self.lineEdit_3.text()) 
        
        self.listWidget.clear()
        self.lineEdit_4.clear()
        self.lineEdit_3.clear()
        self.label_2.show()
    #Fin de Alejandro

    def about(self):
        window = AboutWindow(self)
        window.show()

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    
class TableWindow(QtWidgets.QDialog, Resume):
    def __init__(self, parent=None, vectorInfo=[], matrixInfo=[]):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.center()


        item1=QTableWidgetItem(vectorInfo[0])
        item2=QTableWidgetItem(vectorInfo[1])
        item3=QTableWidgetItem(vectorInfo[2])

        self.tableWidget_2.setItem(-1, 1, item1)
        self.tableWidget_2.setItem(0, 1, item2)
        self.tableWidget_2.setItem(1, 1, item3)

        
        row=0
        for vector in matrixInfo:
            if row>=3:
                self.tableWidget.insertRow(row)
            item1=QTableWidgetItem(vector[1])#"Hola"
            item2=QTableWidgetItem(vector[2])#"Mundo"
            item3=QTableWidgetItem(vector[3])#"nuevo"
            self.tableWidget.setItem(row, 0, item1)
            self.tableWidget.setItem(row, 1, item2)
            self.tableWidget.setItem(row, 2, item3)
            row+=1
            



    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

class BarWindow(QtWidgets.QDialog, Encrypt):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.parent=parent

        self.starBar()
        

    def starBar(self):
        count=0
        while count<=100:
            count+=0.00001
            self.EnPGB.setValue(count)
        """self.thread=MyThread()
        self.thread.change_value.connect(self.setProgressValue)
        self.thread.run()"""
        
    def setProgressValue(self, value):
        self.EnPGB.setValue(value)

class Selection(QtWidgets.QDialog, Ui_Selection):
    def __init__(self, parent=None, content=[]):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.parent=parent
        self.content=content

        self.center()

        self.pushButton.clicked.connect(self.getFile)
        self.pushButton_2.clicked.connect(self.getDirectory)

    def getDirectory(self):
        self.hide()
        directoryPath=QtWidgets.QFileDialog.getExistingDirectory(self)
        if not(directoryPath in self.content):
            
            self.content.append(directoryPath)

            self.parent.listWidget.addItems(self.content)
            self.close()
        self.close()

    def getFile(self):
        self.hide()
        filePath, know=QtWidgets.QFileDialog.getOpenFileName(self)
        
        
        if not(filePath in (self.content)):
            self.content.append(filePath)
            #self.parent.listWidget.clear()
            self.parent.listWidget.addItems(self.content)
            self.close()
        self.close()

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

class AboutWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.center()
    
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

"""
class EnProgressUse(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Encrypt()
        self.ui.setupUi(self)
        
        self.show()

class ProgressEncrypt(threading.Thread):
    count = 0

    def __init__(self,dialog):
        threading.Thread.__init__(self)
        self.dialog = dialog
        self.count = 0

    def run(self):
        while self.count <= 100:
            time.sleep(1)
            dialog.ui.EnPGB.setValue(self.count)
            self.count += 10

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = EnProgressUse()
    t = ProgressEncrypt(dialog)
    t.start()
    dialog.exec()
    sys.exit(app.exec_())
"""