# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Shaohui/OpenFoam/scripts/PyQtVTK/Ui_Files/Ui_layerMesh.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(302, 600)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setObjectName("label_18")
        self.verticalLayout.addWidget(self.label_18)
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setObjectName("label_22")
        self.verticalLayout.addWidget(self.label_22)
        self.label_19 = QtWidgets.QLabel(Form)
        self.label_19.setObjectName("label_19")
        self.verticalLayout.addWidget(self.label_19)
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)
        self.label_20 = QtWidgets.QLabel(Form)
        self.label_20.setObjectName("label_20")
        self.verticalLayout.addWidget(self.label_20)
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setObjectName("label_23")
        self.verticalLayout.addWidget(self.label_23)
        self.label_24 = QtWidgets.QLabel(Form)
        self.label_24.setObjectName("label_24")
        self.verticalLayout.addWidget(self.label_24)
        self.label_25 = QtWidgets.QLabel(Form)
        self.label_25.setObjectName("label_25")
        self.verticalLayout.addWidget(self.label_25)
        self.label_26 = QtWidgets.QLabel(Form)
        self.label_26.setObjectName("label_26")
        self.verticalLayout.addWidget(self.label_26)
        self.label_27 = QtWidgets.QLabel(Form)
        self.label_27.setObjectName("label_27")
        self.verticalLayout.addWidget(self.label_27)
        self.label_28 = QtWidgets.QLabel(Form)
        self.label_28.setObjectName("label_28")
        self.verticalLayout.addWidget(self.label_28)
        self.label_29 = QtWidgets.QLabel(Form)
        self.label_29.setObjectName("label_29")
        self.verticalLayout.addWidget(self.label_29)
        self.label_30 = QtWidgets.QLabel(Form)
        self.label_30.setObjectName("label_30")
        self.verticalLayout.addWidget(self.label_30)
        self.label_31 = QtWidgets.QLabel(Form)
        self.label_31.setObjectName("label_31")
        self.verticalLayout.addWidget(self.label_31)
        self.label_32 = QtWidgets.QLabel(Form)
        self.label_32.setObjectName("label_32")
        self.verticalLayout.addWidget(self.label_32)
        self.label_33 = QtWidgets.QLabel(Form)
        self.label_33.setObjectName("label_33")
        self.verticalLayout.addWidget(self.label_33)
        self.label_34 = QtWidgets.QLabel(Form)
        self.label_34.setObjectName("label_34")
        self.verticalLayout.addWidget(self.label_34)
        self.label_35 = QtWidgets.QLabel(Form)
        self.label_35.setObjectName("label_35")
        self.verticalLayout.addWidget(self.label_35)
        self.label_36 = QtWidgets.QLabel(Form)
        self.label_36.setObjectName("label_36")
        self.verticalLayout.addWidget(self.label_36)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_37 = QtWidgets.QLabel(Form)
        self.label_37.setObjectName("label_37")
        self.verticalLayout.addWidget(self.label_37)
        self.label_38 = QtWidgets.QLabel(Form)
        self.label_38.setObjectName("label_38")
        self.verticalLayout.addWidget(self.label_38)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.relaSizeChecBox = QtWidgets.QCheckBox(Form)
        self.relaSizeChecBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.relaSizeChecBox.setText("")
        self.relaSizeChecBox.setObjectName("relaSizeChecBox")
        self.verticalLayout_2.addWidget(self.relaSizeChecBox)
        self.layerThickCtrlCombox = QtWidgets.QComboBox(Form)
        self.layerThickCtrlCombox.setObjectName("layerThickCtrlCombox")
        self.layerThickCtrlCombox.addItem("")
        self.layerThickCtrlCombox.addItem("")
        self.verticalLayout_2.addWidget(self.layerThickCtrlCombox)
        self.totalThickCtrlCombox = QtWidgets.QComboBox(Form)
        self.totalThickCtrlCombox.setObjectName("totalThickCtrlCombox")
        self.totalThickCtrlCombox.addItem("")
        self.totalThickCtrlCombox.addItem("")
        self.verticalLayout_2.addWidget(self.totalThickCtrlCombox)
        self.defauExpanRatioInput = QtWidgets.QLineEdit(Form)
        self.defauExpanRatioInput.setObjectName("defauExpanRatioInput")
        self.verticalLayout_2.addWidget(self.defauExpanRatioInput)
        self.defauTotalThickInput = QtWidgets.QLineEdit(Form)
        self.defauTotalThickInput.setObjectName("defauTotalThickInput")
        self.verticalLayout_2.addWidget(self.defauTotalThickInput)
        self.defau1stLayerThickInput = QtWidgets.QLineEdit(Form)
        self.defau1stLayerThickInput.setObjectName("defau1stLayerThickInput")
        self.verticalLayout_2.addWidget(self.defau1stLayerThickInput)
        self.defauFinalLayerThickInput = QtWidgets.QLineEdit(Form)
        self.defauFinalLayerThickInput.setObjectName("defauFinalLayerThickInput")
        self.verticalLayout_2.addWidget(self.defauFinalLayerThickInput)
        self.minOverallThickInput = QtWidgets.QLineEdit(Form)
        self.minOverallThickInput.setObjectName("minOverallThickInput")
        self.verticalLayout_2.addWidget(self.minOverallThickInput)
        self.featureAngInput = QtWidgets.QLineEdit(Form)
        self.featureAngInput.setObjectName("featureAngInput")
        self.verticalLayout_2.addWidget(self.featureAngInput)
        self.maxFaceThickRatioInput = QtWidgets.QLineEdit(Form)
        self.maxFaceThickRatioInput.setObjectName("maxFaceThickRatioInput")
        self.verticalLayout_2.addWidget(self.maxFaceThickRatioInput)
        self.surfSmoothIterSpix = QtWidgets.QSpinBox(Form)
        self.surfSmoothIterSpix.setProperty("value", 5)
        self.surfSmoothIterSpix.setObjectName("surfSmoothIterSpix")
        self.verticalLayout_2.addWidget(self.surfSmoothIterSpix)
        self.minMediAxisAngSpix = QtWidgets.QSpinBox(Form)
        self.minMediAxisAngSpix.setProperty("value", 10)
        self.minMediAxisAngSpix.setObjectName("minMediAxisAngSpix")
        self.verticalLayout_2.addWidget(self.minMediAxisAngSpix)
        self.maxThick2MediRatioInput = QtWidgets.QLineEdit(Form)
        self.maxThick2MediRatioInput.setObjectName("maxThick2MediRatioInput")
        self.verticalLayout_2.addWidget(self.maxThick2MediRatioInput)
        self.interSmoothIterInput = QtWidgets.QLineEdit(Form)
        self.interSmoothIterInput.setObjectName("interSmoothIterInput")
        self.verticalLayout_2.addWidget(self.interSmoothIterInput)
        self.meshDispIterSpix = QtWidgets.QSpinBox(Form)
        self.meshDispIterSpix.setProperty("value", 3)
        self.meshDispIterSpix.setObjectName("meshDispIterSpix")
        self.verticalLayout_2.addWidget(self.meshDispIterSpix)
        self.SlipFeatureAngSpix = QtWidgets.QSpinBox(Form)
        self.SlipFeatureAngSpix.setMaximum(1000)
        self.SlipFeatureAngSpix.setProperty("value", 100)
        self.SlipFeatureAngSpix.setObjectName("SlipFeatureAngSpix")
        self.verticalLayout_2.addWidget(self.SlipFeatureAngSpix)
        self.relexaIterInput = QtWidgets.QLineEdit(Form)
        self.relexaIterInput.setObjectName("relexaIterInput")
        self.verticalLayout_2.addWidget(self.relexaIterInput)
        self.buffCellNoExtruSpix = QtWidgets.QSpinBox(Form)
        self.buffCellNoExtruSpix.setProperty("value", 5)
        self.buffCellNoExtruSpix.setObjectName("buffCellNoExtruSpix")
        self.verticalLayout_2.addWidget(self.buffCellNoExtruSpix)
        self.layerAdditionIterSpix = QtWidgets.QSpinBox(Form)
        self.layerAdditionIterSpix.setObjectName("layerAdditionIterSpix")
        self.verticalLayout_2.addWidget(self.layerAdditionIterSpix)
        self.relexaIterSpix = QtWidgets.QSpinBox(Form)
        self.relexaIterSpix.setProperty("value", 50)
        self.relexaIterSpix.setObjectName("relexaIterSpix")
        self.verticalLayout_2.addWidget(self.relexaIterSpix)
        self.detecExtruIslaInput = QtWidgets.QCheckBox(Form)
        self.detecExtruIslaInput.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.detecExtruIslaInput.setText("")
        self.detecExtruIslaInput.setObjectName("detecExtruIslaInput")
        self.verticalLayout_2.addWidget(self.detecExtruIslaInput)
        self.noGrowLayersSpix = QtWidgets.QSpinBox(Form)
        self.noGrowLayersSpix.setProperty("value", 50)
        self.noGrowLayersSpix.setObjectName("noGrowLayersSpix")
        self.verticalLayout_2.addWidget(self.noGrowLayersSpix)
        self.shrinkerCombox = QtWidgets.QComboBox(Form)
        self.shrinkerCombox.setObjectName("shrinkerCombox")
        self.shrinkerCombox.addItem("")
        self.shrinkerCombox.addItem("")
        self.verticalLayout_2.addWidget(self.shrinkerCombox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Relative Sizes"))
        self.label_18.setText(_translate("Form", "Layer Thickness Control"))
        self.label_22.setText(_translate("Form", "Total Thickness Control"))
        self.label_19.setText(_translate("Form", "Default Expansion Ratio"))
        self.label_21.setText(_translate("Form", "Default Total Thickness"))
        self.label_20.setText(_translate("Form", "Default First Layer Thickness"))
        self.label_23.setText(_translate("Form", "Default Final Layer Thickness"))
        self.label_24.setText(_translate("Form", "Minimum Overall Thickness"))
        self.label_25.setText(_translate("Form", "Feature Angle"))
        self.label_26.setText(_translate("Form", "Max Face Thickness Ratio"))
        self.label_27.setText(_translate("Form", "Surface Smoothing Iterations"))
        self.label_28.setText(_translate("Form", "Min Medial Axis Angle"))
        self.label_29.setText(_translate("Form", "Max Thickness To Medial Ratio"))
        self.label_30.setText(_translate("Form", "Interior Smoothign Iterations"))
        self.label_31.setText(_translate("Form", "Mesh Displacement Iteration"))
        self.label_32.setText(_translate("Form", "Slip Feature Angle"))
        self.label_33.setText(_translate("Form", "Relexation Iterations"))
        self.label_34.setText(_translate("Form", "Buffer Cells No Extrude"))
        self.label_35.setText(_translate("Form", "Layer Addition Iterations"))
        self.label_36.setText(_translate("Form", "Relaxed Iterations"))
        self.label_2.setText(_translate("Form", "Detect Extrusion Island"))
        self.label_37.setText(_translate("Form", "No Grow Layers"))
        self.label_38.setText(_translate("Form", "Shrinker"))
        self.layerThickCtrlCombox.setItemText(0, _translate("Form", "First Layer Thickness"))
        self.layerThickCtrlCombox.setItemText(1, _translate("Form", "Final Layer Thickness"))
        self.totalThickCtrlCombox.setItemText(0, _translate("Form", "Expansion Ratio"))
        self.totalThickCtrlCombox.setItemText(1, _translate("Form", "Total Thickness"))
        self.defauExpanRatioInput.setText(_translate("Form", "1.25"))
        self.defauTotalThickInput.setText(_translate("Form", "0.5"))
        self.defau1stLayerThickInput.setText(_translate("Form", "0.2"))
        self.defauFinalLayerThickInput.setText(_translate("Form", "0.3"))
        self.minOverallThickInput.setText(_translate("Form", "0.1"))
        self.featureAngInput.setText(_translate("Form", "180"))
        self.maxFaceThickRatioInput.setText(_translate("Form", "0.5"))
        self.maxThick2MediRatioInput.setText(_translate("Form", "90"))
        self.interSmoothIterInput.setText(_translate("Form", "0.5"))
        self.relexaIterInput.setText(_translate("Form", "30"))
        self.shrinkerCombox.setItemText(0, _translate("Form", "Medial Axis"))
        self.shrinkerCombox.setItemText(1, _translate("Form", "Laplacian"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
