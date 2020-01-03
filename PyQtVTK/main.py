#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
create a simple interface for OpenFOAM using PyQt5 and VTK. Help to setup the OpenFOAM case and visualization.
PyQt5 is used to generate the GUI
VTK   is used to visualize the OpenFOAM mesh

author: Chen Shaohui
Last edited: December 2019
"""

# TODO: add the expandAll and collapseAll button at the treeView region.
# TODO: connect the transparency slider to the transparency value
# TODO: connect the field comboBox to the VTK exists field.
# TODO: Name of Model dynamic to the real model name.
# TODO: move the field select comboBox to the right of auto-scale and set-scale icons.
# TODO: add the table temperature, rotating speed, velocity... instead of a constant value, ramp up the simulation.

#####################################################################################################
# TODO 1, do not miss uniform keyword before the number in boundary condition.
# TODO 2, do not use Wildcard character for boundary definition.
#####################################################################################################

import sys

import vtk
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.numpy_support import vtk_to_numpy

from OpenFOAMCase import *
from ccm import Ui_OpenFOAM
from settingBox import Ui_Setting


class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass


class SettingDialog(QMainWindow, Ui_Setting):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Setting.__init__(self)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


# noinspection PyAttributeOutsideInit
class MyWindow(QMainWindow, Ui_OpenFOAM):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.settingDialog = SettingDialog()
        self.foamConfig = OpenFOAMCase()
        self.caseName = "Model"
        self.numberOfRegions = 0
        self.MRFCount = 0
        self.patches = []
        self.regions = {}  # the structure of the boundary info is like this self.region["air"] = ["wall", "air1"]
        self.setupUi(self)
        self.__message__ = "Ready. Let's FOAM!"
        self.topSplitter.setSizes([100, 500])
        self.leftDomain.setSizes([100, 100])
        self.rightDomain.setSizes([500, 100])
        self.initTree()
        # GUI related initialization. some of them from case files.
        self.fields = ["T", "Ux", "Uy", "Uz", "magU", "p", "k", "epsilon", "G", "rho"]
        self.timeSteps = ["0"]
        self.fieldSelectCombo = QtWidgets.QComboBox()
        self.timeSelectCombo = QtWidgets.QComboBox()
        self.addTransparencyBar()
        self.addMiscell()
        
        self.scalar_bar = vtk.vtkScalarBarActor()
        self.axesWidget = vtk.vtkOrientationMarkerWidget()
        self.vtkContainBox = QVBoxLayout()

        self.defaultFolder = "C:/Shaohui/OpenFoam/radiationTest/air99surf"
        self.paraPath = "C:/Users/CSHAOHUI/Downloads/ParaView-5.6.0-Windows-msvc2015-64bit/bin/paraview.exe"

        self.wireFrame = False
        self.featureEdge = False
        self.actionFrame.triggered.connect(self.featureEdgeView)
        self.setStatusTip("Ready")

        self.showMaximized()

        # VTK related initialization.
        self.vtkWindow = QVTKRenderWindowInteractor(self.geoTab)
        self.foamVTKGeo = vtk.vtkOpenFOAMReader()
        self.filter = vtk.vtkGeometryFilter()
        self.mapper = vtk.vtkCompositePolyDataMapper2()
        self.actor = vtk.vtkActor()
        self.render = vtk.vtkRenderer()

        # actions!!!
        self.actionOpen.triggered.connect(self.openFile)
        self.actionTools.triggered.connect(self.setting)
        self.actionQuit.triggered.connect(self.shutDownWarning)

    def addTransparencyBar(self):
        self.transparencySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.viewBar.addWidget(self.transparencySlider)
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

    def addMiscell(self):
        for item in self.fields:
            self.fieldSelectCombo.addItem(item)
        self.receiveBar.addWidget(self.fieldSelectCombo)

        for time in self.timeSteps:
            self.timeSelectCombo.addItem(time)
        self.receiveBar.addWidget(self.timeSelectCombo)

        self.receiveBar.addAction(self.actionAuto_Scale)
        self.receiveBar.addAction(self.actionSet_Scale)

    def initTree(self):
        # self.item_0 is the head item of the tree. it text is the name of the model.
        regionProperties = self.foamConfig.GetRegionProperty()
        TreeList = {"Geometry": ("region1", "region2"),
                    "fvSolution": ("solver", "residual", "relaxation"),
                    "fvOption": ("Heat Source", "Temp Limit"),
                    "ControlDict": (
                        "Application", "StartFrom", "Time Step", "Write Interval", "End Time", "Adjust OnFly", "MaxCo",
                        "Decompose", "Function")
                    }
        _translate = QtCore.QCoreApplication.translate

        self.pipLine.topLevelItem(0).setText(0, _translate("OpenFOAM", self.caseName))

        self.geoItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Geometry"])

        self.phyItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Physics"])

        self.TurbItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Turbulence"])
        self.TurbItem.setCheckState(0, Qt.Unchecked)

        self.MRFItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["MRF"])
        self.MRFItem.setCheckState(0, Qt.Unchecked)

        self.DynaMeshItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Dynamic Mesh"])
        self.DynaMeshItem.setCheckState(0, Qt.Unchecked)

        self.MultiPhaseItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Multiphase"])
        self.MultiPhaseItem.setCheckState(0, Qt.Unchecked)

        self.HeatTransItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Heat Transfer"])
        self.HeatTransItem.setCheckState(0, Qt.Unchecked)

        self.RadiatItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Radiation"])
        self.RadiatItem.setCheckState(0, Qt.Unchecked)

        self.MatItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Material"])

        self.viscoItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Viscosity"])
        self.viscoItem.setCheckState(0, Qt.Unchecked)

        self.DensiItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Density"])
        self.DensiItem.setCheckState(0, Qt.Unchecked)

        self.HeatConductItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Heat Conductivity"])
        self.HeatConductItem.setCheckState(0, Qt.Unchecked)

        self.SpeficHeatItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Specific Heat"])
        self.SpeficHeatItem.setCheckState(0, Qt.Unchecked)

        self.schemeItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvSchemes"])

        self.ddtItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["ddt"])
        self.ddtItem.setCheckState(0, Qt.Unchecked)

        self.divItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["div"])
        self.divItem.setCheckState(0, Qt.Unchecked)

        self.gradItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["Grad"])
        self.gradItem.setCheckState(0, Qt.Unchecked)

        self.lapItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["Laplacian"])
        self.lapItem.setCheckState(0, Qt.Unchecked)

        self.wallDistItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["Wall Distance"])
        self.wallDistItem.setCheckState(0, Qt.Unchecked)

        self.soluItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvSolution"])

        self.solverItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["solver"])
        self.solverItem.setCheckState(0, Qt.Unchecked)

        self.resiItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["residual"])
        self.resiItem.setCheckState(0, Qt.Unchecked)

        self.relaxItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["Relaxation Factor"])
        self.relaxItem.setCheckState(0, Qt.Unchecked)

        self.optionItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvOption"])

        self.HeatSourceItem = QtWidgets.QTreeWidgetItem(self.optionItem, ["Heat Source"])
        self.HeatSourceItem.setCheckState(0, Qt.Unchecked)

        self.TempLimitItem = QtWidgets.QTreeWidgetItem(self.optionItem, ["Temperature Limit"])
        self.TempLimitItem.setCheckState(0, Qt.Unchecked)

        self.ControlItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["ControlDict"])

        self.TimeControlItem = QtWidgets.QTreeWidgetItem(self.ControlItem, ["Time control"])
        self.TimeControlItem.setCheckState(0, Qt.Unchecked)

        self.PhyCOntrolItem = QtWidgets.QTreeWidgetItem(self.ControlItem, ["Physical control"])
        self.PhyCOntrolItem.setCheckState(0, Qt.Unchecked)

        self.pipLine.currentItemChanged.connect(self.propertyView)
        self.pipLine.show()
        self.pipLine.expandAll()
    def propertyView(self, current, old):
        if current.text(0) == "Turbulence":
            self.TurbProperties()
        elif current.text(0) == "MRF":
            self.MRFProperties()
        elif current.text(0) == "Dynamic Mesh":
            self.DynaMeshProperties()
        elif current.text(0) == "Multiphase":
            self.MultiphaseProperties()
        elif current.text(0) == "Radiation":
            self.RadiationProperties()

    def TurbProperties(self):
        self.properties.setColumnCount(2)
        self.properties.setRowCount(2)
        self.properties.show()

        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        regionLabel = QtWidgets.QLabel("Region")        
        self.properties.setCellWidget(0, 0, regionLabel)
        regions = list(self.regions.keys())
        self.regionComboBox = QtWidgets.QComboBox()
        self.regionComboBox.addItems(regions)
        self.properties.setCellWidget(0, 1, self.regionComboBox)

        simuTypeLabel = QtWidgets.QLabel("simulationType")        
        self.properties.setCellWidget(1, 0, simuTypeLabel)
        simuTypeOp = ["laminar", "RAS", "LES", "DES"]
        self.simuTypeComboBox = QtWidgets.QComboBox()
        self.simuTypeComboBox.addItems(simuTypeOp)
        self.properties.setCellWidget(1, 1, self.simuTypeComboBox)
        
        self.simuTypeComboBox.currentIndexChanged.connect(lambda: self.RASproperty(self.simuTypeComboBox.currentText()))

    def RASproperty(self, simuType):
        if simuType == "RAS":
            self.properties.setColumnCount(2)
            self.properties.setRowCount(5)

            RASModelLabel = QtWidgets.QLabel("RASModel")        
            self.properties.setCellWidget(2, 0, RASModelLabel)
            simuTypeOp = ["kEpsilon", "realizableKE", "RNGkEpsilon", "kOmemga", "kOmegaSST", "kOmegaSSTLM"]
            simuTypeComboBox = QtWidgets.QComboBox()
            simuTypeComboBox.addItems(simuTypeOp)
            self.properties.setCellWidget(2, 1, simuTypeComboBox)

            TurbSwitchLabel = QtWidgets.QLabel("Turbulence")        
            self.properties.setCellWidget(3, 0, TurbSwitchLabel)
            TurbSwitchOp = ["on", "off"]
            TurbSwitchOpComboBox = QtWidgets.QComboBox()
            TurbSwitchOpComboBox.addItems(TurbSwitchOp)
            self.properties.setCellWidget(3, 1, TurbSwitchOpComboBox)
            
            TurbCoeffLabel = QtWidgets.QLabel("printCoeffs")        
            self.properties.setCellWidget(4, 0, TurbCoeffLabel)
            TurbCoeffOp = ["on", "off"]
            TurbCoeffComboBox = QtWidgets.QComboBox()
            TurbCoeffComboBox.addItems(TurbCoeffOp)
            self.properties.setCellWidget(4, 1, TurbCoeffComboBox)

        elif simuType == "laminar":
            self.properties.setColumnCount(2)
            self.properties.setRowCount(1)  

    def MRFProperties(self):
        row, col = 8, 2
        #TODO MRF also need a region input indicate which region the cellZone belongs to. Also, configed MRF need to appare in the tree. 
        self.properties.setColumnCount(col)
        self.properties.setRowCount(row)
        self.properties.show()

        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        MRFNameLabel = QtWidgets.QLabel("MRF Name")        
        self.properties.setCellWidget(0, 0, MRFNameLabel)
        MRFNameInput = QtWidgets.QLineEdit()
        MRFNameInput.setText("MRF_" + str(self.MRFCount)) 
        self.MRFCount += 1
        self.properties.setCellWidget(0, 1, MRFNameInput)

        MRFCellZone = QtWidgets.QLabel("cellZone")        
        self.properties.setCellWidget(1, 0, MRFCellZone)
        cellZoneOp = ["cellZone1", "cellZone2"]
        cellZoneOpComboBox = QtWidgets.QComboBox()
        cellZoneOpComboBox.addItems(cellZoneOp)
        self.properties.setCellWidget(1, 1, cellZoneOpComboBox)
        
        MRFactiveLabel = QtWidgets.QLabel("MRF")        
        self.properties.setCellWidget(2, 0, MRFactiveLabel)
        MRFactiveOp = ["on", "off"]
        MRFactiveComboBox = QtWidgets.QComboBox()
        MRFactiveComboBox.addItems(MRFactiveOp)
        self.properties.setCellWidget(2, 1, MRFactiveComboBox)

        MRFnonRotatLabel = QtWidgets.QLabel("nonRotatingPatches")
        self.properties.setCellWidget(3, 0, MRFnonRotatLabel)
        MRFnonRotatPatchOp = self.patches
        MRFnonRotatPatchCombox = QtWidgets.QComboBox()
        MRFnonRotatPatchCombox.addItems(MRFnonRotatPatchOp)
        self.properties.setCellWidget(3, 1, MRFnonRotatPatchCombox)

        MRForiginLabel = QtWidgets.QLabel("origin")
        self.properties.setCellWidget(4, 0, MRForiginLabel)
        MRForiginInput = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(4, 1, MRForiginInput)

        MRFaxisLabel = QtWidgets.QLabel("axis")
        self.properties.setCellWidget(5, 0, MRFaxisLabel)
        axisOp = ["x", "y", "z"]
        MRFaxisCombobox = QtWidgets.QComboBox()
        MRFaxisCombobox.addItems(axisOp)
        self.properties.setCellWidget(5, 1, MRFaxisCombobox)

        MRFomegaLabel = QtWidgets.QLabel("omega")
        self.properties.setCellWidget(6, 0, MRFomegaLabel)
        MRFomegaInput = QtWidgets.QLineEdit()
        MRFomegaInput.setPlaceholderText("rpm")
        self.properties.setCellWidget(6, 1, MRFomegaInput)

        addMRFButt = QtWidgets.QPushButton('Add/Update')
        self.properties.setCellWidget(7, 0, addMRFButt)
        DeleMRFButt = QtWidgets.QPushButton("Delete")
        self.properties.setCellWidget(7, 1, DeleMRFButt)

    def DynaMeshProperties(self):        
        self.properties.setRowCount(8)
        self.properties.setColumnCount(2)
        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        DynaMeshFvLabel = QtWidgets.QLabel("dynamicFvMesh")
        self.properties.setCellWidget(0, 0, DynaMeshFvLabel)
        DynaMeshFvCombox = QtWidgets.QComboBox()
        DynaMeshFvOp = ["solidBodyMotionFvMesh", "dynamicMotionSolverFvMesh", "dynamicRefineFvMesh", "staticFvMesh"]
        DynaMeshFvCombox.addItems(DynaMeshFvOp)
        self.properties.setCellWidget(0, 1, DynaMeshFvCombox)

        DynaMeshSolver = QtWidgets.QLabel("Motion Solver")
        self.properties.setCellWidget(1, 0, DynaMeshSolver)
        DynaMeshSolverCombox = QtWidgets.QComboBox()
        DynaMeshSolverOp = ["solidBody", "sixDoFRigidBodyMotion", ]
        DynaMeshSolverCombox.addItems(DynaMeshSolverOp)
        self.properties.setCellWidget(1, 1, DynaMeshSolverCombox)

        DynaMeshFuncLabel = QtWidgets.QLabel("Motion function")
        self.properties.setCellWidget(2, 0, DynaMeshFuncLabel)
        motionFuncOp = ["rotatingMotion"]
        motionFuncCombox = QtWidgets.QComboBox()
        motionFuncCombox.addItems(motionFuncOp)
        self.properties.setCellWidget(2, 1, motionFuncCombox)

        DynaMeshCellZone = QtWidgets.QLabel("cellZone")        
        self.properties.setCellWidget(3, 0, DynaMeshCellZone)
        cellZoneOp = ["cellZone1", "cellZone2"]
        cellZoneOpComboBox = QtWidgets.QComboBox()
        cellZoneOpComboBox.addItems(cellZoneOp)
        self.properties.setCellWidget(3, 1, cellZoneOpComboBox)

        DynaMeshoriginLabel = QtWidgets.QLabel("origin")
        self.properties.setCellWidget(4, 0, DynaMeshoriginLabel)
        DynaMeshoriginInput = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(4, 1, DynaMeshoriginInput)

        DynaMeshaxisLabel = QtWidgets.QLabel("axis")
        self.properties.setCellWidget(5, 0, DynaMeshaxisLabel)
        axisOp = ["x", "y", "z"]
        DynaMeshaxisCombobox = QtWidgets.QComboBox()
        DynaMeshaxisCombobox.addItems(axisOp)
        self.properties.setCellWidget(5, 1, DynaMeshaxisCombobox)

        DynaMeshomegaLabel = QtWidgets.QLabel("omega")
        self.properties.setCellWidget(6, 0, DynaMeshomegaLabel)
        DynaMeshomegaInput = QtWidgets.QLineEdit()
        DynaMeshomegaInput.setPlaceholderText("rpm")
        self.properties.setCellWidget(6, 1, DynaMeshomegaInput)

        addDynaMeshButt = QtWidgets.QPushButton('Add/Update')
        self.properties.setCellWidget(7, 0, addDynaMeshButt)
        DeleDynaMeshButt = QtWidgets.QPushButton("Delete")
        self.properties.setCellWidget(7, 1, DeleDynaMeshButt)

    def MultiphaseProperties(self):
        self.properties.setRowCount(6)
        self.properties.setColumnCount(2)
        self.properties.show()
        
        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        fieldNameLabel = QtWidgets.QLabel("Field Values")
        self.properties.setCellWidget(0, 0, fieldNameLabel)
        fieldNameInput = QtWidgets.QLineEdit("Alpha.Water")
        self.properties.setCellWidget(0, 1, fieldNameInput)

        defaultValueLabel = QtWidgets.QLabel("Default Value")
        self.properties.setCellWidget(1, 0, defaultValueLabel)
        defaultValueInput = QtWidgets.QLineEdit("1")
        self.properties.setCellWidget(1, 1, defaultValueInput)

        fieldRegionLabel = QtWidgets.QLabel("Field Region")
        self.properties.setCellWidget(2, 0, fieldRegionLabel)
        fieldRegionCombox = QtWidgets.QComboBox()
        fieldRegionOp = ["boxToCell", "cylinderToCell", "sphereToCell", "cylinderAnnulusToCell", "rotatedBoxToCell", "zoneToCell"]
        fieldRegionCombox.addItems(fieldRegionOp)
        self.properties.setCellWidget(2, 1, fieldRegionCombox)
        
        boxPoint1Label = QtWidgets.QLabel("box point1")
        self.properties.setCellWidget(3, 0, boxPoint1Label)
        boxPoint1Input = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(3, 1, boxPoint1Input)

        boxPoint2Label = QtWidgets.QLabel("box point2")
        self.properties.setCellWidget(4, 0, boxPoint2Label)
        boxPoint2Input = QtWidgets.QLineEdit("10, 10, 10")
        self.properties.setCellWidget(4, 1, boxPoint2Input)

        fieldValueLabel = QtWidgets.QLabel("Field Value")
        self.properties.setCellWidget(5, 0, fieldValueLabel)
        fieldValueInput = QtWidgets.QLineEdit("0")
        self.properties.setCellWidget(5, 1, fieldValueInput)
        
    def RadiationProperties(self):

        self.properties.setRowCount(12)
        self.properties.setColumnCount(2)
        self.properties.verticalHeader().hide()
        self.properties.horizontalHeader().hide()

        radiatSwitchLabel = QtWidgets.QLabel("Ratiation")
        self.properties.setCellWidget(0, 0, radiatSwitchLabel)
        self.radiationSwitchCombox = QtWidgets.QComboBox()
        self.radiationSwitchCombox.addItems(["on", "off"])
        self.properties.setCellWidget(0, 1, self.radiationSwitchCombox)

        radiatModelLabel = QtWidgets.QLabel("Ratiation Model")
        self.properties.setCellWidget(1, 0, radiatModelLabel)
        self.radiatModelCombox = QtWidgets.QComboBox()
        radiatModelOp = ["fvDOM", "P1", "S2S"]
        self.radiatModelCombox = QtWidgets.QComboBox()
        self.radiatModelCombox.addItems(radiatModelOp)
        self.properties.setCellWidget(1, 1, self.radiatModelCombox)

        nPhiLabel = QtWidgets.QLabel("nPhi")
        self.properties.setCellWidget(2, 0, nPhiLabel)
        self.nPhiInput = QtWidgets.QSpinBox()   
        self.nPhiInput.setValue(2)
        self.properties.setCellWidget(2, 1, self.nPhiInput)

        nThetaLabel = QtWidgets.QLabel("nTheta")
        self.properties.setCellWidget(3, 0, nThetaLabel)
        self.nThetaInput = QtWidgets.QSpinBox()
        self.nThetaInput.setValue(4)
        self.properties.setCellWidget(3, 1, self.nThetaInput)

        radmaxIterLabel = QtWidgets.QLabel("maxIter")
        self.properties.setCellWidget(4, 0, radmaxIterLabel)
        self.radmaxIterInput = QtWidgets.QSpinBox()
        self.radmaxIterInput.setValue(5)
        self.properties.setCellWidget(4, 1, self.radmaxIterInput)

        radTolLabel = QtWidgets.QLabel("tolerance")
        self.properties.setCellWidget(5, 0, radTolLabel)
        self.radTolInput = QtWidgets.QLineEdit("1E-3")
        self.properties.setCellWidget(5, 1, self.radTolInput)

        radSolvFreqLabel = QtWidgets.QLabel("solve freq")
        self.properties.setCellWidget(6, 0, radSolvFreqLabel)
        self.radSolvFreqInput = QtWidgets.QSpinBox()
        self.properties.setCellWidget(6, 1, self.radSolvFreqInput)

        radAbsorpLabel = QtWidgets.QLabel("absorptivity")
        self.properties.setCellWidget(7, 0, radAbsorpLabel)
        self.radAbsorpInput = QtWidgets.QLineEdit("0.01")
        self.properties.setCellWidget(7, 1, self.radAbsorpInput)

        radEmissLabel = QtWidgets.QLabel("emissivity")
        self.properties.setCellWidget(8, 0, radEmissLabel)
        self.radEmissInput = QtWidgets.QLineEdit("0.01")
        self.properties.setCellWidget(8, 1, self.radEmissInput)

        radELabel = QtWidgets.QLabel("E")
        self.properties.setCellWidget(9, 0, radELabel)
        self.radEInput = QtWidgets.QLineEdit("0")
        self.properties.setCellWidget(9, 1, self.radEInput)

        radScattLabel = QtWidgets.QLabel("scatter model")
        self.properties.setCellWidget(10, 0, radScattLabel)
        self.radScattInput = QtWidgets.QComboBox()
        self.radScattInput.addItems(["none"])
        self.properties.setCellWidget(10, 1, self.radScattInput)

        radSootLabel = QtWidgets.QLabel("soot model")
        self.properties.setCellWidget(11, 0, radSootLabel)
        self.radSootInput = QtWidgets.QComboBox()
        self.radSootInput.addItems(["none"])
        self.properties.setCellWidget(11, 1, self.radSootInput)

    def setupVTK(self):
        self.vtkContainBox.addWidget(self.vtkWindow)
        self.geoTab.setLayout(self.vtkContainBox)

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

    def setting(self):
        self.settingDialog.show()

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

    def openFile(self):
        # TODO add warning box to save the current config, open a new file will overwrite the current model. just
        #  like ANSA. However, the implimentation below has problem, it always open a new XinFoam instance
        """
        buttonReply = QMessageBox.warning(self, 'FOAM Warning', "Do you want to save before open new case?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            OpenFOAMCase.write()
            self.resetFile()
        if buttonReply == QMessageBox.No:
            self.resetFile()
        if buttonReply == QMessageBox.Cancel:
            self.__messaga__ += "No new case opened."
            return
        """
        self.caseFolder = QFileDialog.getOpenFileName(self, 'Open file', self.defaultFolder,
                                                      "OpenFOAM File (*.foam *.txt)")

        if self.caseFolder[0] != "":
            self.loadCaseGeo()
            self.foamConfig.SetFolderAndName(self.caseFolder)
            self.foamConfig.loadCase()

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
            # the patches are stored in a array together, region_i/patch_n  region_i/internalMesh
            self.patches.append(self.foamVTKGeo.GetPatchArrayName(i))

        # this function will disable all the patches, use this to disable patches not checked
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

    def setPatchProperties(self):
        _translate = QtCore.QCoreApplication.translate
        self.properties.setColumnCount(3)
        self.properties.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setItem(0, 2, item)

        item = self.properties.horizontalHeaderItem(0)
        item.setText(_translate("OpenFOAM", "Property"))
        item = self.properties.horizontalHeaderItem(1)
        item.setText(_translate("OpenFOAM", "Value"))
        item = self.properties.horizontalHeaderItem(2)
        item.setText(_translate("OpenFOAM", "Switch"))
        __sortingEnabled = self.properties.isSortingEnabled()
        self.properties.setSortingEnabled(False)
        item = self.properties.item(0, 0)
        item.setText(_translate("OpenFOAM", "row"))
        item = self.properties.item(0, 1)
        item.setText(_translate("OpenFOAM", "row1"))
        item = self.properties.item(0, 2)
        item.setText(_translate("OpenFOAM", "row2"))
        self.properties.setSortingEnabled(__sortingEnabled)

    def resetFile(self):
        self.__init__()
        self.render = vtk.vtkRenderer()
        self.setupVTKBackGround()
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)

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

    def openNewCaseWarning(self):
        openButtonReply = QMessageBox.warning(self, 'FOAM Warning', "Do you want to save before open a new case?",
                                              QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if openButtonReply == QMessageBox.Yes:
            self.close()  # TODO: change the self.close() to self.write() later.
        if openButtonReply == QMessageBox.No:
            self.close()
        if openButtonReply == QMessageBox.Cancel:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
