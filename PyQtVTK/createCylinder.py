from PyQt5 import QtGui
from Ui_createCylinder import Ui_createCylinder
from PyQt5.QtWidgets import QDialog
import vtk

doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createCylinder(QDialog, Ui_createCylinder):
    def __init__(self, parent=None):

        super(createCylinder, self).__init__(parent)
        self.setupUi(self) 

        self.cylinderRadiusInput.setValidator(doubleValidator)
        self.cylinderHeightInput.setValidator(doubleValidator)

        self.cylinderResoluInput.setValidator(integelValidator)

        self.cylinderCenterXInput.setValidator(doubleValidator)
        self.cylinderCenterYInput.setValidator(doubleValidator)
        self.cylinderCenterZInput.setValidator(doubleValidator)