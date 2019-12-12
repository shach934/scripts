import os
import re

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


class rotationProp(object):
    def __init__(self, origin=(0, 0, 0), axis=(0, 0, 1), omega=20):
        self.origin = origin
        self.aixs = axis
        self.omega = omega


class OpenFOAMCase(object):
    def __init__(self):
        self.__numberOfRegions = 1
        self.__regionName = []
        self.__regionProperty = []
        self.__caseFolder = ""
        self.__caseName = ""
        self.__patches = []
        self.__boundaries = []
        self.__message = "Ready! Let's GO!\n\n"
        self.__solver = {}
        self.__fvSchemes = {}
        self.__fvSolution = {}
        self.__fvOption = {}
        self.__MRF = {}
        self.__dynamicMesh = {}
        self.__radiation = {}
        self.__initial = {}
        self.__alpha = {}

    def SetFolderName(self, caseFolder=("", "")):
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

    def SetRegionName(self, regionsName=[""]):
        self.__regionName = regionsName

    def SetRegionProperty(self):
        if len(self.__regionName) > 1:
            self.__regionProperty.append("fluid")

        zero_folder = self._caseFolder + "/0/"
        constant_folder = self._caseFolder + "/constant/"
        system_folder = self._caseFolder + "/system/"

        if os.path.exists(constant_folder + "regionProperties"):
            with open(constant_folder + "regionProperties") as fid:
                text = fid.read()

            fluid_regions = re.findall(r"fluid.*\((.*)?\)", text)[0].split()
            solid_regions = re.findall(r"solid.*\((.*)?\)", text)[0].split()

            regions = fluid_regions + solid_regions
            regions = [name for name in regions if len(name)]  # maybe there is no fluid or solid region at all.
            regions.sort()

            regions2 = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
            regions2.sort()

            regions3 = [name for name in os.listdir(zero_folder) if os.path.isdir(zero_folder + "/" + name)]
            regions3.sort()

            regions4 = [name for name in os.listdir(system_folder) if os.path.isdir(system_folder + "/" + name)]
            regions4.sort()

            if regions != regions2 or regions != regions3 or regions != regions4:
                self.__message += "\nThe multiRegion folder structure is NOT correct! Check again! \n"
            else:
                region_info = {}
                for reg in solid_regions:
                    if len(reg):
                        region_info[reg] = "solid"
                for reg in fluid_regions:
                    if len(reg):
                        region_info[reg] = "fluid"

        else:
            self.__message += "\nSingle region case, default fluid region exists!\n"


with open(foam_path + "/system/controlDict", 'r') as fid:
    text = fid.read()

# solver, end time and save interval. 
solver = re.findall(r"application (.*);", text)[0]
endT = int(re.findall(r"endTime.*?(\d+)\.?;", text)[0])
write_interval = int(re.findall(r"writeInterval.*?(\d+)\.?;", text)[0])

# regions read from the folders. 
regions = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
regions.sort()

# check if this is a multiRegion case, and load the regions' name if so. 
if os.path.exists(constant_folder + "regionProperties"):
    with open(constant_folder + "regionProperties", 'r') as fid:
        text = fid.read()
else:
    print("This is a pure fluid problem!\nCheck the solver again!\n")
    os.sys.exit()

fluid_regions = re.findall(r"fluid.*\((.*)?\)", text)[0].split()
solid_regions = re.findall(r"solid.*\((.*)?\)", text)[0].split()

regions2 = fluid_regions + solid_regions
regions2.sort()

if regions != regions2:
    print("The multiRegion folder structure is NOT correct! Check again! \n")
    os.sys.exit()

