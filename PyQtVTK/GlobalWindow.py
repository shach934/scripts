#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QMessageBox, QDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import MouseInteractorStyle
from Panel_Property import * 
from Panel_Tree import *
from Panel_VTK import * 
from Panel_Info import *

from Ui_mainWindow import Ui_OpenFOAM
from Ui_newCase import Ui_newCase
from Ui_openCase import Ui_openCase
from Ui_settingDialog import Ui_settingDialog

class GlobalWindow(QMainWindow, Ui_OpenFOAM):

    def __init__(self, parent  =None):
        super(GlobalWindow, self).__init__(parent)
        self.setupUi(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWindow)

        self.leftRightSplitter = QtWidgets.QSplitter(self.mainWindow)
        self.leftRightSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.leftDomain = QtWidgets.QSplitter(self.leftRightSplitter)
        self.leftDomain.setOrientation(QtCore.Qt.Vertical)

        self.rightDomain = QtWidgets.QSplitter(self.leftRightSplitter)
        self.rightDomain.setOrientation(QtCore.Qt.Vertical)

        self.modelTree = ModelTree(self.leftDomain)
        self.property = Property(self.leftDomain)
        self.VTKwindow = Panel_VTK(self.rightDomain)
        self.infoMonitor = Info(self.rightDomain)

        self.verticalLayout.addWidget(self.leftRightSplitter)
        self.setCentralWidget(self.mainWindow)

        self.modelTree.relate2Property(self.property)
        self.property.relate2VTKWindow(self.VTKwindow)

        self.setStatusTip("Ready")
        self.leftRightSplitter.setSizes([100, 500])
        self.leftDomain.setSizes([100, 100])
        self.rightDomain.setSizes([500, 100])
        self.showMaximized()
        self.show()
 
        # actions!!!
        self.actionNew.triggered.connect(self.newCase)
        self.actionOpen.triggered.connect(self.openCase)
        self.actionTools.triggered.connect(self.settingDialog)
        self.actionQuit.triggered.connect(self.shutDownWarning)

    def openCase(self):
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

    def getNewCasePath(self):
        casePath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.newCaseDialog.newCasePathInput.setText(casePath)
    def getOpenCasePath(self):
        casePath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.openCaseDialog.openCasePathInput.setText(casePath)

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

    def  settingDialog(self):
        settingDialog = QtWidgets.QDialog()
        ui = Ui_settingDialog()
        ui.setupUi(settingDialog)
        settingDialog.show()
        response = settingDialog.exec_()
        
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenFOAM = QtWidgets.QMainWindow()
    ui = GlobalWindow()
    sys.exit(app.exec_())