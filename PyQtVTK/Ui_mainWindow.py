# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenFOAM(object):
    def setupUi(self, OpenFOAM):
        OpenFOAM.setObjectName("OpenFOAM")
        OpenFOAM.resize(1034, 728)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpenFOAM.sizePolicy().hasHeightForWidth())
        OpenFOAM.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/OpenFOAM_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        OpenFOAM.setWindowIcon(icon)
        self.mainWindow = QtWidgets.QWidget(OpenFOAM)
        self.mainWindow.setObjectName("mainWindow")
        OpenFOAM.setCentralWidget(self.mainWindow)
        self.menuBar = QtWidgets.QMenuBar(OpenFOAM)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1034, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuGeometry = QtWidgets.QMenu(self.menuBar)
        self.menuGeometry.setObjectName("menuGeometry")
        self.menuSolver = QtWidgets.QMenu(self.menuBar)
        self.menuSolver.setObjectName("menuSolver")
        self.menuPhysics = QtWidgets.QMenu(self.menuBar)
        self.menuPhysics.setObjectName("menuPhysics")
        self.menuHeat_transfer = QtWidgets.QMenu(self.menuPhysics)
        self.menuHeat_transfer.setObjectName("menuHeat_transfer")
        self.menuMaterial = QtWidgets.QMenu(self.menuBar)
        self.menuMaterial.setObjectName("menuMaterial")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuPostprocessing = QtWidgets.QMenu(self.menuBar)
        self.menuPostprocessing.setObjectName("menuPostprocessing")
        OpenFOAM.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(OpenFOAM)
        self.mainToolBar.setObjectName("mainToolBar")
        OpenFOAM.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.viewBar = QtWidgets.QToolBar(OpenFOAM)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewBar.sizePolicy().hasHeightForWidth())
        self.viewBar.setSizePolicy(sizePolicy)
        self.viewBar.setObjectName("viewBar")
        OpenFOAM.addToolBar(QtCore.Qt.TopToolBarArea, self.viewBar)
        self.statusBar = QtWidgets.QStatusBar(OpenFOAM)
        self.statusBar.setBaseSize(QtCore.QSize(0, 50))
        self.statusBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.statusBar.setObjectName("statusBar")
        OpenFOAM.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(OpenFOAM)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionWrite = QtWidgets.QAction(OpenFOAM)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionWrite.setIcon(icon2)
        self.actionWrite.setObjectName("actionWrite")
        self.actionQuit = QtWidgets.QAction(OpenFOAM)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/exit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setObjectName("actionQuit")
        self.actionTurbulence = QtWidgets.QAction(OpenFOAM)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/air-flow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTurbulence.setIcon(icon4)
        self.actionTurbulence.setObjectName("actionTurbulence")
        self.actionMRF = QtWidgets.QAction(OpenFOAM)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/MRF.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMRF.setIcon(icon5)
        self.actionMRF.setObjectName("actionMRF")
        self.actionDynamic_Mesh = QtWidgets.QAction(OpenFOAM)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/dynamicMesh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDynamic_Mesh.setIcon(icon6)
        self.actionDynamic_Mesh.setObjectName("actionDynamic_Mesh")
        self.actionRadiation = QtWidgets.QAction(OpenFOAM)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/radiation.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRadiation.setIcon(icon7)
        self.actionRadiation.setObjectName("actionRadiation")
        self.actionMultiphase = QtWidgets.QAction(OpenFOAM)
        self.actionMultiphase.setObjectName("actionMultiphase")
        self.actionfvSchemes = QtWidgets.QAction(OpenFOAM)
        self.actionfvSchemes.setObjectName("actionfvSchemes")
        self.actionfvOptions = QtWidgets.QAction(OpenFOAM)
        self.actionfvOptions.setObjectName("actionfvOptions")
        self.actionControl = QtWidgets.QAction(OpenFOAM)
        self.actionControl.setObjectName("actionControl")
        self.actionz = QtWidgets.QAction(OpenFOAM)
        self.actionz.setObjectName("actionz")
        self.actionSplit_region = QtWidgets.QAction(OpenFOAM)
        self.actionSplit_region.setObjectName("actionSplit_region")
        self.actionMuti_region = QtWidgets.QAction(OpenFOAM)
        self.actionMuti_region.setObjectName("actionMuti_region")
        self.actionFluid = QtWidgets.QAction(OpenFOAM)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/waterDrop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFluid.setIcon(icon8)
        self.actionFluid.setObjectName("actionFluid")
        self.actionSolid = QtWidgets.QAction(OpenFOAM)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("images/solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSolid.setIcon(icon9)
        self.actionSolid.setObjectName("actionSolid")
        self.actionNote = QtWidgets.QAction(OpenFOAM)
        self.actionNote.setObjectName("actionNote")
        self.actionRun = QtWidgets.QAction(OpenFOAM)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("images/start.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon10)
        self.actionRun.setObjectName("actionRun")
        self.actionStop = QtWidgets.QAction(OpenFOAM)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("images/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon11)
        self.actionStop.setObjectName("actionStop")
        self.actionPostProcess = QtWidgets.QAction(OpenFOAM)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("images/paraview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPostProcess.setIcon(icon12)
        self.actionPostProcess.setObjectName("actionPostProcess")
        self.actionAlign_X = QtWidgets.QAction(OpenFOAM)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("images/Xaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAlign_X.setIcon(icon13)
        self.actionAlign_X.setObjectName("actionAlign_X")
        self.actionAlign_Y = QtWidgets.QAction(OpenFOAM)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("images/Yaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAlign_Y.setIcon(icon14)
        self.actionAlign_Y.setObjectName("actionAlign_Y")
        self.actionAligh_Z = QtWidgets.QAction(OpenFOAM)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("images/Zaxis2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAligh_Z.setIcon(icon15)
        self.actionAligh_Z.setObjectName("actionAligh_Z")
        self.actionPatches = QtWidgets.QAction(OpenFOAM)
        self.actionPatches.setObjectName("actionPatches")
        self.actionDefault_Folder = QtWidgets.QAction(OpenFOAM)
        self.actionDefault_Folder.setObjectName("actionDefault_Folder")
        self.actionParaview_Path = QtWidgets.QAction(OpenFOAM)
        self.actionParaview_Path.setObjectName("actionParaview_Path")
        self.actionTools = QtWidgets.QAction(OpenFOAM)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("images/setting.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTools.setIcon(icon16)
        self.actionTools.setObjectName("actionTools")
        self.actionMesh = QtWidgets.QAction(OpenFOAM)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("images/grid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMesh.setIcon(icon17)
        self.actionMesh.setObjectName("actionMesh")
        self.actionFrame = QtWidgets.QAction(OpenFOAM)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("images/frame.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFrame.setIcon(icon18)
        self.actionFrame.setObjectName("actionFrame")
        self.actionDecompost = QtWidgets.QAction(OpenFOAM)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("images/decompose.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDecompost.setIcon(icon19)
        self.actionDecompost.setObjectName("actionDecompost")
        self.actionTransperancy = QtWidgets.QAction(OpenFOAM)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap("images/transparency.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTransperancy.setIcon(icon20)
        self.actionTransperancy.setObjectName("actionTransperancy")
        self.actionAuto_Scale = QtWidgets.QAction(OpenFOAM)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap("images/autoScale.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAuto_Scale.setIcon(icon21)
        self.actionAuto_Scale.setObjectName("actionAuto_Scale")
        self.actionSet_Scale = QtWidgets.QAction(OpenFOAM)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap("images/setScale.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSet_Scale.setIcon(icon22)
        self.actionSet_Scale.setObjectName("actionSet_Scale")
        self.actioncellZone = QtWidgets.QAction(OpenFOAM)
        self.actioncellZone.setObjectName("actioncellZone")
        self.actionWall_Heat_Flux = QtWidgets.QAction(OpenFOAM)
        self.actionWall_Heat_Flux.setObjectName("actionWall_Heat_Flux")
        self.actionTemperature_Probe = QtWidgets.QAction(OpenFOAM)
        self.actionTemperature_Probe.setObjectName("actionTemperature_Probe")
        self.actionVelocity_Probe = QtWidgets.QAction(OpenFOAM)
        self.actionVelocity_Probe.setObjectName("actionVelocity_Probe")
        self.actionHeat_Transfer_Coefficent = QtWidgets.QAction(OpenFOAM)
        self.actionHeat_Transfer_Coefficent.setObjectName("actionHeat_Transfer_Coefficent")
        self.actionVolume = QtWidgets.QAction(OpenFOAM)
        self.actionVolume.setObjectName("actionVolume")
        self.actionMass_flow_rate = QtWidgets.QAction(OpenFOAM)
        self.actionMass_flow_rate.setObjectName("actionMass_flow_rate")
        self.actionFit_Window = QtWidgets.QAction(OpenFOAM)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap("images/fit window.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFit_Window.setIcon(icon23)
        self.actionFit_Window.setObjectName("actionFit_Window")
        self.actionNew = QtWidgets.QAction(OpenFOAM)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap("images/New.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon24)
        self.actionNew.setObjectName("actionNew")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionWrite)
        self.menuFile.addAction(self.actionQuit)
        self.menuGeometry.addAction(self.actionz)
        self.menuGeometry.addAction(self.actioncellZone)
        self.menuGeometry.addAction(self.actionPatches)
        self.menuSolver.addAction(self.actionfvSchemes)
        self.menuSolver.addAction(self.actionfvOptions)
        self.menuSolver.addAction(self.actionControl)
        self.menuSolver.addAction(self.actionDecompost)
        self.menuSolver.addAction(self.actionRun)
        self.menuSolver.addAction(self.actionStop)
        self.menuSolver.addAction(self.actionPostProcess)
        self.menuHeat_transfer.addAction(self.actionMuti_region)
        self.menuPhysics.addAction(self.actionTurbulence)
        self.menuPhysics.addAction(self.actionMRF)
        self.menuPhysics.addAction(self.actionDynamic_Mesh)
        self.menuPhysics.addAction(self.actionRadiation)
        self.menuPhysics.addAction(self.actionMultiphase)
        self.menuPhysics.addAction(self.menuHeat_transfer.menuAction())
        self.menuMaterial.addAction(self.actionFluid)
        self.menuMaterial.addAction(self.actionSolid)
        self.menuHelp.addAction(self.actionNote)
        self.menuView.addAction(self.actionAlign_X)
        self.menuView.addAction(self.actionAlign_Y)
        self.menuView.addAction(self.actionAligh_Z)
        self.menuView.addAction(self.actionMesh)
        self.menuView.addAction(self.actionFrame)
        self.menuView.addAction(self.actionTransperancy)
        self.menuView.addAction(self.actionAuto_Scale)
        self.menuView.addAction(self.actionSet_Scale)
        self.menuView.addAction(self.actionFit_Window)
        self.menuSetting.addAction(self.actionTools)
        self.menuPostprocessing.addAction(self.actionWall_Heat_Flux)
        self.menuPostprocessing.addAction(self.actionTemperature_Probe)
        self.menuPostprocessing.addAction(self.actionVelocity_Probe)
        self.menuPostprocessing.addAction(self.actionHeat_Transfer_Coefficent)
        self.menuPostprocessing.addAction(self.actionVolume)
        self.menuPostprocessing.addAction(self.actionMass_flow_rate)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuGeometry.menuAction())
        self.menuBar.addAction(self.menuPhysics.menuAction())
        self.menuBar.addAction(self.menuMaterial.menuAction())
        self.menuBar.addAction(self.menuSolver.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())
        self.menuBar.addAction(self.menuPostprocessing.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.mainToolBar.addAction(self.actionNew)
        self.mainToolBar.addAction(self.actionOpen)
        self.mainToolBar.addAction(self.actionWrite)
        self.mainToolBar.addAction(self.actionTurbulence)
        self.mainToolBar.addAction(self.actionRun)
        self.mainToolBar.addAction(self.actionStop)
        self.mainToolBar.addAction(self.actionTools)
        self.mainToolBar.addAction(self.actionQuit)
        self.mainToolBar.addAction(self.actionPostProcess)

        self.retranslateUi(OpenFOAM)
        QtCore.QMetaObject.connectSlotsByName(OpenFOAM)

    def retranslateUi(self, OpenFOAM):
        _translate = QtCore.QCoreApplication.translate
        OpenFOAM.setWindowTitle(_translate("OpenFOAM", "XinFOAM"))
        self.menuFile.setTitle(_translate("OpenFOAM", "File"))
        self.menuGeometry.setTitle(_translate("OpenFOAM", "Geometry"))
        self.menuSolver.setTitle(_translate("OpenFOAM", "Solver"))
        self.menuPhysics.setTitle(_translate("OpenFOAM", "Physics"))
        self.menuHeat_transfer.setTitle(_translate("OpenFOAM", "Heat transfer"))
        self.menuMaterial.setTitle(_translate("OpenFOAM", "Material"))
        self.menuHelp.setTitle(_translate("OpenFOAM", "Help"))
        self.menuView.setTitle(_translate("OpenFOAM", "View"))
        self.menuSetting.setTitle(_translate("OpenFOAM", "Setting"))
        self.menuPostprocessing.setTitle(_translate("OpenFOAM", "Postprocessing"))
        self.mainToolBar.setWindowTitle(_translate("OpenFOAM", "mainBar"))
        self.viewBar.setWindowTitle(_translate("OpenFOAM", "viewBar"))
        self.statusBar.setToolTip(_translate("OpenFOAM", "To see if it exists"))
        self.actionOpen.setText(_translate("OpenFOAM", "Open"))
        self.actionWrite.setText(_translate("OpenFOAM", "Write"))
        self.actionQuit.setText(_translate("OpenFOAM", "Quit"))
        self.actionTurbulence.setText(_translate("OpenFOAM", "Turbulence"))
        self.actionMRF.setText(_translate("OpenFOAM", "MRF"))
        self.actionDynamic_Mesh.setText(_translate("OpenFOAM", "Dynamic Mesh"))
        self.actionRadiation.setText(_translate("OpenFOAM", "Radiation"))
        self.actionMultiphase.setText(_translate("OpenFOAM", "Multiphase"))
        self.actionfvSchemes.setText(_translate("OpenFOAM", "fvSchemes"))
        self.actionfvOptions.setText(_translate("OpenFOAM", "fvOptions"))
        self.actionControl.setText(_translate("OpenFOAM", "Control "))
        self.actionz.setText(_translate("OpenFOAM", "Domain"))
        self.actionSplit_region.setText(_translate("OpenFOAM", "Split region"))
        self.actionMuti_region.setText(_translate("OpenFOAM", "Muti region"))
        self.actionFluid.setText(_translate("OpenFOAM", "Fluid"))
        self.actionSolid.setText(_translate("OpenFOAM", "Solid"))
        self.actionNote.setText(_translate("OpenFOAM", "Note"))
        self.actionRun.setText(_translate("OpenFOAM", "Run"))
        self.actionStop.setText(_translate("OpenFOAM", "Stop"))
        self.actionPostProcess.setText(_translate("OpenFOAM", "PostProcess"))
        self.actionAlign_X.setText(_translate("OpenFOAM", "Align X"))
        self.actionAlign_Y.setText(_translate("OpenFOAM", "Align Y"))
        self.actionAligh_Z.setText(_translate("OpenFOAM", "Aligh Z"))
        self.actionPatches.setText(_translate("OpenFOAM", "Patches"))
        self.actionDefault_Folder.setText(_translate("OpenFOAM", "Default Folder"))
        self.actionParaview_Path.setText(_translate("OpenFOAM", "Paraview Path"))
        self.actionTools.setText(_translate("OpenFOAM", "Tools"))
        self.actionMesh.setText(_translate("OpenFOAM", "Mesh"))
        self.actionFrame.setText(_translate("OpenFOAM", "Frame"))
        self.actionDecompost.setText(_translate("OpenFOAM", "Decompose"))
        self.actionTransperancy.setText(_translate("OpenFOAM", "Transperancy"))
        self.actionAuto_Scale.setText(_translate("OpenFOAM", "Auto Scale"))
        self.actionSet_Scale.setText(_translate("OpenFOAM", "Set Scale"))
        self.actioncellZone.setText(_translate("OpenFOAM", "cellZone"))
        self.actionWall_Heat_Flux.setText(_translate("OpenFOAM", "Wall Heat Flux"))
        self.actionTemperature_Probe.setText(_translate("OpenFOAM", "Temperature Probe"))
        self.actionVelocity_Probe.setText(_translate("OpenFOAM", "Velocity Probe"))
        self.actionHeat_Transfer_Coefficent.setText(_translate("OpenFOAM", "Heat Transfer Coefficent"))
        self.actionVolume.setText(_translate("OpenFOAM", "Volumetric flow rate"))
        self.actionMass_flow_rate.setText(_translate("OpenFOAM", "Mass flow rate"))
        self.actionNew.setText(_translate("OpenFOAM", "New"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenFOAM = QtWidgets.QMainWindow()
    ui = Ui_OpenFOAM()
    ui.setupUi(OpenFOAM)
    OpenFOAM.show()
    sys.exit(app.exec_())
