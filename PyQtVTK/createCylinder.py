from Ui_createCylinder import Ui_createCylinder
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *


doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createCylinder(QDialog, Ui_createCylinder):

    def __init__(self, Panel_VTK, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createCylinder, self).__init__(parent)
        self.outPut = Panel_VTK
        self.cylinder = vtk.vtkCylinderSource()
        self.setupUi(self) 
        self.validInput()
        self.monitor()
        self.drawCylinder()

    def validInput(self):
        self.cylinderRadiusInput.setValidator(doubleValidator)
        self.cylinderHeightInput.setValidator(doubleValidator)
        self.cylinderResoluInput.setValidator(integelValidator)

        self.cylinderCenterXInput.setValidator(doubleValidator)
        self.cylinderCenterYInput.setValidator(doubleValidator)
        self.cylinderCenterZInput.setValidator(doubleValidator)

    def monitor(self):
        self.cylinderRadiusInput.textChanged['QString'].connect(self.drawCylinder)
        self.cylinderHeightInput.textChanged['QString'].connect(self.drawCylinder)
        self.cylinderResoluInput.textChanged['QString'].connect(self.drawCylinder)

        self.cylinderCenterXInput.textChanged['QString'].connect(self.drawCylinder)
        self.cylinderCenterYInput.textChanged['QString'].connect(self.drawCylinder)
        self.cylinderCenterZInput.textChanged['QString'].connect(self.drawCylinder)

        self.cylinderColorCombox.currentTextChanged.connect(self.drawCylinder)
        self.createCylinderBtn.clicked.connect(self.addCylinder)

    def drawCylinder(self):
        self.cylinder.SetCenter([float(self.cylinderCenterXInput.text()), float(self.cylinderCenterYInput.text()), float(self.cylinderCenterZInput.text())])
        self.cylinder.SetHeight(float(self.cylinderHeightInput.text()))
        self.cylinder.SetRadius(float(self.cylinderRadiusInput.text()))
        self.cylinder.SetResolution(int(self.cylinderResoluInput.text()))

        self.cylinder_mapper = vtk.vtkPolyDataMapper()
        self.cylinder_mapper.SetInputConnection(self.cylinder.GetOutputPort())
        self.cylinder_actor = vtk.vtkActor()
        self.cylinder_actor.SetMapper(self.cylinder_mapper)

        color = self.colorTable.GetColor3d(self.cylinderColorCombox.currentText())
        self.cylinder_actor.GetProperty().SetColor(color);
        self.outPut.add2Render(self.cylinder_actor)

    def addCylinder(self):
        pass        