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
from Ui_settingDialog import Ui_settingDialog

class GlobalWindow(QMainWindow, Ui_OpenFOAM):
    def __init__(self, parent=None):
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
        self.VTKwindow = VTKWindow(self.rightDomain)
        self.infoMonitor = Info(self.rightDomain)

        self.verticalLayout.addWidget(self.leftRightSplitter)

        self.setCentralWidget(self.mainWindow)
        self.__message__ = "Ready. Let's FOAM!"
        self.leftRightSplitter.setSizes([100, 500])
        self.leftDomain.setSizes([100, 100])
        self.rightDomain.setSizes([500, 100])
        self.showMaximized()
        self.show()
 
        # actions!!!
        self.actionOpen.triggered.connect(self.openFile)
        self.actionTools.triggered.connect(self.setting)
        self.actionQuit.triggered.connect(self.shutDownWarning)

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

    def  setting(self):
        self.Ui_settingDialog.show()

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