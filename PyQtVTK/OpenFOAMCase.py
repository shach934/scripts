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
    def __init__(self, name=None, region=None, type="cyclicAMI", startFace=0, nFaces=0, Tolerance=0.0,
                 neighbourPatch=None, transform=None):
        super(CyclicAMI, self).__init__(name, region, type, startFace, nFaces)
        self.Tolerance = Tolerance
        self.neighbourPatch = neighbourPatch
        self.transform = transform


class turbulenceModel(object):
    def __init__(self):
        self.__simulationType = None
        self.__RASModel = None
        self.__turbulence = None
        self.__printCoeffs = None

    def SetTurbulenceModel(self, turbulence):
        self.__simulationType = turbulence["simulationType"]
        if self.__simulationType == "RAS":
            self.__RASModel = turbulence["RASModel"]
            self.__turbulence = turbulence["turbulence"]
            self.__printCoeffs = turbulence["printCoeffs"]


class rotationProp(object):
    def __init__(self, origin=(0, 0, 0), axis=(0, 0, 1), omega=["constant", 19.35]):
        self.origin = origin
        self.axes = axis
        self.method = omega[0]
        self.rad = (float(omega[1]) * 2 * pi) / 60  # the unit is rpm.


class controlDict(object):
    def __init__(self, control_dict):
        self.__application = control_dict["application"]
        self.__startTime = control_dict["startTime"]
        self.__endTime = control_dict["endTime"]
        self.__deltaT = control_dict["deltaT"]
        self.__writeControl = control_dict["writeControl"]  # timeStep or adjustableRunTime for steady and transient
        self.__writeInterval = control_dict["writeInterval"]
        self.__runTimeModifiable = control_dict["runTimeModifiable"]
        self.__adjustTimeStep = control_dict["adjustTimeStep"]
        self.__maxCo = control_dict["maxCo"]
        self.__maxAlphaCo = control_dict["maxAlphaCo"]


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
    def __init__(self, numberOfSubdomains, method, coeffs):
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
        self.__numberOfRegions = 1
        self.__regionName = []
        self.__regionProperty = {}
        self.__caseFolder = ""
        self.__caseName = ""
        self.__patches = []
        self.__boundaries = []
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

    def SetFolderAndName(self, caseFolder=("", "")):
        # caseFolder example, from vtkFoamReader:
        # ('C:/Shaohui/OpenFoam/radiationTest/air99surf/case14.foam', 'OpenFOAM File (*.foam *.txt)')
        foam_path = caseFolder[0]
        if len(foam_path):
            foam_path = foam_path[:foam_path.rfind("/")]
            self.__caseFolder = foam_path[:foam_path.rfind("/")]
            self.__caseName = foam_path[foam_path.rfind("/") + 1:]
        else:
            self.__message += "\nNo case folder found\n"

    def GetCasePath(self):
        return self.__caseFolder

    def GetCaseName(self):
        return self.__caseName

    def SetRegionProperty(self, regionNameFromVTK):
        # if there is more than 1 region, go to each folder extract the region's name and find the regionProperties file
        # extract the region's property and using their names to very folders structure.
        regionNameFromVTK = sorted(regionNameFromVTK)  # to compare with the folder names read from the case path.

        if len(regionNameFromVTK) > 1:

            zero_folder = self.__caseFolder + "/0/"
            constant_folder = self.__caseFolder + "/constant/"
            system_folder = self.__caseFolder + "/system/"
            self.__regionName = regionNameFromVTK

            regions2 = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
            regions2.sort()

            regions3 = [name for name in os.listdir(zero_folder) if os.path.isdir(zero_folder + "/" + name)]
            regions3.sort()

            regions4 = [name for name in os.listdir(system_folder) if os.path.isdir(system_folder + "/" + name)]
            regions4.sort()

            if regionNameFromVTK != regions2 or regionNameFromVTK != regions3 or regionNameFromVTK != regions4:
                self.__message += "\nThe multiRegion folder structure is NOT correct! Check again! \n"

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
                self.__message += e
        elif len(regionNameFromVTK) == 1:
            self.__message += "\nSingle region case, default one fluid region!\n"
            self.__regionProperty["default region"] = "fluid"

    def GetRegionProperty(self):
        return self.__regionProperty

    # TODO: currently only RAS and laminar models are considered, Large Eddy Simulation(LES) & Detached Eddy
    #  Simulation(DES)
    def loadTurbulenceModel(self):
        # read in the turbulence model.
        for region in self.__regionName:
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
                self.__turbulenceModel[region] = turbulenceModel(turbulence_model)
            except IOError as e:
                self.__message += e

    def loadSolverInfo(self):
        try:
            with open(self.__caseFolder + "/system/controlDict") as fid:
                controlDict_text = stripFoamHead(fid.read())

            control_dict = {"application": re.findall(r"application\s+(\S+)?\s*;", controlDict_text)[0],
                            "startTime": re.findall(r"startTime\s+(\S+)?;", controlDict_text)[0],
                            "endTime": re.findall(r"endTime\s+(\S+)?\s*;", controlDict_text)[0],
                            "deltaT": re.findall(r"deltaT\s+(\S+)?\s*;", controlDict_text)[0],
                            "writeControl": re.findall(r"writeControl\s+(.*)?\s*;", controlDict_text)[0],
                            "writeInterval": re.findall(r"deltaT\s+(\d*\.?\d*)?\s*;", controlDict_text)[0],
                            "runTimeModifiable": re.findall(r"deltaT\s+(.*)?\s*;", controlDict_text)[0],
                            "adjustTimeStep": re.findall(r"deltaT\s+(.*)?\s*;", controlDict_text)[0],
                            "maxCo": re.findall(r"maxCo\s+(\S+)?\s*;", controlDict_text)[0],
                            "maxAlphaCo": re.findall(r"maxAlphaCo\s+(\S+)?\s*;", controlDict_text)[0]}
            self.__controlDict = controlDict(control_dict)
        except IOError as e:
            self.__message += e

    def GetControlDict(self):
        return self.__controlDict

    def loadBoundary(self):
        # TODO: connect the boundary info to the display.
        # read in boundary patches of each region.

        for region in self.__regionName:
            if self.__regionProperty[region] == "default region":
                path = self.__caseFolder + "/constant/polyMesh/boundary"
            else:
                path = self.__caseFolder + "/constant/" + region + "/polyMesh/boundary"

            try:
                with open(path) as fid:
                    bc_text = stripFoamHead(fid.read())
            except IOError as e:
                self.__message += e
                return

            bc_text = re.findall(r"\((.*)\)", bc_text).split("}")[:-1]  # extract only the boundary definition part
            boundaries = {region: []}

            for bc in bc_text:
                bc_name = bc.split("{")[0]
                patch_type = re.findall(r"type\s+(\S+)\s*;", bc)[0]
                startFace = re.findall(r"startFace\s+(\d+)\s*;", bc)[0]
                nFaces = re.findall(r"nFaces\s+(\d+)\s*;", bc)[0]

                # TODO: more type of boundary, now limited to patch, wall, mappedWall, cyclicAMI.
                #  more: symmetry, empty...
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
                    boundaries[region].append(Patch(bc_name, region, patch_type, startFace, nFaces))
                elif patch_type == "mappedWall":
                    boundaries[region].append(
                        MappedWall(bc_name, region, patch_type, startFace, nFaces, sampleMode, samplePatch,
                                   sampleRegion))
                elif patch_type == "cyclicAMI":
                    boundaries[region].append(
                        CyclicAMI(bc_name, region, patch_type, startFace, nFaces, Tolerance, neighbourPatch, transform))
                else:
                    self.__message += "\nThe path type is not defined yet! \n"

    def differentiateMappedWall(self):
        # now pair the boundaries to make sure the mappedWall and cyclicAMI pair properly.
        # Change the patch name of mappedWall at fluid side to _shadow to avoid confusing.
        # just loop the solid region, slave corresponding fluid's patches.
        for region in self.__regionName:
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
                self.__message += e

        path_global = self.__caseFolder + "/system/decomposeParDict"
        parser(path_global, "global")

        if len(self.__regionName) == 1:
            return
        for region in self.__regionName:
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
                self.__message += e

        if len(self.__regionName) == 1:
            path = self.__caseFolder + "/constant/MRFProperties"
            self.__MRF["default region"] = parser(path)
        else:
            for region in self.__regionName:
                if self.__regionProperty[region] == "fluid":
                    path = self.__caseFolder + "/constant/" + region + "/MRFProperties"
                    self.__MRF[region].append(parser(path))

    def loadRadiation(self):
        self.__regionName

    def loadFvSchemes(self):
        self.__regionName

    def loadFvSolution(self):
        self.__regionName

    def loadInitialCondition(self):
        self.__regionName
        self.__turbulenceModel
        path = self.__caseFolder + "/0/"
        initial_fields = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]

        try:
            with open(path) as fid:
                text = stripFoamHead(fid.read)
            content = re.findall(r"dimensions\s+(.*?);.*internalField\s+(.*?);\s*boundaryField\s*\{(.*)\}", text)
        except IOError as e:
            self.__message += e

    def writeLog(self):
        with open(self.__caseFolder + "/myFoam.log", "a+") as fid:
            fid.write(self.__log)
            fid.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    def clearLog(self):
        open(self.__caseFolder + "/myFoam.log", 'w').close()

    def loadDynamicMesh(self):
        path = self.__caseFolder
        for region in self.__regionName:
            if region == "default region":
                dynamicPath = path + "/constant/dynamicMeshDict"
                try:
                    with open(path) as fid:
                        text = stripFoamHead(fid.read())

                except IOError as e:
                    self.__message += e


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


