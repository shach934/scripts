#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, vtk, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import MouseInteractorStyle

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
        self.setVTK_MonitorTabs()
        self.setUpVTKWindow()
        self.setUpMessagePanel()

        self.connectWires()

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

    #----------------------------------------------------------------------------------------
    def setUpVTKWindow(self):

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
        
        self.GeoFrame.setLayout(self.GeoLayout)

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

        self.setupVTKBackGround()
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
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

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
            self.tempBox = createBox(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempBox)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Sphere":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempSphere = createSphere(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempSphere)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Cylinder":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCylinder = createCylinder(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempCylinder)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "Cone":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCone = createCone(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempCone)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif curr == "blockMesh":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.blockMesh = blockMesh(self.vtkWindow)
            tempHboxLayout.addWidget(self.blockMesh)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

    #------------------------------------------------------------------------------
    def setupVTKBackGround(self):
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.2, 0.4, 0.6)
        self.render.SetBackground(1, 1, 1)

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
        self.showMaximized()
        self.show()
 
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
#------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenFOAM = QtWidgets.QMainWindow()
    ui = GlobalWindow()
    sys.exit(app.exec_())