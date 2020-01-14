from PyQt5 import QtGui
from Ui_createBox import Ui_createBox

doubleValidator = QtGui.QDoubleValidator()

class createBox(QDialog, Ui_createBox):
    def __init__(self, parent=None):
	
        super(createBox, self).__init__(parent)
        self.setupUi(self) 
		
        self.boxLengthXInput.setValidator(doubleValidator)
        self.boxLengthYInput.setValidator(doubleValidator)
        self.boxLengthZInput.setValidator(doubleValidator)

        self.boxCenterXInput.setValidator(doubleValidator)
        self.boxCenterYInput.setValidator(doubleValidator)
        self.boxCenterZInput.setValidator(doubleValidator)