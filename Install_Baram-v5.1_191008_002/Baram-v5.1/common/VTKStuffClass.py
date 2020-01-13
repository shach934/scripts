#-*-coding:utf8-*-

import pickle
import os
import math
import sys
import glob
import time

from vtk import *
from generalSub import *

class VTKStuff():

    def __init__(self,caseDir):
        self.caseDir = caseDir

    #---------------------------------------------------------------------------------------    
    def unsgeometry(self, patchName, renderer):

        fileName = self.caseDir + "/"
        
        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:
            caseType = 1

        reader = vtk.vtkPOpenFOAMReader()
        reader.SetFileName(fileName)
        reader.SetCaseType(caseType)
        reader.CreateCellToPointOn()
        reader.DecomposePolyhedraOn()
        reader.EnableAllPatchArrays()
        reader.SetPatchArrayStatus('internalMesh', 0)
        reader.Update()               
        
        for i in range(len(patchName)):
            reader.SetPatchArrayStatus(patchName[i], 1)
               
        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())
        compositeFilter.Update()
                
        mapper = vtk.vtkPolyDataMapper() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(compositeFilter.GetOutput())
        else:
            mapper.SetInputConnection(compositeFilter.GetOutputPort())
        mapper.ScalarVisibilityOff()
                
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)              
        
        return reader
    #---------------------------------------------------------------------------------------    
    def unsgeometryVTK(self, patchName, renderer):       
       
        renderer.RemoveAllViewProps()
        
        files = []
        for i in range(len(patchName)):
            files.append(self.caseDir + '/VTK/' + patchName[i] + '/' + patchName[i] + '_0.vtk')

        readers = []
        mappers = []
        actors = []
        for i in range(len(files)):
            readers.append(vtkPolyDataReader())
            readers[i].SetFileName(files[i])
            readers[i].Update()

            mappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort()) 
 
            actors.append(vtkActor())
            actors[i].SetMapper(mappers[i])            

            renderer.AddActor(actors[i])

        return actors
    #---------------------------------------------------------------------------------------    
    def unsgeometryVTK_feature(self, patchName, renderer, displayOpt):
                
        renderer.RemoveAllViewProps()
        
        files = []
        for i in range(len(patchName)):
            files.append(self.caseDir + '/VTK/' + patchName[i] + '/' + patchName[i] + '_0.vtk')

        readers = []
        mappers = []
        actors = []
        edges = []
        featureMappers = []
        featureActors = []
        bounds = []
        for i in range(len(files)):
            readers.append(vtkPolyDataReader())
            readers[i].SetFileName(files[i])
            readers[i].Update()
            
            edges.append(vtk.vtkFeatureEdges())
            if vtk.VTK_MAJOR_VERSION <= 5:
                edges[i].SetInput(readers[i].GetOutput())
            else:
                edges[i].SetInputConnection(readers[i].GetOutputPort())
            edges[i].ColoringOff() 

            mappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort())
            
            featureMappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                featureMappers[i].SetInput(edges[i].GetOutput())
            else:
                featureMappers[i].SetInputConnection(edges[i].GetOutputPort()) 
 
            actors.append(vtkActor())
            actors[i].SetMapper(mappers[i])
            bounds.append(actors[i].GetBounds()) 
            
            featureActors.append(vtkActor())
            featureActors[i].SetMapper(featureMappers[i])            

            if displayOpt == 'Feature':
                renderer.AddActor(featureActors[i])
            else:
                renderer.AddActor(actors[i])            
                if displayOpt == 'Surface':
                    actors[i].GetProperty().EdgeVisibilityOff()
                    actors[i].GetProperty().SetRepresentation(2)
                elif displayOpt == 'SurfaceEdge':
                    actors[i].GetProperty().EdgeVisibilityOn()
                    actors[i].GetProperty().SetRepresentation(2)
                elif displayOpt == 'Wireframe':
                    actors[i].GetProperty().SetRepresentationToWireframe()

        xmin = []
        ymin = []
        zmin = []
        xmax = []
        ymax = []
        zmax = []
        for ii in bounds:
            xmin.append(ii[0])
            xmax.append(ii[1])
            ymin.append(ii[2])
            ymax.append(ii[3])
            zmin.append(ii[4])
            zmax.append(ii[5])
            
        domainRange = [min(xmin), max(xmax), min(ymin), max(ymax), min(zmin), max(zmax)]
        
        return actors, featureActors, domainRange   
    #---------------------------------------------------------------------------------------    
    def displayZone(self, zoneName):

        vtkFile = self.caseDir + '/VTK/' + zoneName + '/' + zoneName + '_0.vtk'

        reader = vtkPolyDataReader()
        reader.SetFileName(vtkFile)
        reader.Update()

        mapper = vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())
 
        actor = vtkActor()
        actor.SetMapper(mapper)
        
        return actor                
    #---------------------------------------------------------------------------------------
    def showPoint(self, xc, yc, zc):
    
        GEN = generalClass(self)
        patches, types = GEN.getBCName()
        files = []
        
        for ii in patches:
            files.append(self.caseDir + '/VTK/' + ii + '/' + ii + '_0.vtk')

        readers = []
        mappers = []
        actors = []
        for i in range(len(files)): 
            readers.append(vtkPolyDataReader())
            readers[i].SetFileName(files[i])
            readers[i].Update()

            mappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort()) 
 
            actors.append(vtkActor())
            actors[i].SetMapper(mappers[i])
            
            actors[i].GetProperty().SetRepresentationToWireframe()

        minmax = GEN.getDomainRange()
        delx = float(minmax[1][0]) - float(minmax[0][0])
        dely = float(minmax[1][1]) - float(minmax[0][1])
        delz = float(minmax[1][2]) - float(minmax[0][2])
        mmm = [delx, dely, delz]
        mmm.sort()
        xx = mmm[-1] * 0.1  

        cone = vtk.vtkConeSource()
        cone.SetResolution(60)
        cone.SetCenter(float(xc), float(yc), float(zc))
        cone.SetHeight(xx * 0.5)
        cone.SetRadius(xx / 4.0)
        cone.SetCenter(float(xc) - cone.GetHeight() / 2.0, float(yc), float(zc))

        coneMapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            coneMapper.SetInput(cone.GetOutput())
        else:
            coneMapper.SetInputConnection(cone.GetOutputPort())

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)

        color = (1, 0, 0)
        coneActor.GetProperty().SetColor(color)
 
        return actors, coneActor
    #---------------------------------------------------------------------------------------
    def showSTLCfMesh(self, stlfiles):
    
        readers = []
        mappers = []
        actors = []
        props = []
        bounds = []
        for i in range(len(stlfiles)):
            readers.append(vtk.vtkSTLReader())
            readers[i].SetFileName(stlfiles[i])
            readers[i].Update()
            
            mappers.append(vtk.vtkPolyDataMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort())
                
            actors.append(vtk.vtkActor())
            actors[i].SetMapper(mappers[i])
            
            bounds.append(actors[i].GetBounds())

        if stlfiles != []:
            xmin = []
            ymin = []
            zmin = []
            xmax = []
            ymax = []
            zmax = []
            for ii in bounds:
                xmin.append(ii[0])
                xmax.append(ii[1])
                ymin.append(ii[2])
                ymax.append(ii[3])
                zmin.append(ii[4])
                zmax.append(ii[5])
                
            domainRange = [min(xmin), max(xmax), min(ymin), max(ymax), min(zmin), max(zmax)]
        else:
            domainRange = []
        
        return actors, domainRange

    #---------------------------------------------------------------------------------------
    def showSTL(self, stlfile):
    
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlfile)
        
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())
            
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        prop.SetColor(1, 1, 1)                     

        return actor
    #---------------------------------------------------------------------------------------
    def showSTLMulti(self, stlfiles):

        readers = []
        mappers = []
        actors = []
        props = []
        for i in range(len(stlfiles)):
            readers.append(vtk.vtkSTLReader())
            #readers[i].SetFileName(self.caseDir + '/system/settings/' + stlfiles[i] + '.stl')
            readers[i].SetFileName(stlfiles[i])
            readers[i].Update()
            
            mappers.append(vtk.vtkPolyDataMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort())
                
            actors.append(vtk.vtkActor())
            actors[i].SetMapper(mappers[i])
            
            props.append(vtk.vtkProperty())
            props[i].SetColor(1, 1, 1)
            
            actors[i].SetProperty(props[i])            
            actors[i].GetProperty().SetRepresentationToWireframe()        

        return actors
    #---------------------------------------------------------------------------------------
    def showObjectBox(self, minx, miny, minz, maxx, maxy, maxz):
        
        actor = vtk.vtkActor()
        
        minx = float(minx)
        miny = float(miny)
        minz = float(minz)
        maxx = float(maxx)
        maxy = float(maxy)
        maxz = float(maxz)
        
        numberOfVertices = 8         
        points = vtk.vtkPoints()
        points.InsertNextPoint(minx, miny, minz)
        points.InsertNextPoint(maxx, miny, minz)
        points.InsertNextPoint(maxx, maxy, minz)
        points.InsertNextPoint(minx, maxy, minz)
        points.InsertNextPoint(minx, miny, maxz)
        points.InsertNextPoint(maxx, miny, maxz)
        points.InsertNextPoint(maxx, maxy, maxz)
        points.InsertNextPoint(minx, maxy, maxz)

        hex_ = vtk.vtkHexahedron()
        for i in range(0, numberOfVertices):
            hex_.GetPointIds().SetId(i, i)
         
        uGrid = vtk.vtkUnstructuredGrid()
        uGrid.SetPoints(points)
        uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
            
        mapper = vtk.vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(uGrid)
        else:
            mapper.SetInputData(uGrid)               
            
        actor.SetMapper(mapper)

        return [actor]
    #---------------------------------------------------------------------------------------
    def showSphere(self, centerx, centery, centerz, radius):
        
        actor = vtk.vtkActor()
        
        source = vtk.vtkSphereSource()
        source.SetCenter(float(centerx), float(centery), float(centerz))
        source.SetRadius(float(radius))
        source.SetThetaResolution(20)
        source.SetPhiResolution(20)
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())         
            
        actor.SetMapper(mapper)

        return [actor]
    #---------------------------------------------------------------------------------------
    def showLine(self, minx, miny, minz, maxx, maxy, maxz):
            
        actor = vtk.vtkActor()
            
        source = vtk.vtkLineSource()
        source.SetPoint1(float(minx), float(miny), float(minz))
        source.SetPoint2(float(maxx), float(maxy), float(maxz))            
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())
            
        actor.SetMapper(mapper)

        return [actor]
    #---------------------------------------------------------------------------------------
    def showCone(self, centerx, centery, centerz, height, direction, radius0, radius1):
        
        r0 = float(radius0)
        r1 = float(radius1)
        h = float(height)

        line = vtk.vtkLineSource()
        line.SetPoint1(0, r0, 0.5*h)
        line.SetPoint2(0, r1, -0.5*h )
        line.SetResolution(10)
        
        line1 = vtk.vtkLineSource()
        line1.SetPoint1(0, 0, 0.5*h)
        line1.SetPoint2(0, r0, 0.5*h )
        line1.SetResolution(10)

        line2 = vtk.vtkLineSource()
        line2.SetPoint1(0, 0, -0.5*h)
        line2.SetPoint2(0, r1, -0.5*h )
        line2.SetResolution(10)

        lineSweeper = vtk.vtkRotationalExtrusionFilter()
        lineSweeper.SetResolution(20)
        lineSweeper.SetInputConnection(line.GetOutputPort())
        lineSweeper.SetAngle(360)

        lineSweeper1 = vtk.vtkRotationalExtrusionFilter()
        lineSweeper1.SetResolution(20)
        lineSweeper1.SetInputConnection(line1.GetOutputPort())
        lineSweeper1.SetAngle(360)

        lineSweeper2 = vtk.vtkRotationalExtrusionFilter()
        lineSweeper2.SetResolution(20)
        lineSweeper2.SetInputConnection(line2.GetOutputPort())
        lineSweeper2.SetAngle(360)

        rotate = vtk.vtkTransform()
        if direction == 'x':
            rotate.RotateWXYZ(90, 0, 1, 0)
        elif direction == 'y':
            rotate.RotateWXYZ(90, 1, 0, 0)
        elif direction == 'z':
            rotate.RotateWXYZ(90, 0, 0, 1)
        rotateFilter=vtk.vtkTransformPolyDataFilter()
        rotateFilter.SetTransform(rotate)
        rotateFilter.SetInputConnection(lineSweeper.GetOutputPort())
        rotateFilter.Update()

        transform = vtk.vtkTransform()
        transform.Translate(float(centerx), float(centery), float(centerz))
        transformFilter=vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(rotateFilter.GetOutputPort())
        transformFilter.Update()

        rotate1 = vtk.vtkTransform()
        if direction == 'x':
            rotate1.RotateWXYZ(90, 0, 1, 0)
        elif direction == 'y':
            rotate1.RotateWXYZ(90, 1, 0, 0)
        elif direction == 'z':
            rotate1.RotateWXYZ(90, 0, 0, 1)
        rotateFilter1=vtk.vtkTransformPolyDataFilter()
        rotateFilter1.SetTransform(rotate1)
        rotateFilter1.SetInputConnection(lineSweeper1.GetOutputPort())
        rotateFilter1.Update()

        transform1 = vtk.vtkTransform()
        transform1.Translate(float(centerx), float(centery), float(centerz))
        transformFilter1=vtk.vtkTransformPolyDataFilter()
        transformFilter1.SetTransform(transform1)
        transformFilter1.SetInputConnection(rotateFilter1.GetOutputPort())
        transformFilter1.Update()
        
        rotate2 = vtk.vtkTransform()
        if direction == 'x':
            rotate2.RotateWXYZ(90, 0, 1, 0)
        elif direction == 'y':
            rotate2.RotateWXYZ(90, 1, 0, 0)
        elif direction == 'z':
            rotate2.RotateWXYZ(90, 0, 0, 1)
        rotateFilter2=vtk.vtkTransformPolyDataFilter()
        rotateFilter2.SetTransform(rotate2)
        rotateFilter2.SetInputConnection(lineSweeper2.GetOutputPort())
        rotateFilter2.Update()

        transform2 = vtk.vtkTransform()
        transform2.Translate(float(centerx), float(centery), float(centerz))
        transformFilter2 = vtk.vtkTransformPolyDataFilter()
        transformFilter2.SetTransform(transform2)
        transformFilter2.SetInputConnection(rotateFilter2.GetOutputPort())
        transformFilter2.Update()
                        
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(transformFilter.GetOutput())
        else:
            mapper.SetInputConnection(transformFilter.GetOutputPort())         

        mapper1 = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper1.SetInput(transformFilter1.GetOutput())
        else:
            mapper1.SetInputConnection(transformFilter1.GetOutputPort()) 

        mapper2 = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper2.SetInput(transformFilter2.GetOutput())
        else:
            mapper2.SetInputConnection(transformFilter2.GetOutputPort()) 
                                    
        actor = vtk.vtkActor()
        actor1 = vtk.vtkActor()
        actor2 = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor1.SetMapper(mapper1)
        actor2.SetMapper(mapper2)

        return [actor, actor1, actor2]
    #---------------------------------------------------------------------------------------
    def showHexaSphereLine(self, cx, cy, cz, lx, ly, lz, radius, minmax, thick, objecttype, viewposition, stlfile):
        
        minx = float(cx) - float(lx) * 0.5
        maxx = float(cx) + float(lx) * 0.5
        miny = float(cy) - float(ly) * 0.5
        maxy = float(cy) + float(ly) * 0.5
        minz = float(cz) - float(lz) * 0.5
        maxz = float(cz) + float(lz) * 0.5
            
        actor = vtk.vtkActor()
        prop = vtk.vtkProperty()
        prop.SetColor(1, 0, 0)
        actor.SetProperty(prop)                
            
        if objecttype == 'box':        
            numberOfVertices = 8         
            points = vtk.vtkPoints()
            points.InsertNextPoint(minx, miny, minz)
            points.InsertNextPoint(maxx, miny, minz)
            points.InsertNextPoint(maxx, maxy, minz)
            points.InsertNextPoint(minx, maxy, minz)
            points.InsertNextPoint(minx, miny, maxz)
            points.InsertNextPoint(maxx, miny, maxz)
            points.InsertNextPoint(maxx, maxy, maxz)
            points.InsertNextPoint(minx, maxy, maxz)

            hex_ = vtk.vtkHexahedron()
            for i in range(0, numberOfVertices):
                hex_.GetPointIds().SetId(i, i)
         
            uGrid = vtk.vtkUnstructuredGrid()
            uGrid.SetPoints(points)
            uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
            
            mapper = vtk.vtkDataSetMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(uGrid)
            else:
                mapper.SetInputData(uGrid)
            
        elif objecttype == 'sphere':
            source = vtk.vtkSphereSource()
            source.SetCenter(float(cx), float(cy), float(cz))
            source.SetRadius(float(radius))
            mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(source.GetOutput())
            else:
                mapper.SetInputConnection(source.GetOutputPort())
            
        elif objecttype == 'line':
            source = vtk.vtkLineSource()
            source.SetPoint1(float(minmax[0]), float(minmax[1]), float(minmax[2]))
            source.SetPoint2(float(minmax[3]), float(minmax[4]), float(minmax[5]))            
            mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(source.GetOutput())
            else:
                mapper.SetInputConnection(source.GetOutputPort())
            
        actor.SetMapper(mapper)
        #--------------------------
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlfile)
        
        stlmapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            stlmapper.SetInput(reader.GetOutput())
        else:
            stlmapper.SetInputConnection(reader.GetOutputPort())
            
        stlactor = vtk.vtkActor()                       
        stlactor.SetMapper(stlmapper)        
        stlprop = vtk.vtkProperty()
        stlprop.SetColor(1, 1, 1)           
        stlactor.SetProperty(stlprop)
        stlactor.GetProperty().SetRepresentationToWireframe()

        return actor, stlactor
    #---------------------------------------------------------------------------------------
    def showFarfield(self, minx, miny, minz, maxx, maxy, maxz, viewposition, stlfile):
        
        minx = float(minx)
        miny = float(miny)
        minz = float(minz)
        maxx = float(maxx)
        maxy = float(maxy)
        maxz = float(maxz)
            
        actor = vtk.vtkActor()
        actor.GetProperty().SetRepresentationToWireframe()
            
        numberOfVertices = 8         
        points = vtk.vtkPoints()
        points.InsertNextPoint(minx, miny, minz)
        points.InsertNextPoint(maxx, miny, minz)
        points.InsertNextPoint(maxx, maxy, minz)
        points.InsertNextPoint(minx, maxy, minz)
        points.InsertNextPoint(minx, miny, maxz)
        points.InsertNextPoint(maxx, miny, maxz)
        points.InsertNextPoint(maxx, maxy, maxz)
        points.InsertNextPoint(minx, maxy, maxz)

        hex_ = vtk.vtkHexahedron()
        for i in range(0, numberOfVertices):
            hex_.GetPointIds().SetId(i, i)
         
        uGrid = vtk.vtkUnstructuredGrid()
        uGrid.SetPoints(points)
        uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
            
        mapper = vtk.vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(uGrid)
        else:
            mapper.SetInputData(uGrid)
        actor.SetMapper(mapper)
        #--------------------------
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlfile)
        
        stlmapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            stlmapper.SetInput(reader.GetOutput())
        else:
            stlmapper.SetInputConnection(reader.GetOutputPort())
            
        stlactor = vtk.vtkActor()                       
        stlactor.SetMapper(stlmapper)        
        stlprop = vtk.vtkProperty()
        stlprop.SetColor(1, 1, 1)           
        stlactor.SetProperty(stlprop)
      
        return actor, stlactor
    #---------------------------------------------------------------------------------------
    def showSetFieldRegion(self, minx, miny, minz, maxx, maxy, maxz, viewposition, patchName):
            
        actor = vtk.vtkActor()
        actor.GetProperty().SetRepresentationToWireframe()        
            
        numberOfVertices = 8         
        points = vtk.vtkPoints()
        points.InsertNextPoint(float(minx), float(miny), float(minz))
        points.InsertNextPoint(float(maxx), float(miny), float(minz))
        points.InsertNextPoint(float(maxx), float(maxy), float(minz))
        points.InsertNextPoint(float(minx), float(maxy), float(minz))
        points.InsertNextPoint(float(minx), float(miny), float(maxz))
        points.InsertNextPoint(float(maxx), float(miny), float(maxz))
        points.InsertNextPoint(float(maxx), float(maxy), float(maxz))
        points.InsertNextPoint(float(minx), float(maxy), float(maxz))

        hex_ = vtk.vtkHexahedron()
        for i in range(0, numberOfVertices):
            hex_.GetPointIds().SetId(i, i)
         
        uGrid = vtk.vtkUnstructuredGrid()
        uGrid.SetPoints(points)
        uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
            
        mapper = vtk.vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(uGrid)
        else:
            mapper.SetInputData(uGrid)
            
        actor.SetMapper(mapper)
        #--------------------------        
        onOff = []
        for ii in patchName:
            onOff.append(1)
        onOff.append(0)
            
        files = []
        for i in range(len(patchName)):
            if onOff[i] == 1:
                files.append(self.caseDir + '/VTK/' + patchName[i] + '/' + patchName[i] + '_0.vtk')

        readers = []
        mappers = []
        actors = []
        props = []
        for i in range(len(files)): 
            readers.append(vtkPolyDataReader())
            readers[i].SetFileName(files[i])
            readers[i].Update()

            mappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort()) 
 
            actors.append(vtkActor())
            actors[i].SetMapper(mappers[i])
         
        return actor, actors
    #---------------------------------------------------------------------------------------
    def showCuttingPlane(self, p0, p1, p2, p3):
    
        GEN=generalClass(self)
            
        actor = vtk.vtkActor()
        actor.GetProperty().SetRepresentationToSurface()
        prop = vtk.vtkProperty()
        prop.SetColor(1, 0, 0)
        actor.SetProperty(prop)  
        
        points = vtk.vtkPoints()
        points.InsertNextPoint(p0)
        points.InsertNextPoint(p1)
        points.InsertNextPoint(p2)
        points.InsertNextPoint(p3)
 
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, 0)
        quad.GetPointIds().SetId(1, 1)
        quad.GetPointIds().SetId(2, 2)
        quad.GetPointIds().SetId(3, 3)
         
        quads = vtk.vtkCellArray()
        quads.InsertNextCell(quad)
         
        polydata = vtk.vtkPolyData()
         
        polydata.SetPoints(points)
        polydata.SetPolys(quads)
            
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata) 
            
        actor.SetMapper(mapper)
        
        patchName, patchType = GEN.getBCName()
        minmax = GEN.getDomainRange()
                  
        onOff = []
        for ii in patchName:
            onOff.append(1)
        onOff.append(0)
            
        files = []
        for i in range(len(patchName)):
            if onOff[i] == 1:
                files.append(self.caseDir + '/VTK/' + patchName[i] + '/' + patchName[i] + '_0.vtk')

        readers = []
        mappers = []
        actors = []
        props = []
        for i in range(len(files)): 
            readers.append(vtkPolyDataReader())
            readers[i].SetFileName(files[i])
            readers[i].Update()

            mappers.append(vtkDataSetMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort()) 
 
            actors.append(vtkActor())
            actors[i].SetMapper(mappers[i])
            
            props.append(vtk.vtkProperty())

        return actor, actors
    #---------------------------------------------------------------------------------------
    def cutPlane(self, reader, normal, origin, fieldName, stime, displayOpt, vectorScalar, scaleFactor, colormap, colormapDict):

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()

        readergetblock = reader.GetOutput().GetBlock(0)
        
        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())    
        compositeFilter.Update()

        plane = vtk.vtkPlane()
        plane.SetOrigin(float(origin[0]), float(origin[1]), float(origin[2]))
        plane.SetNormal(float(normal[0]), float(normal[1]), float(normal[2]))

        cutter=vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        if vtk.VTK_MAJOR_VERSION <= 5:
            cutter.SetInput(readergetblock)
        else:
            cutter.SetInputData(readergetblock)
        cutter.Update()

        colorFunction = vtk.vtkColorTransferFunction()        
        colorFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        colorFunction.AddRGBPoint(1, 1.0, 0.0, 0.0)
        
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)
        scalar_bar.SetOrientationToVertical()
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.2f')

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cutter.GetOutput())
        else:
            mapper.SetInputConnection(cutter.GetOutputPort()) 
        mapper.SetLookupTable(colorFunction)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(fieldName)
            
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()
        actor.SetProperty(prop)
            
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()          
        # --- vector -----------------
        arrow = vtk.vtkArrowSource()

        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(cutter.GetOutputPort())
        glyph.SetSourceConnection(arrow.GetOutputPort())
        glyph.ScalingOn()
        glyph.SetScaleModeToScaleByVector()
        glyph.SetScaleFactor(float(scaleFactor))		
        glyph.SetVectorModeToUseVector()
        glyph.SetColorModeToColorByScalar()
        glyph.OrientOn()
           
        mapperv = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapperv.SetInput(glyph.GetOutput())
        else:
            mapperv.SetInputConnection(glyph.GetOutputPort()) 
        mapperv.SetLookupTable(colorFunction)
        mapperv.SetScalarModeToUsePointFieldData()
        mapperv.SelectColorArray(fieldName)
            
        actorv=vtk.vtkActor()
        actorv.SetMapper(mapperv)

        return actor, actorv, scalar_bar, cutter, glyph
    #---------------------------------------------------------------------------------------
    def cutPlaneMesh(self, reader, normal, origin, fieldName, stime, displayOpt):

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()
        
        readergetblock = reader.GetOutput().GetBlock(0)

        compositeFilter = vtk.vtkCompositeDataGeometryFilter()
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort()) 
        compositeFilter.Update()

        plane = vtk.vtkPlane()
        plane.SetOrigin(float(origin[0]), float(origin[1]), float(origin[2]))
        plane.SetNormal(float(normal[0]), float(normal[1]), float(normal[2]))

        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        if vtk.VTK_MAJOR_VERSION <= 5:
            cutter.SetInput(readergetblock)
        else:
            cutter.SetInputData(readergetblock)
        cutter.Update()
                    
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cutter.GetOutput())
        else:
            mapper.SetInputConnection(cutter.GetOutputPort()) 
        mapper.SetScalarModeToUsePointFieldData() 
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
            
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()   
        else:
            prop = vtk.vtkProperty()
            prop.EdgeVisibilityOn()
            actor.SetProperty(prop)            

        return actor, cutter
    #---------------------------------------------------------------------------------------
    def patchField(self, reader, patchzone, onOff, fieldName, stime, displayOpt, vectorScalar, scaleFactor, colormap, colormapDict):

        patchzone.append('internalMesh')
        onOff.append(0)

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)      

        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()

        for i in range(len(patchzone)):
            reader.SetPatchArrayStatus(patchzone[i], onOff[i])
        reader.Update()

        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())
        compositeFilter.Update()
        
        drange = compositeFilter.GetOutput().GetCellData().GetArray(fieldName).GetRange()
	        
        colorFunction = vtk.vtkColorTransferFunction()
        if colormap == 'blue to red':
            colorFunction.AddRGBPoint(drange[0], 0.0, 0.0, 1.0)
            colorFunction.AddRGBPoint(drange[1], 1.0, 0.0, 0.0)
            colorFunction.SetColorSpaceToHSV()
            colorFunction.HSVWrapOff()
        elif colormap == 'cool to warm':
            colorFunction.AddRGBPoint(drange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            colorFunction.AddRGBPoint(drange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            colorFunction.SetColorSpaceToDiverging()           
        else:
            num = colormapDict[colormap][0]
            data = colormapDict[colormap][1]
            delta = drange[1] - drange[0]
            for i in range(num - 1):
                colorFunction.AddRGBPoint(drange[0] + delta*(i) / num, data[i][0], data[i][1], data[i][2])

        mapper = vtk.vtkPolyDataMapper() 
        mapper.SetInputConnection(compositeFilter.GetOutputPort())
        mapper.SetLookupTable(colorFunction)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(fieldName)        
        mapper.SetScalarRange(drange)
        
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)        
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.02f')

        cactor = vtk.vtkActor()
        cactor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()
        cactor.SetProperty(prop)
        
        if displayOpt == 'wireframe':
            cactor.GetProperty().SetRepresentationToWireframe() 
        # vector
        arrow = vtk.vtkArrowSource()
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(compositeFilter.GetOutputPort())
        glyph.SetSourceConnection(arrow.GetOutputPort())

        glyph.ScalingOn()
        glyph.SetScaleModeToScaleByVector()
        glyph.SetScaleFactor(float(scaleFactor))		
        glyph.OrientOn()
        
        mapper1=vtk.vtkPolyDataMapper() 
        mapper1.SetInputConnection(glyph.GetOutputPort())
        mapper1.SelectColorArray(fieldName)        
        mapper1.SetLookupTable(colorFunction)
        mapper1.SetScalarRange(drange)

        vactor = vtk.vtkActor()
        vactor.SetMapper(mapper1)       
       
        return cactor, vactor, scalar_bar, compositeFilter, glyph    
    #---------------------------------------------------------------------------------------
    def isoSurface(self, reader, isoField, value, fieldName, stime, displayOpt, colormap, colormapDict):

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()
        self.getCoordinate(reader)

        readergetblock=reader.GetOutput().GetBlock(0)
        
        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())    
        compositeFilter.Update()

        # iso
        iso = vtk.vtkContourFilter()                                    
        if vtk.VTK_MAJOR_VERSION <= 5:
            iso.SetInput(readergetblock)
        else:
            iso.SetInputData(readergetblock)                        
        iso.SetInputArrayToProcess(0, 0, 0, 3, isoField)                       
        iso.SetValue(0, value)
        
        colorFunction = vtk.vtkColorTransferFunction()        
        colorFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        colorFunction.AddRGBPoint(1, 1.0, 0.0, 0.0)

        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)
        scalar_bar.SetOrientationToVertical()
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.2f')

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(iso.GetOutput())
        else:
            mapper.SetInputConnection(iso.GetOutputPort()) 
        mapper.SetLookupTable(colorFunction)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(fieldName)
            
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()
        actor.SetProperty(prop)
            
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()          

        return actor, scalar_bar, iso
    #---------------------------------------------------------------------------------------
    def multiIsoSurface(self, reader, isoField, start, end, steps, fieldName, stime, displayOpt, colormap, colormapDict):

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()
        self.getCoordinate(reader)

        readergetblock=reader.GetOutput().GetBlock(0)
        
        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())    
        compositeFilter.Update()

        # iso
        iso = vtk.vtkContourFilter()                                    
        if vtk.VTK_MAJOR_VERSION <= 5:
            iso.SetInput(readergetblock)
        else:
            iso.SetInputData(readergetblock)                        
        iso.SetInputArrayToProcess(0, 0, 0, 3, isoField)                       
        steps = int(steps)
        iso.SetNumberOfContours(steps)
        iso.GenerateValues(steps,start,end)
        
        colorFunction = vtk.vtkColorTransferFunction()        
        colorFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        colorFunction.AddRGBPoint(1, 1.0, 0.0, 0.0)

        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)
        scalar_bar.SetOrientationToVertical()
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.2f')

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(iso.GetOutput())
        else:
            mapper.SetInputConnection(iso.GetOutputPort()) 
        mapper.SetLookupTable(colorFunction)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(fieldName)
            
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()
        actor.SetProperty(prop)
            
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()          

        return actor, scalar_bar, iso
    #---------------------------------------------------------------------------------------
    def clip(self, reader, clipBy, value, fieldName, stime, displayOpt, colormap, colormapDict, dataSets):

        if clipBy == 'coordsX' or clipBy == 'coordsY' or clipBy == 'coordsZ':         
            plane = vtk.vtkPlane()
            if clipBy == 'coordsX':        
                plane.SetOrigin(value, 0, 0)
                plane.SetNormal(1, 0, 0)
            elif clipBy == 'coordsY':        
                plane.SetOrigin(0, value, 0)
                plane.SetNormal(0, 1, 0)
            elif clipBy == 'coordsZ':        
                plane.SetOrigin(0, 0, value)
                plane.SetNormal(0, 0, 1)
        
        colorFunction = vtk.vtkColorTransferFunction()        
        colorFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        colorFunction.AddRGBPoint(1, 1.0, 0.0, 0.0)

        clipperList = []
        actorList = []
        for ii in dataSets:
            clipper = vtk.vtkClipDataSet()
            clipper.GenerateClippedOutputOn()
            #clipper.GenerateClipScalarsOn()

            if vtk.VTK_MAJOR_VERSION <= 5:
                clipper.SetInput(ii)
            else:
                clipper.SetInputData(ii)
            
            if clipBy == 'coordsX' or clipBy == 'coordsY' or clipBy == 'coordsZ':                    
                clipper.SetClipFunction(plane)
            else:
                scalar = ii.GetPointData().GetArray(clipBy)
                ii.GetPointData().SetScalars(scalar)
            clipper.SetValue(value)

            mapper = vtk.vtkDataSetMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(clipper.GetOutput())
            else:
                mapper.SetInputConnection(clipper.GetOutputPort()) 
            mapper.SetLookupTable(colorFunction)
            mapper.SetScalarModeToUsePointFieldData()
            mapper.SelectColorArray(fieldName)
                
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            prop = vtk.vtkProperty()
            if displayOpt == 'surfaceEdge':
                prop.EdgeVisibilityOn()
            actor.SetProperty(prop)
                
            if displayOpt == 'wireframe':
                actor.GetProperty().SetRepresentationToWireframe()   
            
            clipperList.append(clipper)
            actorList.append(actor)

        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)
        scalar_bar.SetOrientationToVertical()
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.2f')

        return actorList, scalar_bar, clipperList
    #---------------------------------------------------------------------------------------
    def streamTracer(self, reader, dic, seedName):
    
        fieldName = dic['scalar']
        stime = dic['time']
        seedType = dic[seedName]['seedType']
        resolution = dic[seedName]['resolution']
        integrator = dic['integrator']
        direction = dic['direction']
        maxLength = dic['maxLength']
        shape = dic['shape']
        point1 = [dic[seedName]['point1'][0], dic[seedName]['point1'][1], dic[seedName]['point1'][2]]
        point2 = [dic[seedName]['point2'][0], dic[seedName]['point2'][1], dic[seedName]['point2'][2]]
        point3 = [dic[seedName]['point3'][0], dic[seedName]['point3'][1], dic[seedName]['point3'][2]]
        center = [dic[seedName]['center'][0], dic[seedName]['center'][1], dic[seedName]['center'][2]]

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()

        readergetblock = reader.GetOutput().GetBlock(0)

        if seedType == 'line':
            seed = vtk.vtkLineSource()
            seed.SetPoint1(float(point1[0]), float(point1[1]), float(point1[2]))
            seed.SetPoint2(float(point2[0]), float(point2[1]), float(point2[2]))
            seed.SetResolution(int(resolution))
        elif seedType == 'plane':
            seed = vtk.vtkPlaneSource()
            seed.SetOrigin(float(point1[0]), float(point1[1]), float(point1[2]))
            seed.SetPoint1(float(point2[0]), float(point2[1]), float(point2[2]))
            seed.SetPoint2(float(point3[0]), float(point3[1]), float(point3[2]))
            seed.SetXResolution(int(resolution))
            seed.SetYResolution(int(resolution))
        elif seedType == 'sphere':
            seed = vtk.vtkPointSource()
            seed.SetCenter(float(center[0]), float(center[1]), float(center[2]))
            seed.SetRadius(float(dic[seedName]['radius']))
            seed.SetNumberOfPoints(int(resolution))

        seedMapper = vtk.vtkPolyDataMapper()
        seedMapper.SetInputConnection(seed.GetOutputPort())

        seedActor = vtk.vtkActor()
        seedActor.SetMapper(seedMapper)
        seedActor.GetProperty().SetColor(1, 1, 0)
        
        if integrator == 'RungeKutta2':
            integ = vtk.vtkRungeKutta2()    
        elif integrator == 'RungeKutta4':
            integ = vtk.vtkRungeKutta4()    
        else:
            integ = vtk.vtkRungeKutta45()

        sl = vtk.vtkStreamTracer()
        if vtk.VTK_MAJOR_VERSION <= 5:        
            sl.SetInput(readergetblock)
        else:
            sl.SetInputData(readergetblock)
            
        sl.SetSourceConnection(seed.GetOutputPort())
        sl.SetIntegrator(integ)
        sl.SetMaximumPropagation(float(maxLength))
        sl.SetInitialIntegrationStep(0.01)
        if direction == 'backward':
            sl.SetIntegrationDirectionToBackward()
        elif direction == 'forward':
            sl.SetIntegrationDirectionToForward()
        else:
            sl.SetIntegrationDirectionToBoth()    
        
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        if shape == 'line':
            
            mapper.SetInputConnection(sl.GetOutputPort())
            actor.GetProperty().SetLineWidth(float(dic['lineWidth']))
            
        elif shape == 'tube':
            tube = vtk.vtkTubeFilter()
            tube.SetInputConnection(sl.GetOutputPort())
            tube.SetRadius(float(dic['tubeRadius']))
            tube.SetNumberOfSides(6)
            tube.SetOffset(0)
            mapper.SetInputConnection(tube.GetOutputPort())

        elif shape == 'ribbon':
            ribbon = vtk.vtkRibbonFilter()
            ribbon.SetInputConnection(sl.GetOutputPort())
            ribbon.SetWidth(float(dic['ribbonWidth']))
            ribbon.SetAngle(float(dic['ribbonAngle']))
            ribbon.VaryWidthOff()
            mapper.SetInputConnection(ribbon.GetOutputPort())

        colorFunction = vtk.vtkColorTransferFunction()        
        colorFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        colorFunction.AddRGBPoint(1, 1.0, 0.0, 0.0)
        
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetTitle(fieldName)
        scalar_bar.SetOrientationToVertical()
        scalar_bar.SetLookupTable(colorFunction)
        scalar_bar.SetLabelFormat('%0.2f')

        mapper.SetLookupTable(colorFunction)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(fieldName)                             

        return actor, seedActor, scalar_bar 
    #---------------------------------------------------------------------------------------------------------                            
    def seed_line(self, point1, point2, resolution):
        
        seed = vtk.vtkLineSource()
        seed.SetPoint1(float(point1[0]), float(point1[1]), float(point1[2]))
        seed.SetPoint2(float(point2[0]), float(point2[1]), float(point2[2]))
        seed.SetResolution(int(resolution))

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(seed.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 0)
        return actor        
    #---------------------------------------------------------------------------------------------------------                            
    def seed_plane(self, point1, point2, point3, resolution):
        
        seed = vtk.vtkPlaneSource()
        seed.SetOrigin(float(point1[0]), float(point1[1]), float(point1[2]))
        seed.SetPoint1(float(point2[0]), float(point2[1]), float(point2[2]))
        seed.SetPoint2(float(point3[0]), float(point3[1]), float(point3[2]))
        seed.SetXResolution(int(resolution))
        seed.SetYResolution(int(resolution))

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(seed.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 0)
        return actor  
    #---------------------------------------------------------------------------------------------------------                            
    def seed_sphere(self, center, radius, resolution):
        
        seed = vtk.vtkPointSource()
        seed.SetCenter(float(center[0]), float(center[1]), float(center[2]))
        seed.SetRadius(float(radius))
        seed.SetNumberOfPoints(int(resolution))

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(seed.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 0)
        actor.GetProperty().SetPointSize(10)
        return actor
    #---------------------------------------------------------------------------------------------------------                            
    def getCoordinate(self, reader):
    
        vtkunsgrid = reader.GetOutput().GetBlock(0)
        
        vtkpoints = vtkunsgrid.GetPoints()
        num = vtkpoints.GetNumberOfPoints()
        coordsX = vtk.vtkFloatArray()
        coordsY = vtk.vtkFloatArray()
        coordsZ = vtk.vtkFloatArray()
        for i in range(num):
            coordsX.InsertNextTuple1(vtkunsgrid.GetPoint(i)[0])
            coordsY.InsertNextTuple1(vtkunsgrid.GetPoint(i)[1])
            coordsZ.InsertNextTuple1(vtkunsgrid.GetPoint(i)[2])

        numArray = vtkunsgrid.GetPointData().GetNumberOfArrays()

        vtkunsgrid.GetPointData().AddArray(coordsX)
        vtkunsgrid.GetPointData().GetArray(numArray).SetName('coordsX')
        vtkunsgrid.GetPointData().AddArray(coordsY)
        vtkunsgrid.GetPointData().GetArray(numArray + 1).SetName('coordsY')
        vtkunsgrid.GetPointData().AddArray(coordsZ)
        vtkunsgrid.GetPointData().GetArray(numArray + 2).SetName('coordsZ')
    #---------------------------------------------------------------------------------------------------
    #   for snappyHexMesh
    #---------------------------------------------------------------------------------------------------
    def blockMesh(self):

        fileName = self.caseDir + '/ '
        viewposition = [1, 1, 1]
        
        reader = vtk.vtkOpenFOAMReader()
        reader.SetFileName(fileName)
        reader.Update() 
        
        GEN = generalClass(self)
        patchName, patchType = GEN.getBCName()        
        patchName.append('internalMesh')
        numberOfPatch = len(patchName)
        onOff = []
        for i in range(numberOfPatch):
            onOff.append(1)
        onOff.append(0)

        for i in range(numberOfPatch):
            reader.SetPatchArrayStatus(patchName[i], onOff[i])
        reader.Update()

        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort()) 
        compositeFilter.Update()

        mapper = vtk.vtkPolyDataMapper() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(compositeFilter.GetOutput())
        else:
            mapper.SetInputConnection(compositeFilter.GetOutputPort()) 
        mapper.ScalarVisibilityOff()

        prop = vtk.vtkProperty()
        prop.SetColor(0, 0, 0)
        transform = vtk.vtkTransform()
        transform.Translate(0, 0, 0)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetProperty(prop)
        actor.GetProperty().SetRepresentationToWireframe()
        
        stlreaders = []
        stlmappers = []
        stlactors = []
        stlprops = []
        
        if os.path.isfile(self.caseDir + '/system/settings/stlFileSetup'):
            stlDict = GEN.pickleLoad(self.caseDir + '/system/settings/stlFileSetup')
            stlfilelist = []
            nn = stlDict.keys()
            for ii in nn:
                stlfilelist.append(self.caseDir + '/constant/triSurface/' + ii + '.stl')
            
            for i in range(len(stlfilelist)):
                stlreaders.append(vtk.vtkSTLReader())
                stlreaders[i].SetFileName(stlfilelist[i])
                stlreaders[i].Update()
                stlmappers.append(vtk.vtkPolyDataMapper())
                if vtk.VTK_MAJOR_VERSION <= 5:
                    stlmappers[i].SetInput(stlreaders[i].GetOutput())
                else:
                    stlmappers[i].SetInputConnection(stlreaders[i].GetOutputPort())
                stlactors.append(vtk.vtkActor())
                stlactors[i].SetMapper(stlmappers[i])
                stlprops.append(vtk.vtkProperty())
                stlprops[i].SetColor(1, 0, 0)
                stlactors[i].SetProperty(stlprops[i])

        return actor, stlactors
    #---------------------------------------------------------------------------------------
    def showSTLMultiForSnappy(self, stlfiles):

        readers = []
        mappers = []
        actors = []
        props = []
        for i in range(len(stlfiles)):
            readers.append(vtk.vtkSTLReader())
            readers[i].SetFileName(stlfiles[i])
            readers[i].Update()
            
            mappers.append(vtk.vtkPolyDataMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort())
                
            actors.append(vtk.vtkActor())
            actors[i].SetMapper(mappers[i])

        return actors
    #---------------------------------------------------------------------------------------
    def showBox(self, xmin, ymin, zmin, xmax, ymax, zmax, viewposition, stlfiles):
        
        minx = float(xmin)
        miny = float(ymin)
        minz = float(zmin)
        maxx = float(xmax)
        maxy = float(ymax)
        maxz = float(zmax)
            
        actor = vtk.vtkActor()
        actor.GetProperty().SetRepresentationToWireframe()        
            
        numberOfVertices = 8         
        points = vtk.vtkPoints()
        points.InsertNextPoint(minx, miny, minz)
        points.InsertNextPoint(maxx, miny, minz)
        points.InsertNextPoint(maxx, maxy, minz)
        points.InsertNextPoint(minx, maxy, minz)
        points.InsertNextPoint(minx, miny, maxz)
        points.InsertNextPoint(maxx, miny, maxz)
        points.InsertNextPoint(maxx, maxy, maxz)
        points.InsertNextPoint(minx, maxy, maxz)

        hex_ = vtk.vtkHexahedron()
        for i in range(0, numberOfVertices):
            hex_.GetPointIds().SetId(i, i)
         
        uGrid = vtk.vtkUnstructuredGrid()
        uGrid.SetPoints(points)
        uGrid.InsertNextCell(hex_.GetCellType(), hex_.GetPointIds())
            
        mapper = vtk.vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(uGrid)
        else:
            mapper.SetInputData(uGrid)

        actor.SetMapper(mapper)
        
        props = vtk.vtkProperty()
        props.SetColor(1, 0, 0)
        actor.SetProperty(props)
        actor.GetProperty().SetRepresentationToWireframe()
        #--------------------------
        readers = []
        mappers = []
        stlactors = []
        props = []
        for i in range(len(stlfiles)):
            readers.append(vtk.vtkSTLReader())
            readers[i].SetFileName(stlfiles[i])
            readers[i].Update()
            
            mappers.append(vtk.vtkPolyDataMapper())
            if vtk.VTK_MAJOR_VERSION <= 5:
                mappers[i].SetInput(readers[i].GetOutput())
            else:
                mappers[i].SetInputConnection(readers[i].GetOutputPort())
                
            stlactors.append(vtk.vtkActor())
            stlactors[i].SetMapper(mappers[i])
            
            stlactors[i].GetProperty().SetRepresentationToWireframe()
            
        return actor, stlactors
    #---------------------------------------------------------------------------------------
    def showMeshSnappy(self, patchName, onOff, viewposition, displayOpt):

        fileName = self.caseDir + '/ '       
        reader = vtk.vtkOpenFOAMReader()
        reader.SetFileName(fileName)
        reader.SetCreateCellToPoint(1)
        reader.DecomposePolyhedraOn()
        reader.Update() 

        patchName.append('internalMesh')
        numberOfPatch = len(patchName)
        onOff.append(0)
        for i in range(len(patchName)):
            reader.SetPatchArrayStatus(patchName[i], onOff[i])
        reader.Update()

        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())   
        compositeFilter.Update()

        mapper = vtk.vtkPolyDataMapper() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(compositeFilter.GetOutput())
        else:
            mapper.SetInputConnection(compositeFilter.GetOutputPort()) 
        mapper.ScalarVisibilityOff()

        prop = vtk.vtkProperty()
        prop.SetColor(1, 1, 0.8)
        
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetProperty(prop)
        
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()   

        return actor
    #---------------------------------------------------------------------------------------
    def cutPlaneSnappy(self, setNormallist, setOriginlist, caseType, stime, viewposition, displayOpt):

        fileName = self.caseDir + "/ "

        reader = vtk.vtkPOpenFOAMReader()
        reader.SetFileName(fileName)
        reader.SetCaseType(caseType)
        reader.CreateCellToPointOn()
        reader.SetCreateCellToPoint(1)
        reader.DecomposePolyhedraOn()
        reader.EnableAllPatchArrays()
        reader.SetPatchArrayStatus('internalMesh', 1)
        reader.Update()

        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        if stime == 'latestTime':
            timedata = []
            for stepI in range(nTimeSteps):
                timeValue = outInfo.Get(timeStepsKey, stepI)
                timedata.append(timeValue)  
            plottime = timedata[-1]
        else:
            plottime = float(stime)
        exe.SetUpdateTimeStep(0, plottime)
        reader.Modified()
        reader.Update()
        
        readergetblock=reader.GetOutput().GetBlock(0)

        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort())
        compositeFilter.Update()

        outline = vtk.vtkOutlineFilter()
        if vtk.VTK_MAJOR_VERSION <= 5:
            outline.SetInput(compositeFilter.GetOutput())
        else:
            outline.SetInputConnection(compositeFilter.GetOutputPort()) 
        
        outlineMapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            outlineMapper.SetInput(outline.GetOutput())
        else:
            outlineMapper.SetInputConnection(outline.GetOutputPort()) 

        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)
        outlineActor.GetProperty().SetColor(0, 0, 0)
        #----------------------
        plane = vtk.vtkPlane()
        plane.SetOrigin(float(setOriginlist[0]), float(setOriginlist[1]), float(setOriginlist[2]))
        plane.SetNormal(float(setNormallist[0]), float(setNormallist[1]), float(setNormallist[2]))

        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        if vtk.VTK_MAJOR_VERSION <= 5:
            cutter.SetInput(readergetblock)
        else:
            cutter.SetInputData(readergetblock)
        cutter.Update()            

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cutter.GetOutput())
        else:
            mapper.SetInputConnection(cutter.GetOutputPort()) 

        prop = vtk.vtkProperty()
        prop.SetColor(1, 1, 0.8)
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetProperty(prop)
       
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()  

        return outlineActor, actor
    #---------------------------------------------------------------------------------------
    def showMeshAutoPatch(self, patchName, onOff, viewposition, displayOpt):

        fileName = self.caseDir + '/'       
        reader = vtk.vtkOpenFOAMReader()
        reader.SetFileName(fileName)
        reader.SetCreateCellToPoint(1)
        reader.DecomposePolyhedraOn()
        reader.Update()
        
        reader.UpdateInformation()
        exe = reader.GetExecutive()
        outInfo = exe.GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)

        exe.SetUpdateTimeStep(0, 1)
        reader.Modified()
        reader.Update()

        patchName.append('internalMesh')
        numberOfPatch=len(patchName)
        onOff.append(0)
        for i in range(len(patchName)):
            reader.SetPatchArrayStatus(patchName[i],onOff[i])
        reader.Update()

        compositeFilter = vtk.vtkCompositeDataGeometryFilter() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            compositeFilter.SetInput(reader.GetOutput())
        else:
            compositeFilter.SetInputConnection(reader.GetOutputPort()) 
        compositeFilter.Update()

        mapper = vtk.vtkPolyDataMapper() 
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(compositeFilter.GetOutput())
        else:
            mapper.SetInputConnection(compositeFilter.GetOutputPort()) 
        mapper.ScalarVisibilityOff()

        prop = vtk.vtkProperty()
        prop.SetColor(1, 1, 0.8)
        
        if displayOpt == 'surfaceEdge':
            prop.EdgeVisibilityOn()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetProperty(prop)
        
        if displayOpt == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()   
 
        return actor
    #---------------------------------------------------------------------------------------
    def showPointSnappy(self, xc, yc, zc):

        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.caseDir + '/mesh.stl')
        
        mapper = vtk.vtkPolyDataMapper()    
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())
            
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        prop = vtk.vtkProperty()
        prop.SetColor(0, 0, 1)             
        actor.SetProperty(prop)        
        actor.GetProperty().SetRepresentationToWireframe()        

        GEN = generalClass(self)
        minmax = GEN.getDomainRange()
        delx = float(minmax[1][0]) - float(minmax[0][0])
        dely = float(minmax[1][1]) - float(minmax[0][1])
        delz = float(minmax[1][2]) - float(minmax[0][2])
        mmm = [delx, dely, delz]
        mmm.sort()
        xx = mmm[-1] * 0.1  
        
        # cone
        cone = vtk.vtkConeSource()
        cone.SetResolution(60)
        cone.SetCenter(float(xc), float(yc), float(zc))
        cone.SetHeight(xx * 0.5)
        cone.SetRadius(xx / 4.0)
        cone.SetCenter(float(xc) - cone.GetHeight() / 2.0, float(yc), float(zc)) 
        
        coneMapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            coneMapper.SetInput(cone.GetOutput())
        else:
            coneMapper.SetInputConnection(cone.GetOutputPort())

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        color = (1, 0, 0)
        coneActor.GetProperty().SetColor(color)

        return actor, coneActor
 

        
        
                
        

