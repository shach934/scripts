# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ccm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QSize

class Ui_OpenFOAM(object):
    def setupUi(self, OpenFOAM):
        OpenFOAM.setObjectName("OpenFOAM")
        screen = QDesktopWidget().screenGeometry()
        self.width = screen.width()
        self.height = screen.height() - 75
        OpenFOAM.resize(self.width, self.height)
        OpenFOAM.setWindowIcon(QtGui.QIcon("OpenFOAM_icon.png"))
        OpenFOAM.statusBar().showMessage('Ready')
        self.centralwidget = QtWidgets.QWidget(OpenFOAM)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 231, 271))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(290, 50, 741, 371))
        self.tabWidget.setObjectName("tabWidget")
        self.Geometry = QtWidgets.QWidget()
        self.Geometry.setObjectName("Geometry")
        self.graphicsView = QtWidgets.QGraphicsView(self.Geometry)
        self.graphicsView.setGeometry(QtCore.QRect(50, 0, 691, 351))
        self.graphicsView.setObjectName("graphicsView")
        self.tabWidget.addTab(self.Geometry, "")
        self.Monitor = QtWidgets.QWidget()
        self.Monitor.setObjectName("Monitor")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.Monitor)
        self.graphicsView_2.setGeometry(QtCore.QRect(50, 0, 691, 361))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.tabWidget.addTab(self.Monitor, "")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(290, 450, 741, 171))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 330, 241, 291))
        self.textBrowser_2.setObjectName("textBrowser_2")
        OpenFOAM.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OpenFOAM)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1239, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuGeometry = QtWidgets.QMenu(self.menubar)
        self.menuGeometry.setObjectName("menuGeometry")
        self.menuSolver = QtWidgets.QMenu(self.menubar)
        self.menuSolver.setObjectName("menuSolver")
        self.menuPhysics = QtWidgets.QMenu(self.menubar)
        self.menuPhysics.setObjectName("menuPhysics")
        self.menuHeat_transfer = QtWidgets.QMenu(self.menuPhysics)
        self.menuHeat_transfer.setObjectName("menuHeat_transfer")
        self.menuMaterial = QtWidgets.QMenu(self.menubar)
        self.menuMaterial.setObjectName("menuMaterial")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        OpenFOAM.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OpenFOAM)
        self.statusbar.setObjectName("statusbar")
        OpenFOAM.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(OpenFOAM)
        self.toolBar.setObjectName("toolBar")
        OpenFOAM.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        OpenFOAM.insertToolBarBreak(self.toolBar)
        self.actionOpen = QtWidgets.QAction(OpenFOAM)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionWrite = QtWidgets.QAction(OpenFOAM)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionWrite.setIcon(icon1)
        self.actionWrite.setObjectName("actionWrite")
        self.actionQuit = QtWidgets.QAction(OpenFOAM)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("exit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setObjectName("actionQuit")
        self.actionTurbulence = QtWidgets.QAction(OpenFOAM)
        self.actionTurbulence.setObjectName("actionTurbulence")
        self.actionMRF = QtWidgets.QAction(OpenFOAM)
        self.actionMRF.setObjectName("actionMRF")
        self.actionDynamic_Mesh = QtWidgets.QAction(OpenFOAM)
        self.actionDynamic_Mesh.setObjectName("actionDynamic_Mesh")
        self.actionRadiation = QtWidgets.QAction(OpenFOAM)
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
        self.actionFluid.setObjectName("actionFluid")
        self.actionSolid = QtWidgets.QAction(OpenFOAM)
        self.actionSolid.setObjectName("actionSolid")
        self.actionNote = QtWidgets.QAction(OpenFOAM)
        self.actionNote.setObjectName("actionNote")
        self.actionRun = QtWidgets.QAction(OpenFOAM)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("start.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRun.setIcon(icon3)
        self.actionRun.setObjectName("actionRun")
        self.actionStop = QtWidgets.QAction(OpenFOAM)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStop.setIcon(icon4)
        self.actionStop.setObjectName("actionStop")
        self.actionPostProcess = QtWidgets.QAction(OpenFOAM)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("paraview.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionPostProcess.setIcon(icon5)
        self.actionPostProcess.setObjectName("actionPostProcess")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionWrite)
        self.menuFile.addAction(self.actionQuit)
        self.menuGeometry.addAction(self.actionz)
        self.menuSolver.addAction(self.actionfvSchemes)
        self.menuSolver.addAction(self.actionfvOptions)
        self.menuSolver.addAction(self.actionControl)
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
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGeometry.menuAction())
        self.menubar.addAction(self.menuPhysics.menuAction())
        self.menubar.addAction(self.menuMaterial.menuAction())
        self.menubar.addAction(self.menuSolver.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionWrite)
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionQuit)
        self.toolBar.addAction(self.actionPostProcess)

        self.retranslateUi(OpenFOAM)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(OpenFOAM)
        self.setFixedSize(self.layout.sizeHint())

    def retranslateUi(self, OpenFOAM):
        _translate = QtCore.QCoreApplication.translate
        OpenFOAM.setWindowTitle(_translate("OpenFOAM", "OpenFOAM"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("OpenFOAM", "Geometry"))
        item = self.listWidget.item(1)
        item.setText(_translate("OpenFOAM", "Physics"))
        item = self.listWidget.item(2)
        item.setText(_translate("OpenFOAM", "Material"))
        item = self.listWidget.item(3)
        item.setText(_translate("OpenFOAM", "fvSchemes"))
        item = self.listWidget.item(4)
        item.setText(_translate("OpenFOAM", "fvOption"))
        item = self.listWidget.item(5)
        item.setText(_translate("OpenFOAM", "Solver"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Geometry), _translate("OpenFOAM", "Geometry"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Monitor), _translate("OpenFOAM", "Monitor"))
        self.menuFile.setTitle(_translate("OpenFOAM", "File"))
        self.menuGeometry.setTitle(_translate("OpenFOAM", "Geometry"))
        self.menuSolver.setTitle(_translate("OpenFOAM", "Solver"))
        self.menuPhysics.setTitle(_translate("OpenFOAM", "Physics"))
        self.menuHeat_transfer.setTitle(_translate("OpenFOAM", "Heat transfer"))
        self.menuMaterial.setTitle(_translate("OpenFOAM", "Material"))
        self.menuHelp.setTitle(_translate("OpenFOAM", "Help"))
        self.toolBar.setWindowTitle(_translate("OpenFOAM", "toolBar"))
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
        self.actionz.setText(_translate("OpenFOAM", "z=="))
        self.actionSplit_region.setText(_translate("OpenFOAM", "Split region"))
        self.actionMuti_region.setText(_translate("OpenFOAM", "Muti region"))
        self.actionFluid.setText(_translate("OpenFOAM", "Fluid"))
        self.actionSolid.setText(_translate("OpenFOAM", "Solid"))
        self.actionNote.setText(_translate("OpenFOAM", "Note"))
        self.actionRun.setText(_translate("OpenFOAM", "Run"))
        self.actionStop.setText(_translate("OpenFOAM", "Stop"))
        self.actionPostProcess.setText(_translate("OpenFOAM", "PostProcess"))