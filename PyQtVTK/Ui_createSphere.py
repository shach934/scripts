# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_createSphere.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_createSphere(object):
    def setupUi(self, createSphere):
        createSphere.setObjectName("createSphere")
        createSphere.resize(241, 187)
        self.gridLayout = QtWidgets.QGridLayout(createSphere)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(createSphere)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.sphereNameInput = QtWidgets.QLineEdit(createSphere)
        self.sphereNameInput.setObjectName("sphereNameInput")
        self.gridLayout.addWidget(self.sphereNameInput, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(createSphere)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.sphereColorComboBox = QtWidgets.QComboBox(createSphere)
        self.sphereColorComboBox.setObjectName("sphereColorComboBox")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.sphereColorComboBox.addItem("")
        self.gridLayout.addWidget(self.sphereColorComboBox, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(createSphere)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(createSphere)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_6 = QtWidgets.QLabel(createSphere)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sphereRadiusInput = QtWidgets.QLineEdit(createSphere)
        self.sphereRadiusInput.setObjectName("sphereRadiusInput")
        self.horizontalLayout_2.addWidget(self.sphereRadiusInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sphereCenterXInput = QtWidgets.QLineEdit(createSphere)
        self.sphereCenterXInput.setObjectName("sphereCenterXInput")
        self.horizontalLayout.addWidget(self.sphereCenterXInput)
        self.sphereCenterYInput = QtWidgets.QLineEdit(createSphere)
        self.sphereCenterYInput.setObjectName("sphereCenterYInput")
        self.horizontalLayout.addWidget(self.sphereCenterYInput)
        self.sphereCenterZInpt = QtWidgets.QLineEdit(createSphere)
        self.sphereCenterZInpt.setObjectName("sphereCenterZInpt")
        self.horizontalLayout.addWidget(self.sphereCenterZInpt)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sphereResoluThetaInput = QtWidgets.QLineEdit(createSphere)
        self.sphereResoluThetaInput.setObjectName("sphereResoluThetaInput")
        self.horizontalLayout_3.addWidget(self.sphereResoluThetaInput)
        self.sphereResoluDeltaInput = QtWidgets.QLineEdit(createSphere)
        self.sphereResoluDeltaInput.setObjectName("sphereResoluDeltaInput")
        self.horizontalLayout_3.addWidget(self.sphereResoluDeltaInput)
        self.sphereResoluAlphaInput = QtWidgets.QLineEdit(createSphere)
        self.sphereResoluAlphaInput.setObjectName("sphereResoluAlphaInput")
        self.horizontalLayout_3.addWidget(self.sphereResoluAlphaInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.createSphereBtn = QtWidgets.QPushButton(createSphere)
        self.createSphereBtn.setObjectName("createSphereBtn")
        self.horizontalLayout_4.addWidget(self.createSphereBtn)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 2)

        self.retranslateUi(createSphere)
        QtCore.QMetaObject.connectSlotsByName(createSphere)

    def retranslateUi(self, createSphere):
        _translate = QtCore.QCoreApplication.translate
        createSphere.setWindowTitle(_translate("createSphere", "Form"))
        self.label_3.setText(_translate("createSphere", "Name"))
        self.sphereNameInput.setText(_translate("createSphere", "Sphere_1"))
        self.label_5.setText(_translate("createSphere", "Color"))
        self.sphereColorComboBox.setItemText(0, _translate("createSphere", "blue"))
        self.sphereColorComboBox.setItemText(1, _translate("createSphere", "darkBlue"))
        self.sphereColorComboBox.setItemText(2, _translate("createSphere", "gray"))
        self.sphereColorComboBox.setItemText(3, _translate("createSphere", "darkGray"))
        self.sphereColorComboBox.setItemText(4, _translate("createSphere", "lightGray"))
        self.sphereColorComboBox.setItemText(5, _translate("createSphere", "green"))
        self.sphereColorComboBox.setItemText(6, _translate("createSphere", "darkGreen"))
        self.sphereColorComboBox.setItemText(7, _translate("createSphere", "cyan"))
        self.sphereColorComboBox.setItemText(8, _translate("createSphere", "darkCyan"))
        self.sphereColorComboBox.setItemText(9, _translate("createSphere", "red"))
        self.sphereColorComboBox.setItemText(10, _translate("createSphere", "darkRed"))
        self.sphereColorComboBox.setItemText(11, _translate("createSphere", "magenta"))
        self.sphereColorComboBox.setItemText(12, _translate("createSphere", "darkMagenta"))
        self.sphereColorComboBox.setItemText(13, _translate("createSphere", "white"))
        self.sphereColorComboBox.setItemText(14, _translate("createSphere", "black"))
        self.sphereColorComboBox.setItemText(15, _translate("createSphere", "PICK"))
        self.label_2.setText(_translate("createSphere", "Radius"))
        self.label.setText(_translate("createSphere", "Center"))
        self.label_6.setText(_translate("createSphere", "Resolution"))
        self.sphereRadiusInput.setText(_translate("createSphere", "1"))
        self.sphereCenterXInput.setText(_translate("createSphere", "0"))
        self.sphereCenterYInput.setText(_translate("createSphere", "0"))
        self.sphereCenterZInpt.setText(_translate("createSphere", "0"))
        self.sphereResoluThetaInput.setText(_translate("createSphere", "10"))
        self.sphereResoluDeltaInput.setText(_translate("createSphere", "10"))
        self.sphereResoluAlphaInput.setText(_translate("createSphere", "10"))
        self.createSphereBtn.setText(_translate("createSphere", "Create"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createSphere = QtWidgets.QWidget()
    ui = Ui_createSphere()
    ui.setupUi(createSphere)
    createSphere.show()
    sys.exit(app.exec_())
