# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createBox.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_createBox(object):
    def setupUi(self, createBox):
        createBox.setObjectName("createBox")
        createBox.resize(214, 155)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(createBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(createBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(createBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.BoxName = QtWidgets.QLineEdit(createBox)
        self.BoxName.setObjectName("BoxName")
        self.gridLayout.addWidget(self.BoxName, 0, 1, 1, 1)
        self.BoxColorComboBox = QtWidgets.QComboBox(createBox)
        self.BoxColorComboBox.setObjectName("BoxColorComboBox")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.BoxColorComboBox.addItem("")
        self.gridLayout.addWidget(self.BoxColorComboBox, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(createBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(createBox)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.boxCenterXInput = QtWidgets.QLineEdit(createBox)
        self.boxCenterXInput.setObjectName("boxCenterXInput")
        self.horizontalLayout_2.addWidget(self.boxCenterXInput)
        self.boxCenterYInput = QtWidgets.QLineEdit(createBox)
        self.boxCenterYInput.setObjectName("boxCenterYInput")
        self.horizontalLayout_2.addWidget(self.boxCenterYInput)
        self.boxCenterZInput = QtWidgets.QLineEdit(createBox)
        self.boxCenterZInput.setObjectName("boxCenterZInput")
        self.horizontalLayout_2.addWidget(self.boxCenterZInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.boxLengthXInput = QtWidgets.QLineEdit(createBox)
        self.boxLengthXInput.setObjectName("boxLengthXInput")
        self.horizontalLayout.addWidget(self.boxLengthXInput)
        self.boxLengthYInput = QtWidgets.QLineEdit(createBox)
        self.boxLengthYInput.setObjectName("boxLengthYInput")
        self.horizontalLayout.addWidget(self.boxLengthYInput)
        self.boxLengthZInput = QtWidgets.QLineEdit(createBox)
        self.boxLengthZInput.setObjectName("boxLengthZInput")
        self.horizontalLayout.addWidget(self.boxLengthZInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.previewBoxBtn = QtWidgets.QPushButton(createBox)
        self.previewBoxBtn.setObjectName("previewBoxBtn")
        self.horizontalLayout_3.addWidget(self.previewBoxBtn)
        self.createBoxBtn = QtWidgets.QPushButton(createBox)
        self.createBoxBtn.setObjectName("createBoxBtn")
        self.horizontalLayout_3.addWidget(self.createBoxBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(createBox)
        QtCore.QMetaObject.connectSlotsByName(createBox)

    def retranslateUi(self, createBox):
        _translate = QtCore.QCoreApplication.translate
        createBox.setWindowTitle(_translate("createBox", "Form"))
        self.label_3.setText(_translate("createBox", "Name"))
        self.label_5.setText(_translate("createBox", "Color"))
        self.BoxName.setText(_translate("createBox", "Box_1"))
        self.BoxColorComboBox.setItemText(0, _translate("createBox", "blue"))
        self.BoxColorComboBox.setItemText(1, _translate("createBox", "darkBlue"))
        self.BoxColorComboBox.setItemText(2, _translate("createBox", "gray"))
        self.BoxColorComboBox.setItemText(3, _translate("createBox", "darkGray"))
        self.BoxColorComboBox.setItemText(4, _translate("createBox", "lightGray"))
        self.BoxColorComboBox.setItemText(5, _translate("createBox", "green"))
        self.BoxColorComboBox.setItemText(6, _translate("createBox", "darkGreen"))
        self.BoxColorComboBox.setItemText(7, _translate("createBox", "cyan"))
        self.BoxColorComboBox.setItemText(8, _translate("createBox", "darkCyan"))
        self.BoxColorComboBox.setItemText(9, _translate("createBox", "red"))
        self.BoxColorComboBox.setItemText(10, _translate("createBox", "darkRed"))
        self.BoxColorComboBox.setItemText(11, _translate("createBox", "magenta"))
        self.BoxColorComboBox.setItemText(12, _translate("createBox", "darkMagenta"))
        self.BoxColorComboBox.setItemText(13, _translate("createBox", "white"))
        self.BoxColorComboBox.setItemText(14, _translate("createBox", "black"))
        self.BoxColorComboBox.setItemText(15, _translate("createBox", "PICK"))
        self.label_2.setText(_translate("createBox", "Size"))
        self.label.setText(_translate("createBox", "Center"))
        self.boxCenterXInput.setText(_translate("createBox", "1"))
        self.boxCenterYInput.setText(_translate("createBox", "1"))
        self.boxCenterZInput.setText(_translate("createBox", "1"))
        self.boxLengthXInput.setText(_translate("createBox", "0"))
        self.boxLengthYInput.setText(_translate("createBox", "0"))
        self.boxLengthZInpt.setText(_translate("createBox", "0"))
        self.previewBoxBtn.setText(_translate("createBox", "Preview"))
        self.createBoxBtn.setText(_translate("createBox", "Create"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createBox = QtWidgets.QWidget()
    ui = Ui_createBox()
    ui.setupUi(createBox)
    createBox.show()
    sys.exit(app.exec_())
