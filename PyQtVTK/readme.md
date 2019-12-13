Development document for the myFoam GUI
main file structure:

* [main.py](main.py)

* [OpenFOAMCase.py](OpenFOAMCase.py)
    * class Patch(object):
    * class MappedWall(Patch):
    * class CyclicAMI(Patch):
    * class turbulenceModel(object):
        * def SetTurbulenceModel(self, turbulence):
    * class rotationProp(object):
    * class controlDict(object):
    * class MRF(object):
    * class postFunction(object):
    * class OpenFOAMCase(object):
        * def SetFolderAndName(self, caseFolder=("", "")):
        * def GetCasePath(self):
        * def GetCaseName(self):
        * def SetRegionProperty(self, regionNameFromVTK):
        * def GetRegionProperty(self):
        * def loadTurbulenceModel(self):
        * def loadSolverInfo(self):
        * def GetControlDict(self):
        * def loadBoundary(self):
        * def differentiateMappedWall(self):
* [Global.py](Global.py)
* [images](images)
* [ccm.py](ccm.py)
* [settingBox.py](settingBox.py)
