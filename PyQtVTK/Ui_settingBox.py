# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_settingBox.ui'
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
        self.layoutWidget = QtWidgets.QWidget(Setting)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 305, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.defaultDict = QtWidgets.QLabel(self.layoutWidget)
        self.defaultDict.setObjectName("defaultDict")
        self.horizontalLayout.addWidget(self.defaultDict)
        self.dict_input = QtWidgets.QLineEdit(self.layoutWidget)
        self.dict_input.setObjectName("dict_input")
        self.horizontalLayout.addWidget(self.dict_input)
        self.toolButton = QtWidgets.QToolButton(self.layoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.defaultDict_2 = QtWidgets.QLabel(Setting)
        self.defaultDict_2.setGeometry(QtCore.QRect(20, 60, 41, 31))
        self.defaultDict_2.setObjectName("defaultDict_2")
        self.dict_input_2 = QtWidgets.QLineEdit(Setting)
        self.dict_input_2.setGeometry(QtCore.QRect(92, 60, 191, 20))
        self.dict_input_2.setObjectName("dict_input_2")
        self.toolButton_2 = QtWidgets.QToolButton(Setting)
        self.toolButton_2.setGeometry(QtCore.QRect(300, 60, 25, 19))
        self.toolButton_2.setObjectName("toolButton_2")

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
        self.defaultDict_2.setText(_translate("Setting", "Paraview"))
        self.toolButton_2.setText(_translate("Setting", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Setting = QtWidgets.QWidget()
    ui = Ui_Setting()
    ui.setupUi(Setting)
    Setting.show()
    sys.exit(app.exec_())
