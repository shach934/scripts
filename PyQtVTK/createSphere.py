from PyQt5 import QtGui
from Ui_createSphere import Ui_createSphere
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *

doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

class createSphere(QDialog, Ui_createSphere):

    def __init__(self, Panel_VTK, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createSphere, self).__init__(parent)
        self.outPut = Panel_VTK
        self.sphere = vtk.vtkSphereSource()
        self.setupUi(self) 
        self.validInput()
        self.monitor()
        self.drawSphere()

    def validInput(self):
        self.sphereCenterXInput.setValidator(doubleValidator)
        self.sphereCenterYInput.setValidator(doubleValidator)
        self.sphereCenterZInput.setValidator(doubleValidator)

        self.sphereRadiusInput.setValidator(doubleValidator)
            
        self.sphereResoluThetaInput.setValidator(integelValidator)
        self.sphereResoluPhiInput.setValidator(integelValidator)

    def monitor(self):
        self.sphereResoluThetaInput.textChanged['QString'].connect(self.drawSphere)
        self.sphereResoluPhiInput.textChanged['QString'].connect(self.drawSphere)

        self.sphereCenterXInput.textChanged['QString'].connect(self.drawSphere)
        self.sphereCenterYInput.textChanged['QString'].connect(self.drawSphere)
        self.sphereCenterZInput.textChanged['QString'].connect(self.drawSphere)
        self.sphereRadiusInput.textChanged["QString"].connect(self.drawSphere)

        self.sphereColorCombox.currentTextChanged.connect(self.drawSphere)
        self.createSphereBtn.clicked.connect(self.addSphere)

    def drawSphere(self):
        self.sphere.SetCenter([float(self.sphereCenterXInput.text()), float(self.sphereCenterYInput.text()), float(self.sphereCenterZInput.text())])
        self.sphere.SetRadius(float(self.sphereRadiusInput.text()))
        self.sphere.SetThetaResolution(int(self.sphereResoluThetaInput.text()))
        self.sphere.SetPhiResolution(int(self.sphereResoluPhiInput.text()))

        self.sphereResoluThetaInput.textChanged['QString'].connect(self.drawSphere)
        self.sphereResoluPhiInput.textChanged['QString'].connect(self.drawSphere)

        self.sphere_mapper = vtk.vtkPolyDataMapper()
        self.sphere_mapper.SetInputConnection(self.sphere.GetOutputPort())
        self.sphere_actor = vtk.vtkActor()
        self.sphere_actor.SetMapper(self.sphere_mapper)

        color = self.colorTable.GetColor3d(self.sphereColorCombox.currentText())
        self.sphere_actor.GetProperty().SetColor(color);
        self.outPut.add2Render(self.sphere_actor)

    def addSphere(self):
        pass        