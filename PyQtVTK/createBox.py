from PyQt5 import QtGui
from Ui_createBox import Ui_createBox
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *

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


    def drawBox(self):
        # Create source
        self.box = vtk.vtkCubeSource()
        self.box.SetCenter([float(self.boxCenterXInput.text()), float(self.boxCenterYInput.text()), float(self.boxCenterZInput.text())])
        self.box.SetXLength(float(self.boxLengthXInput.text()))
        self.box.SetYLength(float(self.boxLengthYInput.text()))
        self.box.SetZLength(float(self.boxLengthZInput.text()))

        # Create a mapper
        self.box_mapper = vtk.vtkPolyDataMapper()
        self.box_mapper.SetInputConnection(self.box.GetOutputPort())
        
        # Create an actor
        self.box_actor = vtk.vtkActor()
        self.box_actor.SetMapper(self.box_mapper)
        #TODO: try to transfer the text color name to a rgb array
        # self.box_actor.GetProperty().SetColor(self.BoxColorComboBox.currentText())
        self.box_actor.GetProperty().SetColor([0.2, 0.4, 0.6])
    
    def push2Window(self, Panel_VTK):
        self.drawBox()
        Panel_VTK.add2Render(self.box_actor)

    def addBox(self):
        pass