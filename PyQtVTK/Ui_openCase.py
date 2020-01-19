# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_openCase.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_openCase(object):
    def setupUi(self, openCase):
        openCase.setObjectName("openCase")
        openCase.resize(400, 92)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(openCase)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(openCase)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.openCasePathInput = QtWidgets.QLineEdit(openCase)
        self.openCasePathInput.setObjectName("openCasePathInput")
        self.horizontalLayout.addWidget(self.openCasePathInput)
        self.openCaseBrowser = QtWidgets.QToolButton(openCase)
        self.openCaseBrowser.setObjectName("openCaseBrowser")
        self.horizontalLayout.addWidget(self.openCaseBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(openCase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(openCase)
        self.buttonBox.accepted.connect(openCase.accept)
        self.buttonBox.rejected.connect(openCase.reject)
        QtCore.QMetaObject.connectSlotsByName(openCase)

    def retranslateUi(self, openCase):
        _translate = QtCore.QCoreApplication.translate
        openCase.setWindowTitle(_translate("openCase", "Dialog"))
        self.label_2.setText(_translate("openCase", "Path"))
        self.openCaseBrowser.setText(_translate("openCase", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    openCase = QtWidgets.QDialog()
    ui = Ui_openCase()
    ui.setupUi(openCase)
    openCase.show()
    sys.exit(app.exec_())
