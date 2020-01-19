from Ui_createCone import Ui_createCone
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *


doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createCone(QDialog, Ui_createCone):
    def __init__(self, Panel_VTK, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createCone, self).__init__(parent)
        self.outPut = Panel_VTK
        self.cone = vtk.vtkConeSource()
        self.setupUi(self) 
        self.validInput()
        self.monitor()
        self.drawCone()

    def validInput(self):
        self.coneRadiusInput.setValidator(doubleValidator)
        self.coneHeightInput.setValidator(doubleValidator)
        self.coneResoluInput.setValidator(integelValidator)
        
        self.coneDirectXInput.setValidator(doubleValidator)
        self.coneDirectYInput.setValidator(doubleValidator)
        self.coneDirectZInput.setValidator(doubleValidator)

        self.coneCenterXInput.setValidator(doubleValidator)
        self.coneCenterYInput.setValidator(doubleValidator)
        self.coneCenterZInput.setValidator(doubleValidator)

    def monitor(self):
        self.coneRadiusInput.textChanged['QString'].connect(self.drawCone)
        self.coneHeightInput.textChanged['QString'].connect(self.drawCone)
        self.coneResoluInput.textChanged['QString'].connect(self.drawCone)

        self.coneDirectXInput.textChanged['QString'].connect(self.drawCone)
        self.coneDirectYInput.textChanged['QString'].connect(self.drawCone)
        self.coneDirectZInput.textChanged['QString'].connect(self.drawCone)

        self.coneCenterXInput.textChanged['QString'].connect(self.drawCone)
        self.coneCenterYInput.textChanged['QString'].connect(self.drawCone)
        self.coneCenterZInput.textChanged['QString'].connect(self.drawCone)

        self.coneColorCombox.currentTextChanged.connect(self.drawCone)
        self.createConeBtn.clicked.connect(self.addCone)

    def drawCone(self):
        self.cone.SetCenter([float(self.coneCenterXInput.text()), float(self.coneCenterYInput.text()), float(self.coneCenterZInput.text())])
        self.cone.SetHeight(float(self.coneHeightInput.text()))
        self.cone.SetRadius(float(self.coneRadiusInput.text()))
        self.cone.SetDirection([float(self.coneDirectXInput.text()), float(self.coneDirectYInput.text()), float(self.coneDirectZInput.text())])
        self.cone.SetResolution(int(self.coneResoluInput.text()))

        self.cone_mapper = vtk.vtkPolyDataMapper()
        self.cone_mapper.SetInputConnection(self.cone.GetOutputPort())
        self.cone_actor = vtk.vtkActor()
        self.cone_actor.SetMapper(self.cone_mapper)

        color = self.colorTable.GetColor3d(self.coneColorCombox.currentText())
        self.cone_actor.GetProperty().SetColor(color);
        self.outPut.add2Render(self.cone_actor)

    def addCone(self):
        filename = self.coneNameInput.text() + "stl" 
        self.cone.SetResolution(int(self.coneResoluInput.text())) 
        
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.cone.GetOutputPort()) 
        writer.Write() 