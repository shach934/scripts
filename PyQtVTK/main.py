#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
create a simple interface for OpenFOAM using PyQt5 and VTK. Help to setup the OpenFOAM case and visualization.
PyQt5 is used to generate the GUI
VTK   is used to visualize the OpenFOAM mesh
XinFoam 
v0.1_preAlpha
author: Chen Shaohui
Last updated: Ongoing.
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

import sys, vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import vtkCylinderSource, vtkConeSource, vtkCubeSource, vtkSphereSource

from OpenFOAMCase import *
from GlobalWindow import *

import MouseInteractorStyle

class main(GlobalWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)

        self.foamConfig = OpenFOAMCase()
        self.caseName = "Model"
        self.numberOfRegions = 0
        self.MRFCount = 0
        self.patches = []
        self.regions = {}  # the structure of the boundary info is like this self.region["air"] = ["wall", "air1"]

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

    def resetFile(self):
        self.__init__()
        self.render = vtk.vtkRenderer()
        self.setupVTKBackGround()
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)



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
    myWin = main()
    myWin.show()
    sys.exit(app.exec_())
