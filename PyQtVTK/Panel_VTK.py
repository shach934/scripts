from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QToolBar
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import MouseInteractorStyle

class VTKWindow(object):
    def __init__(self, domain):
        super().__init__()

        self.wireFrame = False
        self.featureEdge = False
        # self.actionFrame.triggered.connect(self.featureEdgeView)
        
        self.mainViewTabs = QtWidgets.QTabWidget(domain)
        
        self.geoTab = QtWidgets.QWidget()
        self.geoTab.setSizeIncrement(QtCore.QSize(0, 0))

        self.geoTab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainViewTabs.addTab(self.geoTab, "Geometry")
        
        self.geoTabLayout = QtWidgets.QVBoxLayout()
        self.receiveBar = QToolBar()
        self.geoTabLayout.addWidget(self.receiveBar)

        self.monitorTab = QtWidgets.QWidget()
        self.mainViewTabs.addTab(self.monitorTab, "Monitor")

        self.vtkWindow = QVTKRenderWindowInteractor()
        self.foamVTKGeo = vtk.vtkOpenFOAMReader()
        self.filter = vtk.vtkGeometryFilter()
        self.mapper = vtk.vtkCompositePolyDataMapper2()
        self.actor = vtk.vtkActor()
        self.render = vtk.vtkRenderer()

        self.geoTabLayout.addWidget(self.vtkWindow)
        self.fields = ["T", "Ux", "Uy", "Uz", "magU", "p", "k", "epsilon", "G", "rho"]
        self.timeSteps = ["0"]
        self.fieldSelectCombo = QtWidgets.QComboBox()
        self.timeSelectCombo = QtWidgets.QComboBox()
        for item in self.fields:
            self.fieldSelectCombo.addItem(item)
        for time in self.timeSteps:
            self.timeSelectCombo.addItem(time)

        self.receiveBar.addWidget(self.fieldSelectCombo)
        self.receiveBar.addWidget(self.timeSelectCombo)
        
        self.mainViewTabs.show()
        """
        # VTK related initialization.


        self.geoTab.setLayout(self.geoTabLayout)
        # GUI related initialization. some of them from case files.

        # self.receiveBar.addAction(self.actionAuto_Scale)
        # self.receiveBar.addAction(self.actionSet_Scale)
        # self.addTransparencyBar()

        """
    def render(self, vtkObject):

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

        self.render.AddActor(self.actor)

        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)
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
        self.vtkWindow.Render()

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
            self.vtkWindow.Render()
        else:
            self.mapper.SetInputConnection(self.filter.GetOutputPort())
            self.mapper.SetScalarModeToUseCellFieldData()
            self.vtkWindow.Render()
            self.featureEdge = False

    def meshOnOff(self):
        prop = self.actor.GetProperty()
        prop.EdgeVisibilityOff()
        prop.EdgeVisibilityOn()
        prop.SetEdgeColor(1, 1, 1)
        prop.SetLineWidth(0)
        self.vtkWindow.Render()
    
    def AddAxes(self):
        axesActor = vtk.vtkAxesActor()
        self.axesWidget.SetOrientationMarker(axesActor)
        self.axesWidget.SetInteractor(self.vtkWindow)
        self.axesWidget.SetOutlineColor(1, 1, 1)
        self.axesWidget.EnabledOn()
        self.axesWidget.InteractiveOff()  # InteractiveOn to enable move the axis
        self.axesWidget.SetViewport(0., 0., 0.2, 0.2)


    def setupVTKBackGround(self):
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.2, 0.4, 0.6)
        self.render.SetBackground(1, 1, 1)

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
        self.vtkWindow.Render()