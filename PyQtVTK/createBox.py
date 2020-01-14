from PyQt5 import QtGui
from Ui_createBox import Ui_createBox
from PyQt5.QtWidgets import QDialog

doubleValidator = QtGui.QDoubleValidator()

class createBox(QDialog, Ui_createBox):

    def __init__(self, parent=None):
	
        super(createBox, self).__init__(parent)
        self.setupUi(self) 
		
        self.boxCenterXInput.setValidator(doubleValidator)
        self.boxCenterYInput.setValidator(doubleValidator)
        self.boxCenterZInput.setValidator(doubleValidator)
        
        self.boxLengthXInput.setValidator(doubleValidator)
        self.boxLengthYInput.setValidator(doubleValidator)
        self.boxLengthZInput.setValidator(doubleValidator)

