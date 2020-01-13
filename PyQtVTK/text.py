import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog, QGroupBox, QTabWidget
from PyQt5.uic import loadUi, loadUiType


Form, Base = loadUiType('physicsProperty.ui') # this path should be a relative path. For testing you can use absolute path.
class CustomWidget(Form, Base):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.setupUi(self)
        

Form2, Base2 = loadUiType('mainWindow.ui') # this path should be a relative path. For testing you can use absolute path.
class Window(Form2, Base2):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.cWidget = CustomWidget(self)
        h_la = QtWidgets.QHBoxLayout()
        h_la.addWidget(self.cWidget)
        self.propertyBox.setLayout(h_la)

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())