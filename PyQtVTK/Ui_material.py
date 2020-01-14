# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_material.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 54, 47, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 120, 47, 14))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(70, 160, 47, 14))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(180, 60, 60, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(180, 110, 60, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Equation of State"))
        self.label_2.setText(_translate("Form", "ThermoDynamics"))
        self.label_3.setText(_translate("Form", "Transport"))
        self.comboBox.setItemText(0, _translate("Form", "Perfect Gas"))
        self.comboBox.setItemText(1, _translate("Form", "Incompressible Perfect Gas"))
        self.comboBox.setItemText(2, _translate("Form", "Constant Density"))
        self.comboBox.setItemText(3, _translate("Form", "Perfect Fluid"))
        self.comboBox.setItemText(4, _translate("Form", "Adiabatic Perfect Fluid"))
        self.comboBox.setItemText(5, _translate("Form", "Polynomial"))
        self.comboBox.setItemText(6, _translate("Form", "Peng-Robinson"))
        self.comboBox_2.setItemText(0, _translate("Form", "constant"))
        self.comboBox_2.setItemText(1, _translate("Form", "Janaf"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
