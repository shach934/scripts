Development document for the myFoam GUI
main file structure:

* [main.py](main.py)

* [OpenFOAMCase.py](OpenFOAMCase.py)
    * class Patch(object)
    * class MappedWall(Patch)
    * class CyclicAMI(Patch)
    * class turbulenceModel(object)
        * def SetTurbulenceModel(self, turbulence)
    * class rotationProp(object)
    * class controlDict(object)
    * class MRF(object)
    * class decomposePar(object)
    * class postFunction(object)
    * class OpenFOAMCase(object)
        * def SetFolderAndName(self, caseFolder=("", ""))
        * def GetCasePath(self)
        * def GetCaseName(self)
        * def SetRegionProperty(self, regionNameFromVTK)
        * def GetRegionProperty(self)
        * def loadTurbulenceModel(self)
        * def loadSolverInfo(self)
        * def GetControlDict(self)
        * def loadBoundary(self)
        * def differentiateMappedWall(self)
        
        * def writeLog(self)
        * def clearLog(self)
* [Global.py](Global.py)
* [images](images)
* [ccm.py](ccm.py)
* [settingBox.py](settingBox.py)

OpenFOAMCase.message keeps the message during operation and promote it to output region.
The log parameter will keep all the message and the time stamp and write it to the log file before the close window.
