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

array = vtk.vtkDoubleArray()
array.SetName("mydata")
array.SetNumberOfComponents(1)
array.InsertNextValue(2)
array.InsertNextValue(1)
grid.GetCellData().AddArray(array)

array = grid.GetCellData().GetArray("mydata")
print(array.GetValue(0), array.GetValue(1))
print(array.GetRange())

# lookup table
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.SetNumberOfColors(2)
lut.Build()

# mapper
mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(grid)
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("mydata")
mapper.SetScalarRange(array.GetRange())
mapper.SetLookupTable(lut)

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

prop = actor.GetProperty()
prop.SetAmbient(0.5)

prop.EdgeVisibilityOn()
prop.SetEdgeColor(0, 0, 0)
prop.SetLineWidth(2)

prop.VertexVisibilityOn()
prop.SetVertexColor(0.5, 1, 0.5)
prop.SetPointSize(5)

prop.SetRepresentationToSurface()

# renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.GradientBackgroundOn()
ren.SetBackground(1, 1, 1)
ren.SetBackground2(0.4, 0.55, .75)

ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(1000, 600)

inter = vtk.vtkRenderWindowInteractor()
inter.SetRenderWindow(ren_win)
inter.SetInteractorStyle(MouseInteractorStyle())

# scalar bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)

scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(inter)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()

ren_win.Render()
inter.Initialize()
inter.Start()