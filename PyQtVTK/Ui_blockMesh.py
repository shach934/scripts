# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_blockMesh.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_blockMesh(object):
    def setupUi(self, blockMesh):
        blockMesh.setObjectName("blockMesh")
        blockMesh.resize(276, 261)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(blockMesh)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(blockMesh)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.gradYInput = QtWidgets.QLineEdit(self.widget)
        self.gradYInput.setObjectName("gradYInput")
        self.gridLayout.addWidget(self.gradYInput, 5, 3, 1, 1)
        self.cellsizeYShow = QtWidgets.QLineEdit(self.widget)
        self.cellsizeYShow.setEnabled(False)
        self.cellsizeYShow.setObjectName("cellsizeYShow")
        self.gridLayout.addWidget(self.cellsizeYShow, 7, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 6, 1, 1, 1)
        self.minXInput = QtWidgets.QLineEdit(self.widget)
        self.minXInput.setObjectName("minXInput")
        self.gridLayout.addWidget(self.minXInput, 2, 2, 1, 1)
        self.pointXInput = QtWidgets.QLineEdit(self.widget)
        self.pointXInput.setObjectName("pointXInput")
        self.gridLayout.addWidget(self.pointXInput, 9, 2, 1, 1)
        self.cellNumXInput = QtWidgets.QLineEdit(self.widget)
        self.cellNumXInput.setObjectName("cellNumXInput")
        self.gridLayout.addWidget(self.cellNumXInput, 6, 2, 1, 1)
        self.pointYInput = QtWidgets.QLineEdit(self.widget)
        self.pointYInput.setObjectName("pointYInput")
        self.gridLayout.addWidget(self.pointYInput, 9, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.pointZInput = QtWidgets.QLineEdit(self.widget)
        self.pointZInput.setObjectName("pointZInput")
        self.gridLayout.addWidget(self.pointZInput, 9, 4, 1, 1)
        self.gradZInput = QtWidgets.QLineEdit(self.widget)
        self.gradZInput.setObjectName("gradZInput")
        self.gridLayout.addWidget(self.gradZInput, 5, 4, 1, 1)
        self.minYInput = QtWidgets.QLineEdit(self.widget)
        self.minYInput.setObjectName("minYInput")
        self.gridLayout.addWidget(self.minYInput, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 1, 1, 1)
        self.cellsizeXShow = QtWidgets.QLineEdit(self.widget)
        self.cellsizeXShow.setEnabled(False)
        self.cellsizeXShow.setObjectName("cellsizeXShow")
        self.gridLayout.addWidget(self.cellsizeXShow, 7, 2, 1, 1)
        self.maxYInput = QtWidgets.QLineEdit(self.widget)
        self.maxYInput.setObjectName("maxYInput")
        self.gridLayout.addWidget(self.maxYInput, 3, 3, 1, 1)
        self.maxXInput = QtWidgets.QLineEdit(self.widget)
        self.maxXInput.setObjectName("maxXInput")
        self.gridLayout.addWidget(self.maxXInput, 3, 2, 1, 1)
        self.gradXInput = QtWidgets.QLineEdit(self.widget)
        self.gradXInput.setObjectName("gradXInput")
        self.gridLayout.addWidget(self.gradXInput, 5, 2, 1, 1)
        self.minZInput = QtWidgets.QLineEdit(self.widget)
        self.minZInput.setObjectName("minZInput")
        self.gridLayout.addWidget(self.minZInput, 2, 4, 1, 1)
        self.cellsizeZShow = QtWidgets.QLineEdit(self.widget)
        self.cellsizeZShow.setEnabled(False)
        self.cellsizeZShow.setObjectName("cellsizeZShow")
        self.gridLayout.addWidget(self.cellsizeZShow, 7, 4, 1, 1)
        self.cellNumZInput = QtWidgets.QLineEdit(self.widget)
        self.cellNumZInput.setObjectName("cellNumZInput")
        self.gridLayout.addWidget(self.cellNumZInput, 6, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 9, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 1, 1, 4)
        self.cellNumYinput = QtWidgets.QLineEdit(self.widget)
        self.cellNumYinput.setObjectName("cellNumYinput")
        self.gridLayout.addWidget(self.cellNumYinput, 6, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 8, 1, 1, 4)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 1, 1, 4)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 1, 1, 1)
        self.maxZInput = QtWidgets.QLineEdit(self.widget)
        self.maxZInput.setObjectName("maxZInput")
        self.gridLayout.addWidget(self.maxZInput, 3, 4, 1, 1)
        self.createBlockMeshBtn = QtWidgets.QPushButton(self.widget)
        self.createBlockMeshBtn.setObjectName("createBlockMeshBtn")
        self.gridLayout.addWidget(self.createBlockMeshBtn, 10, 3, 1, 2)
        self.previewBlockMeshBtn = QtWidgets.QPushButton(self.widget)
        self.previewBlockMeshBtn.setObjectName("previewBlockMeshBtn")
        self.gridLayout.addWidget(self.previewBlockMeshBtn, 10, 1, 1, 2)
        self.verticalLayout_3.addWidget(self.widget)

        self.retranslateUi(blockMesh)
        QtCore.QMetaObject.connectSlotsByName(blockMesh)

    def retranslateUi(self, blockMesh):
        _translate = QtCore.QCoreApplication.translate
        blockMesh.setWindowTitle(_translate("blockMesh", "Form"))
        self.gradYInput.setText(_translate("blockMesh", "1"))
        self.cellsizeYShow.setText(_translate("blockMesh", "1"))
        self.label_8.setText(_translate("blockMesh", "Cell Count"))
        self.minXInput.setText(_translate("blockMesh", "-5"))
        self.pointXInput.setText(_translate("blockMesh", "0"))
        self.cellNumXInput.setText(_translate("blockMesh", "10"))
        self.pointYInput.setText(_translate("blockMesh", "0"))
        self.label_6.setText(_translate("blockMesh", "Max(mm)"))
        self.label.setText(_translate("blockMesh", "BlockMesh"))
        self.label_5.setText(_translate("blockMesh", "X"))
        self.pointZInput.setText(_translate("blockMesh", "0"))
        self.gradZInput.setText(_translate("blockMesh", "1"))
        self.minYInput.setText(_translate("blockMesh", "-5"))
        self.label_3.setText(_translate("blockMesh", "Grading"))
        self.cellsizeXShow.setText(_translate("blockMesh", "1"))
        self.maxYInput.setText(_translate("blockMesh", "5"))
        self.maxXInput.setText(_translate("blockMesh", "5"))
        self.gradXInput.setText(_translate("blockMesh", "1"))
        self.minZInput.setText(_translate("blockMesh", "-5"))
        self.cellsizeZShow.setText(_translate("blockMesh", "1"))
        self.cellNumZInput.setText(_translate("blockMesh", "10"))
        self.label_7.setText(_translate("blockMesh", "Y"))
        self.label_4.setText(_translate("blockMesh", "Point"))
        self.cellNumYinput.setText(_translate("blockMesh", "10"))
        self.label_10.setText(_translate("blockMesh", "Z"))
        self.label_2.setText(_translate("blockMesh", "Cell Size"))
        self.label_9.setText(_translate("blockMesh", "Min(mm)"))
        self.maxZInput.setText(_translate("blockMesh", "5"))
        self.createBlockMeshBtn.setText(_translate("blockMesh", "Create"))
        self.previewBlockMeshBtn.setText(_translate("blockMesh", "Preview"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    blockMesh = QtWidgets.QWidget()
    ui = Ui_blockMesh()
    ui.setupUi(blockMesh)
    blockMesh.show()
    sys.exit(app.exec_())
