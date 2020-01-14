# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_tab.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(Form)
        self.tabs.setObjectName("tabs")
        self.Geometry = QtWidgets.QWidget()
        self.Geometry.setObjectName("Geometry")
        self.tabs.addTab(self.Geometry, "")
        self.Monitor = QtWidgets.QWidget()
        self.Monitor.setObjectName("Monitor")
        self.tabs.addTab(self.Monitor, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(Form)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabs.setTabText(self.tabs.indexOf(self.Geometry), _translate("Form", "Geometry"))
        self.tabs.setTabText(self.tabs.indexOf(self.Monitor), _translate("Form", "Monitor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
