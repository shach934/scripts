# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_createCone.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_createCone(object):
    def setupUi(self, createCone):
        createCone.setObjectName("createCone")
        createCone.resize(232, 233)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(createCone)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(createCone)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(createCone)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.coneNameInput = QtWidgets.QLineEdit(createCone)
        self.coneNameInput.setObjectName("coneNameInput")
        self.gridLayout.addWidget(self.coneNameInput, 0, 1, 1, 1)
        self.coneColorCombox = QtWidgets.QComboBox(createCone)
        self.coneColorCombox.setObjectName("coneColorCombox")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.coneColorCombox.addItem("")
        self.gridLayout.addWidget(self.coneColorCombox, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(createCone)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.coneResoluInput = QtWidgets.QLineEdit(createCone)
        self.coneResoluInput.setObjectName("coneResoluInput")
        self.gridLayout.addWidget(self.coneResoluInput, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(createCone)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(createCone)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_8 = QtWidgets.QLabel(createCone)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label = QtWidgets.QLabel(createCone)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.coneRadiusInput = QtWidgets.QLineEdit(createCone)
        self.coneRadiusInput.setObjectName("coneRadiusInput")
        self.verticalLayout_2.addWidget(self.coneRadiusInput)
        self.coneHeightInput = QtWidgets.QLineEdit(createCone)
        self.coneHeightInput.setObjectName("coneHeightInput")
        self.verticalLayout_2.addWidget(self.coneHeightInput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.coneDirectXInput = QtWidgets.QLineEdit(createCone)
        self.coneDirectXInput.setObjectName("coneDirectXInput")
        self.horizontalLayout_2.addWidget(self.coneDirectXInput)
        self.coneDirectYInput = QtWidgets.QLineEdit(createCone)
        self.coneDirectYInput.setObjectName("coneDirectYInput")
        self.horizontalLayout_2.addWidget(self.coneDirectYInput)
        self.coneDirectZInpt = QtWidgets.QLineEdit(createCone)
        self.coneDirectZInpt.setObjectName("coneDirectZInpt")
        self.horizontalLayout_2.addWidget(self.coneDirectZInpt)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coneCenterZInput = QtWidgets.QLineEdit(createCone)
        self.coneCenterZInput.setObjectName("coneCenterZInput")
        self.horizontalLayout.addWidget(self.coneCenterZInput)
        self.coneCenterXInput = QtWidgets.QLineEdit(createCone)
        self.coneCenterXInput.setObjectName("coneCenterXInput")
        self.horizontalLayout.addWidget(self.coneCenterXInput)
        self.coneCenterYInput = QtWidgets.QLineEdit(createCone)
        self.coneCenterYInput.setObjectName("coneCenterYInput")
        self.horizontalLayout.addWidget(self.coneCenterYInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.createConeBtn = QtWidgets.QPushButton(createCone)
        self.createConeBtn.setObjectName("createConeBtn")
        self.horizontalLayout_3.addWidget(self.createConeBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(createCone)
        QtCore.QMetaObject.connectSlotsByName(createCone)

    def retranslateUi(self, createCone):
        _translate = QtCore.QCoreApplication.translate
        createCone.setWindowTitle(_translate("createCone", "Form"))
        self.label_3.setText(_translate("createCone", "Name"))
        self.label_5.setText(_translate("createCone", "Color"))
        self.coneNameInput.setText(_translate("createCone", "Cone_1"))
        self.coneColorCombox.setItemText(0, _translate("createCone", "blue"))
        self.coneColorCombox.setItemText(1, _translate("createCone", "darkBlue"))
        self.coneColorCombox.setItemText(2, _translate("createCone", "gray"))
        self.coneColorCombox.setItemText(3, _translate("createCone", "darkGray"))
        self.coneColorCombox.setItemText(4, _translate("createCone", "lightGray"))
        self.coneColorCombox.setItemText(5, _translate("createCone", "green"))
        self.coneColorCombox.setItemText(6, _translate("createCone", "darkGreen"))
        self.coneColorCombox.setItemText(7, _translate("createCone", "cyan"))
        self.coneColorCombox.setItemText(8, _translate("createCone", "darkCyan"))
        self.coneColorCombox.setItemText(9, _translate("createCone", "red"))
        self.coneColorCombox.setItemText(10, _translate("createCone", "darkRed"))
        self.coneColorCombox.setItemText(11, _translate("createCone", "magenta"))
        self.coneColorCombox.setItemText(12, _translate("createCone", "darkMagenta"))
        self.coneColorCombox.setItemText(13, _translate("createCone", "white"))
        self.coneColorCombox.setItemText(14, _translate("createCone", "black"))
        self.coneColorCombox.setItemText(15, _translate("createCone", "PICK"))
        self.label_6.setText(_translate("createCone", "Resolution"))
        self.coneResoluInput.setText(_translate("createCone", "10"))
        self.label_2.setText(_translate("createCone", "Radius"))
        self.label_4.setText(_translate("createCone", "Height"))
        self.label_8.setText(_translate("createCone", "Direction"))
        self.label.setText(_translate("createCone", "Center"))
        self.coneRadiusInput.setText(_translate("createCone", "1"))
        self.coneHeightInput.setText(_translate("createCone", "1"))
        self.coneDirectXInput.setText(_translate("createCone", "0"))
        self.coneDirectYInput.setText(_translate("createCone", "0"))
        self.coneDirectZInpt.setText(_translate("createCone", "1"))
        self.coneCenterZInput.setText(_translate("createCone", "0"))
        self.coneCenterXInput.setText(_translate("createCone", "0"))
        self.coneCenterYInput.setText(_translate("createCone", "0"))
        self.createConeBtn.setText(_translate("createCone", "Create"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createCone = QtWidgets.QWidget()
    ui = Ui_createCone()
    ui.setupUi(createCone)
    createCone.show()
    sys.exit(app.exec_())