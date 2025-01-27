from PyQt5 import QtGui
from Ui_blockMesh import Ui_blockMesh
from PyQt5.QtWidgets import QDialog
import vtk
from Panel_VTK import *
#TODO: Rightnow it only support single block, later may extend to multiblock support. It will be more flexible. 
doubleValidator = QtGui.QDoubleValidator()
integelValidator = QtGui.QIntValidator(1, 100000000)

# preview using the blockMesh -blockTopology  to generate a obj file to open, 
# create button will write blockMeshDict and generate polyMesh folder under constant folder. 

class blockMesh(QDialog, Ui_blockMesh):

    def __init__(self, Panel_VTK, parent=None, casePath):
        self.colorTable = vtk.vtkNamedColors()
        super(blockMesh, self).__init__(parent)
        self.casePath = casePath
        self.outputWindow = Panel_VTK
        self.validInput()
        self.setupUi(self) 
        self.monitor()
        self.drawBlockMesh()

    def validInput(self):
        self.maxXInput.setValidator(doubleValidator)
        self.maxYInput.setValidator(doubleValidator)
        self.maxZInput.setValidator(doubleValidator)

        self.minXInput.setValidator(doubleValidator)
        self.minYInput.setValidator(doubleValidator)
        self.minZInput.setValidator(doubleValidator)

        self.pointXInput.setValidator(doubleValidator)
        self.pointYInput.setValidator(doubleValidator)
        self.pointZInput.setValidator(doubleValidator)

        self.gradXInput.setValidator(integelValidator)
        self.gradYInput.setValidator(integelValidator)
        self.gradZInput.setValidator(integelValidator)

        self.cellNumXInput.setValidator(integelValidator)
        self.cellNumYinput.setValidator(integelValidator)
        self.cellNumZInput.setValidator(integelValidator)

    def monitor(self):

        self.maxXInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.maxYInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.maxZInput.textChanged['QString'].connect(self.drawBlockMesh)

        self.minXInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.minYInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.minZInput.textChanged['QString'].connect(self.drawBlockMesh)

        self.pointXInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.pointYInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.pointZInput.textChanged['QString'].connect(self.drawBlockMesh)

        self.gradXInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.gradYInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.gradZInput.textChanged['QString'].connect(self.drawBlockMesh)

        self.cellNumXInput.textChanged['QString'].connect(self.drawBlockMesh)
        self.cellNumYinput.textChanged['QString'].connect(self.drawBlockMesh)
        self.cellNumZInput.textChanged['QString'].connect(self.drawBlockMesh)

        self.previewBlockMeshBtn.clicked.connect(self.previewBlockMesh)
        self.createBlockMeshBtn.clicked.connect(self.createBlockMesh)

    def previewBlockMesh(self):
        self.blockMesh = vtk.vtkCubeSource()
        self.blockMesh_mapper = vtk.vtkPolyDataMapper()
        self.blockMesh_mapper.SetInputConnection(self.blockMesh.GetOutputPort())
        self.blockMesh_actor = vtk.vtkActor()
        self.blockMesh_actor.SetMapper(self.blockMesh_mapper)
        self.blockMesh_actor.SetOpticity(0.5)
        self.blockMesh_actor.EdgeVisibilityOff()
        self.blockMesh_actor.SetEdgeColor(1, 0, 0)
        self.blockMesh_actor.SetLineWidth(2)
        self.box_actor.GetProperty().SetColor(self.colorTable.GetColor3d("gray");
        self.outputWindow.add2Render(self.box_actor)

    def weiteBlockMeshDict(self):
        self.maxX, self.maxY, self.maxZ = float(self.maxXInput.text()), float(self.maxYInput.text()), float(self.maxZInput.text())
        self.minX, self.minY, self.minZ = float(self.minXInput.text()), float(self.minYInput.text()), float(self.minZInput.text())
        self.pX, self.pY, self.pZ = float(self.pointXInput.text()), float(self.pointYInput.text()), float(self.pointZInput.text())
        self.gradX, self.gradY, self.gradZ = float(self.gradXInput.text()), float(self.gradYInput.text()), float(self.gradZInput.text())
        self.cellNX, self.cellNY, self.cellNZ  = int(self.cellNumXInput.text()), int(self.cellNumYinput.text()), int(self.cellNumZInput.text())

        aa = glob.glob(self.caseDir + '/system')
        if aa == []:
            os.system('mkdir ' + self.caseDir + '/system')
        f = open(self.caseDir + '/system/blockMeshDict', 'w')
        
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  v1906                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.com                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     v1906; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      blockMeshDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

        f.write('convertToMeters 1; \n')
        f.write('vertices \n')
        f.write('( \n')
        f.write('   ( ' + str(self.minX) + ' ' + str(self.minY) + ' ' + str(self.minZ) + ' ) \n') 
        f.write('   ( ' + str(self.maxX) + ' ' + str(self.minY) + ' ' + str(self.minZ) + ' ) \n')         
        f.write('   ( ' + str(self.maxX) + ' ' + str(self.maxY) + ' ' + str(self.minZ) + ' ) \n')         
        f.write('   ( ' + str(self.minX) + ' ' + str(self.maxY) + ' ' + str(self.minZ) + ' ) \n')         
        f.write('   ( ' + str(self.minX) + ' ' + str(self.minY) + ' ' + str(self.maxZ) + ' ) \n')         
        f.write('   ( ' + str(self.maxX) + ' ' + str(self.minY) + ' ' + str(self.maxZ) + ' ) \n') 
        f.write('   ( ' + str(self.maxX) + ' ' + str(self.maxY) + ' ' + str(self.maxZ) + ' ) \n') 
        f.write('   ( ' + str(self.minX) + ' ' + str(self.maxY) + ' ' + str(self.maxZ) + ' ) \n') 
        f.write(');\n')
        f.write('blocks\n')
        f.write('(\n')
        f.write('    hex (0 1 2 3 4 5 6 7) (' + str(self.cellNX) + ' ' + str(self.cellNY) + ' ' + str(self.cellNZ) + ') simpleGrading (' + str(self.gradX) + ' ' + str(self.gradY) + ' ' + str(self.gradZ) +')\n')
        f.write(');\n')
        f.write('edges\n')
        f.write('(\n')
        f.write(');\n')
        f.write('boundary\n')
        f.write('(\n')
        
        f.write('    minX \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 3 7 4) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxX \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (1 2 6 5) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    minY \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 1 5 4) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxY \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (3 7 6 2) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    minZ \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 1 2 3) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxZ \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (4 5 6 7) \n')
        f.write('        ); \n')
        f.write('    } \n')
        
        f.write('); \n')
           
        f.close() 
    #-------------------------------------------------------------------------------------------------

    def createBlockMesh(self):
        os.system("batch -i -c blockMesh > log")