# read in boundary patches of each region.
boundaries = {}
for region in regions:

    # loop over each region 
    path = constant_folder + region + "/polyMesh/boundary"

    # load the boundary file for this region
    with open(path, 'r') as fid:
        text = fid.read()

    file_head = re.findall(r"(.*)\d+.*\(.*\)", text)

    text = text.replace("\n", "")
    text = text.replace("\t", "")

    file_head = re.findall(r"FoamFile.*?\{(.*?)\}", text)

    # here the replace number is hard coded, as the OpenFOAM file head has 5 input in total, if something wrong, change it here.
    file_head = file_head[0].replace(";", ";\n\t", 4)
    file_head = file_head.replace(" ", "\t\t")
    file_head = "FoamFile\n{\n\t" + file_head + "\n}\n"

    bcs = re.findall(r".*(\d+)\((.*)\)", text)
    N_bc, bc_text = int(bcs[0][0]), bcs[0][1].split("}")[:-1]
    # print(bc_text)
    boundaries[region] = []

    for bc in bc_text:
        print(bc)
        bc_name = bc.split("{")[0]

        patch_type = re.findall(r"type (\S+);", bc)[0]
        startFace = re.findall(r"startFace (\d+);", bc)[0]
        nFaces = re.findall(r"nFaces (\d+);", bc)[0]
        # print(patch_type + startFace + nFaces)

        if patch_type == "mappedWall":
            sampleMode = re.findall(r"sampleMode (\S+);", bc)[0]
            sampleRegion = re.findall(r"sampleRegion (\S+);", bc)[0]
            samplePatch = re.findall(r"samplePatch (\S+);", bc)[0]

        elif patch_type == "cyclicAMI":
            Tolerance = re.findall(r"Tolerance (\S+);", bc)[0]
            neighbourPatch = re.findall(r"neighbourPatch (\S+);", bc)[0]
            transform = re.findall(r"transform (\S+);", bc)[0]

        elif patch_type != "patch" and patch_type != "wall":
            print("I don't know the patch type! \nCheck again!")

        if patch_type == "wall" or patch_type == "patch":
            boundaries[region].append(Patch(bc_name, region, patch_type, startFace, nFaces))
        elif patch_type == "mappedWall":
            boundaries[region].append(
                MappedWall(bc_name, region, patch_type, startFace, nFaces, sampleMode, samplePatch, sampleRegion))
        elif patch_type == "cyclicAMI":
            boundaries[region].append(
                CyclicAMI(bc_name, region, patch_type, startFace, nFaces, Tolerance, neighbourPatch, transform))
        else:
            print("No suitable patch class for this boundary! \n")

# now pair the boundaries to make sure the mappedWall and cyclicAMI pair properly. 
# Change the patch name of mappedWall at fluid side to _shadow to avoid confusing.
# just loop the solid region, slave correspoinding fluid's patches.
for region in solid_regions:
    boundary = boundaries[region]
    for patch in boundary:

        if patch.type == "mappedWall" and patch.name == patch.samplePatch:

            patch2change = patch.samplePatch
            patch.samplePatch = patch.samplePatch + "_shadow"

            candidate_patches = boundaries[patch.sampleRegion]
            found = False
            for patch in candidate_patches:
                # check the corresponding slave patch is mappedWall type
                if patch.name == patch2change and patch.type != "mappedWall":
                    print("Check the patch type, it is not a mappedWall!\n")
                    found = True
                # check the corresponding slave patch is mapped to the master patch.    
                elif patch.name == patch2change and patch.samplePatch == patch2change:
                    patch.name = patch.name + "_shadow"
                    found = True
            if not found:
                print("Didn't found the mappedWall slave in corresspoding region! Check again!\n")

        elif patch.type == "mappedWall" and patch.name != patch.samplePatch:
            print("Master and slave mappedWall are differentiated already!\n")

# pair and differentiate the AMI master and slave later.... TO DO! 

turbulance_model = {}
# read in the turbulance model.

for region in fluid_regions:
    turbulance_path = constant_folder + "/" + region + "/turbulenceProperties"
    if os.path.isfile(turbulance_path):
        with open(turbulance_path, "r") as fid:
            text = fid.read()
        simulationType = re.findall(r"simulationType (.*);?", text)[0]
        turbulance_model[region] = simulationType

        if simulationType == "RAS":
            RASModel = re.findall(r"RASModel (.*);?", text)[0]
            turbulance = re.findall(r"turbulence (.*);?", text)[0]
            printCoeffs = re.findall(r"printCoeffs (.*);?", text)[0]
            turbulance_model["RASModel"] = RASModel
            turbulance_model["turbulence"] = turbulance
            turbulance_model["printCoeffs"] = printCoeffs

        elif simulationType == "laminar":
            print("Turbulance model of region " + region + " is laminar, check again!\n")

    else:
        print("The turbulanceProperties doesn't exist for fluid " + region + "!, check again! \n")

wallDist = "method meshWave"
interpolationSchemes = "default linear"

if __name__ == "__main__":
    pass
