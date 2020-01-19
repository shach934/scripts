# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_newCase.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newCase(object):
    def setupUi(self, newCase):
        newCase.setObjectName("newCase")
        newCase.resize(341, 130)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(newCase)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(newCase)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(newCase)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.newCaseNameInput = QtWidgets.QLineEdit(newCase)
        self.newCaseNameInput.setObjectName("newCaseNameInput")
        self.verticalLayout.addWidget(self.newCaseNameInput)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newCasePathInput = QtWidgets.QLineEdit(newCase)
        self.newCasePathInput.setObjectName("newCasePathInput")
        self.horizontalLayout.addWidget(self.newCasePathInput)
        self.newCaseBrowser = QtWidgets.QToolButton(newCase)
        self.newCaseBrowser.setObjectName("newCaseBrowser")
        self.horizontalLayout.addWidget(self.newCaseBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(newCase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(newCase)
        self.buttonBox.accepted.connect(newCase.accept)
        self.buttonBox.rejected.connect(newCase.reject)
        QtCore.QMetaObject.connectSlotsByName(newCase)

    def retranslateUi(self, newCase):
        _translate = QtCore.QCoreApplication.translate
        newCase.setWindowTitle(_translate("newCase", "Dialog"))
        self.label.setText(_translate("newCase", "Name"))
        self.label_2.setText(_translate("newCase", "Path"))
        self.newCaseNameInput.setText(_translate("newCase", "case_1"))
        self.newCaseBrowser.setText(_translate("newCase", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newCase = QtWidgets.QDialog()
    ui = Ui_newCase()
    ui.setupUi(newCase)
    newCase.show()
    sys.exit(app.exec_())
