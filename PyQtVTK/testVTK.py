import sys, math
import vtk
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass

class main(object):

    def __init__(self, parent = None):
        # Qt.QMainWindow.__init__(self, parent)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        Label = QLabel("Test Label")
        self.vl.addWidget(Label)

        self.btn = QPushButton("Click mig")
        self.vl.addWidget(self.btn)
        self.btn.clicked.connect(self.resetView)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)

        self.vtkWidget.SetInteractorStyle(MouseInteractorStyle())

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        sphere = vtk.vtkCubeSource()
        sphere.SetCenter(0, 0, 0)
        sphere.SetXLength(5.0)
        sphere.SetYLength(15.0)
        sphere.SetZLength(5.0)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.ren.AddActor(actor)
        self.ren.GradientBackgroundOn()
        self.ren.SetBackground2(0.2, 0.4, 0.6)
        self.ren.SetBackground(1, 1, 1)

        self.frame.setLayout(self.vl)
        self.iren.Initialize()
        self.iren.Start()
        self.frame.show()

    def resetView(self):
        self.ren.ResetCamera()
        fp = self.ren.GetActiveCamera().GetFocalPoint()
        p = self.ren.GetActiveCamera().GetPosition()
        dist = math.sqrt( (p[0]-fp[0])**2 + (p[1]-fp[1])**2 + (p[2]-fp[2])**2 )
        self.ren.GetActiveCamera().SetPosition(fp[0], fp[1], fp[2]+dist)
        self.ren.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.iren.Initialize()
        self.iren.Start()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = main()
    sys.exit(app.exec_())