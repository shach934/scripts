import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog, QGroupBox, QTabWidget
from PyQt5.uic import loadUi, loadUiType
from mainWindow import Ui_OpenFOAM
from physicsProperty import Ui_physicsProperties
from createBox import Ui_createBox

class physicsProperty(QDialog, Ui_physicsProperties):
    def __init__(self, parent=None):
        super(physicsProperty, self).__init__(parent)
        self.setupUi(self)

class createBox(QDialog, Ui_createBox):
    def __init__(self, parent=None):
        super(createBox, self).__init__(parent)
        self.setupUi(self) 

class Window(QMainWindow, Ui_OpenFOAM):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.cWidget = createBox(self)
        h_la = QtWidgets.QHBoxLayout()
        h_la.addWidget(self.cWidget)
        self.propertyBox.setLayout(h_la)

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())