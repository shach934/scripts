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

class main(GlobalWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)

        self.foamConfig = OpenFOAMCase()
        self.caseName = "Model"
        self.numberOfRegions = 0
        self.patches = []
        self.regions = {}  # the structure of the boundary info is like this self.region["air"] = ["wall", "air1"]

        self.defaultFolder = "C:/Shaohui/OpenFoam/radiationTest/air99surf"
        self.paraPath = "C:/Users/CSHAOHUI/Downloads/ParaView-5.6.0-Windows-msvc2015-64bit/bin/paraview.exe"

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