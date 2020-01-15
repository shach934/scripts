from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QToolBar
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import MouseInteractorStyle

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass

class Panel_VTK(object):
    def __init__(self, domain):
        super().__init__()
        self.setUpUi(domain)

    def setUpUi(self, domain):

        self.window = QtWidgets.QFrame(domain)
        self.windowLayout= QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        self.windowLayout.addWidget(self.tabs)

        self.Geometry = QtWidgets.QWidget()
        self.tabs.addTab(self.Geometry, "Geometry")
        self.Monitor = QtWidgets.QWidget()
        self.tabs.addTab(self.Monitor, "Monitor")
        self.tabs.setCurrentIndex(0)

        self.window.setLayout(self.windowLayout)

        self.GeoFrame = QtWidgets.QFrame()
        vl = QtWidgets.QVBoxLayout(self.Geometry)
        vl.addWidget(self.GeoFrame)
        self.MonitorFrame = QtWidgets.QFrame()
        vl = QtWidgets.QVBoxLayout(self.Monitor)
        vl.addWidget(self.MonitorFrame)
        
        self.GeoLayout = QtWidgets.QVBoxLayout(self.GeoFrame)
        self.MonitorLayout = QtWidgets.QVBoxLayout(self.MonitorFrame)

        self.receiveBar = QtWidgets.QToolBar()
        self.GeoLayout.addWidget(self.receiveBar)

        self.vtkWindow = QVTKRenderWindowInteractor(self.GeoFrame)
        self.GeoLayout.addWidget(self.vtkWindow)

        self.render = vtk.vtkRenderer()
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)

        self.vtkWindow.SetInteractorStyle(MouseInteractorStyle())
        self.interRender = self.vtkWindow.GetRenderWindow().GetInteractor()

        sphere = vtk.vtkCubeSource()
        sphere.SetCenter(0, 0, 0)
        sphere.SetXLength(5.0)
        sphere.SetYLength(15.0)
        sphere.SetZLength(5.0)

        self.filter = vtk.vtkGeometryFilter()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(sphere.GetOutputPort())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        self.render.AddActor(self.actor)
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.2, 0.4, 0.6)
        self.render.SetBackground(1, 1, 1)

        self.fields = []
        self.timeSteps = []
        Label = QtWidgets.QLabel("Field")
        self.receiveBar.addWidget(Label)
        Label = QtWidgets.QLabel("Time")
        self.receiveBar.addWidget(Label)

        self.fieldSelectCombo = QtWidgets.QComboBox()
        self.timeSelectCombo = QtWidgets.QComboBox()

        self.receiveBar.addWidget(self.fieldSelectCombo)
        self.receiveBar.addWidget(self.timeSelectCombo)

        self.GeoFrame.setLayout(self.GeoLayout)
        self.interRender.Initialize()
        self.interRender.Start()
        self.window.show()

        """
        # self.receiveBar.addAction(self.actionAuto_Scale)
        # self.receiveBar.addAction(self.actionSet_Scale)
        # self.addTransparencyBar()
        """
    def OFinterRender(self, vtkObject):

        tArray = vtk_to_numpy(self.foamVTKGeo.GetTimeValues())
        self.foamVTKGeo.UpdateTimeStep(tArray[-1])
        self.foamVTKGeo.Update()

        self.filter.SetInputConnection(self.foamVTKGeo.GetOutputPort())

        self.mapper.SetInputConnection(self.filter.GetOutputPort())
        self.mapper.SetScalarModeToUseCellFieldData()

        self.mapper.SelectColorArray("U")
        self.mapper.SetScalarRange(0, 3)

        self.actor.SetMapper(self.mapper)
        # set the presentation style
        actorProper = self.actor.GetProperty()  # property of the VTK view

        # show the mesh edge, it is using the surface and integralMesh together
        actorProper.EdgeVisibilityOn()
        actorProper.SetEdgeColor(0, 0, 0)
        actorProper.SetLineWidth(2)

        self.interRender.AddActor(self.actor)

        self.vtkWindow.GetinterRenderWindow().AddinterRenderer(self.interRender)
        self.vtkWindow.SetInteractorStyle(MouseInteractorStyle())
        self.vtkWindow.Initialize()
        self.setupVTKBackGround()
        self.AddAxes()
        self.setScaleBar()
        self.vtkWindow.Start()
        self.vtkWindow.show()

    def wireFrameView(self):
        prop = self.actor.GetProperty()
        if not self.wireFrame:
            prop.SetRepresentationToWireframe()
            self.wireFrame = True
        else:
            prop.SetRepresentationToSurface()
            self.wireFrame = False
        self.vtkWindow.interRender()

    def featureEdgeView(self):
        if not self.featureEdge:
            feature_edge = vtk.vtkFeatureEdges()
            feature_edge.SetInputConnection(self.filter.GetOutputPort())
            self.mapper.SetInputConnection(feature_edge.GetOutputPort())
            self.featureEdge = True
            prop = self.actor.GetProperty()
            prop.SetColor(0, 0, 0)
            prop.SetLineWidth(2)
            prop.SetRepresentationToSurface()
            self.vtkWindow.interRender()
        else:
            self.mapper.SetInputConnection(self.filter.GetOutputPort())
            self.mapper.SetScalarModeToUseCellFieldData()
            self.vtkWindow.interRender()
            self.featureEdge = False

    def meshOnOff(self):
        prop = self.actor.GetProperty()
        prop.EdgeVisibilityOff()
        prop.EdgeVisibilityOn()
        prop.SetEdgeColor(1, 1, 1)
        prop.SetLineWidth(0)
        self.vtkWindow.interRender()
    
    def AddAxes(self):
        axesActor = vtk.vtkAxesActor()
        self.axesWidget.SetOrientationMarker(axesActor)
        self.axesWidget.SetInteractor(self.vtkWindow)
        self.axesWidget.SetOutlineColor(1, 1, 1)
        self.axesWidget.EnabledOn()
        self.axesWidget.InteractiveOff()  # InteractiveOn to enable move the axis
        self.axesWidget.SetViewport(0., 0., 0.2, 0.2)

    def setupVTKBackGround(self):
        self.interRender.GradientBackgroundOn()
        self.interRender.SetBackground2(0.2, 0.4, 0.6)
        self.interRender.SetBackground(1, 1, 1)

    def setScaleBar(self):
        # lookup table
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.667, 0)
        lut.SetNumberOfColors(10)
        lut.Build()

        # scalar bar
        self.scalar_bar.SetLookupTable(lut)

        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(self.vtkWindow)
        scalar_bar_widget.SetScalarBarActor(self.scalar_bar)
        scalar_bar_widget.On()

    def updateMapperField(self):
        mapperField = str(self.fieldSelectCombo.currentText())

    def updateTime(self):
        timeStep = int(str(self.timeSelectCombo.currentText()))

    def addTransparencyBar(self):
        self.transparencySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.receiveBar.addWidget(self.transparencySlider)
        self.transparencySlider.setFixedWidth(100)
        self.transparencySlider.setMinimum(0)
        self.transparencySlider.setMaximum(100)
        self.transparencySlider.setValue(0)
        self.transparencySlider.setSingleStep(1)
        self.transparencySlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transparencySlider.setTickInterval(20)
        self.transparencySlider.valueChanged.connect(self.adjustTransparent)

    def adjustTransparent(self):
        transparencyValue = self.transparencySlider.value()
        prop = self.actor.GetProperty()
        prop.SetOpacity(1 - transparencyValue / 100)
        self.vtkWindow.interRender()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QFrame()
    ui = Panel_VTK(window)
    window.show()
    sys.exit(app.exec_())