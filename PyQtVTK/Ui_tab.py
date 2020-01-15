# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_tab.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(domain)
        self.tabs = QtWidgets.QTabWidget()
        self.Geometry = QtWidgets.QWidget()
        self.GeoLayout = QtWidgets.QVBoxLayout(self.Geometry)
        self.GeoFrame = QtWidgets.QFrame(self.Geometry)
        self.GeoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GeoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GeoLayout.addWidget(self.GeoFrame)
        self.tabs.addTab(self.Geometry, "Geometry")
        self.Monitor = QtWidgets.QWidget()
        self.MoniLayout = QtWidgets.QVBoxLayout(self.Monitor)
        self.MonitorFrame = QtWidgets.QFrame(self.Monitor)
        self.MonitorFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MonitorFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MoniLayout.addWidget(self.MonitorFrame)
        self.tabs.addTab(self.Monitor, "Monitor")
        self.verticalLayout.addWidget(self.tabs)
        self.tabs.setCurrentIndex(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Form()
    ui.setupUi()
    sys.exit(app.exec_())
