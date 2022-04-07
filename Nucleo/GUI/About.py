# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(395, 561)
        Dialog.setMinimumSize(QtCore.QSize(395, 561))
        Dialog.setMaximumSize(QtCore.QSize(395, 561))
        Dialog.setStyleSheet("background-color: rgb(235, 189, 48);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 391, 561))
        self.label.setStyleSheet("background-color: rgb(244,194,114);\n"
"image: url(:/Imagen1/FotoJet (2) (2).jpg);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../FotoJet (2) (2).jpg"))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
from Nucleo.GUI.Imagenes import INFO_rc
