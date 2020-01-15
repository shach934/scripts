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
        self.box = vtk.vtBoxSource()
        self.box.SetCenter([float(self.boxCenterXInput), float(self.boxCenterYInput), float(self.boxCenterZInput)])
        self.box.SetXLength(float(self.boxLengthXInput))
        self.box.SetYLength(float(self.boxLengthYInput))
        self.box.SetZLength(float(self.boxLengthZInput))

        # Create a mapper
        self.box_mapper = vtk.vtkPolyDataMapper()
        self.box_mapper.SetInputConnection(self.box.GetOutputPort())
        
        # Create an actor
        self.box_actor = vtk.vtkActor()
        self.box_actor.SetMapper(self.box_mapper)
        self.box_actor.GetProperty().SetColor(self.BoxColorComboBox)
        self.push2Window(self.box_actor)
    
    def push2Window(self, Panel_VTK):
        Panel_VTK.render.AddActor(self.box_actor)