import os
import re
from math import pi
from time import localtime, strftime

"""
The procedure to generate a chtMultiRegionSimpleFoam case. 
Main function: 
 * pair the mappedWall patches. 
 * put the boundaries to initial folders.
 * proper initial condition for each region and patch.
 * set the thermophysicalProperties, radiationProperties, gravity....
"""

""" 
The start point is the ANSA out put OpenFOAM folder. 
rules when mesh the geometry in ANSA 
 1, different Mid for solids, fluids regions, solver set to chtMultiRegionSimpleFoam to enable multiRegion folder structure.
 2, mappedWall for the interface.
 3, _wall for wall, inlet, outlet
 4, turbulence model 
"""


class Patch(object):
    def __init__(self, name=None, region=None, type="", startFace=0, nFaces=0):
        self.name = name
        self.region = region
        self.type = type
        self.startFace = startFace
        self.nFaces = nFaces


# TODO: for each patch and turbulence model and boundary, set a write function to enable structured output to file.
class MappedWall(Patch):
    def __init__(self, name=None, region=None, type="mappedWall", startFace=0, nFaces=0, sampleMode=None,
                 samplePatch=None, sampleRegion=None):
        super(MappedWall, self).__init__(name, region, type, startFace, nFaces)
        self.sampleMode = sampleMode
        self.samplePatch = samplePatch
        self.sampleRegion = sampleRegion


class CyclicAMI(Patch):
    def __init__(self, name=None, region=None, utype="cyclicAMI", startFace=0, nFaces=0, Tolerance=0.0,
                 neighbourPatch=None, transform=None):
        super(CyclicAMI, self).__init__(name, region, type, startFace, nFaces)
        self.Tolerance = Tolerance
        self.neighbourPatch = neighbourPatch
        self.transform = transform


class rotationProp(object):
    def __init__(self, origin=(0, 0, 0), axis=(0, 0, 1), omega=["constant", 19.35]):
        self.origin = origin
        self.axes = axis
        self.method = omega[0]
        self.rad = (float(omega[1]) * 2 * pi) / 60  # the unit is rpm.


class MRF(object):
    def __init__(self, name, cellZone, active, nonRotatingPatches, rotateProp):
        self.name = name
        self.cellZone = cellZone
        self.active = active
        self.nonRotatingPatches = nonRotatingPatches
        self.rotation = rotateProp


class decomposePar(object):
    # available decompose methods, simple, hierarchical, scotch, manual
    # ref: https://cfd.direct/openfoam/user-guide/v6-running-applications-parallel/
    def __init__(self, numberOfSubdomains, method="scotch", coeffs=" "):
        self.numberOfSubdomains = numberOfSubdomains
        self.method = method
        self.coeffs = coeffs


# TODO: add the functions class in OpenFOAM utilities to enable the visualization of postprocess
class postFunction(object):
    """  function objects to do postProcessing.
    ref: https://www.openfoam.com/documentation/guides/latest/doc/guide-function-objects.html
    functions
    {
        <user-defined name>
        {
            type        <object type>;
            libs        (<list of library file names>);
            ...
        }
    }
    """

    def __init__(self):
        self.funcName = "probe"
        self.type = ""


def stripFoamHead(text):
    return text[text.find("}") + 1:]


