# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/AndroidApps/ui2py/design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets
import sys
import os
import tkinter.filedialog

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ui2py(object):
    def setupUi(self, ui2py):
        ui2py.setObjectName("ui2py")
        ui2py.resize(445, 260)
        ui2py.setMinimumSize(QtCore.QSize(445, 260))
        self.centralwidget = QtWidgets.QWidget(ui2py)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.OpenButton = QtWidgets.QPushButton(self.centralwidget)
        self.OpenButton.setObjectName("OpenButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.OpenButton)
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setObjectName("SaveButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.SaveButton)
        self.PathLabel = QtWidgets.QLabel(self.centralwidget)
        self.PathLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.PathLabel.setText("")
        self.PathLabel.setObjectName("PathLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.PathLabel)
        self.ClearButton = QtWidgets.QPushButton(self.centralwidget)
        self.ClearButton.setObjectName("ClearButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ClearButton)
        self.SelectedFilesLabel = QtWidgets.QLabel(self.centralwidget)
        self.SelectedFilesLabel.setObjectName("SelectedFilesLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.SelectedFilesLabel)
        ui2py.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ui2py)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 445, 21))
        self.menubar.setObjectName("menubar")
        ui2py.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ui2py)
        self.statusbar.setObjectName("statusbar")
        ui2py.setStatusBar(self.statusbar)
        self.actionUsage = QtWidgets.QAction(ui2py)
        self.actionUsage.setObjectName("actionUsage")
        self.actionInfo = QtWidgets.QAction(ui2py)
        self.actionInfo.setObjectName("actionInfo")
        self.actionAbout = QtWidgets.QAction(ui2py)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(ui2py)
        QtCore.QMetaObject.connectSlotsByName(ui2py)

    def retranslateUi(self, ui2py):
        _translate = QtCore.QCoreApplication.translate
        ui2py.setWindowTitle(_translate("ui2py", "ui2py"))
        self.OpenButton.setText(_translate("ui2py", "Open"))
        self.SaveButton.setText(_translate("ui2py", "Convert"))
        self.ClearButton.setText(_translate("ui2py", "Clear"))
        self.SelectedFilesLabel.setText(_translate("ui2py", "No files selected"))
        self.actionUsage.setText(_translate("ui2py", "Help"))
        self.actionInfo.setText(_translate("ui2py", "Info"))
        self.actionAbout.setText(_translate("ui2py", "About"))
		
"""
TODO: Shift Text UI to right center
      Reference Help and About from UI and point to MenuHandler
      Implement Drag and Drop
      Resize messageboxes
      resize mainwindow
~Ashwin Pilgaonkar~
"""

class ui2py(QtWidgets.QMainWindow, Ui_ui2py):

    # Set initial path to current working directory
    savedir = os.getcwd()

    def __init__(self, parent=None):
        super(ui2py, self).__init__(parent)
        self.setupUi(self)
        self.OpenButton.clicked.connect(self.OpenUI)
        self.SaveButton.clicked.connect(self.Convert)
        self.ClearButton.clicked.connect(self.Clear)

        #MenuBar items (needs to be redone)
        bar = self.menuBar()
        help = bar.addMenu("Help")
        help.addAction("Usage")
        help.triggered[QtWidgets.QAction].connect(self.MenuHandler)

        about = bar.addMenu("About")
        about.addAction("Info")
        about.triggered[QtWidgets.QAction].connect(self.MenuHandler)

    def OpenUI(self):
        #Hides the Tkinter window
        root = tkinter.Tk()
        root.withdraw()

        count=0
        pathtext=""

        filepath = tkinter.filedialog.askopenfiles(initialdir=self.savedir, title="Select File", filetypes=(("PyQt Designer UI Files", "*.ui"), ("", "")))

        #Save the path of the selected file for easier selection
        self.savedir = filepath

        for file in self.savedir:
            #Check if file extension is *.ui
            if filepath[count].name[len(filepath[count].name)-1]!='i' and filepath[count].name[len(filepath[count].name)-2]!='u' :
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Oops, Wrong file!")
                msg.setInformativeText("Please select a QtDesigner *.ui file.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                self.Clear()

            else:
                pathtext = pathtext + filepath[count].name + "   "
                count = count+1

                #Update UI elements
                self.SelectedFilesLabel.setText("%d files selected" %count)
                self.PathLabel.setText(pathtext)

    def Convert(self):
        #If no files are selected
        if isinstance(self.savedir, str):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Oops! No files selected")
            msg.setInformativeText("Please select one or more files.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

        else:
            for file in self.savedir:
                #Change extension of output file to .py
                pyname = file.name
                pyname = pyname[:len(pyname)-2] + pyname[len(pyname):]
                pyname = pyname + "py"
                os.system("pyuic5 -x "+file.name+" -o "+pyname)
                self.PathLabel.setText("Done!")

    def Clear(self):
        #Clear UI Elements
        self.SelectedFilesLabel.setText("No files selected")
        self.PathLabel.setText("")

    #~~~~~~~~~~~~~~~~~~~~
    #needs to be implemented
    def MenuHandler(self):
        mode = 0
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        if mode==0:
            msg.setText("Usage:")
            msg.setInformativeText("WIP.")
            msg.setWindowTitle("Help")

        else:
            msg.setText("ui2py")
            msg.setInformativeText("Created by Ashwin Pilgaonkar")
            msg.setWindowTitle("About")

        msg.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ui2py()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()