# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_fvSchemes_grad.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(253, 251)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.divInterpolCombox = QtWidgets.QComboBox(Form)
        self.divInterpolCombox.setObjectName("divInterpolCombox")
        self.divInterpolCombox.addItem("")
        self.divInterpolCombox.addItem("")
        self.divInterpolCombox.addItem("")
        self.gridLayout.addWidget(self.divInterpolCombox, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.divGradGaussRadBtn = QtWidgets.QRadioButton(self.groupBox)
        self.divGradGaussRadBtn.setObjectName("divGradGaussRadBtn")
        self.gridLayout_2.addWidget(self.divGradGaussRadBtn, 0, 0, 1, 1)
        self.divGradGaussInput = QtWidgets.QComboBox(self.groupBox)
        self.divGradGaussInput.setObjectName("divGradGaussInput")
        self.divGradGaussInput.addItem("")
        self.divGradGaussInput.addItem("")
        self.divGradGaussInput.addItem("")
        self.gridLayout_2.addWidget(self.divGradGaussInput, 0, 1, 1, 4)
        self.divGradLeastSquareRadBtn = QtWidgets.QRadioButton(self.groupBox)
        self.divGradLeastSquareRadBtn.setObjectName("divGradLeastSquareRadBtn")
        self.gridLayout_2.addWidget(self.divGradLeastSquareRadBtn, 1, 0, 1, 3)
        self.divGradForthRadBtn = QtWidgets.QRadioButton(self.groupBox)
        self.divGradForthRadBtn.setObjectName("divGradForthRadBtn")
        self.gridLayout_2.addWidget(self.divGradForthRadBtn, 2, 0, 1, 1)
        self.divGradLimitChecBox = QtWidgets.QCheckBox(self.groupBox)
        self.divGradLimitChecBox.setObjectName("divGradLimitChecBox")
        self.gridLayout_2.addWidget(self.divGradLimitChecBox, 3, 0, 1, 2)
        self.divGradLimitCombox = QtWidgets.QComboBox(self.groupBox)
        self.divGradLimitCombox.setObjectName("divGradLimitCombox")
        self.divGradLimitCombox.addItem("")
        self.divGradLimitCombox.addItem("")
        self.gridLayout_2.addWidget(self.divGradLimitCombox, 3, 2, 1, 3)
        self.divGradLimitInput = QtWidgets.QLineEdit(self.groupBox)
        self.divGradLimitInput.setObjectName("divGradLimitInput")
        self.gridLayout_2.addWidget(self.divGradLimitInput, 3, 5, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 6)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 6)
        self.divsnGradCombox = QtWidgets.QComboBox(self.groupBox)
        self.divsnGradCombox.setObjectName("divsnGradCombox")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.divsnGradCombox.addItem("")
        self.gridLayout_2.addWidget(self.divsnGradCombox, 6, 0, 1, 4)
        self.divsnGradInput = QtWidgets.QLineEdit(self.groupBox)
        self.divsnGradInput.setObjectName("divsnGradInput")
        self.gridLayout_2.addWidget(self.divsnGradInput, 6, 4, 1, 2)
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 7, 0, 1, 6)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 8, 0, 1, 1)
        self.divLaplacianInput = QtWidgets.QLabel(self.groupBox)
        self.divLaplacianInput.setObjectName("divLaplacianInput")
        self.gridLayout_2.addWidget(self.divLaplacianInput, 8, 3, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Interpolation"))
        self.divInterpolCombox.setItemText(0, _translate("Form", "Linear"))
        self.divInterpolCombox.setItemText(1, _translate("Form", "Cubic"))
        self.divInterpolCombox.setItemText(2, _translate("Form", "Midpoint"))
        self.groupBox.setTitle(_translate("Form", "grad"))
        self.divGradGaussRadBtn.setText(_translate("Form", "Gauss"))
        self.divGradGaussInput.setItemText(0, _translate("Form", "Linear"))
        self.divGradGaussInput.setItemText(1, _translate("Form", "Cubic"))
        self.divGradGaussInput.setItemText(2, _translate("Form", "Midpoint"))
        self.divGradLeastSquareRadBtn.setText(_translate("Form", "Least Square"))
        self.divGradForthRadBtn.setText(_translate("Form", "Fourth"))
        self.divGradLimitChecBox.setText(_translate("Form", "Limiting"))
        self.divGradLimitCombox.setItemText(0, _translate("Form", "Cell Limited"))
        self.divGradLimitCombox.setItemText(1, _translate("Form", "Face Limited"))
        self.divGradLimitInput.setText(_translate("Form", "1"))
        self.label_2.setText(_translate("Form", "snGrad"))
        self.divsnGradCombox.setItemText(0, _translate("Form", "Corrected"))
        self.divsnGradCombox.setItemText(1, _translate("Form", "Uncorrected"))
        self.divsnGradCombox.setItemText(2, _translate("Form", "Orthogonal"))
        self.divsnGradCombox.setItemText(3, _translate("Form", "Face Corrected"))
        self.divsnGradCombox.setItemText(4, _translate("Form", "Limited"))
        self.divsnGradCombox.setItemText(5, _translate("Form", "Linear Fit"))
        self.divsnGradCombox.setItemText(6, _translate("Form", "Quadatic Fit"))
        self.divsnGradInput.setText(_translate("Form", "1"))
        self.label_3.setText(_translate("Form", "Laplacian"))
        self.divLaplacianInput.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())