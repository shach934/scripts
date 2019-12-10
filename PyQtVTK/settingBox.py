# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingBox.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(496, 193)
        self.YesButton = QtWidgets.QPushButton(Setting)
        self.YesButton.setGeometry(QtCore.QRect(240, 150, 75, 23))
        self.YesButton.setObjectName("YesButton")
        self.CancelButton = QtWidgets.QPushButton(Setting)
        self.CancelButton.setGeometry(QtCore.QRect(400, 150, 75, 23))
        self.CancelButton.setObjectName("CancelButton")
        self.widget = QtWidgets.QWidget(Setting)
        self.widget.setGeometry(QtCore.QRect(20, 20, 305, 29))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.defaultDict = QtWidgets.QLabel(self.widget)
        self.defaultDict.setObjectName("defaultDict")
        self.horizontalLayout.addWidget(self.defaultDict)
        self.dict_input = QtWidgets.QLineEdit(self.widget)
        self.dict_input.setObjectName("dict_input")
        self.horizontalLayout.addWidget(self.dict_input)
        self.toolButton = QtWidgets.QToolButton(self.widget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)

        self.retranslateUi(Setting)
        self.YesButton.clicked.connect(Setting.close)
        self.CancelButton.clicked.connect(Setting.close)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Tools"))
        self.YesButton.setText(_translate("Setting", "Yes"))
        self.CancelButton.setText(_translate("Setting", "Cancel"))
        self.defaultDict.setText(_translate("Setting", "Default Path"))
        self.toolButton.setText(_translate("Setting", "..."))
