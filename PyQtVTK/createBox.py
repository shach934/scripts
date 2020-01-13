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
        createBox.resize(239, 129)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(createBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(createBox)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(createBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_5 = QtWidgets.QLabel(createBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
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
        self.boxLengthZInpt = QtWidgets.QLineEdit(createBox)
        self.boxLengthZInpt.setObjectName("boxLengthZInpt")
        self.horizontalLayout.addWidget(self.boxLengthZInpt)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.boxColorRInput = QtWidgets.QLineEdit(createBox)
        self.boxColorRInput.setObjectName("boxColorRInput")
        self.horizontalLayout_3.addWidget(self.boxColorRInput)
        self.boxColorGInput = QtWidgets.QLineEdit(createBox)
        self.boxColorGInput.setObjectName("boxColorGInput")
        self.horizontalLayout_3.addWidget(self.boxColorGInput)
        self.boxColorBInput = QtWidgets.QLineEdit(createBox)
        self.boxColorBInput.setObjectName("boxColorBInput")
        self.horizontalLayout_3.addWidget(self.boxColorBInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.pushButton = QtWidgets.QPushButton(createBox)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)

        self.retranslateUi(createBox)
        QtCore.QMetaObject.connectSlotsByName(createBox)

    def retranslateUi(self, createBox):
        _translate = QtCore.QCoreApplication.translate
        createBox.setWindowTitle(_translate("createBox", "Form"))
        self.label.setText(_translate("createBox", "Center"))
        self.label_2.setText(_translate("createBox", "Size"))
        self.label_5.setText(_translate("createBox", "Color"))
        self.boxCenterXInput.setText(_translate("createBox", "0"))
        self.boxCenterYInput.setText(_translate("createBox", "0"))
        self.boxCenterZInput.setText(_translate("createBox", "0"))
        self.boxLengthXInput.setText(_translate("createBox", "10"))
        self.boxLengthYInput.setText(_translate("createBox", "10"))
        self.boxLengthZInpt.setText(_translate("createBox", "10"))
        self.boxColorRInput.setText(_translate("createBox", "0"))
        self.boxColorGInput.setText(_translate("createBox", "0"))
        self.boxColorBInput.setText(_translate("createBox", "1"))
        self.pushButton.setText(_translate("createBox", "Create"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createBox = QtWidgets.QWidget()
    ui = Ui_createBox()
    ui.setupUi(createBox)
    createBox.show()
    sys.exit(app.exec_())
