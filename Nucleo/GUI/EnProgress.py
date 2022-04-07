# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EnProgress.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Encrypt(object):
    def setupUi(self, Encrypt):
        Encrypt.setObjectName("Encrypt")
        Encrypt.resize(311, 90)
        Encrypt.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 80, 80, 255), stop:1 rgba(202, 183, 141, 255));")
        self.EnLbl = QtWidgets.QLabel(Encrypt)
        self.EnLbl.setGeometry(QtCore.QRect(60, 20, 181, 17))
        self.EnLbl.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 80, 80, 0), stop:1 rgba(202, 183, 141, 0));")
        self.EnLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.EnLbl.setObjectName("EnLbl")
        self.EnPGB = QtWidgets.QProgressBar(Encrypt)
        self.EnPGB.setGeometry(QtCore.QRect(10, 50, 291, 23))
        self.EnPGB.setProperty("value", 0)
        self.EnPGB.setObjectName("EnPGB")

        self.retranslateUi(Encrypt)
        QtCore.QMetaObject.connectSlotsByName(Encrypt)

    def retranslateUi(self, Encrypt):
        _translate = QtCore.QCoreApplication.translate
        Encrypt.setWindowTitle(_translate("Encrypt", "Progress"))
        self.EnLbl.setText(_translate("Encrypt", "Realizando Proceso..."))
