#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
create a simple interface for OpenFOAM using PyQt5 and VTK. Help to setup the OpenFOAM case and visualization.
PyQt5 is used to generate the GUI
VTK   is used to visualize the OpenFOAM mesh

author: Chen Shaohui
Last edited: December 2019
"""

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QDesktopWidget, QVBoxLayout
from ccm import Ui_OpenFOAM
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy


class MyWindow(QMainWindow, Ui_OpenFOAM):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionOpen.triggered.connect(self.setupVTK)

    def setupVTK(self):


    def setupAxes(self):

        axesActor = vtk.vtkAxesActor()

        self.axesWidget = vtk.vtkOrientationMarkerWidget()
        self.axesWidget.SetOrientationMarker(axesActor)
        self.axesWidget.SetInteractor(self.widget)

        self.axesWidget.EnabledOn()
        self.axesWidget.InteractiveOn()
        self.widget.Render()


    def setupVTKBackGround(self):
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.2, 0.4, 0.6)
        self.render.SetBackground(1, 1, 1)

    def resetFile(self):
        self.render = vtk.vtkRenderer()
        self.setupVTKBackGround()

        self.widget.GetRenderWindow().AddRenderer(self.render)
        self.widget.Render()

    def openFile(self):
        self.fileName = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop',
                                               "OpenFOAM File (*.foam)")
        self.foam_reader.SetFileName(str(self.fileName[0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
