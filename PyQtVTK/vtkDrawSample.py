import sys
import vtk
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(0, 0, 0)
        sphere.SetRadius(1.0)
        sphere.SetPhiResolution (10)

        # Create a mapper
        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())
        
        # Create an actor
        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)

        cube = vtk.vtkCubeSource()
        cube.SetCenter(0, 0, 0)
        cube.SetXLength(1)
        cube.SetYLength(1)
        cube.SetZLength(5)
        
        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        
        self.vtkWidget.SetInteractorStyle(MouseInteractorStyle())

        self.ren.AddActor(sphere_actor)
        self.ren.AddActor(cube_actor)
        self.ren.SetBackground( 0.1, 0.1, 0.1 )
        self.ren.ResetCamera()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()
        self.iren.Start()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())