#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class snappyHexMeshRunClass:

    def __init__(self, caseDir, installpath, terminal):
    
        self.caseDir = caseDir
        self.installpath = installpath
        self.terminal = terminal
        
    def runSnappyHex(self, inputDictList, notebook):
       
        stlDict = inputDictList[0]
        stlList = stlDict.keys()
        stlList.sort()
        
        featureAngle = inputDictList[1]
        objDict = inputDictList[2]
        blockDict = inputDictList[3]
        castelDict = inputDictList[4]
        snapDict = inputDictList[5]
        layerDict = inputDictList[6]
        advDict = inputDictList[7]
        runDict = inputDictList[8]

        nCore = runDict['nCores']
        startFrom = runDict['startFrom']
        smpOrCluster = runDict['parallelType']
        hostfile = runDict['hostfile']
        overwrite = runDict['overwrite']

        WFILE = writeFileClassSnappy(self.caseDir)
	
        if not os.path.isfile(self.caseDir + '/Running'):
            WFILE.decomposeParDict(nCore)
            WFILE.controlDictFile(runDict)
            WFILE.makeFeatureFile(stlList,featureAngle)
            WFILE.creatPatchNone()

            WFILE.snappyHexMeshDict(inputDictList)
            os.system('surfaceFeatureExtract -case ' + self.caseDir)
            self.snappyHexMeshRun(startFrom, nCore, smpOrCluster, hostfile, overwrite, notebook)
        else:
            messa = "snappyHexMesh is Running or stopped by cotrol-C.\n if stopped by control-C, initialize first"
            md = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, messa)
            md.run()
            md.destroy()
    #----------------------------------------------------------------------------------
    def snappyHexMeshRun(self, startFrom, nCore, smpOrCluster, hostfile, overwrite, notebook):

        GEN = generalClass(self)
        a1 = glob.glob(self.caseDir + '/1')
        a2 = glob.glob(self.caseDir + '/2')
        a3 = glob.glob(self.caseDir + '/3')
        
        if startFrom == '0':
            if a1 != []:
                os.system('rm -r ' + a1[0])
            if a2 != []:
                os.system('rm -r ' + a2[0])
            if a3 != []:
                os.system('rm -r ' + a3[0])                                    
        elif startFrom == '1':
            if a2 != []:
                os.system('rm -r ' + a2[0])
            if a3 != []:
                os.system('rm -r ' + a3[0])            
            if a1 == []:
                GEN.makeDialog('Error!!! There is not "1" folder')            
        elif startFrom == '2':
            if a3 != []:
                os.system('rm -r ' + a3[0])
            if a2 == []:
                GEN.makeDialog('Error!!! There is not "2" folder')
        
        notebook.set_current_page(1) 
        
        rf = open(self.caseDir + '/runSolver', 'w')
        rf.write('touch ' + self.caseDir + '/Running \n')        

        if nCore == '1':#serial
            aa = glob.glob(self.caseDir + '/processor*')
            if aa:
                rf.write('rm -r ' + self.caseDir + '/processor*\n')
                
            if overwrite == 'false':
                rf.write('snappyHexMesh -case ' + self.caseDir + '\n')
            else:
                rf.write('snappyHexMesh -overwrite -case ' + self.caseDir + '\n')

        else:#parallel
            rf.write('decomposePar -force -case ' + self.caseDir + '\n')
            if smpOrCluster == 'SMP':
                if overwrite == 'false':
                    rf.write('mpirun -np ' + nCore + ' snappyHexMesh -case ' + self.caseDir + ' -parallel \n')
                else:
                    rf.write('mpirun -np ' + nCore + ' snappyHexMesh -overwrite -case ' + self.caseDir + ' -parallel \n')
            else:
                if overwrite == 'false':
                    rf.write('mpirun --hostfile ' + hostfile + ' -np '+nCore+' snappyHexMesh -case ' + self.caseDir + ' -parallel \n')
                else:
                    rf.write('mpirun --hostfile ' + hostfile + ' -np '+nCore+' snappyHexMesh -overwrite -case ' + self.caseDir + ' -parallel \n')
            rf.write('reconstructParMesh -constant -mergeTol 1e-06\n')

        rf.write('createPatch -overwrite -case ' + self.caseDir + '\n')

        rf.write('rm ' + self.caseDir + '/Running \n')
        rf.close()
        os.system('chmod +x ' + self.caseDir + '/runSolver')
        
        cmd = self.caseDir + '/runSolver\n'
        self.terminal.feed_child(cmd,len(cmd))






         

  


