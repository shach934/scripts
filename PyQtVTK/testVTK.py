import sys
import vtk

case = "multiRegionHeater"
filename = "{}/system/controlDict".format(case)

enabled_block = [
    "rightSolid/internalMesh",
    "leftSolid/internalMesh",
    "heater/internalMesh",
]

field = "T"
data_type = "point"

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass


# reader
reader = vtk.vtkOpenFOAMReader()
reader.SetFileName(filename)
reader.Update()

latest_time = reader.GetTimeValues().GetRange()[1]
print("Latest time:", latest_time)

reader.UpdateTimeStep(latest_time)
reader.Update()


n = reader.GetNumberOfPatchArrays()
for i in range(n):
    name = reader.GetPatchArrayName(i)
    print(name)

reader.DisableAllPatchArrays()
for b in enabled_block:
    reader.SetPatchArrayStatus(b, 1)
reader.Update()


block = reader.GetOutput()

array_name = field
array_min = sys.float_info.max
array_max = sys.float_info.min

itr = block.NewIterator()
itr.InitTraversal()
while not itr.IsDoneWithTraversal():
    grid = itr.GetCurrentDataObject()

    if data_type == "cell":
        T = grid.GetCellData().GetArray(field)
    elif data_type == "point":
        T = grid.GetPointData().GetArray(field)
    else:
        assert(0)

    T_min, T_max = T.GetRange()

    if T_min < array_min:
        array_min = T_min
    if T_max > array_max:
        array_max = T_max

    itr.GoToNextItem()


# filter
geom_filter = vtk.vtkGeometryFilter()
geom_filter.SetInputData(reader.GetOutput())

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
mapper.SetScalarRange(array_min, array_max)
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
ren.SetBackground2(0.4, 0.55, .75)

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
text.SetPosition(200, 30)
ren.AddActor(text)

ren_win.Render()
inter.Initialize()
inter.Start()