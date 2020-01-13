#-*-coding:utf8-*-

from common.fromAll     import *

class solverRunClass:

    def __init__(self,mainself):
    
        self.caseDir = mainself.caseDir
        self.installpath = mainself.installpath
        self.terminal = mainself.terminal
        self.notebook = mainself.notebook        
      
        self.GEN = generalClass(self)
        self.WFILE = writeFileClass(self.caseDir)
        self.WFILEBC = writeBCFileClass(self)
        self.DEFAULT = defaultValueClass(self)        
    #-----------------------------------------------------------------------------------------------------------
    def initialize(self):

        if self.isSolverRunning():
            self.GEN.makeDialog('Solver is Running')
            return

        savedResult = self.GEN.getResult()
        if len(savedResult[0]) != 0 or len(savedResult[1]) != 0:                       
            res = self.GEN.makeDialog_question('All the saved data will be deleted. OK?')
            if res == -9:
                return
            else:
                savedResult = self.GEN.getResult()
                for ii in savedResult[0]:
                    os.system('rm -r ' + self.caseDir + '/'+ii)                
                if len(savedResult[1]) != 0:
                    os.system('rm -r ' + self.caseDir + '/processor*')
                if os.path.isdir(self.caseDir + '/postProcessing'):
                    os.system('rm -r ' + self.caseDir + '/postProcessing')
                
                self.makeFiles()
    #-----------------------------------------------------------------------------------------------------------
    def runSolver(self):
    
        if self.isSolverRunning():
            self.GEN.makeDialog('Solver is Running')
            return         

        self.makeFiles()

        if self.runDict['startFrom']=='startTime':
            setConditions = 'setConditions -case ' + self.caseDir + ' -time ' + self.runDict['startTime']
        else:
            setConditions = 'setConditions -case ' + self.caseDir + ' -latestTime'
        
        WFILE = writeFileClass(self.caseDir)
        WFILE.turbulenceProperties(self.simDict)
        os.system(setConditions)
        
        if self.simDict['radiationModel'] == 'P1' or self.simDict['radiationModel'] == 'fvDOM':
            WFILE.modifyFvSolutionForRad(self.simDict)
        if self.simDict['Turbulence model'] == 'laminar':
            WFILE.modifyTurbulence()
        
        self.notebook.set_current_page(1)
        self.makeRunFile(self.caseDir)
        os.system('chmod +x ' + self.caseDir + '/runSolver')
        
        logDir = self.caseDir + '/system/settings'        
        cmd = self.caseDir + '/runSolver & \n' + 'echo $! > ' + logDir + '/runPID' + '\n'
        self.terminal.feed_child(cmd,len(cmd))        
    #----------------------------------------------------------------------------------
    def makeRunFile(self,caseDir):
    
        nCore = self.runDict['nCores']
        plotresidual = self.runDict['plotResidual']
        smpOrCluster = self.runDict['machineType']
        hostfile = self.runDict['hostfile']
        startFrom = self.runDict['startFrom']
        startTime = self.runDict['startTime']

        results = self.GEN.getResult()        
        serialResult = results[0]
        parallelResult = results[1]
        
        run_serial_plot = 'pyFoamPlotRunner.py --no-continuity ' + self.solver + ' -case ' + caseDir
        run_serial_noplot = 'pyFoamRunner.py ' + self.solver + ' -case ' + caseDir        
        run_par_smp_plot = 'pyFoamPlotRunner.py --no-continuity mpirun -np ' + nCore + ' ' + self.solver + ' -case ' + caseDir + ' -parallel'
        run_par_smp_noplot = 'pyFoamRunner.py mpirun -np ' + nCore + ' ' + self.solver + ' -case ' + caseDir + ' -parallel' 
        run_par_cluster_plot = 'pyFoamPlotRunner.py --no-continuity mpirun --hostfile ' + hostfile + ' -np ' + nCore + ' ' + self.solver + ' -case ' + caseDir + ' -parallel'
        run_par_cluster_noplot = 'pyFoamRunner.py  mpirun --hostfile ' + hostfile + ' -np ' + nCore + ' ' + self.solver + ' -case ' + caseDir + ' -parallel'        
        
        rf = open(caseDir + '/runSolver','w')

        if glob.glob(caseDir + '/postProcessing') != []:
            rf.write('rm -r ' + caseDir + '/postProcessing\n')
        if glob.glob(caseDir + '/PyFoam*') != []:
            rf.write('rm -r ' + caseDir + '/PyFoam*\n')
	
        if nCore == '1':
            if len(parallelResult) == 0:
                self.GEN.clearParallel()
            else:
                if startForm == 'latestTime':
                    rf.write('reconstructNPar -case /' + caseDir + ' -latestTime\n')
                else:
                    if startTime ==' 0':
                        self.GEN.clearParallel()
                    else:
                        if self.GEN.isTherInList(parallelResult,startTime) == 'true':
                            rf.write('reconstructNPar -case /' + caseDir + ' -latestTime\n')
                        else:
                            self.GEN.makeDialog('Error!!! there is not saved data at startTime ' + startTime)
                            return                        

            if plotresidual == 'yes':
                rf.write(run_serial_plot + '\n')
            else:
                rf.write(run_serial_noplot + '\n')

        else:# parallel
            nCorePrev = str(len(glob.glob(caseDir + '/processor*')))
            if nCore == nCorePrev:
                
                if startFrom == 'startTime' and startTime == '0':
                    self.GEN.clearResult(serialResult, '0')
                    self.GEN.clearResult(parallelResult, '1')
                elif startFrom == 'startTime' and startTime != '0':
                    if isThereInList(parallelResult,startTime) == 'false':
                        self.GEN.makeDialog('Error!!! there is not saved data at startTime ' + startTime)
                        return                    
                
                self.GEN.clearResult(serialResult, '0')                
                
                if smpOrCluster == 'SMP':
                    if plotresidual == 'yes':
                        rf.write(run_par_smp_plot + '\n')
                    else:
                        rf.write(run_par_smp_noplot + '\n')
                else:
                    if plotresidual == 'yes':
                        rf.write(run_par_cluster_plot + '\n')
                    else:
                        rf.write(run_par_cluster_noplot + '\n')
            
            else:
                if nCorePrev == '0':
                    if 'startFrom' == 'startTime' and startTime != '0':
                        if isThereInList(parallelResult,startTime) == 'false':
                            self.GEN.makeDialog('Error!!! there is not saved data at startTime ' + startTime)
                            return                      
                    rf.write('decomposeNPar -force -case ' + caseDir + '\n')
                else:
                    self.GEN.clearResult(serialResult,'0')
                    if startFrom == 'startTime' and startTime != '0':
                        if isThereInList(parallelResult,startTime) == 'false':
                            self.GEN.makeDialog('Error!!! there is not saved data at startTime ' + startTime)
                            return
                        else:
                            rf.write('reconstructNPar -time '+startTime+' -case ' + caseDir + '\n')  
                    elif startFrom == 'latestTime':
                        if parallelResult != []:
                            rf.write('reconstructNPar -latestTime -case ' + caseDir + '\n')

                    rf.write('decomposeNPar -force -case ' + caseDir + '\n')                

                if smpOrCluster == 'SMP':
                    if plotresidual == 'yes':
                        rf.write(run_par_smp_plot + '\n')
                    else:
                        rf.write(run_par_smp_noplot + '\n')
                else:
                    if plotresidual == 'yes':
                        rf.write(run_par_cluster_plot + '\n')
                    else:
                        rf.write(run_par_cluster_noplot + '\n')

        rf.close()
    #----------------------------------------------------------------------------------
    def makeFiles(self):
    
        self.collectDicts()
        self.solver = self.simDict['solver']                            
        self.WFILEBC.boundaryConditions(self.simDict, self.iniDict, self.bcTypeDict, self.bcValueDict, self.AMIDict)
        self.WFILEBC.initialConditions(self.iniDict, self.simDict)
        self.WFILE.controlDictFile(self.runDict, self.solver)
        self.WFILE.decomposeParDict(self.runDict['nCores']) 
    #----------------------------------------------------------------------------------
    def collectDicts(self):   
    
        dicts = self.DEFAULT.defaultDict()
    
        self.simDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')
        if self.simDict == None:
            self.simDict = dicts[0]
            
        self.iniDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/initialSettings')
        if self.iniDict == None:
            self.iniDict = dicts[1]
        
        self.runDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/runConditions')        
        if self.runDict == None:
            self.runDict = dicts[2]
        
        self.bcTypeDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/boundaryTypes')        
        if self.bcTypeDict == None:
            self.bcNameList, self.polyTypeList = self.GEN.getBCName()
            self.bcTypeDict = {}
            for i in range(len(self.bcNameList)):
                if self.polyTypeList[i] == 'patch':
                    upper = self.bcNameList[i].upper()
                    if 'OUT' in upper:
                        self.bcTypeDict[self.bcNameList[i]] = 'pressureOutlet' 
                    else:
                        self.bcTypeDict[self.bcNameList[i]] = 'surfaceNormalVelocityInlet'
                elif self.polyTypeList[i] == 'wall':
                    self.bcTypeDict[self.bcNameList[i]] = 'adiabaticWall'
                elif self.polyTypeList[i] == 'mappedWall':
                    self.bcTypeDict[self.bcNameList[i]] = 'thermoCoupledWall'                 
                else:                
                    self.bcTypeDict[self.bcNameList[i]] = self.polyTypeList[i]

        self.bcValueDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/boundaryValues')        
        if self.bcValueDict == None:
            self.bcValueDict = {}            
            keys = ['velocity_x', 'velocity_y', 'velocity_z', 'Umag', 'massFlowRate', 'rho', 'volumeFlowRate',
                    'totalPressure', 'staticPressure',
                    'temperature', 'heatFlux', 'h', 'Ta', 'totalTemperature',
                    'turbulentIntensity', 'viscosityRatio', 'nuTilda',            
                    'velocityMode', 'movingVelocity_x', 'movingVelocity_y', 'movingVelocity_z',
                    'rotatingOrigin_x', 'rotatingOrigin_y', 'rotatingOrigin_z', 'rotatingAxis_x', 'rotatingAxis_y', 'rotatingAxis_z', 'RPM']
                   
            values = ['1', '0', '0', '1', '1', '1', '1',
                      '0', '0',
                      '300', '1000', '100', '300', '300',
                      '0.001', '10', '1e-8',
                      'noSlip', '0', '0', '0', '0', '0', '0', '0', '0', '1', '100']                      
                    
            for i in range(len(self.bcNameList)):
                self.bcValueDict[self.bcNameList[i]] = {}
                for j in range(len(keys)):
                    self.bcValueDict[self.bcNameList[i]][keys[j]] = values[j]

        self.AMIDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/AMIConditions')        
        if self.AMIDict == None:
            self.AMIDict = {}
    #----------------------------------------------------------------------------------
    def isSolverRunning(self): 
        pidfile = self.caseDir + '/system/settings/runPID'
        if os.path.isfile(pidfile):
            with open(pidfile, 'r') as ff:
                pid = ff.read()
            if self.GEN.isRunning(int(pid)):
                return True
        else:
            return False
    #----------------------------------------------------------------------------------

  


