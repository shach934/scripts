#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, vtk, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MouseInteractorStyle import *

from Ui_mainWindow import Ui_OpenFOAM
from Ui_newCase import Ui_newCase
from Ui_openCase import Ui_openCase
from Ui_settingDialog import Ui_settingDialog

class GlobalWindow(QMainWindow, Ui_OpenFOAM):

    def __init__(self, parent  =None):
        super(GlobalWindow, self).__init__(parent)

        self.setupUi(self)
        self.setUpGlobalPanels()

        self.setUpTree()
        self.setUpPropertyPanel()
        self.setVTK_MonitorTabs()
        self.setUpMessagePanel()

        self.connectWires()

        self.showMaximized()
        self.show()

    #------------------------------------------------------------------------------
    def setUpGlobalPanels(self):

        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWindow)

        self.leftRightSplitter = QtWidgets.QSplitter(self.mainWindow)
        self.leftRightSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.leftDomain = QtWidgets.QSplitter(self.leftRightSplitter)
        self.leftDomain.setOrientation(QtCore.Qt.Vertical)

        self.rightDomain = QtWidgets.QSplitter(self.leftRightSplitter)
        self.rightDomain.setOrientation(QtCore.Qt.Vertical)

        self.verticalLayout.addWidget(self.leftRightSplitter)
        self.setCentralWidget(self.mainWindow)

        self.setStatusTip("Ready")
        self.leftRightSplitter.setSizes([100, 500])
        self.leftDomain.setSizes([100, 100])
        self.rightDomain.setSizes([500, 100])

    #------------------------------------------------------------------------------
    def setUpTree(self):

        self.pipLine = QtWidgets.QTreeWidget(self.leftDomain)
        self.pipLine.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pipLine.sizePolicy().hasHeightForWidth())
        self.pipLine.setSizePolicy(sizePolicy)
        self.pipLine.setSizeIncrement(QtCore.QSize(300, 0))
        self.pipLine.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.pipLine.setDragEnabled(False)

        self.pipLine.headerItem().setText(0, "Model")
        
        self.TopItem = QtWidgets.QTreeWidgetItem(self.pipLine)
        self.TopItem.setText(0, "Model Name")
        self.TopItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
        self.geoItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Geometry"])
        self.geoItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)

        self.createGeoItem = QtWidgets.QTreeWidgetItem(self.geoItem, ["Create"])
        self.createBoxGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Box"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/box.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createBoxGeoItem.setIcon(0, icon)
        self.createCylGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Cylinder"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cylinder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createCylGeoItem.setIcon(0, icon)
        self.createSphGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Sphere"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/sphere.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createSphGeoItem.setIcon(0, icon)
        self.createConeGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Cone"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cone.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createConeGeoItem.setIcon(0, icon)

        self.importGeoItem = QtWidgets.QTreeWidgetItem(self.geoItem, ["Import"])
        self.meshItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Mesh"])

        self.meshGeoItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Parts"])
        self.blockMeshItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["BlockMesh"])
        self.snappyItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["SnappyMesh"])
        self.layersItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Layers"])
        self.meshCriteriaItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Criteria"])

        self.phyItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Setup"])

        self.pipLine.currentItemChanged.connect(self.propertyView)

        self.pipLine.show()
        self.pipLine.expandAll()  

    #------------------------------------------------------------------------------
    def setVTK_MonitorTabs(self):

        self.window = QtWidgets.QFrame(self.rightDomain)
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
        
        self.actionFrame.triggered.connect(self.wireFrameView)
        self.actionMesh.triggered.connect(self.meshOnOff)
        self.axesWidget = vtk.vtkOrientationMarkerWidget()
        self.scalar_bar = vtk.vtkScalarBarActor()

        self.vtkWindow = QVTKRenderWindowInteractor()
        self.GeoLayout.addWidget(self.vtkWindow)

        self.render = vtk.vtkRenderer()
        self.actor = vtk.vtkActor()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor.SetMapper(self.mapper)
        self.render.AddActor(self.actor)
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)

        self.interRender = self.vtkWindow.GetRenderWindow().GetInteractor()
        self.interRender.SetInteractorStyle(MouseInteractorStyle())

        self.setupVTKBackGround()
        self.AddAxes()
        self.setScaleBar()
        self.interRender.Initialize()
        self.interRender.Start()
        self.window.show()

    #------------------------------------------------------------------------------
    def setUpPropertyPanel(self):
        self.propertyBox = QtWidgets.QFrame(self.leftDomain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.propertyBox.setSizePolicy(sizePolicy)
        self.propertyBox.show()

    #------------------------------------------------------------------------------
    def clearLayout(self, layout):
        if cur_lay is not None:
            while cur_lay.count():
                item = cur_lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
            sip.delete(cur_lay)

    #------------------------------------------------------------------------------
    def setUpMessagePanel(self):
        self.messageBox = QtWidgets.QTextBrowser(self.rightDomain)
        self.messageBox.setText("This is a message box!\n")

    #------------------------------------------------------------------------------
    def logLog(self):
        try:
            fid = open(self.path + "/log.log", "wr")
            fid.write(self.log)
        except IOError as e:
            self.__message__("cannot open the log file")

    #------------------------------------------------------------------------------
    def connectWires(self):
        pass
        # self.actionFit_Window.triggered.connect(self.resetView)
        # self.actionAlign_X.triggered.connect(self.align_X)  
        # self.actionAlign_Y.triggered.connect(self.align_Y)
        # self.actionAligh_Z.triggered.connect(self.align_Z)

    #------------------------------------------------------------------------------
    def propertyView(self, curr, prev):

        if curr == "Box":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempBox = createBox(self.render)
            tempHboxLayout.addWidget(self.tempBox)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Sphere":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempSphere = createSphere(self.render)
            tempHboxLayout.addWidget(self.tempSphere)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Cylinder":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCylinder = createCylinder(self.render)
            tempHboxLayout.addWidget(self.tempCylinder)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Cone":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCone = createCone(self.render)
            tempHboxLayout.addWidget(self.tempCone)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "blockMesh":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.blockMesh = blockMesh(self.render)
            tempHboxLayout.addWidget(self.blockMesh)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

    #------------------------------------------------------------------------------
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
        actorProper = self.actor.GetProperty()

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

    #------------------------------------------------------------------------------
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
        self.axes.GetXAxisCaptionActor2D().SetCaptionTextProperty(prop)
        self.axes.GetYAxisCaptionActor2D().SetCaptionTextProperty(prop)
        self.axes.GetZAxisCaptionActor2D().SetCaptionTextProperty(prop)

    #------------------------------------------------------------------------------
    def wireFrameView(self):
        prop = self.actor.GetProperty()
        if not self.wireFrame:
            prop.SetRepresentationToWireframe()
            self.wireFrame = True
        else:
            prop.SetRepresentationToSurface()
            self.wireFrame = False
        self.interRender.ReInitialize()

    #------------------------------------------------------------------------------
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

    #------------------------------------------------------------------------------
    def meshOnOff(self):
        prop = self.actor.GetProperty()
        prop.EdgeVisibilityOff()
        prop.SetEdgeColor(1, 1, 1)
        prop.SetLineWidth(0)
        self.interRender.ReInitialize()

    #------------------------------------------------------------------------------
    def setupVTKBackGround(self):
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.2, 0.4, 0.6)
        self.render.SetBackground(1, 1, 1)

    #------------------------------------------------------------------------------
    def setScaleBar(self):
        # lookup table
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.667, 0)
        lut.SetNumberOfColors(10)
        lut.Build()

        self.scalar_bar.SetLookupTable(lut)
        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(self.vtkWindow)
        scalar_bar_widget.SetScalarBarActor(self.scalar_bar)
        scalar_bar_widget.On()

    #------------------------------------------------------------------------------
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

    #------------------------------------------------------------------------------
    def adjustTransparent(self):
        transparencyValue = self.transparencySlider.value()
        for actor in self.render.GetActors():
            actor.GetProperty().SetOpacity(1 - transparencyValue / 100)
        self.interRender.ReInitialize()
 
    #------------------------------------------------------------------------------
    def assignGeoTree(self):
        # itemChanged  itemClicked are 2 signals that indicate item is changed or clicked.
        self.GeoRegionSubItems, self.GeoPatchSubItems = [], []
        for region, patches in self.regions.items():
            GeoRegionItem = QtWidgets.QTreeWidgetItem(self.geoItem, [region])
            GeoRegionItem.setFlags(GeoRegionItem.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            GeoRegionItem.setCheckState(0, Qt.Checked)
            for patch in patches:
                GeoPatchItem = QtWidgets.QTreeWidgetItem(GeoRegionItem, [patch])
                GeoRegionItem.addChild(GeoPatchItem)
                GeoPatchItem.setFlags(GeoPatchItem.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
                GeoPatchItem.setCheckState(0, Qt.Checked)
                self.GeoPatchSubItems.append(GeoPatchItem)
            self.GeoRegionSubItems.append(GeoRegionItem)
        self.pipLine.show()

    #------------------------------------------------------------------------------
    def newCase(self):
        self.Dialog = QtWidgets.QDialog()
        self.newCaseDialog = Ui_newCase()
        self.newCaseDialog.setupUi(self.Dialog)
        self.newCaseDialog.newCaseBrowser.clicked.connect(self.getNewCasePath)
        self.Dialog.show()
        response = self.Dialog.exec_()
        if response == QtWidgets.QDialog.Accepted:
            self.caseName = self.newCaseDialog.newCaseNameInput.text()
            self.casePath = self.newCaseDialog.newCasePathInput.text()
            self.path = self.casePath + "/" + self.caseName
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print("Directory " , self.path ,  " Created ")
        else:    
            print("Directory " , self.path ,  " already exists")
            buttonReply = QMessageBox.question(self, 'The folder is already exits\n', "Do you want to override it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                os.rmdir(self.path)
                os.mkdir(self.path)
            else:
                self.newCase()

    #------------------------------------------------------------------------------
    def openCase(self):

        self.Dialog = QtWidgets.QDialog()
        self.openCaseDialog = Ui_openCase()
        self.openCaseDialog.setupUi(self.Dialog)
        self.openCaseDialog.openCaseBrowser.clicked.connect(self.getOpenCasePath)
        self.Dialog.show()

        response = self.Dialog.exec_()
        if response == QtWidgets.QDialog.Accepted:
            self.casePath = self.openCaseDialog.openCasePathInput.text()
            self.caseName = self.casePath.split("/")[-1]
            self.foamConfig.SetFolderAndName(self.caseFolder)
            self.foamConfig.loadCase()
    #------------------------------------------------------------------------------
    def getNewCasePath(self):
        casePath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.newCaseDialog.newCasePathInput.setText(casePath)

    #------------------------------------------------------------------------------
    def getOpenCasePath(self):
        casePath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.openCaseDialog.openCasePathInput.setText(casePath)

    #------------------------------------------------------------------------------
    def loadCaseGeo(self):
        self.caseName = self.caseFolder[0].split("/")[-2]
        self.foamVTKGeo.SetFileName(str(self.caseFolder[0]))
        self.foamVTKGeo.CreateCellToPointOn()
        self.foamVTKGeo.DecomposePolyhedraOn()
        self.foamVTKGeo.EnableAllCellArrays()
        self.foamVTKGeo.Update()
        self.setupVTK()

        self.setWindowTitle(self.caseFolder[0])
        self.pipLine.topLevelItem(0).setText(0, self.caseName)

        # TODO for now, every time reinitialize the render,
        #  later should initialize only once and use disableAllPatchArrays method.

        n = self.foamVTKGeo.GetNumberOfPatchArrays()
        for i in range(n):
            self.patches.append(self.foamVTKGeo.GetPatchArrayName(i))

        # self.foamReader.DisableAllPatchArrays()

        # TODO count the number of regions/blocks
        # TODO clear all the variables when a new case is opened. right now the values are all inherited.
        block = self.foamVTKGeo.GetOutput()

        while block.GetBlock(self.numberOfRegions) is not None:
            self.numberOfRegions += 1
        if self.numberOfRegions > 1:
            for patch in self.patches:
                if patch.split("/")[0] in self.regions:
                    self.regions[patch.split("/")[0]].append(patch.split("/")[1])
                else:
                    self.regions[patch.split("/")[0]] = [patch.split("/")[1]]
        else:
            self.regions["default region"] = self.patches
        if not self.foamConfig.checkBoundary(self.regions):
            self.__message__ += "\nThe patches and regions from VTK are not consistent with the file!\n"

        self.assignGeoTree()
        self.pipLine.expandAll()

    #------------------------------------------------------------------------------
    def  settingDialog(self):
        settingDialog = QtWidgets.QDialog()
        ui = Ui_settingDialog()
        ui.setupUi(settingDialog)
        settingDialog.show()
        response = settingDialog.exec_()
        if response == QtWidgets.QDialog.Accepted:
            self.defaut 

    #------------------------------------------------------------------------------
    def shutDownWarning(self):
        closeButtonReply = QMessageBox.warning(self, 'FOAM Warning', "Do you want to save before exit?",
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                               QMessageBox.Cancel)
        if closeButtonReply == QMessageBox.Yes:
            self.close()  # TODO: change the self.close() to self.write() later.
        if closeButtonReply == QMessageBox.No:
            self.close()
        if closeButtonReply == QMessageBox.Cancel:
            pass

    #------------------------------------------------------------------------------
    def connectActions(self):
        # actions!!!
        self.actionNew.triggered.connect(self.newCase)
        self.actionOpen.triggered.connect(self.openCase)
        self.actionTools.triggered.connect(self.settingDialog)
        self.actionQuit.triggered.connect(self.shutDownWarning)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenFOAM = QtWidgets.QMainWindow()
    ui = GlobalWindow()
    sys.exit(app.exec_())