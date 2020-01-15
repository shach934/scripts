from PyQt5 import QtCore, QtWidgets
from Panel_Tree import ModelTree
from createBox import *
from createCone import *
from createCylinder import *
from createSphere import *

class Property(object):
    
    def __init__(self, domain):
        super().__init__()
    
        self.propertyBox = QtWidgets.QFrame(domain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.propertyBox.setSizePolicy(sizePolicy)

        self.propertyBox.show()

    def setViewItem(self, clickedItem):
        self.currentItem = clickedItem
        self.propertyView()

    def relateTo(self, ModelTree):
        self.ModelTree = ModelTree

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

    def propertyView(self):
            
        if self.currentItem == "Box":
            self.tempBox = createBox()
            h_la = QtWidgets.QHBoxLayout()
            h_la.addWidget(self.newBoxPanel)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(h_la)

            for inputLine in (self.tempBox.boxLengthXInput, self.tempBox.boxLengthYInput, self.tempBox.boxLengthZInput, \
                             self.tempBox.boxCenterXInput, self.tempBox.boxCenterYInput, self.tempBox.boxCenterZInput):
                inputLine.textChanged['QString'].connect(self.tempBox.drawBox)

            self.tempBox.BoxColorComboBox.currentTextChanged.connect(self.tempBox.drawBox)
            self.tempBox.createBoxBtn.clicked.connect(self.tempBox.addBox)

        elif self.currentItem == "Sphere":
            self.tempSphere = createSphere()
            h_la = QtWidgets.QHBoxLayout()
            h_la.addWidget(self.tempSphere)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(h_la)
            for inputBox in (self.tempSphere.sphereRadiusInput, self.tempSphere.sphereCenterXInput, self.tempSphere.sphereCenterYInput,self.tempSphere.sphereCenterZInput, self.tempSphere.sphereResoluAlphaInput, self.tempSphere.sphereResoluThetaInput, self.tempSphere.sphereResoluDeltaInput):
                inputBox.textChanged['QString'].connect(self.tempSphere.drawSphere)

            self.tempSphere.sphereColorComboBox.currentTextChanged.connect(self.tempSphere.drawSphere)
            self.createSphereBtn.clicked.connect(self.tempSphere.addSphere)

        elif self.currentItem == "Cylinder":
            self.tempCylinder = createCylinder()
            h_la = QtWidgets.QHBoxLayout()
            h_la.addWidget(self.tempCylinder)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(h_la)
            for inputBox in (self.tempCylinder.cylinderRadiusInput, self.tempCylinder.cylinderHeightInput, self.tempCylinder.cylinderCenterXInput, self.tempCylinder.cylinderCenterYInput, self.tempCylinder.cylinderCenterZInput, self.tempCylinder.cylinderResoluInput):
                inputBox.textChanged['QString'].connect(self.tempCylinder.drawCylinder2Window)

            self.tempCylinder.cylinderColorComboBox.currentTextChanged.connect(self.tempCylinder.drawCylinder2Window)
            self.createCylinderBtn.clicked.connect(self.tempCylinder.addCylinder)
            
        elif self.currentItem == "Cone":
            self.tempCone = createCone()
            h_la = QtWidgets.QHBoxLayout()
            h_la.addWidget(self.tempCone)
            self.clearLayout(self.propertyBox.layout())
            self.propertyBox.setLayout(h_la)
            for inputBox in (self.tempCone.coneRadiusInput, self.tempCone.coneCenterXInput, self.tempCone.coneCenterYInput,self.tempCone.coneCenterZInput, self.tempCone.coneHeightInput, self.tempCone.coneResoluInput):
                inputBox.textChanged['QString'].connect(self.tempCone.drawCone)

            self.tempCone.coneColorComboBox.currentTextChanged.connect(self.tempCone.drawCone)
            self.createConeBtn.clicked.connect(self.tempCone.addCone)

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

    def MRFProperties(self):
        row, col = 8, 2
        #TODO MRF also need a region input indicate which region the cellZone belongs to. Also, configed MRF need to appare in the tree. 
        self.properties.setColumnCount(col)
        self.properties.setRowCount(row)
        self.properties.show()

        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        MRFNameLabel = QtWidgets.QLabel("MRF Name")        
        self.properties.setCellWidget(0, 0, MRFNameLabel)
        MRFNameInput = QtWidgets.QLineEdit()
        MRFNameInput.setText("MRF_" + str(self.MRFCount)) 
        self.MRFCount += 1
        self.properties.setCellWidget(0, 1, MRFNameInput)

        MRFCellZone = QtWidgets.QLabel("cellZone")        
        self.properties.setCellWidget(1, 0, MRFCellZone)
        cellZoneOp = ["cellZone1", "cellZone2"]
        cellZoneOpComboBox = QtWidgets.QComboBox()
        cellZoneOpComboBox.addItems(cellZoneOp)
        self.properties.setCellWidget(1, 1, cellZoneOpComboBox)
        
        MRFactiveLabel = QtWidgets.QLabel("MRF")        
        self.properties.setCellWidget(2, 0, MRFactiveLabel)
        MRFactiveOp = ["on", "off"]
        MRFactiveComboBox = QtWidgets.QComboBox()
        MRFactiveComboBox.addItems(MRFactiveOp)
        self.properties.setCellWidget(2, 1, MRFactiveComboBox)

        MRFnonRotatLabel = QtWidgets.QLabel("nonRotatingPatches")
        self.properties.setCellWidget(3, 0, MRFnonRotatLabel)
        MRFnonRotatPatchOp = self.patches
        MRFnonRotatPatchCombox = QtWidgets.QComboBox()
        MRFnonRotatPatchCombox.addItems(MRFnonRotatPatchOp)
        self.properties.setCellWidget(3, 1, MRFnonRotatPatchCombox)

        MRForiginLabel = QtWidgets.QLabel("origin")
        self.properties.setCellWidget(4, 0, MRForiginLabel)
        MRForiginInput = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(4, 1, MRForiginInput)

        MRFaxisLabel = QtWidgets.QLabel("axis")
        self.properties.setCellWidget(5, 0, MRFaxisLabel)
        axisOp = ["x", "y", "z"]
        MRFaxisCombobox = QtWidgets.QComboBox()
        MRFaxisCombobox.addItems(axisOp)
        self.properties.setCellWidget(5, 1, MRFaxisCombobox)

        MRFomegaLabel = QtWidgets.QLabel("omega")
        self.properties.setCellWidget(6, 0, MRFomegaLabel)
        MRFomegaInput = QtWidgets.QLineEdit()
        MRFomegaInput.setPlaceholderText("rpm")
        self.properties.setCellWidget(6, 1, MRFomegaInput)

        addMRFButt = QtWidgets.QPushButton('Add/Update')
        self.properties.setCellWidget(7, 0, addMRFButt)
        DeleMRFButt = QtWidgets.QPushButton("Delete")
        self.properties.setCellWidget(7, 1, DeleMRFButt)

    def DynaMeshProperties(self):        
        self.properties.setRowCount(8)
        self.properties.setColumnCount(2)
        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        DynaMeshFvLabel = QtWidgets.QLabel("dynamicFvMesh")
        self.properties.setCellWidget(0, 0, DynaMeshFvLabel)
        DynaMeshFvCombox = QtWidgets.QComboBox()
        DynaMeshFvOp = ["solidBodyMotionFvMesh", "dynamicMotionSolverFvMesh", "dynamicRefineFvMesh", "staticFvMesh"]
        DynaMeshFvCombox.addItems(DynaMeshFvOp)
        self.properties.setCellWidget(0, 1, DynaMeshFvCombox)

        DynaMeshSolver = QtWidgets.QLabel("Motion Solver")
        self.properties.setCellWidget(1, 0, DynaMeshSolver)
        DynaMeshSolverCombox = QtWidgets.QComboBox()
        DynaMeshSolverOp = ["solidBody", "sixDoFRigidBodyMotion", ]
        DynaMeshSolverCombox.addItems(DynaMeshSolverOp)
        self.properties.setCellWidget(1, 1, DynaMeshSolverCombox)

        DynaMeshFuncLabel = QtWidgets.QLabel("Motion function")
        self.properties.setCellWidget(2, 0, DynaMeshFuncLabel)
        motionFuncOp = ["rotatingMotion"]
        motionFuncCombox = QtWidgets.QComboBox()
        motionFuncCombox.addItems(motionFuncOp)
        self.properties.setCellWidget(2, 1, motionFuncCombox)

        DynaMeshCellZone = QtWidgets.QLabel("cellZone")        
        self.properties.setCellWidget(3, 0, DynaMeshCellZone)
        cellZoneOp = ["cellZone1", "cellZone2"]
        cellZoneOpComboBox = QtWidgets.QComboBox()
        cellZoneOpComboBox.addItems(cellZoneOp)
        self.properties.setCellWidget(3, 1, cellZoneOpComboBox)

        DynaMeshoriginLabel = QtWidgets.QLabel("origin")
        self.properties.setCellWidget(4, 0, DynaMeshoriginLabel)
        DynaMeshoriginInput = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(4, 1, DynaMeshoriginInput)

        DynaMeshaxisLabel = QtWidgets.QLabel("axis")
        self.properties.setCellWidget(5, 0, DynaMeshaxisLabel)
        axisOp = ["x", "y", "z"]
        DynaMeshaxisCombobox = QtWidgets.QComboBox()
        DynaMeshaxisCombobox.addItems(axisOp)
        self.properties.setCellWidget(5, 1, DynaMeshaxisCombobox)

        DynaMeshomegaLabel = QtWidgets.QLabel("omega")
        self.properties.setCellWidget(6, 0, DynaMeshomegaLabel)
        DynaMeshomegaInput = QtWidgets.QLineEdit()
        DynaMeshomegaInput.setPlaceholderText("rpm")
        self.properties.setCellWidget(6, 1, DynaMeshomegaInput)

        addDynaMeshButt = QtWidgets.QPushButton('Add/Update')
        self.properties.setCellWidget(7, 0, addDynaMeshButt)
        DeleDynaMeshButt = QtWidgets.QPushButton("Delete")
        self.properties.setCellWidget(7, 1, DeleDynaMeshButt)

    def MultiphaseProperties(self):
        self.properties.setRowCount(6)
        self.properties.setColumnCount(2)
        self.properties.show()
        
        self.properties.horizontalHeader().hide()
        self.properties.verticalHeader().hide()

        fieldNameLabel = QtWidgets.QLabel("Field Values")
        self.properties.setCellWidget(0, 0, fieldNameLabel)
        fieldNameInput = QtWidgets.QLineEdit("Alpha.Water")
        self.properties.setCellWidget(0, 1, fieldNameInput)

        defaultValueLabel = QtWidgets.QLabel("Default Value")
        self.properties.setCellWidget(1, 0, defaultValueLabel)
        defaultValueInput = QtWidgets.QLineEdit("1")
        self.properties.setCellWidget(1, 1, defaultValueInput)

        fieldRegionLabel = QtWidgets.QLabel("Field Region")
        self.properties.setCellWidget(2, 0, fieldRegionLabel)
        fieldRegionCombox = QtWidgets.QComboBox()
        fieldRegionOp = ["boxToCell", "cylinderToCell", "sphereToCell", "cylinderAnnulusToCell", "rotatedBoxToCell", "zoneToCell"]
        fieldRegionCombox.addItems(fieldRegionOp)
        self.properties.setCellWidget(2, 1, fieldRegionCombox)
        
        boxPoint1Label = QtWidgets.QLabel("box point1")
        self.properties.setCellWidget(3, 0, boxPoint1Label)
        boxPoint1Input = QtWidgets.QLineEdit("0, 0, 0")
        self.properties.setCellWidget(3, 1, boxPoint1Input)

        boxPoint2Label = QtWidgets.QLabel("box point2")
        self.properties.setCellWidget(4, 0, boxPoint2Label)
        boxPoint2Input = QtWidgets.QLineEdit("10, 10, 10")
        self.properties.setCellWidget(4, 1, boxPoint2Input)

        fieldValueLabel = QtWidgets.QLabel("Field Value")
        self.properties.setCellWidget(5, 0, fieldValueLabel)
        fieldValueInput = QtWidgets.QLineEdit("0")
        self.properties.setCellWidget(5, 1, fieldValueInput)
        
    def RadiationProperties(self):

        self.properties.setRowCount(12)
        self.properties.setColumnCount(2)
        self.properties.verticalHeader().hide()
        self.properties.horizontalHeader().hide()

        radiatSwitchLabel = QtWidgets.QLabel("Ratiation")
        self.properties.setCellWidget(0, 0, radiatSwitchLabel)
        self.radiationSwitchCombox = QtWidgets.QComboBox()
        self.radiationSwitchCombox.addItems(["on", "off"])
        self.properties.setCellWidget(0, 1, self.radiationSwitchCombox)

        radiatModelLabel = QtWidgets.QLabel("Ratiation Model")
        self.properties.setCellWidget(1, 0, radiatModelLabel)
        self.radiatModelCombox = QtWidgets.QComboBox()
        radiatModelOp = ["fvDOM", "P1", "S2S"]
        self.radiatModelCombox = QtWidgets.QComboBox()
        self.radiatModelCombox.addItems(radiatModelOp)
        self.properties.setCellWidget(1, 1, self.radiatModelCombox)

        nPhiLabel = QtWidgets.QLabel("nPhi")
        self.properties.setCellWidget(2, 0, nPhiLabel)
        self.nPhiInput = QtWidgets.QSpinBox()   
        self.nPhiInput.setValue(2)
        self.properties.setCellWidget(2, 1, self.nPhiInput)

        nThetaLabel = QtWidgets.QLabel("nTheta")
        self.properties.setCellWidget(3, 0, nThetaLabel)
        self.nThetaInput = QtWidgets.QSpinBox()
        self.nThetaInput.setValue(4)
        self.properties.setCellWidget(3, 1, self.nThetaInput)

        radmaxIterLabel = QtWidgets.QLabel("maxIter")
        self.properties.setCellWidget(4, 0, radmaxIterLabel)
        self.radmaxIterInput = QtWidgets.QSpinBox()
        self.radmaxIterInput.setValue(5)
        self.properties.setCellWidget(4, 1, self.radmaxIterInput)

        radTolLabel = QtWidgets.QLabel("tolerance")
        self.properties.setCellWidget(5, 0, radTolLabel)
        self.radTolInput = QtWidgets.QLineEdit("1E-3")
        self.properties.setCellWidget(5, 1, self.radTolInput)

        radSolvFreqLabel = QtWidgets.QLabel("solve freq")
        self.properties.setCellWidget(6, 0, radSolvFreqLabel)
        self.radSolvFreqInput = QtWidgets.QSpinBox()
        self.properties.setCellWidget(6, 1, self.radSolvFreqInput)

        radAbsorpLabel = QtWidgets.QLabel("absorptivity")
        self.properties.setCellWidget(7, 0, radAbsorpLabel)
        self.radAbsorpInput = QtWidgets.QLineEdit("0.01")
        self.properties.setCellWidget(7, 1, self.radAbsorpInput)

        radEmissLabel = QtWidgets.QLabel("emissivity")
        self.properties.setCellWidget(8, 0, radEmissLabel)
        self.radEmissInput = QtWidgets.QLineEdit("0.01")
        self.properties.setCellWidget(8, 1, self.radEmissInput)

        radELabel = QtWidgets.QLabel("E")
        self.properties.setCellWidget(9, 0, radELabel)
        self.radEInput = QtWidgets.QLineEdit("0")
        self.properties.setCellWidget(9, 1, self.radEInput)

        radScattLabel = QtWidgets.QLabel("scatter model")
        self.properties.setCellWidget(10, 0, radScattLabel)
        self.radScattInput = QtWidgets.QComboBox()
        self.radScattInput.addItems(["none"])
        self.properties.setCellWidget(10, 1, self.radScattInput)

        radSootLabel = QtWidgets.QLabel("soot model")
        self.properties.setCellWidget(11, 0, radSootLabel)
        self.radSootInput = QtWidgets.QComboBox()
        self.radSootInput.addItems(["none"])
        self.properties.setCellWidget(11, 1, self.radSootInput)

    def HeatTransProperties(self):
        """
        type            heRhoThermo;
        mixture         pureMixture;
        transport       polynomial;
        thermo          hPolynomial;
        equationOfState icoPolynomial;
        specie          specie;
        energy          sensibleEnthalpy;
        """
        self.properties.setRowCount(10)
        self.properties.setColumnCount(2)
        self.properties.verticalHeader().hide()
        self.properties.horizontalHeader().hide()

        regionLabel = QtWidgets.QLabel("Region")
        self.properties.setCellWidget(0, 0, regionLabel)
        self.HeatTransRegionInput = QtWidgets.QComboBox()
        self.HeatTransRegionInput.addItems(list(self.regions.keys()))
        self.properties.setCellWidget(0, 1, self.HeatTransRegionInput)

        ThermoType = QtWidgets.QLabel("Thermo Type")
        self.properties.setCellWidget(1, 0, ThermoType)
        self.ThermoTypeInput = QtWidgets.QComboBox()
        ThermoTypeOp = ["hePsiThermo", "heRhoThermo", "heheuPsiThermo"]
        self.ThermoTypeInput.addItems(ThermoTypeOp)
        self.properties.setCellWidget(1, 1, self.ThermoTypeInput)

        ThermoMixLabel = QtWidgets.QLabel("Mixture")
        self.properties.setCellWidget(2, 0, ThermoMixLabel)
        self.ThermoMixInput = QtWidgets.QComboBox()
        ThermoMixOp = ["pureMixture", "reactingMixture", "homogeneousMixture", "inhomogeneousMixture", "veryInhomogeneousMixture"]
        self.ThermoMixInput.addItems(ThermoMixOp)
        self.properties.setCellWidget(2, 1, self.ThermoMixInput)
        
        ThermoTransportLabel = QtWidgets.QLabel("transport")
        self.properties.setCellWidget(3, 0, ThermoTransportLabel)
        self.ThermoTranspInput = QtWidgets.QComboBox()
        ThermoTranspOp = ["const", "sutherland", "polynomial", "logPolynomial"]
        self.ThermoTranspInput.addItems(ThermoTranspOp)
        self.properties.setCellWidget(3, 1, self.ThermoTranspInput)

        ThermoThermoLabel = QtWidgets.QLabel("thermo")
        self.properties.setCellWidget(4, 0, ThermoThermoLabel)   
        self.ThermoThermoInput = QtWidgets.QComboBox()
        ThermoThermoOp = ["hConst", "eConst", "janaf", "hPolynomial"]
        self.ThermoThermoInput.addItems(ThermoThermoOp)
        self.properties.setCellWidget(4, 1, self.ThermoThermoInput)

        ThermoEoSLabel = QtWidgets.QLabel("equationOfState")
        self.properties.setCellWidget(5, 0, ThermoEoSLabel)
        self.ThermoEOSInput = QtWidgets.QComboBox()
        ThermoEOSOp = ["rhoConst", "perfectGas", "incompressiblePerfectGas", "perfectFluid", "linear", "adiabaticPerfectFluid", "Boussinesq","PengRobinsonGas", "icoPolynomial"]
        self.ThermoEOSInput.addItems(ThermoEOSOp)
        self.properties.setCellWidget(5, 1, self.ThermoEOSInput)

        ThermoSpecieLabel = QtWidgets.QLabel("specie")
        self.properties.setCellWidget(6, 0, ThermoSpecieLabel)
        self.ThermoSpecieInput = QtWidgets.QComboBox()
        ThermoSpecieOp = ["specie", "thermodynamics", "transport"]
        self.ThermoSpecieInput.addItems(ThermoSpecieOp)
        self.properties.setCellWidget(6, 1, self.ThermoSpecieInput)

        ThermoEnergyLabel = QtWidgets.QLabel("energy")
        self.properties.setCellWidget(7, 0, ThermoEnergyLabel)
        self.ThermoEnergyInput = QtWidgets.QComboBox()
        ThermoEnergyOp = ["sensibleEnthalpy", "sensibleInternalEnergy", "absoluteEnthalpy"]
        self.ThermoEnergyInput.addItems(ThermoEnergyOp)
        self.properties.setCellWidget(7, 1, self.ThermoEnergyInput)

    def ddtProperties(self):
        self.properties.setColumnCount(2)
        self.properties.setRowCount(2)
        self.properties.verticalHeader().hide()
        self.properties.horizontalHeader().hide()

        ddtLabel = QtWidgets.QLabel("ddtSchemes")
        self.properties.setCellWidget(0, 0, ddtLabel)
        self.ddtInput = QtWidgets.QComboBox()
        ddtOp = ["steadyState", "Euler", "localEuler", "CrankNicholson \u03C8", "backward"]
        self.ddtInput.addItems(ddtOp)
        self.properties.setCellWidget(0, 1, self.ddtInput)

        gradLabel = QtWidgets.QLabel("grad")
        self.properties.setCellWidget(1, 0, gradLabel)
        self.gradInput = QtWidgets.QComboBox()
        gradOp = [""]