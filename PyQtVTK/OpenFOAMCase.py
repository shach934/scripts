import os
import re
from datetime import datetime
from math import pi

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
    def __init__(self, origin=(0, 0, 0), axis=(0, 0, 1), omega=20):
        self.origin = origin
        self.axes = axis
        self.omega = (omega * 2 * pi) / 60  # the unit is rpm.


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
    def __init__(self):
        self.name = ""
        self.cellZone = ""
        self.rotation = rotationProp()


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
        self.__dynamicMesh = {}
        self.__radiation = {}
        self.__initial = {}
        self.__alpha = {}
        self.__turbulenceModel = {}
        self.__message = "Ready! Let's GO!\n\n"
        self.__timeStamp = datetime.now.strftime("%H:%M:%S")

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

            if os.path.exists(constant_folder + "regionProperties"):
                with open(constant_folder + "regionProperties") as fid:
                    text = fid.read()

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
            else:
                self.__message += "\nThe regionProperties dict is missing, cannot define solid and fluid region!\n"
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
            elif self.__regionProperty[region] == "fluid":  # multiregion case, read only fluid region.
                turbulence_file_path = self.__caseFolder + "/constant/" + region + "/turbulenceProperties"

            if os.path.isfile(turbulence_file_path):
                with open(turbulence_file_path) as fid:
                    text = fid.read()
                simulationType = re.findall(r"simulationType\s* (.*);?", text)[0]
                turbulence_model[region] = simulationType
                if simulationType == "RAS":
                    turbulence_model["RASModel"] = re.findall(r"RASModel (.*);?", text)[0]
                    turbulence_model["turbulence"] = re.findall(r"turbulence (.*);?", text)[0]
                    turbulence_model["printCoeffs"] = re.findall(r"printCoeffs (.*);?", text)[0]
                self.__turbulenceModel[region] = turbulenceModel(turbulence_model)
            else:
                self.__message += "\nturbulenceProperties file is missing for region: " + region + ".\n"

    def loadSolverInfo(self):

        if os.path.isfile(self.__caseFolder + "/system/controlDict"):
            with open(self.__caseFolder + "/system/controlDict") as fid:
                controlDict_text = fid.read()
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
        else:
            self.__message += "\nThe controlDict is missing. \n"

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

            if os.path.isfile(path):
                with open(path) as fid:
                    bc_text = fid.read()
            else:
                self.__message += "\nThe boundary file for region:" + " is not exist!\n"
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

