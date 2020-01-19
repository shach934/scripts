from PyQt5 import QtGui
from Ui_createBox import Ui_createBox
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *

doubleValidator = QtGui.QDoubleValidator()

class createBox(QDialog, Ui_createBox):

    def __init__(self, Panel_VTK, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createBox, self).__init__(parent)
        self.outPut = Panel_VTK
        self.box = vtk.vtkCubeSource()
        self.setupUi(self) 
        self.validInput()
        self.monitor()
        self.drawBox()

    def validInput(self):
        self.boxCenterXInput.setValidator(doubleValidator)
        self.boxCenterYInput.setValidator(doubleValidator)
        self.boxCenterZInput.setValidator(doubleValidator)

        self.boxLengthXInput.setValidator(doubleValidator)
        self.boxLengthYInput.setValidator(doubleValidator)
        self.boxLengthZInput.setValidator(doubleValidator)

    def monitor(self):
        self.boxLengthXInput.textChanged['QString'].connect(self.drawBox)
        self.boxLengthYInput.textChanged['QString'].connect(self.drawBox)
        self.boxLengthZInput.textChanged['QString'].connect(self.drawBox)

        self.boxCenterXInput.textChanged['QString'].connect(self.drawBox)
        self.boxCenterYInput.textChanged['QString'].connect(self.drawBox)
        self.boxCenterZInput.textChanged['QString'].connect(self.drawBox)

        self.boxColorCombox.currentTextChanged.connect(self.drawBox)
        self.createBoxBtn.clicked.connect(self.addBox)

    def drawBox(self):
        self.box.SetCenter([float(self.boxCenterXInput.text()), float(self.boxCenterYInput.text()), float(self.boxCenterZInput.text())])
        self.box.SetXLength(float(self.boxLengthXInput.text()))
        self.box.SetYLength(float(self.boxLengthYInput.text()))
        self.box.SetZLength(float(self.boxLengthZInput.text()))

        self.box_mapper = vtk.vtkPolyDataMapper()
        self.box_mapper.SetInputConnection(self.box.GetOutputPort())
        self.box_actor = vtk.vtkActor()
        self.box_actor.SetMapper(self.box_mapper)
        #TODO: try to transfer the text color name to a rgb array
        color = self.colorTable.GetColor3d(self.boxColorCombox.currentText())
        self.box_actor.GetProperty().SetColor(color);
        self.outPut.add2Render(self.box_actor)

    def addBox(self):
        filename = self.boxNameInput.text() + ".stl" 
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.box.GetOutputPort()) 
        writer.Write() 