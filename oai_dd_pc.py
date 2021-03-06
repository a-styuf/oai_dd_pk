# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oai_dd_pc.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(637, 474)
        self.GetADCButton = QtWidgets.QPushButton(Form)
        self.GetADCButton.setGeometry(QtCore.QRect(414, 10, 121, 23))
        self.GetADCButton.setObjectName("GetADCButton")
        self.SetDACButton = QtWidgets.QPushButton(Form)
        self.SetDACButton.setGeometry(QtCore.QRect(414, 40, 121, 23))
        self.SetDACButton.setObjectName("SetDACButton")
        self.COMOpenButton = QtWidgets.QPushButton(Form)
        self.COMOpenButton.setGeometry(QtCore.QRect(530, 440, 101, 31))
        self.COMOpenButton.setObjectName("COMOpenButton")
        self.SerialNumEntry = QtWidgets.QLineEdit(Form)
        self.SerialNumEntry.setGeometry(QtCore.QRect(530, 410, 101, 20))
        self.SerialNumEntry.setAlignment(QtCore.Qt.AlignCenter)
        self.SerialNumEntry.setObjectName("SerialNumEntry")
        self.SerialNumLabel = QtWidgets.QLabel(Form)
        self.SerialNumLabel.setGeometry(QtCore.QRect(422, 410, 101, 20))
        self.SerialNumLabel.setObjectName("SerialNumLabel")
        self.StateMessage = QtWidgets.QTextBrowser(Form)
        self.StateMessage.setGeometry(QtCore.QRect(10, 410, 411, 61))
        self.StateMessage.setObjectName("StateMessage")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 10, 371, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.DACEntry = QtWidgets.QSpinBox(Form)
        self.DACEntry.setGeometry(QtCore.QRect(540, 40, 71, 22))
        self.DACEntry.setMaximum(4096)
        self.DACEntry.setSingleStep(100)
        self.DACEntry.setProperty("value", 1000)
        self.DACEntry.setObjectName("DACEntry")
        self.CycleButton = QtWidgets.QPushButton(Form)
        self.CycleButton.setGeometry(QtCore.QRect(414, 70, 121, 41))
        self.CycleButton.setCheckable(True)
        self.CycleButton.setAutoRepeat(False)
        self.CycleButton.setObjectName("CycleButton")
        self.GraphButton = QtWidgets.QPushButton(Form)
        self.GraphButton.setGeometry(QtCore.QRect(10, 360, 121, 41))
        self.GraphButton.setCheckable(False)
        self.GraphButton.setAutoRepeat(False)
        self.GraphButton.setObjectName("GraphButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ОАИ ДД"))
        self.GetADCButton.setText(_translate("Form", "Read ADC"))
        self.SetDACButton.setText(_translate("Form", "Set DAC"))
        self.COMOpenButton.setText(_translate("Form", "COM Open"))
        self.SerialNumEntry.setText(_translate("Form", "A94ZVTLXA"))
        self.SerialNumLabel.setText(_translate("Form", "SerialNumber"))
        self.CycleButton.setText(_translate("Form", "Циклический \n"
"опрос"))
        self.GraphButton.setText(_translate("Form", "Графики"))

