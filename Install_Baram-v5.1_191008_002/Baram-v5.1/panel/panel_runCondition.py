#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelRunConditionClass:

    def __init__(self, mainself):

        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.solver = mainself.solver
        self.gvtk = mainself.gvtk

        self.GEN = generalClass(mainself)
        self.WFILE = writeFileClass(self.caseDir)
        self.DEFAULT = defaultValueClass(self)
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  

    def runCondition(self):

        self.runbox = gtk.VBox()
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.runbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Run Conditions  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox)           
        
        self.vpan = gtk.VPaned()
        self.runbox.pack_start(self.vpan, True, True, 0)

        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 10)

        self.vpan.pack1(swin, False, True)
        self.vpan.pack2(swin1, False, True)

        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        swin.add_with_viewport(ebox)
        ebox1 = gtk.EventBox()
        ebox1.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        swin1.add_with_viewport(ebox1)
        self.mainbox = gtk.VBox(False, 0)
        ebox.add(self.mainbox)
        self.valuebox = gtk.VBox(False, 0)
        ebox1.add(self.valuebox)
        #-------------------------------------------------------------------------------------
        self.simDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')        
        if self.simDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.simDict = dicts[0]

        self.setFileRun = self.caseDir + '/system/settings/runConditions'
        self.loadRunDict()
        self.getStoreDict()
        #-------------------------------------------------------------------------------------       
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool, str)
        
        self.treeview = gtk.TreeView(self.treestore)
        
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(False)
        
        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1 = gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)

        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.renToggle = gtk.CellRendererToggle()                  
        self.ren1 = gtk.CellRendererCombo()                  

        self.ren0.set_property('editable', False)
        self.renToggle.set_property('activatable', True)
        self.ren1.set_property('editable', True)
        self.ren1.set_property('text-column', 0)
        
        self.ren0.set_fixed_size(170, -1)       

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False) 
        self.tvcolumn1.pack_start(self.renToggle, False)
        self.tvcolumn1.pack_start(self.ren1, False)
        
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, text = 1)  
        self.tvcolumn1.add_attribute(self.renToggle, 'active', 2)

        
        self.renToggle.connect('toggled',self.toggleRen, self.treestore)
        self.ren1.connect('edited', self.changeValue)        
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func)
        
        self.getTreeStore()        
        self.treeview.expand_all()        
        self.mainbox.add(self.treeview)
        
        # button     
        self.runAppB = gtk.Button('Start Run')
        self.runAppB.set_size_request(150, 28)
        self.runAppB.connect('clicked', self.applyrun)
        self.initializeB = gtk.Button('Initialize')
        self.initializeB.set_size_request(150, 28)
        self.initializeB.connect('clicked', self.initialize)

        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.initializeB, True, True, 0)
        hbox.pack_end(self.runAppB, True, True, 0)

        return self.runbox
    #---------------------------------------------------------------------------------------------------------        
    def getTreeStore(self):
    
        self.treestore.clear()
        
        row_main = self.treestore.append(None, [self.pixbuf_main, 'Run Conditions', None, None])
       
        if self.simDict['Time advance'] == 'Steady':
            self.treestore.append(row_main, [self.pixbuf_first, 'No. of Iteration', None, self.runDict['endTime']])
        else:
            self.treestore.append(row_main, [self.pixbuf_first, 'End Time', None, self.runDict['endTime']])
            self.treestore.append(row_main, [self.pixbuf_first, 'Time Step Size', None, self.runDict['deltaT']])
            #self.treestore.append(row_main, [self.pixbuf_first, 'Adjust Time Step', None, self.runDict['adjustTimeStep']])
            if self.runDict['adjustTimeStep'] == 'yes':
                self.treestore.append(row_main, [self.pixbuf_first, 'Adjust Time Step', True, None])
                self.treestore.append(row_main, [self.pixbuf_first, 'Max. CFL No.', None, self.runDict['maxCo']])
            else:
                self.treestore.append(row_main, [self.pixbuf_first, 'Adjust Time Step', False, None])
                
            self.treestore.append(row_main, [self.pixbuf_first, 'Write Control', None, self.runDict['writeControl']])
            
        self.treestore.append(row_main, [self.pixbuf_first, 'Write Interval', None, self.runDict['writeInterval']])
        self.treestore.append(row_main, [self.pixbuf_first, 'Max. No. of Saved Data', None, self.runDict['purgeWrite']])
        self.treestore.append(row_main, [self.pixbuf_first, 'Write Precision', None, self.runDict['writePrecision']])

        self.treestore.append(row_main, [self.pixbuf_first, 'Write Format', None, self.runDict['writeFormat']])
        
        if self.runDict['writeCompression'] == 'yes':
            self.treestore.append(row_main, [self.pixbuf_first, 'write Compression', True, None])
        else:
            self.treestore.append(row_main, [self.pixbuf_first, 'write Compression', False, None])

        if self.runDict['plotResidual'] == 'yes':
            self.treestore.append(row_main, [self.pixbuf_first, 'Plot Residual', True, None])
        else:
            self.treestore.append(row_main, [self.pixbuf_first, 'Plot Residual', False, None])
            
        self.treestore.append(row_main, [self.pixbuf_first, 'No. of Cores', None, self.runDict['nCores']])
        self.treestore.append(row_main, [self.pixbuf_first, 'Machine Type', None,self.runDict['machineType']])    
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):

        what = model.get_value(iter, 1)
        path = model.get_path(iter)
        
        entryList = ['End Time', 'No. of Iteration', 'Time Step Size', 'Max. CFL No.', 'Write Interval',
                     'Max. No. of Saved Data', 'Write Precision', 'No. of Cores']
        comboList = ['Write Control', 'Write Format', 'Machine Type']
        checkList = ['Adjust Time Step', 'write Compression', 'Plot Residual']       
        
        if what == 'Run Conditions':
            self.renToggle.set_property('visible', 0)
            self.ren1.set_property('visible' ,0)

        elif what in entryList:
            self.renToggle.set_property('visible', 0)
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            if what == 'End Time' or what == 'No. of Iteration':
                self.ren1.set_property('text', self.runDict['endTime'])
            elif what == 'Time Step Size':
                self.ren1.set_property('text', self.runDict['deltaT'])
            elif what == 'Max. CFL No.':
                self.ren1.set_property('text', self.runDict['maxCo'])
            elif what == 'Write Interval':
                self.ren1.set_property('text', self.runDict['writeInterval'])
            elif what == 'Max. No. of Saved Data':
                self.ren1.set_property('text', self.runDict['purgeWrite'])
            elif what == 'Write Precision':
                self.ren1.set_property('text', self.runDict['writePrecision'])
            elif what == 'No. of Cores':
                self.ren1.set_property('text', self.runDict['nCores'])
            
        elif what in comboList:
            self.renToggle.set_property('visible', 0)
            self.ren1.set_property('visible', 1) 
            self.ren1.set_property('has-entry', False)
            if what == 'Write Control':
                self.ren1.set_property('model', self.storeDict['writeControl'])
                self.ren1.set_property('text', self.runDict['writeControl'])
            elif what == 'Write Format':
                self.ren1.set_property('model', self.storeDict['writeFormat'])
                self.ren1.set_property('text', self.runDict['writeFormat'])
            elif what == 'Machine Type':
                self.ren1.set_property('model', self.storeDict['machineType'])
                self.ren1.set_property('text', self.runDict['machineType'])
            
        elif what in checkList:
            self.renToggle.set_property('visible', 1)
            self.ren1.set_property('visible', 0) 
    #---------------------------------------------------------------------------------------------------------
    def toggleRen(self, widget, path, model):
    
        model[path][2] = not model[path][2]       
        value0 = self.treestore[path][1]

        checkList = ['Adjust Time Step', 'write Compression', 'Plot Residual']
        
        if value0 == 'Adjust Time Step':
            if model[path][2] == True:
                self.runDict['adjustTimeStep'] = 'yes'
            else:
                self.runDict['adjustTimeStep'] = 'no'
            self.getTreeStore()
        elif value0 == 'write Compression':
            if model[path][2] == True:
                self.runDict['writeCompression'] = 'yes'
            else:
                self.runDict['writeCompression'] = 'no'
        elif value0 == 'Plot Residual':
            if model[path][2] == True:
                self.runDict['plotResidual'] = 'yes'
            else:
                self.runDict['plotResidual'] = 'no'

        self.GEN.pickleDump(self.setFileRun,self.runDict)
        self.treeview.expand_all()
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)        

        if value0 == 'End Time' or value0 == 'No. of Iteration':
            if self.GEN.checkNumber(value0, what):
                self.runDict['endTime'] = what
        elif value0 == 'Time Step Size':
            if self.GEN.checkNumber(value0, what):
                self.runDict['deltaT'] = what        
        elif value0 == 'Max. CFL No.':
            if self.GEN.checkNumber(value0, what):
                self.runDict['maxCo'] = what
        elif value0 == 'Write Interval':
            if self.GEN.checkNumber(value0, what):
                self.runDict['writeInterval'] = what
        elif value0 == 'Max. No. of Saved Data':
            if self.GEN.checkNumber(value0, what):
                self.runDict['purgeWrite'] = what
        elif value0 == 'Write Precision':
            if self.GEN.checkNumber(value0, what):
                self.runDict['writePrecision'] = what
        elif value0 == 'No. of Cores':
            if self.GEN.checkNumber(value0, what):
                self.runDict['nCores'] = what       
        elif value0 == 'Write Control':
            self.runDict['writeControl'] = what
        elif value0 == 'Write Format':
            self.runDict['writeFormat'] = what
        elif value0 == 'Machine Type':
            self.runDict['machineType'] = what
            if what == 'Cluster':
                self.selhostfile(path)

        self.GEN.pickleDump(self.setFileRun, self.runDict)            
    # -------------------------------------------------------------------------
    def initialize(self, widget):
    
        RUN = solverRunClass(self)
        RUN.initialize()
    #------------------------------------------------------------------------
    def applyrun(self, widget):
    
        RUN = solverRunClass(self)
        RUN.runSolver()
    #------------------------------------------------------------------------
    def selhostfile(self, path):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                 (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            hostfilename = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            hostfilename = 'None'
        dialog.destroy()

        if hostfilename == 'None':
            self.treestore[path][3] = 'SMP'
            self.runDict['machineType'] = 'SMP'            
        else:
            self.runDict['machineType'] = 'Cluster'

        self.GEN.pickleDump(self.setFileRun, self.runDict)
        with open(self.caseDir + '/system/settings/hostfilename','w') as f:
            f.write(hostfilename)
    # -------------------------------------------------------------------------
    def loadRunDict(self):
        
        self.runDict = self.GEN.pickleLoad(self.setFileRun)
        if self.runDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.runDict = dicts[2]
            self.GEN.pickleDump(self.setFileRun, self.runDict)
    #---------------------------------------------------------------------------------------------
    def getStoreDict(self):
            
        startfrom = ['startTime', 'latestTime']
        writecontrol = ['timeStep', 'runTime', 'adjustableRunTime']
        timeformat = ['general', 'fixed', 'scientific']
        partype = ['SMP', 'Cluster']
        writeformat = ['ascii', 'binary']
        yesno = ['yes', 'no']

        self.liststore_startfrom = gtk.ListStore(str)
        for ii in startfrom:
            self.liststore_startfrom.append([ii])
        
        self.liststore_adjust = gtk.ListStore(str)
        for ii in yesno:
            self.liststore_adjust.append([ii])
        
        self.liststore_writecontrol = gtk.ListStore(str)
        for ii in writecontrol:
            self.liststore_writecontrol.append([ii])
        
        self.liststore_timeformat = gtk.ListStore(str)
        for ii in timeformat:
            self.liststore_timeformat.append([ii])
        
        self.liststore_partype = gtk.ListStore(str)
        for ii in partype:
            self.liststore_partype.append([ii])
        
        self.liststore_writeformat = gtk.ListStore(str)
        for ii in writeformat:
            self.liststore_writeformat.append([ii])
        
        self.liststore_compress = gtk.ListStore(str)
        for ii in yesno:
            self.liststore_compress.append([ii])
        
        self.liststore_plotres = gtk.ListStore(str)
        for ii in yesno:
            self.liststore_plotres.append([ii])
        
        self.storeDict = {}
        keys = ['startFrom', 'adjustTimeStep', 'writeControl', 'timeFormat', 'machineType', 'writeFormat', 'writeCompression', 'plotResidual']
        values = [self.liststore_startfrom, self.liststore_adjust, self.liststore_writecontrol, self.liststore_timeformat, self.liststore_partype,
                  self.liststore_writeformat, self.liststore_compress, self.liststore_plotres]
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]
            



