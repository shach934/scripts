from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QToolBar
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk, math
import MouseInteractorStyle

#TODO: the cursor change the shape in the window. try to change it back to a normal mouse.

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass

class Panel_VTK(object):
    def __init__(self, domain):
        super().__init__()
        self.setUpUiStructure(domain)
        self.setUpBar()
        self.setUpVTKWindow()

    def setUpUiStructure(self, domain):

        self.window = QtWidgets.QFrame(domain)
        self.windowLayout= QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        self.windowLayout.addWidget(self.tabs)
        self.window.setLayout(self.windowLayout)

        self.Geometry = QtWidgets.QWidget()
        self.tabs.addTab(self.Geometry, "Geometry")
        self.Monitor = QtWidgets.QWidget()
        self.tabs.addTab(self.Monitor, "Monitor")
        self.tabs.setCurrentIndex(0)

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

    def setUpBar(self):

        self.actionAlign_X = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Xaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAlign_X.setIcon(icon)
        
        self.actionAlign_Y = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Yaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAlign_Y.setIcon(icon)
        
        self.actionAligh_Z = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Zaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAligh_Z.setIcon(icon)

        self.actionFit_Window = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/fit window.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFit_Window.setIcon(icon)

        self.actionFrame = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/frame.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFrame.setIcon(icon)

        self.actionAuto_Scale = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/autoScale.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAuto_Scale.setIcon(icon)

        self.actionSet_Scale = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/setScale.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSet_Scale.setIcon(icon)

        self.actionMesh = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/grid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMesh.setIcon(icon)

        self.actionTransperancy = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/transparency.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTransperancy.setIcon(icon)

        self.fields = []
        self.timeSteps = []
        self.fieldSelectCombo = QtWidgets.QComboBox()
        self.timeSelectCombo = QtWidgets.QComboBox()

        fieldLabel = QtWidgets.QLabel("Field  ")
        timeLabel = QtWidgets.QLabel("   Time  ")

        self.receiveBar.addWidget(fieldLabel)
        self.receiveBar.addWidget(self.fieldSelectCombo)
        self.receiveBar.addWidget(timeLabel)
        self.receiveBar.addWidget(self.timeSelectCombo)

        self.receiveBar.addAction(self.actionAlign_X)
        self.receiveBar.addAction(self.actionAlign_Y)
        self.receiveBar.addAction(self.actionAligh_Z)
        self.receiveBar.addAction(self.actionFit_Window)
        self.receiveBar.addAction(self.actionMesh)
        self.receiveBar.addAction(self.actionFrame)
        self.receiveBar.addAction(self.actionTransperancy)
        self.addTransparencyBar()
        self.receiveBar.addAction(self.actionAuto_Scale)
        self.receiveBar.addAction(self.actionSet_Scale)
        
        self.actionFit_Window.triggered.connect(self.resetView)
        self.actionAlign_X.triggered.connect(self.align_X)  
        self.actionAlign_Y.triggered.connect(self.align_Y)
        self.actionAligh_Z.triggered.connect(self.align_Z)

        self.GeoFrame.setLayout(self.GeoLayout)

    def setUpVTKWindow(self):
        self.axesWidget = vtk.vtkOrientationMarkerWidget()
        self.scalar_bar = vtk.vtkScalarBarActor()

        self.vtkWindow = QVTKRenderWindowInteractor(self.GeoFrame)
        self.GeoLayout.addWidget(self.vtkWindow)

        self.render = vtk.vtkRenderer()
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)

        self.vtkWindow.SetInteractorStyle(MouseInteractorStyle())
        self.interRender = self.vtkWindow.GetRenderWindow().GetInteractor()

        """
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
        """
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.render.AddActor(self.actor)

        self.setupVTKBackGround()
        self.AddAxes()
        self.setScaleBar()
        self.resetView()
        self.interRender.Initialize()
        self.interRender.Start()
        self.window.show()

    def add2Render(self, newActor):
        self.render.AddActor(newActor)
        self.interRender.ReInitialize()

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

        self.vtkWindow.Start()
        self.vtkWindow.show()

    def resetView(self):
        self.render.GetActiveCamera().ParallelProjectionOff()
        fp = self.render.GetActiveCamera().GetFocalPoint()
        p = self.render.GetActiveCamera().GetPosition()
        dist = math.sqrt( (p[0]-fp[0])**2 + (p[1]-fp[1])**2 + (p[2]-fp[2])**2 )
        self.render.GetActiveCamera().SetPosition(fp[0], fp[1], fp[2]+dist)
        self.render.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.vtkWindow.Initialize()

    def align_X(self):
        self.render.GetActiveCamera().SetViewUp(1.0, 0.0, 0.0)
        self.interRender.ReInitialize()

    def align_Y(self):
        self.render.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.interRender.ReInitialize()

    def align_Z(self):
        self.resetView()

    def AddAxes(self):
        self.axes = vtk.vtkAxesActor()
        self.axes.GetXAxisShaftProperty().SetColor(0, 0, 0)
        self.axes.GetXAxisShaftProperty().SetLineWidth(2)
        self.axes.GetYAxisShaftProperty().SetColor(0, 0, 0)
        self.axes.GetYAxisShaftProperty().SetLineWidth(2)
        self.axes.GetZAxisShaftProperty().SetColor(0, 0, 0)
        self.axes.GetZAxisShaftProperty().SetLineWidth(2)

        self.axes_widget = vtk.vtkOrientationMarkerWidget()
        self.axes_widget.SetOutlineColor(0, 0, 0)
        self.axes_widget.SetOrientationMarker(self.axes)
        self.axes_widget.SetInteractor(self.interRender)
        self.axes_widget.SetViewport(0., 0., 0.3, 0.3)
        self.axes_widget.EnabledOn()
        self.axes_widget.InteractiveOff()

        prop = vtk.vtkTextProperty()
        prop.SetColor(0, 0, 0)
        prop.BoldOn()
        self.axes.GetXAxisCaptionActor2D(). SetCaptionTextProperty(prop)
        self.axes.GetYAxisCaptionActor2D(). SetCaptionTextProperty(prop)
        self.axes.GetZAxisCaptionActor2D(). SetCaptionTextProperty(prop)

    def wireFrameView(self):
        prop = self.actor.GetProperty()
        if not self.wireFrame:
            prop.SetRepresentationToWireframe()
            self.wireFrame = True
        else:
            prop.SetRepresentationToSurface()
            self.wireFrame = False
        self.interRender.ReInitialize()

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
            self.interRender.ReInitialize()
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
        self.interRender.ReInitialize()

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
        for actor in self.render.GetActors():
            actor.GetProperty().SetOpacity(1 - transparencyValue / 100)
        self.interRender.ReInitialize()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QFrame()
    ui = Panel_VTK(window)
    window.show()
    sys.exit(app.exec_())