class OpenFOAMCase(object):
    def __init__(self):
        self.__regionProperty = {}
        self.__caseFolder = ""
        self.__caseName = ""
        self.__boundaries = {}
        self.__controlDict = {}
        self.__fvSchemes = {}
        self.__fvSolution = {}
        self.__fvOption = {}
        self.__MRF = {}
        self.__decomposeParDict = {}
        self.__dynamicMesh = {}
        self.__radiation = {}
        self.__initial = {}
        self.__alpha = {}
        self.__turbulenceModel = {}
        self.__message = "Ready! Let's GO!\n\n"
        self.__log = ""

    def loadCase(self):
        self.SetFolderAndName()
        self.SetRegionProperty()
        self.loadBoundary()
        self.loadDecomposePar()
        self.loadDynamicMesh()
        self.loadFvSchemes()
        self.loadFvSolution()
        self.loadRadiation()
        self.loadMRF()
        self.loadSolverInfo()
        self.loadInitialCondition()
        self.loadTurbulenceModel()
        self.loadDecomposePar()

    def SetFolderAndName(self, caseFolder=("", "")):
        # caseFolder example, from vtkFoamReader:
        # ('C:/Shaohui/OpenFoam/radiationTest/air99surf/case14.foam', 'OpenFOAM File (*.foam *.txt)')
        foam_path = caseFolder[0]
        if len(foam_path):
            foam_path = foam_path[:foam_path.rfind("/")]
            self.__caseFolder = foam_path
            self.__caseName = foam_path[foam_path.rfind("/") + 1:]
        else:
            self.__message += "\nNo case folder found\n"

    def GetCasePath(self):
        return self.__caseFolder

    def GetCaseName(self):
        return self.__caseName

    def SetRegionProperty(self):
        # check the file structure first, then go to the properties dict.
        zero_folder = self.__caseFolder + "/0/"
        constant_folder = self.__caseFolder + "/constant/"
        system_folder = self.__caseFolder + "/system/"

        regions_constant = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
        regions_constant.sort()

        regions_zero = [name for name in os.listdir(zero_folder) if os.path.isdir(zero_folder + "/" + name)]
        regions_zero.sort()

        regions_system = [name for name in os.listdir(system_folder) if os.path.isdir(system_folder + "/" + name)]
        regions_system.sort()

        if len(regions_constant) == 0 and len(regions_system) == 0 and len(regions_zero) == 0:
            self.__message += "\nThere is no sub regions exist! Single region problem. \n"
            self.__regionProperty["default region"] = "fluid"
            singleRegion = True
        else:
            try:
                with open(constant_folder + "regionProperties") as fid:
                    text = stripFoamHead(fid.read())

                fluid_regions = re.findall(r"fluid.*\((.*)?\)", text)[0].split()
                solid_regions = re.findall(r"solid.*\((.*)?\)", text)[0].split()

                regions = fluid_regions + solid_regions
                regions = [name for name in regions if len(name)]  # maybe there is no fluid or solid region at all.
                regions.sort()

                for reg in solid_regions:
                    if len(reg):
                        self.__regionProperty[reg] = "solid"
                for reg in fluid_regions:
                    if len(reg):
                        self.__regionProperty[reg] = "fluid"
            except IOError as e:
                self.__message += str(e)
                self.__message += "\nManually change the regionProperties to define the regions\n"
            if regions != regions_constant or regions != regions_system or regions != regions_zero:
                self.__message += "\nThe folder structure doesn't consistent with properties dict!\n"

    def GetRegionProperty(self):
        return self.__regionProperty

    # TODO: currently only RAS and laminar models are considered,
    #  Large Eddy Simulation(LES) & Detached Eddy Simulation(DES) added later.
    def loadTurbulenceModel(self):
        # read in the turbulence model.
        for region in list(self.__regionProperty.keys()):
            turbulence_model = {}
            if region == "default region":  # if single region, its name is default region, upon done, exit loop.
                turbulence_file_path = self.__caseFolder + "/constant/turbulenceProperties"
            elif self.__regionProperty[region] == "fluid":  # multiRegion case, read only fluid region.
                turbulence_file_path = self.__caseFolder + "/constant/" + region + "/turbulenceProperties"
            else:
                continue
            try:
                with open(turbulence_file_path) as fid:
                    text = stripFoamHead(fid.read())
                simulationType = re.findall(r"simulationType\s* (.*);?", text)[0]
                turbulence_model[region] = simulationType
                if simulationType == "RAS":
                    turbulence_model["RASModel"] = re.findall(r"RASModel (.*);?", text)[0]
                    turbulence_model["turbulence"] = re.findall(r"turbulence (.*);?", text)[0]
                    turbulence_model["printCoeffs"] = re.findall(r"printCoeffs (.*);?", text)[0]
                self.__turbulenceModel[region] = turbulence_model
            except IOError as e:
                self.__message += str(e)

    def loadSolverInfo(self):
        try:
            with open(self.__caseFolder + "/system/controlDict") as fid:
                controlDict_text = stripFoamHead(fid.read())
            controlDict_dict = {}

            # these items are not necessarily defined in the controlDict file.
            app = re.findall(r"application\s+(\S+)?\s*;", controlDict_text)
            if len(app):
                controlDict_dict["application"] = app

            startTime = re.findall(r"startTime\s+(\S+)?;", controlDict_text)
            if len(startTime):
                controlDict_dict["startTime"] = startTime

            endTime = re.findall(r"endTime\s+(\S+)?\s*;", controlDict_text)
            if len(endTime):
                controlDict_dict["endTime"] = endTime

            deltaT = re.findall(r"deltaT\s+(\S+)?\s*;", controlDict_text)
            if len(deltaT):
                controlDict_dict["deltaT"] = deltaT

            writeControl = re.findall(r"writeControl\s+(.*)?\s*;", controlDict_text)
            if len(writeControl) :
                controlDict_dict["writeControl"] = writeControl

            writeInterval = re.findall(r"writeInterval\s+(.*)?\s*;", controlDict_text)
            if len(writeControl) :
                controlDict_dict["writeInterval"] = writeInterval

            runTimeModifiable = re.findall(r"runTimeModifiable\s+(\d*\.?\d*)?\s*;", controlDict_text)
            if len(runTimeModifiable):
                controlDict_dict["runTimeModifiable"] = runTimeModifiable

            adjustTimeStep = re.findall(r"adjustTimeStep\s+(.*)?\s*;", controlDict_text)
            if len(adjustTimeStep):
                controlDict_dict["adjustTimeStep"] = adjustTimeStep

            maxCo = re.findall(r"maxCo\s+(\S+)?\s*;", controlDict_text)
            if len(maxCo):
                controlDict_dict["maxCo"] = maxCo

            maxAlphaCo = re.findall(r"maxAlphaCo\s+(\S+)?\s*;", controlDict_text)
            if len(maxAlphaCo):
                controlDict_dict["maxAlphaCo"] = maxAlphaCo

            self.__controlDict = controlDict_dict

        except IOError as e:
            self.__message += str(e)

    def GetControlDict(self):
        return self.__controlDict

    def loadBoundary(self):
        # TODO: connect the boundary info to the display.
        # read in boundary patches of each region.

        for region in list(self.__regionProperty.keys()):
            if self.__regionProperty[region] == "default region":
                path = self.__caseFolder + "/constant/polyMesh/boundary"
            else:
                path = self.__caseFolder + "/constant/" + region + "/polyMesh/boundary"
            try:
                with open(path) as fid:
                    bc_text = stripFoamHead(fid.read())
            except IOError as e:
                self.__message += str(e)
                return

            bc_text = re.findall(r"(\d+)\s*\((.*)\)\s+", bc_text, re.DOTALL)[0][1].split("}")[
                      :-1]  # extract only the boundary definition part
            self.__boundaries[region] = []

            for bc in bc_text:
                bc_name = bc.split("{")[0]
                patch_type = re.findall(r"type\s+(\S+)\s*;", bc)[0]
                startFace = re.findall(r"startFace\s+(\d+)\s*;", bc)[0]
                nFaces = re.findall(r"nFaces\s+(\d+)\s*;", bc)[0]

                # TODO: more type of boundary, now limited to patch, wall, mappedWall, cyclicAMI.
                #  more boundary type such as: symmetry, empty...
                if patch_type == "mappedWall":
                    sampleMode = re.findall(r"sampleMode\s+(\S+)\s*;", bc)[0]
                    sampleRegion = re.findall(r"sampleRegion\s+(\S+)\s*;", bc)[0]
                    samplePatch = re.findall(r"samplePatch\s+(\S+)\s*;", bc)[0]

                elif patch_type == "cyclicAMI":
                    Tolerance = re.findall(r"Tolerance\s+(\S+)?\s*;", bc)[0]
                    neighbourPatch = re.findall(r"neighbourPatch\s+(\S+)\s*;", bc)[0]
                    transform = re.findall(r"transform\s+(\S+)\s*;", bc)[0]

                elif patch_type != "patch" and patch_type != "wall":
                    self.__message += "\nThe path type is not defined yet! \n"

                if patch_type == "wall" or patch_type == "patch":
                    self.__boundaries[region].append(Patch(bc_name, region, patch_type, startFace, nFaces))
                elif patch_type == "mappedWall":
                    self.__boundaries[region].append(
                        MappedWall(bc_name, region, patch_type, startFace, nFaces, sampleMode, samplePatch,
                                   sampleRegion))
                elif patch_type == "cyclicAMI":
                    self.__boundaries[region].append(
                        CyclicAMI(bc_name, region, patch_type, startFace, nFaces, Tolerance, neighbourPatch, transform))
                else:
                    self.__message += "\nThe path type is not defined yet! \n"

    def checkBoundary(self, regions):
        if set(self.__boundaries.keys()) != set(regions.keys()):
            return False
        for region in self.__boundaries:
            patch1 = set(self.__boundaries[region])
            patch1.add("internalMesh")
            patch2 = set(regions[region])
            if set(self.__boundaries[region]) != set(regions[region]):
                return False
        return True

    def differentiateMappedWall(self):
        # now pair the boundaries to make sure the mappedWall and cyclicAMI pair properly.
        # Change the patch name of mappedWall at fluid side to _shadow to avoid confusing.
        # just loop the solid region, slave corresponding fluid's patches.
        for region in list(self.__regionProperty.keys()):
            if self.__regionProperty[region] == "fluid":
                continue
            boundary = self.__boundaries[region]
            for bc in boundary:
                if bc.type == "mappedWall" and bc.name == bc.samplePatch:
                    patch2change = bc.samplePatch
                    candidate_patches = self.__boundaries[patch.sampleRegion]
                    found = False
                    for patch in candidate_patches:
                        # check the corresponding slave patch is mappedWall type
                        if patch.name == patch2change and patch.type != "mappedWall":
                            self.__message += "\n***found patch, but its type is not mappedWall!\n"
                            found = True
                        # check the corresponding slave patch is mapped to the master patch.
                        elif patch.name == patch2change and patch.samplePatch == patch2change:
                            patch.name += "_shadow"
                            bc.samplePatch += "_shadow"
                            found = True
                    if not found:
                        self.__message += "\n***Missing slave for mappedWall " + patch.name + "!\n"

                elif patch.type == "mappedWall" and patch.name != patch.samplePatch:
                    self.__message += "\nMaster and slave mappedWall of " + bc.name + " are differentiated already!\n"

    def loadDecomposePar(self):
        # TODO: change all the open file block with a try error mode. otherwise the program will exit with error.
        def parser(path, region_name):
            try:
                with open(path) as fid:
                    text = stripFoamHead(fid.read())
                    decomposePar({"numberOfSubdomains": re.findall(r"numberOfSubdomains\s+(\d+)\s*;", text),
                                  "method": re.findall(r"method\s+(\S+)\s*", text),
                                  "Coeffs": re.findall(r"Coeffs(.*)", text)})
                self.__decomposeParDict[region_name] = decomposePar
            except IOError as e:
                self.__message += str(e)

        path_global = self.__caseFolder + "/system/decomposeParDict"
        parser(path_global, "global")

        if len(self.__regionProperty.keys()) == 1:
            return
        for region in list(self.__regionProperty.keys()):
            path = self.__caseFolder + "/system/" + region + "/decomposeParDict"
            parser(path_global, region)

    def loadMRF(self):
        def parser(mrf_path):
            try:
                with open(mrf_path) as fid:
                    text = stripFoamHead(fid.read())
                mrf_list = []
                MRF_name = re.findall(r"(\S+).?\{", text)
                MRF_cellZone = re.findall(r"cellZone\s+(\S+)\s*;", text)
                MRF_active = re.findall(r"active\s+(\S+)\s*;", text)
                MRF_nonRotatingPatches = re.findall(r"nonRotatingPatches\s+\((.?)\)\s*;", text)
                MRF_origin = re.findall(r"origin\s+(.*?)\s*;", text)
                MRF_axis = re.findall(r"axis\s*(.*?)\s*;", text)
                MRF_omega = re.findall(r"omega\s+(\S+)\s+(.*?)\s*;", text)
                for i in range(len(MRF_name)):
                    rotate = rotationProp(MRF_origin[i], MRF_axis[i], MRF_omega[i])
                    mrf_list.append(MRF_name[i], MRF_cellZone[i], MRF_active[i], MRF_nonRotatingPatches[i], rotate)
                return mrf_list
            except IOError as e:
                self.__message += str(e)

        if len(self.__regionProperty.keys()) == 1:
            path = self.__caseFolder + "/constant/MRFProperties"
            self.__MRF["default region"] = parser(path)
        else:
            for region in list(self.__regionProperty.keys()):
                if self.__regionProperty[region] == "fluid":
                    path = self.__caseFolder + "/constant/" + region + "/MRFProperties"
                    self.__MRF[region] = parser(path)

    def loadRadiation(self):
        self.__regionProperty

    def loadFvSchemes(self):
        self.__regionProperty

    def loadFvSolution(self):
        self.__regionProperty

    def loadInitialCondition(self):
        self.__regionProperty
        path = self.__caseFolder + "/0/"

        try:
            with open(path) as fid:
                text = stripFoamHead(fid.read)
            content = re.findall(r"dimensions\s+(.*?);.*internalField\s+(.*?);\s*boundaryField\s*\{(.*)\}", text)
        except IOError as e:
            self.__message += str(e)

    def writeLog(self):
        with open(self.__caseFolder + "/myFoam.log", "a+") as fid:
            fid.write(self.__log)
            fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    def clearLog(self):
        open(self.__caseFolder + "/myFoam.log", 'w').close()

    def loadDynamicMesh(self):
        path = self.__caseFolder
        for region in list(self.__regionProperty.keys()):
            if region == "default region":
                dynamicPath = path + "/constant/dynamicMeshDict"
                try:
                    with open(path) as fid:
                        text = stripFoamHead(fid.read())

                except IOError as e:
                    self.__message += str(e)


"""
    dynamicFvMesh       solidBodyMotionFvMesh;
    motionSolverLibs    ("linfvMotionSolver.so")

    solidBodyMotionFvMeshCoeffs
    {
        cellZone            rotor;
        solidBodyMotionFunction     rotatingMotion;
        rotationMotionCoeffs
        {
            origin      (0 0 0);
            axis        (0 0 1);
            omega       constant 6.28; #rad/s
        }

    }
                except IOError as e:
                    self.__message += e
"""



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