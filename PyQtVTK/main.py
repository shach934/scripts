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
# TODO: move the field select comboBox to the right of autoscale and setscale icons.

import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QDesktopWidget, QVBoxLayout, QMessageBox, \
    QWidget, QPushButton
from PyQt5 import QtCore
from ccm import Ui_OpenFOAM
from settingBox import Ui_Setting
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from vtk.util.numpy_support import vtk_to_numpy


class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    pass


class SettingDialog(QMainWindow, Ui_Setting):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Setting.__init__(self)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class MyWindow(QMainWindow, Ui_OpenFOAM):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.topSplitter.setSizes([100, 500])
        self.leftDomain.setSizes([100, 100])
        self.rightDomain.setSizes([500, 100])

        # GUI related initialization. some of them from case files.
        self.fields = ["T", "Ux", "Uy", "Uz", "magU", "p", "k", "epsilon", "G", "rho"]
        self.timeSteps = ["0"]
        self.fieldSelectCombo = QtWidgets.QComboBox()
        self.timeSelectCombo = QtWidgets.QComboBox()
        self.defaultFolder = "C:/Shaohui/OpenFoam/radiationTest/air99surf"
        self.paraPath = "C:/Users/CSHAOHUI/Downloads/ParaView-5.6.0-Windows-msvc2015-64bit/bin/paraview.exe"
        self.transparencySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scalar_bar = vtk.vtkScalarBarActor()
        self.axesWidget = vtk.vtkOrientationMarkerWidget()
        self.vtkContainBox = QVBoxLayout()
        self.transparency = 0

        self.addMiscell()

        self.setStatusTip("Ready")

        # screen = QDesktopWidget().screenGeometry()
        # self.setGeometry(0, 0, screen.width(), screen.height())
        self.showMaximized()

        # VTK related initialization.
        self.vtkWindow = QVTKRenderWindowInteractor(self.geoTab)
        self.foamReader = vtk.vtkOpenFOAMReader()
        self.filter = vtk.vtkGeometryFilter()
        self.mapper = vtk.vtkCompositePolyDataMapper2()
        self.actor = vtk.vtkActor()
        self.render = vtk.vtkRenderer()

        # actions!!!
        self.actionOpen.triggered.connect(self.openFile)
        self.actionTools.triggered.connect(self.setting)
        self.actionQuit.triggered.connect(self.shutDownWarning)

    def addMiscell(self):
        # transparency bar to the tool bar
        self.viewBar.addWidget(self.transparencySlider)
        self.transparencySlider.setFixedWidth(100)

        for item in self.fields:
            self.fieldSelectCombo.addItem(item)
        self.receiveBar.addWidget(self.fieldSelectCombo)

        for time in self.timeSteps:
            self.timeSelectCombo.addItem(time)
        self.receiveBar.addWidget(self.timeSelectCombo)

    def setupVTK(self):
        self.vtkContainBox.addWidget(self.vtkWindow)
        self.geoTab.setLayout(self.vtkContainBox)

        tArray = vtk_to_numpy(self.foamReader.GetTimeValues())
        self.foamReader.UpdateTimeStep(tArray[-1])
        self.foamReader.Update()

        self.filter.SetInputConnection(self.foamReader.GetOutputPort())

        self.mapper.SetInputConnection(self.filter.GetOutputPort())
        self.mapper.SetScalarModeToUseCellFieldData()

        # TODO 1, do not miss uniform keyword before the number in boundary condition.
        # TODO 2, do not use Wildcard character for boundary definition.
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
        # self.vtkWindow.SetSize(850, 850)
        self.vtkWindow.Initialize()
        self.setupVTKBackGround()
        self.AddAxes()
        self.setScaleBar()
        self.vtkWindow.Start()
        self.vtkWindow.show()

    def setting(self):
        self.settingDialog = SettingDialog()
        self.settingDialog.show()

    def AddAxes(self):
        axesActor = vtk.vtkAxesActor()
        self.axesWidget.SetOrientationMarker(axesActor)
        self.axesWidget.SetInteractor(self.vtkWindow)

        self.axesWidget.EnabledOn()
        self.axesWidget.InteractiveOff()  # InteractiveOn to enable move the axis
        self.axesWidget.Modified()
        self.vtkWindow.Render()

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

    def resetFile(self):
        self.render = vtk.vtkRenderer()
        self.setupVTKBackGround()

        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)
        self.vtkWindow.Render()

    def openFile(self):
        # TODO add warning box to save the current config, open a new file will overwrite the current model. just
        #  like ANSA.
        self.caseFolder = QFileDialog.getOpenFileName(self, 'Open file', self.defaultFolder,
                                                      "OpenFOAM File (*.foam *.txt)")

        if self.caseFolder[0] != "":
            self.foamReader.SetFileName(str(self.caseFolder[0]))
            self.foamReader.CreateCellToPointOn()
            self.foamReader.DecomposePolyhedraOn()
            self.foamReader.EnableAllCellArrays()
            self.foamReader.Update()
            self.setupVTK()
            self.setWindowTitle(self.caseFolder[0])

    def resetFile(self):
        self.render = vtk.vtkRenderer()
        self.setupVTKBackGround()
        self.vtkWindow.GetRenderWindow().AddRenderer(self.render)

    def shutDownWarning(self):
        buttonReply = QMessageBox.warning(self, 'FOAM Warning', "Do you want to save before exit?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            self.close()
        if buttonReply == QMessageBox.No:
            self.close()
        if buttonReply == QMessageBox.Cancel:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
