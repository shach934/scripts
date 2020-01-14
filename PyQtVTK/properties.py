import Lib

__methods__ = [] # self is a DataStore
register_method = Lib.register_method(__methods__)

@register_method
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

@register_method
def propertyView(self, current, old):
		
	if current.text(0) == "Box":
		self.newBoxPanel = createBox()
		h_la = QtWidgets.QHBoxLayout()
		h_la.addWidget(self.newBoxPanel)
		self.clearLayout(self.propertyBox.layout())
		self.propertyBox.setLayout(h_la)
		self.drawBox()
		for inputLine in (self.boxLengthXInput, self.boxLengthYInput, self.boxLengthZInput, self.boxCenterXInput, self.boxCenterYInput, self.boxCenterZInput):
			inputLine.textChanged['QString'].connect(self.drawBox)
		self.BoxColorComboBox.currentTextChanged.connect(self.drawBox)

		self.createBoxBtn.clicked.connect(self.addBox)

	elif current.text(0) == "Sphere":
		self.newSphere = createSphere()
		h_la = QtWidgets.QHBoxLayout()
		h_la.addWidget(self.newSphere)
		self.clearLayout(self.propertyBox.layout())
		self.propertyBox.setLayout(h_la)
		for inputBox in (self.sphereRadiusInput, self.sphereCenterXInput, self.sphereCenterYInput, self.sphereCenterZInput, self.sphereResoluAlphaInput, sphereResoluThetaInput, sphereResoluDeltaInput):
			inputBox.textChanged['QString'].connect(self.drawSphere)
			
		self.createSphereBtn.clicked.connect(self.addSphere)

	elif current.text(0) == "Cylinder":
		self.newCylinder = createCylinder()
		h_la = QtWidgets.QHBoxLayout()
		h_la.addWidget(self.newCylinder)
		self.clearLayout(self.propertyBox.layout())
		self.propertyBox.setLayout(h_la)
		self.previewCylinderBtn.clicked.connect(self.drawCylinder)
		self.createCylinderBtn.clicked.connect(self.addCylinder)
		
	elif current.text(0) == "Cone":
		self.newCone = createCone()
		h_la = QtWidgets.QHBoxLayout()
		h_la.addWidget(self.newCone)
		self.clearLayout(self.propertyBox.layout())
		self.propertyBox.setLayout(h_la)
		self.previewConeBtn.clicked.connect(self.drawCone)
		self.createConeBtn.clicked.connect(self.addCone)