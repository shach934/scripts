from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *

from Ui_createBox import Ui_createBox
from Ui_createSphere import Ui_createSphere
from Ui_createCone import Ui_createCone
from Ui_createCylinder import Ui_createCylinder

doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 1000)

#------------------------------------------------------------------------------
class createBox(QDialog, Ui_createBox):

    def __init__(self, render, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createBox, self).__init__(parent)
        self.render = render
        self.box = vtk.vtkCubeSource()
        self.setupUi(self) 
        self.validInput()
        self.monitor()
        self.drawBox()
        self.show()
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
        self.createBoxBtn.clicked.connect(self.saveBox)

    def drawBox(self):
        self.box.SetCenter([float(self.boxCenterXInput.text()), float(self.boxCenterYInput.text()), float(self.boxCenterZInput.text())])
        self.box.SetXLength(float(self.boxLengthXInput.text()))
        self.box.SetYLength(float(self.boxLengthYInput.text()))
        self.box.SetZLength(float(self.boxLengthZInput.text()))

        self.box_mapper = vtk.vtkPolyDataMapper()
        self.box_mapper.SetInputConnection(self.box.GetOutputPort())
        self.box_actor = vtk.vtkActor()
        self.box_actor.SetMapper(self.box_mapper)
        color = self.colorTable.GetColor3d(self.boxColorCombox.currentText())
        self.box_actor.GetProperty().SetColor(color);
        self.render.AddActor(self.box_actor)

    def saveBox(self, path):
        filename = path + "/" + self.boxNameInput.text() + ".stl" 
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.box.GetOutputPort()) 
        writer.Write() 

#------------------------------------------------------------------------------
class createSphere(QDialog, Ui_createSphere):

    def __init__(self, render, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createSphere, self).__init__(parent)
        self.render = render
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
        self.createSphereBtn.clicked.connect(self.saveSphere)

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
        self.render.AddActor(self.sphere_actor)

    def saveSphere(self, path):
        filename = path + "/" + self.sphereNameInput.text() + "stl" 
        self.sphere.SetThetaResolution(int(self.sphereResoluThetaInput.text())) 
        self.sphere.SetPhiResolution(int(self.sphereResoluPhiInput.text())) 
        
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.sphere.GetOutputPort()) 
        writer.Write() 

#------------------------------------------------------------------------------
class createCylinder(QDialog, Ui_createCylinder):

    def __init__(self, render, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createCylinder, self).__init__(parent)
        self.render = render
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
        self.createCylinderBtn.clicked.connect(self.saveCylinder)

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
        self.render.AddActor(self.cylinder_actor)

    def saveCylinder(self, path):
        filename = path + "/" + self.cylinderNameInput.text() + "stl" 
        self.cylinder.SetResolution(int(self.cylinderResoluInput.text())) 
        
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.cylinder.GetOutputPort()) 
        writer.Write() 

#------------------------------------------------------------------------------
class createCone(QDialog, Ui_createCone):
    def __init__(self, render, parent=None):
        self.colorTable = vtk.vtkNamedColors()
        super(createCone, self).__init__(parent)
        self.render = render
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
        self.createConeBtn.clicked.connect(self.saveCone)

    def drawCone(self, window):
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
        self.render.AddActor(self.cone_actor)

    def saveCone(self, path):
        filename = path + "/" + self.coneNameInput.text() + "stl" 
        self.cone.SetResolution(int(self.coneResoluInput.text())) 
        
        writer = vtk.vtkSTLWriter() 
        writer.SetFileName(filename) 
        writer.SetInputConnection(self.cone.GetOutputPort()) 
        writer.Write() 