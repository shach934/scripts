from PyQt5 import QtGui
from Ui_createSphere import Ui_createSphere

doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createSphere(QDialog, Ui_createSphere):
    def __init__(self, parent=None):
	
        super(createSphere, self).__init__(parent)
        self.setupUi(self) 
		
        self.sphereRadiusInput.setValidator(doubleValidator)
		
        self.sphereResoluThetaInput.setValidator(integelValidator)
        self.sphereResoluAlphaInput.setValidator(integelValidator)
		self.sphereResoluDeltaInput.setValidator(integelValidator)
		
        self.sphereCenterXInput.setValidator(doubleValidator)
        self.sphereCenterYInput.setValidator(doubleValidator)
        self.sphereCenterZInput.setValidator(doubleValidator)