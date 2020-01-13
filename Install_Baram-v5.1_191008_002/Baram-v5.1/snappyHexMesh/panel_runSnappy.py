#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelRunSnappyClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        
        self.GEN = generalClass(mainself)
        
    def runSnappy(self):       
   
        # entry
        self.wprecisionEntry = gtk.Entry()
        self.wprecisionEntry.set_size_request(80, 28)
        self.ncoreEntry = gtk.Entry()
        self.ncoreEntry.set_size_request(80, 28)

        self.entrys = [self.wprecisionEntry, self.ncoreEntry]
        self.entrykeys = ['writePrecision', 'nCores']
                                        
        # combo
        self.startCombo = gtk.combo_box_entry_new_text()
        self.startCombo.set_size_request(80, 28)
        self.startFrom = ['0', '1', '2']  
        for ii in self.startFrom:
            self.startCombo.append_text(ii)

        self.wformatCombo = gtk.combo_box_entry_new_text()
        self.wformatCombo.set_size_request(80, 28)
        self.wformat = ['ascii', 'binary']  
        for ii in self.wformat:
            self.wformatCombo.append_text(ii)
                
        self.partypeCombo = gtk.combo_box_entry_new_text()
        self.partypeCombo.set_size_request(100, 28)
        self.partype = ['SMP', 'Cluster']  
        for ii in self.partype:
            self.partypeCombo.append_text(ii)
        
        self.combos = [self.startCombo, self.wformatCombo, self.partypeCombo]
        self.combokeys = ['startFrom', 'writeFormat', 'parallelType']
        
        # checkbutton
        self.castelCB = gtk.CheckButton('castellate')
        self.snapCB = gtk.CheckButton('snap')
        self.layerCB = gtk.CheckButton('addLayer')
        self.compressCheck = gtk.CheckButton('Data compression')
        self.overwriteCB = gtk.CheckButton('overWrite')
        
        self.checkbuttons = [self.castelCB, self.snapCB, self.layerCB, self.compressCheck, self.overwriteCB]
        self.checkbuttonkeys = ['castellate', 'snap', 'layer', 'dataCompression', 'overwrite']        
                
        # button
        self.resetB = gtk.Button('Initialize')
        self.runAppB = gtk.Button('Start Run')
        #----------------------------------------------------------------------------------------------------      
        self.runbox = gtk.VBox(False, 5)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                
        label = gtk.Label()
        label.set_markup('<b>  Run snappyHexMesh  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.runbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)
                
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.castelCB, False, False, 5)      
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.snapCB, False, False, 5)       
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.layerCB, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.runbox.pack_start(separator, False, True, 5)                                     

        label = gtk.Label('Start from')           
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(self.startCombo, False, False, 2)               
       
        label = gtk.Label('Write precision')
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(self.wprecisionEntry, False, False, 2)
        
        label = gtk.Label('Write format')
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(self.wformatCombo, False, False, 2)
        
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.compressCheck, False, False, 2)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.runbox.pack_start(separator, False, True, 5)                                     

        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.overwriteCB, False, False, 5)
        
        label = gtk.Label('No. of cores')
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(self.ncoreEntry, False, False, 2)
                
        label = gtk.Label('Parallel type')
        label.set_size_request(100, 28)
        label.set_alignment(0, 0.5)
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(self.partypeCombo, False, False, 2)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.runbox.pack_start(separator, False, True, 5)                                     

        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(self.resetB, True, True, 5)
        hbox = gtk.HBox(False, 5)
        self.runbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(self.runAppB, True, True, 5)
        
        # connect
        self.partypeCombo.connect('changed', self.selhostfile)
        self.resetB.connect('clicked', self.resetMesh)
        self.runAppB.connect('clicked', self.applyrun)
                    
        self.setSavedValue()
        
        return self.runbox
        
    #------------------------------------------------------------------------
    def applyrun(self, widget):
    
        RUN=snappyHexMeshRunClass(self.caseDir, self.installpath, self.terminal)            
        
        runControlDict = {}
        for i in range(len(self.entrykeys)):
            runControlDict[self.entrykeys[i]] = self.entrys[i].get_text()
        for i in range(len(self.combokeys)):
            runControlDict[self.combokeys[i]] = self.combos[i].child.get_text()            
        for i in range(len(self.checkbuttons)):
            if self.checkbuttons[i].get_active() == 1:
                runControlDict[self.checkbuttonkeys[i]] = 'true'
            else:
                runControlDict[self.checkbuttonkeys[i]] = 'false'        

        aa = glob.glob(self.caseDir + '/system/settings/hostfilename')
        if aa:
            with open(aa[0], 'r') as f:
                runControlDict['hostfile'] = f.read()                
        else:
            runControlDict['hostfile'] = 'None'
        
        checklist = [runControlDict['writePrecision'], runControlDict['nCores']]
        errorstr = ['writePrecision', 'nCores']
        self.GEN.checkNumberSnappy(checklist, errorstr)
        
        self.GEN.pickleDump(self.caseDir + '/system/settings/snappyRunConditions', runControlDict)

        inputDictList = self.collectDicts(runControlDict)
        RUN.runSnappyHex(inputDictList, self.notebook)
    #------------------------------------------------------------------------
    def resetMesh(self, widget):
    
        results=self.GEN.getResult()
        serialResult = results[0]
        parallelResult = results[1]
        
        aa = glob.glob(self.caseDir + '/Running')
        if aa:
            os.system('rm ' + self.caseDir + '/Running')
        
        aa = glob.glob(self.caseDir + '/processor*')
        if aa:
            os.system('rm -r ' + self.caseDir + '/processor*')
        
        for kk in serialResult:
            os.system('rm -r ' + self.caseDir + '/' + kk)
        
        aa = glob.glob(self.caseDir + '/constant/polyMesh/*')
        for ii in aa:
            if ii != self.caseDir + '/constant/polyMesh/blockMeshDict':
                os.system('rm ' + ii)
        os.system('blockMesh -case ' + self.caseDir)        
    #------------------------------------------------------------------------
    def setSavedValue(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/snappyRunConditions')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            
            for i in range(len(self.entrykeys)):
                self.entrys[i].set_text(dic[self.entrykeys[i]])              
            for i in range(len(self.combokeys)):
                self.combos[i].child.set_text(dic[self.combokeys[i]])
            for i in range(len(self.checkbuttons)):
                if dic[self.checkbuttonkeys[i]] == 'true':
                    self.checkbuttons[i].set_active(1)
                else:
                    self.checkbuttons[i].set_active(0)
        else:
            self.setDefaultValue()
    #---------------------------------------------------------------------------------------------
    def setDefaultValue(self):
    
        self.wprecisionEntry.set_text('6')
        self.ncoreEntry.set_text('1')
        self.startCombo.set_active(0)   
        self.wformatCombo.set_active(0)
        self.partypeCombo.set_active(0)
        self.castelCB.set_active(1)
        self.snapCB.set_active(1)
        self.layerCB.set_active(1)
        self.overwriteCB.set_active(1)        
    #------------------------------------------------------------------------
    def selhostfile(self, widget):
    
        partype=widget.child.get_text()
        if partype == 'Cluster':        
            dialog = gtk.FileChooserDialog("Open..", None,gtk.FILE_CHOOSER_ACTION_OPEN, 
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                hostfilename = dialog.get_filename()
            elif response == gtk.RESPONSE_CANCEL:
                hostfilename = 'None'
            dialog.destroy()       

            if hostfilename == 'None':
                widget.set_active(0) 
        else:
            hostfilename = 'None'
        f = open(self.caseDir + '/system/settings/hostfilename','w')
        f.write('hostfile;' + hostfilename + '\n')
        f.close()  
    #------------------------------------------------------------------------
    def collectDicts(self, runControlDict):
        
        aa = glob.glob(self.caseDir + '/system/settings/stlFileSetup')
        if aa:
            stlDict = self.GEN.pickleLoad(aa[0])
        else:
            self.GEN.makeDialog('Error!!! stl 파일이 선택되지 않았습니다.')
            return

        aa = glob.glob(self.caseDir + '/system/settings/featureAngle')
        if aa:
            with open(aa[0], 'r') as f:
                featureAngle = f.read()
        else:
            featureAngle = '150'
            
                        
        aa = glob.glob(self.caseDir + '/system/settings/objectRefine-*')
        objDict = {}
        if aa:
            for i in range(len(aa)):
                dic = self.GEN.pickleLoad(aa[i])
                objDict[dic['objectname']] = dic
           
        aa = glob.glob(self.caseDir + '/system/settings/blockMeshSetup')
        if aa:
            blockDict = self.GEN.pickleLoad(aa[0])
        else:
            self.GEN.makeDialog('Error!!! blockMesh가 설정되지 않았습니다.')
            return

        aa = glob.glob(self.caseDir + '/system/settings/castellateSetup')
        if aa:
            castelDict = self.GEN.pickleLoad(aa[0])
        else:
            self.GEN.makeDialog('Error!!! castellate mesh가 설정되지 않았습니다.')
            return        

        aa = glob.glob(self.caseDir + '/system/settings/snapSetup')
        if aa:
            snapDict = self.GEN.pickleLoad(aa[0])
        else:
            snapDict['nSmoothPatch'] = '3'
            snapDict['tolerance'] = '3'
            snapDict['nSolveIter'] = '30'
            snapDict['nRelaxIter'] = '5'
            snapDict['nFeatureSnapIter'] = '15'
            snapDict['implicitFeatureSnap'] = 'false'
            snapDict['explicitFeatureSnap'] = 'true'
            snapDict['multiRegionFeatureSnap'] = 'false'            

        aa = glob.glob(self.caseDir + '/system/settings/layerSetup')
        if aa:
            layerDict = self.GEN.pickleLoad(aa[0])
        else:
            if runControlDict['layer'] == 'true':
                self.GEN.makeDialog('Error!!! boundary layer가 설정되지 않았습니다.')
                return                        
            
            layerlist = ['relativesize', 'expansionRatio', 'thickmethod', 'firstthick', 'finalthick', 'overallthick',
                         'minThickness', 'nlayers', 'nGrow', 'featureAngle', 'nRelaxIter', 'nSmoothSurfaceNormals',
                         'nSmoothNormals', 'nSmoothThickness', 'maxFaceThicknessRatio', 'maxThicknessToMedialRatio',
                         'minMedianAxisAngle', 'nBufferCellsNoExtrude', 'nLayerIter', 'nRelaxedIter']
            layervalue = ['true', '1.2', 'firstLayer', '0.3', '0.3', '0.3', '0.2', '5', '0', '60',
                          '10', '1', '3', '10', '0.5', '0.3', '90', '0', '50', '20']     
            layerDict = {}            
            for i in range(len(layerlist)):
                layerDict[layerlist[i]] = layervalue[i]            
            layerDict['stlnames'] = stlDict.keys()
            layerDict['layerOnOff'] = []
            for i in range(len(layerDict['stlnames'])):
                layerDict['layerOnOff'].append(1)

        aa = glob.glob(self.caseDir + '/system/settings/advancedSnappySetup')
        if aa:
            advDict = self.GEN.pickleLoad(aa[0])
        else:
            meshquality = ['maxNonOrtho', 'maxBoundarySkewness', 'maxInternalSkewness', 'maxConcave', 'minVol',
                           'minTetQuality', 'minArea', 'minTwist', 'minDeterminant', 'minFaceWeight', 'minVolRatio',
                           'minTriangleTwist', 'nSmoothScale', 'errorReduction', 'relaxedMaxNonOrtho']
            meshqualityvalue = ['65', '20', '4', '80', '1e-13', '1e-9', '-1', '0.05', '0.001', 
                                '0.05', '0.01', '-1', '4', '0.75', '75']
            advDict = {}
            for i in range(len(meshquality)):
                advDict[meshquality[i]] = meshqualityvalue[i]
            advDict['mergeTolerance'] = '1e-6'
                            
        inputDictList = [stlDict, featureAngle, objDict, blockDict, castelDict, snapDict, layerDict, advDict, runControlDict]
        
        return inputDictList
    #------------------------------------------------------------------------

  
    
    


