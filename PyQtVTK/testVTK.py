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













import vtk

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

    def leftButtonPressEvent(self, obj, event):
        self.OnLeftButtonDown()

grid = vtk.vtkUnstructuredGrid()
points = vtk.vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(1, 0, 1)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(0, 1, 1)

points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(2, 0, 0)
points.InsertNextPoint(2, 1, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(1, 0, 1)
points.InsertNextPoint(2, 0, 1)
points.InsertNextPoint(2, 1, 1)
points.InsertNextPoint(1, 1, 1)
grid.SetPoints(points)

cells = vtk.vtkCellArray()
hexa = vtk.vtkHexahedron()
hexa.GetPointIds().SetId(0, 0)
hexa.GetPointIds().SetId(1, 1)
hexa.GetPointIds().SetId(2, 2)
hexa.GetPointIds().SetId(3, 3)
hexa.GetPointIds().SetId(4, 4)
hexa.GetPointIds().SetId(5, 5)
hexa.GetPointIds().SetId(6, 6)
hexa.GetPointIds().SetId(7, 7)
cells.InsertNextCell(hexa)

hexa = vtk.vtkHexahedron()
hexa.GetPointIds().SetId(0, 8)
hexa.GetPointIds().SetId(1, 9)
hexa.GetPointIds().SetId(2, 10)
hexa.GetPointIds().SetId(3, 11)
hexa.GetPointIds().SetId(4, 12)
hexa.GetPointIds().SetId(5, 13)
hexa.GetPointIds().SetId(6, 14)
hexa.GetPointIds().SetId(7, 15)
cells.InsertNextCell(hexa)
grid.SetCells(vtk.VTK_HEXAHEDRON, cells)

# filter
id_filter = vtk.vtkIdFilter()
id_filter.PointIdsOff()
id_filter.CellIdsOn()
id_filter.SetInputData(grid)

# lookup table
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.Build()

# mapper
mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(id_filter.GetOutputPort())
mapper.SelectColorArray(id_filter.GetIdsArrayName())
mapper.SetScalarRange(id_filter.GetOutput().GetScalarRange())
mapper.SetLookupTable(lut)

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

prop = actor.GetProperty()
prop.SetAmbient(0.5)

prop.VertexVisibilityOn()
prop.SetVertexColor(0.5, 1, 0.5)
prop.SetPointSize(5)

prop.SetRepresentationToSurface()
prop.SetRepresentationToWireframe()
# prop.SetRepresentationToPoints()

prop.EdgeVisibilityOff()
prop.SetEdgeColor(1, 1, 0)
prop.SetLineWidth(4)


feature_edge = vtk.vtkFeatureEdges()
feature_edge.SetInputConnection(filter.GetOutputPort())
mapper.SetInputConnection(feature_edge.GetOutputPort())
featureEdge = True
prop = actor.GetProperty()
prop.SetColor(0, 0, 0)
prop.SetLineWidth(2)
prop.SetRepresentationToSurface()
interRender.ReInitialize()

# renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.GradientBackgroundOn()
ren.SetBackground(1, 1, 1)
ren.SetBackground2(0.4, 0.55, .75)

ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(640, 480)

# interactor
inter = vtk.vtkRenderWindowInteractor()
inter.SetRenderWindow(ren_win)
inter.SetInteractorStyle(MouseInteractorStyle())

ren_win.Render()
inter.Initialize()
inter.Start()