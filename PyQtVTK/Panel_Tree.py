
class Model_Tree(object):
    def __init__(self):
        super().__init__()
        
    def initTree(self):
        # self.item_0 is the head item of the tree. it text is the name of the model.
        regionProperties = self.foamConfig.GetRegionProperty()

        _translate = QtCore.QCoreApplication.translate

        self.pipLine.topLevelItem(0).setText(0, _translate("OpenFOAM", self.caseName))

        self.geoItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Geometry"])

        self.createGeoItem = QtWidgets.QTreeWidgetItem(self.geoItem, ["Create"])
        self.createBoxGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Box"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/box.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createBoxGeoItem.setIcon(0, icon)
        self.createCylGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Cylinder"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cylinder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createCylGeoItem.setIcon(0, icon)
        self.createSphGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Sphere"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/sphere.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createSphGeoItem.setIcon(0, icon)
        self.createConeGeoItem = QtWidgets.QTreeWidgetItem(self.createGeoItem, ["Cone"])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cone.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createConeGeoItem.setIcon(0, icon)

        self.importGeoItem = QtWidgets.QTreeWidgetItem(self.geoItem, ["Import"])


        self.meshItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Mesh"])

        self.meshGeoItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Geometry"])
        self.blockMeshItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["BlockMesh"])
        self.meshPointItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Point"])
        self.meshMeshItem = QtWidgets.QTreeWidgetItem(self.meshItem, ["Mesh"])


        self.phyItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Setup"])


        self.TurbItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Turbulence"])
        self.MRFItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["MRF"])
        self.DynaMeshItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Dynamic Mesh"])
        self.MultiPhaseItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Multiphase"])
        self.HeatTransItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Heat Transfer"])
        self.RadiatItem = QtWidgets.QTreeWidgetItem(self.phyItem, ["Radiation"])


        self.MatItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["Material"])

        self.viscoItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Viscosity"])
        self.DensiItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Density"])
        self.HeatConductItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Heat Conductivity"])
        self.SpeficHeatItem = QtWidgets.QTreeWidgetItem(self.MatItem, ["Specific Heat"])


        self.schemeItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvSchemes"])

        self.ddtItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["ddt"])
        self.gradItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["grad"])
        self.divItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["div"])
        self.lapItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["laplacian"])
        self.interporlItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["interpolation"])
        self.snGradItem = QtWidgets.QTreeWidgetItem(self.schemeItem, ["snGrad"])


        self.soluItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvSolution"])

        self.solverItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["solver"])
        self.resiItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["residual"])
        self.relaxItem = QtWidgets.QTreeWidgetItem(self.soluItem, ["Relaxation Factor"])


        self.optionItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["fvOption"])

        self.HeatSourceItem = QtWidgets.QTreeWidgetItem(self.optionItem, ["Heat Source"])
        self.TempLimitItem = QtWidgets.QTreeWidgetItem(self.optionItem, ["Temperature Limit"])

        self.ControlItem = QtWidgets.QTreeWidgetItem(self.pipLine.topLevelItem(0), ["ControlDict"])

        self.TimeControlItem = QtWidgets.QTreeWidgetItem(self.ControlItem, ["Time control"])
        self.PhyCOntrolItem = QtWidgets.QTreeWidgetItem(self.ControlItem, ["Physical control"])

        self.pipLine.currentItemChanged.connect(self.propertyView)
        self.pipLine.show()
        self.pipLine.expandAll()        