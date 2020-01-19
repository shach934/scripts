# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_settingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settingDialog(object):
    def setupUi(self, settingDialog):
        settingDialog.setObjectName("settingDialog")
        settingDialog.resize(383, 97)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(settingDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.defaultDict = QtWidgets.QLabel(settingDialog)
        self.defaultDict.setObjectName("defaultDict")
        self.verticalLayout.addWidget(self.defaultDict)
        self.defaultDict_2 = QtWidgets.QLabel(settingDialog)
        self.defaultDict_2.setObjectName("defaultDict_2")
        self.verticalLayout.addWidget(self.defaultDict_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.defaultPathInput = QtWidgets.QLineEdit(settingDialog)
        self.defaultPathInput.setObjectName("defaultPathInput")
        self.verticalLayout_2.addWidget(self.defaultPathInput)
        self.paraPathInput = QtWidgets.QLineEdit(settingDialog)
        self.paraPathInput.setObjectName("paraPathInput")
        self.verticalLayout_2.addWidget(self.paraPathInput)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.defaultPathBrowser = QtWidgets.QToolButton(settingDialog)
        self.defaultPathBrowser.setObjectName("defaultPathBrowser")
        self.verticalLayout_3.addWidget(self.defaultPathBrowser)
        self.paraPathBrowser = QtWidgets.QToolButton(settingDialog)
        self.paraPathBrowser.setObjectName("paraPathBrowser")
        self.verticalLayout_3.addWidget(self.paraPathBrowser)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(settingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(settingDialog)
        self.buttonBox.accepted.connect(settingDialog.accept)
        self.buttonBox.rejected.connect(settingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settingDialog)

    def retranslateUi(self, settingDialog):
        _translate = QtCore.QCoreApplication.translate
        settingDialog.setWindowTitle(_translate("settingDialog", "Dialog"))
        self.defaultDict.setText(_translate("settingDialog", "Default Path  "))
        self.defaultDict_2.setText(_translate("settingDialog", "Paraview Path "))
        self.defaultPathBrowser.setText(_translate("settingDialog", "..."))
        self.paraPathBrowser.setText(_translate("settingDialog", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settingDialog = QtWidgets.QDialog()
    ui = Ui_settingDialog()
    ui.setupUi(settingDialog)
    settingDialog.show()
    sys.exit(app.exec_())
