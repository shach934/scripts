import vtk
from math import sqrt

case = "cavity"
filename = "{}/system/controlDict".format(case)
field = "U"
data_type = "cell"

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass

# reader
reader = vtk.vtkOpenFOAMReader()
reader.SetFileName(filename)
reader.Update()

#n = reader.GetTimeValues().GetNumberOfValues()
#latest_time = reader.GetTimeValues().GetValue(n-1)
latest_time = reader.GetTimeValues().GetRange()[1]

reader.UpdateTimeStep(latest_time)
reader.Update()

block = reader.GetOutput()
grid = block.GetBlock(0)

if field == "p":
    if data_type == "cell":
        p = grid.GetCellData().GetArray("p")
    elif data_type == "point":
        p = grid.GetPointData().GetArray("p")
    else:
        assert(0)

    array_name = "p"
    array = p
elif field == "U":
    magU = vtk.vtkDoubleArray()
    magU.SetName("magU")
    magU.SetNumberOfComponents(1)

    if data_type == "cell":
        U = grid.GetCellData().GetArray("U")
    elif data_type == "point":
        U = grid.GetPointData().GetArray("U")
    else:
        assert(0)

    for i in range(U.GetNumberOfTuples()):
        Ux = U.GetComponent(i, 0)
        Uy = U.GetComponent(i, 1)
        Uz = U.GetComponent(i, 2)
        magU.InsertNextValue(sqrt(Ux*Ux + Uy*Uy + Uz*Uz))

    if data_type == "cell":
        grid.GetCellData().AddArray(magU)
    elif data_type == "point":
        grid.GetPointData().AddArray(magU)
    else:
        assert(0)

    array_name = "magU"
    array = magU
else:
    assert(0)

# filter
geom_filter = vtk.vtkGeometryFilter()
geom_filter.SetInputData(block)

# lookup table
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.Build()

# mapper
mapper = vtk.vtkCompositePolyDataMapper()
mapper.SetInputConnection(geom_filter.GetOutputPort())
if data_type == "cell":
    mapper.SetScalarModeToUseCellFieldData()
elif data_type == "point":
    mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray(array_name)
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

prop.SetRepresentationToSurface()

# renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.GradientBackgroundOn()
ren.SetBackground(1, 1, 1)
ren.SetBackground2(0.4, 0.55, 0.75)

ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(640, 480)

# interactor
inter = vtk.vtkRenderWindowInteractor()
inter.SetRenderWindow(ren_win)
inter.SetInteractorStyle(MouseInteractorStyle())

# scalar bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToVertical()
scalar_bar.SetLookupTable(lut)
prop = vtk.vtkTextProperty()
prop.SetColor(0, 0, 0)
prop.SetFontSize(20)
prop.SetFontFamilyToArial()
prop.ItalicOff()
prop.BoldOff()
scalar_bar.UnconstrainedFontSizeOn()
scalar_bar.SetTitleTextProperty(prop)
scalar_bar.SetLabelTextProperty(prop)
scalar_bar.SetLabelFormat("%5.2f")
scalar_bar.SetTitle(array_name)
ren.AddActor(scalar_bar)

# text
text = vtk.vtkTextActor()
text.SetInput(case)
text.GetTextProperty().SetColor(0, 0, 0)
text.GetTextProperty().SetFontSize(24)
text.SetPosition(300, 30)
ren.AddActor(text)

ren_win.Render()
inter.Initialize()
inter.Start()