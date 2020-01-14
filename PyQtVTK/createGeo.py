
def drawBox(self):
    self.tempBox = vtkCubeSource()
    
    self.tempBox.SetCenter([float(self.boxCenterXInput.text()), float(self.boxCenterYInput.text()), float(self.boxCenterZInput.text())])
    self.tempBox.SetXLength(float(self.boxLengthXInput.text()))
    self.tempBox.SetYLength(float(self.boxLengthYInput.text()))
    self.tempBox.SetZLength(float(self.boxLengthZInput.text()))

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(self.tempBox.GetOutputPort())

    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    self.ren.AddActor(actor)
    self.ren.ResetCamera()

    self.show()
    self.render.Initialize()