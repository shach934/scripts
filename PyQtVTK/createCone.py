from PyQt5 import QtGui
from Ui_createCone import Ui_createCone

doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createCone(QDialog, Ui_createCone):
    def __init__(self, parent=None):
	
        super(createCone, self).__init__(parent)
        self.setupUi(self) 
		
        self.coneRadiusInput.setValidator(doubleValidator)
		self.coneHeightInput.setValidator(doubleValidator)
		
        self.coneResoluInput.setValidator(integelValidator)
		
        self.coneCenterXInput.setValidator(doubleValidator)
        self.coneCenterYInput.setValidator(doubleValidator)
        self.coneCenterZInput.setValidator(doubleValidator)