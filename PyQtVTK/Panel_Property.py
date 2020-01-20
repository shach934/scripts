from PyQt5 import QtCore, QtWidgets
from Panel_Tree import ModelTree
import sip
from createGeo import *
from Ui_blockMesh import Ui_blockMesh

class Property(object):
    
    def __init__(self, domain):
        super().__init__()
    
        self.propertyBox = QtWidgets.QFrame(domain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.propertyBox.setSizePolicy(sizePolicy)
        self.propertyBox.show()

    def setViewItem(self, clickedItem, previousClickedItem):
        self.currentItem = clickedItem
        self.propertyView()

    def relate2VTKWindow(self, Panel_VTK):
        self.vtkWindow = Panel_VTK

    def clearLayout(self, cur_lay):
        if cur_lay is not None:
            while cur_lay.count():
                item = cur_lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
            sip.delete(cur_lay)
# TODO: update the view window according to the last item. 
    def propertyView(self):
        if self.currentItem == "Box":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempBox = createBox(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempBox)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif self.currentItem == "Sphere":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempSphere = createSphere(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempSphere)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif self.currentItem == "Cylinder":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCylinder = createCylinder(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempCylinder)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif self.currentItem == "Cone":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.tempCone = createCone(self.vtkWindow)
            tempHboxLayout.addWidget(self.tempCone)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        elif self.currentItem == "blockMesh":
            tempHboxLayout = QtWidgets.QVBoxLayout()
            self.blockMesh = blockMesh(self.vtkWindow)
            tempHboxLayout.addWidget(self.blockMesh)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(tempHboxLayout)

        def TurbProperties(self):
            self.properties.setColumnCount(2)
            self.properties.setRowCount(2)
            self.properties.show()

            self.properties.horizontalHeader().hide()
            self.properties.verticalHeader().hide()

            regionLabel = QtWidgets.QLabel("Region")        
            self.properties.setCellWidget(0, 0, regionLabel)
            regions = list(self.regions.keys())
            self.regionComboBox = QtWidgets.QComboBox()
            self.regionComboBox.addItems(regions)
            self.properties.setCellWidget(0, 1, self.regionComboBox)

            simuTypeLabel = QtWidgets.QLabel("simulationType")        
            self.properties.setCellWidget(1, 0, simuTypeLabel)
            simuTypeOp = ["laminar", "RAS", "LES", "DES"]
            self.simuTypeComboBox = QtWidgets.QComboBox()
            self.simuTypeComboBox.addItems(simuTypeOp)
            self.properties.setCellWidget(1, 1, self.simuTypeComboBox)
            
            self.simuTypeComboBox.currentIndexChanged.connect(lambda: self.RASproperty(self.simuTypeComboBox.currentText()))

    def RASproperty(self, simuType):
        if simuType == "RAS":
            self.properties.setColumnCount(2)
            self.properties.setRowCount(5)

            RASModelLabel = QtWidgets.QLabel("RASModel")        
            self.properties.setCellWidget(2, 0, RASModelLabel)
            simuTypeOp = ["kEpsilon", "realizableKE", "RNGkEpsilon", "kOmemga", "kOmegaSST", "kOmegaSSTLM"]
            simuTypeComboBox = QtWidgets.QComboBox()
            simuTypeComboBox.addItems(simuTypeOp)
            self.properties.setCellWidget(2, 1, simuTypeComboBox)

            TurbSwitchLabel = QtWidgets.QLabel("Turbulence")        
            self.properties.setCellWidget(3, 0, TurbSwitchLabel)
            TurbSwitchOp = ["on", "off"]
            TurbSwitchOpComboBox = QtWidgets.QComboBox()
            TurbSwitchOpComboBox.addItems(TurbSwitchOp)
            self.properties.setCellWidget(3, 1, TurbSwitchOpComboBox)
            
            TurbCoeffLabel = QtWidgets.QLabel("printCoeffs")        
            self.properties.setCellWidget(4, 0, TurbCoeffLabel)
            TurbCoeffOp = ["on", "off"]
            TurbCoeffComboBox = QtWidgets.QComboBox()
            TurbCoeffComboBox.addItems(TurbCoeffOp)
            self.properties.setCellWidget(4, 1, TurbCoeffComboBox)

        elif simuType == "laminar":
            self.properties.setColumnCount(2)
            self.properties.setRowCount(1)  

