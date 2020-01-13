    def drawBox(self):
        if "self.box" not in locals():
            self.box = []
        else:
            self.box.append(vtkCubeSource())
            self.box[-1].SetCenter([float(self.boxCenterXInput.text()), float(self.boxCenterYInput.text()), float(self.boxCenterZInput.text())])
            self.box[-1].SetXLength(float(self.boxLengthXInput.text()))
            self.box[-1].SetYLength(float(self.boxLengthYInput.text()))
            self.box[-1].SetZLength(float(self.boxLengthZInput.text()))

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(self.box[-1].GetOutputPort())
    
            # Create an actor
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
    
            self.ren.AddActor(actor)
    
            self.ren.ResetCamera()
    
            self.frame.setLayout(self.vl)
            self.setCentralWidget(self.frame)
    
            self.show()
            self.iren.Initialize()
