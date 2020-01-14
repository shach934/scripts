#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelSimulationClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.notebook = mainself.notebook
        self.solver = mainself.solver
        self.DEFAULT = defaultValueClass(self)        
        self.GEN = generalClass(mainself)
        self.WFILE = writeFileClass(self.caseDir)
        
        self.bcNameList, self.polyPatchTypeList = self.GEN.getBCName()
        self.wallList = []
        if self.polyPatchTypeList != False:
            for i in range(len(self.bcNameList)):
                if self.polyPatchTypeList[i] == 'wall' or self.polyPatchTypeList[i] == 'mappedWall':
                    self.wallList.append(self.bcNameList[i])

        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')  
        
    def simulation(self):        
    
        self.setFile = self.caseDir + '/system/settings/simulationConditions'        
        self.loadSimDict()
        self.setListStore()
        
        self.simulationbox = gtk.VBox()          
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.simulationbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Flow Conditions  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
        
        self.vbox = gtk.VBox()
        self.simulationbox.add(self.vbox)
        self.mainbox = gtk.EventBox()
        self.mainbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.vbox.add(self.mainbox)
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, -1)
        self.mainbox.add(swin)
        
        self.whitebox = gtk.EventBox()
        self.whitebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))      
        self.treebox = gtk.VBox(False, 0)
        swin.add_with_viewport(self.whitebox)
        self.whitebox.add(self.treebox)
        # treesview - physics ------------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)
        self.makeTreeStore()                 

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
        self.ren1 = gtk.CellRendererCombo()                  

        self.ren0.set_property('editable', False)
        self.ren1.set_property('editable', True)
        self.ren1.set_property('text-column', 0)
        
        self.ren0.set_fixed_size(150, -1) 
        
        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, True)
        self.tvcolumn1.pack_start(self.ren1, True)        
        
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        
        self.ren1.connect('edited', self.changeValue1)        
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func1)
        
        self.treeview.expand_all()        
        self.treebox.pack_start(self.treeview, False, False, 0)

        return self.simulationbox
    #---------------------------------------------------------------------------------------------
    def makeTreeStore(self):
    
        self.row_physics = self.treestore.append(None, [self.pixbuf_main, 'Physics', None])
        
        self.treestore.append(self.row_physics, [self.pixbuf_first, 'Time advance', self.simDict['Time advance']])
        self.treestore.append(self.row_physics, [self.pixbuf_first, 'Energy', self.simDict['Energy']])
        self.row_tur = self.treestore.append(self.row_physics, [self.pixbuf_first, 'Turbulence model', self.simDict['Turbulence model']])
        if self.simDict['Turbulence model'] != 'laminar':
            self.treestore.append(self.row_tur, [self.pixbuf_second, 'Prt', self.simDict['Prt']])
        if self.simDict['Turbulence model'] == 'realizableKEtwoLayer':
            self.treestore.append(self.row_tur, [self.pixbuf_second, 'ReyStar', self.simDict['ReyStar']])
            self.treestore.append(self.row_tur, [self.pixbuf_second, 'deltaRey', self.simDict['deltaRey']])
        
        if self.simDict['Energy'] == 'On':
            self.treestore.append(self.row_physics, [self.pixbuf_first, 'Gravity', self.simDict['Gravity']]) 

        self.row_material = self.treestore.append(None, [self.pixbuf_main, 'Material Properties', None])
        
        if self.simDict['Energy'] == 'Off':
            self.treestore.append(self.row_material, [self.pixbuf_first, 'density', self.simDict['density']])
            self.treestore.append(self.row_material, [self.pixbuf_first, 'viscosity', self.simDict['viscosity']])
        else:
            densityMethod = self.treestore.append(self.row_material, [self.pixbuf_first, 'density_method', self.simDict['density_method']])
            if self.simDict['density_method'] == 'Constant':
                self.treestore.append(densityMethod, [self.pixbuf_second, 'density', self.simDict['density']])         
            
            transportMethod = self.treestore.append(self.row_material, [self.pixbuf_first, 'transport_method', self.simDict['transport_method']]) 
            if self.simDict['transport_method'] == 'Constant':
                self.treestore.append(transportMethod, [self.pixbuf_second, 'viscosity', self.simDict['viscosity']])  
                self.treestore.append(transportMethod, [self.pixbuf_second, 'conductivity', self.simDict['conductivity']])  
            else:
                self.treestore.append(transportMethod, [self.pixbuf_second, 'As', self.simDict['As']]) 
                self.treestore.append(transportMethod, [self.pixbuf_second, 'Ts', self.simDict['Ts']]) 
            self.cp = self.treestore.append(self.row_material, [self.pixbuf_first, 'Cp', self.simDict['Cp']])
            
        if self.simDict['Energy'] == 'On':
            self.row_radiation = self.treestore.append(None, [self.pixbuf_main, 'Radiation Properties', None])
            
            self.treestore.append(self.row_radiation, [self.pixbuf_first, 'radiationModel', self.simDict['radiationModel']])

            if self.simDict['radiationModel'] == 'P1':
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'solverFrequency', self.simDict['solverFrequency']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'absorptivity', self.simDict['absorptivity']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'emissivity', self.simDict['emissivity']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'E', self.simDict['E']])

            elif self.simDict['radiationModel'] == 'fvDOM':
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'solverFrequency', self.simDict['solverFrequency']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'absorptivity', self.simDict['absorptivity']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'emissivity', self.simDict['emissivity']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'E', self.simDict['E']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'nPhi', self.simDict['nPhi']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'nTheta', self.simDict['nTheta']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'convergence', self.simDict['convergence']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'maxIter', self.simDict['maxIter']])
                self.treestore.append(self.row_radiation, [self.pixbuf_first, 'cacheDiv', self.simDict['cacheDiv']])
                
            self.row_wallEmi = self.treestore.append(self.row_radiation, [self.pixbuf_first, 'wallEmissivity', None])
            if self.simDict['radiationModel'] == 'P1' or self.simDict['radiationModel'] == 'fvDOM':
                for ii in self.wallList:
                    self.treestore.append(self.row_wallEmi, [self.pixbuf_second, ii, self.simDict['wallEmissivity'][ii]])
    #---------------------------------------------------------------------------------------------
    def changeValue1(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)        
        old = self.treestore[path][2]
        
        if what == old:
            return    

        if value0 == 'Energy':
            if what == 'On':
                if self.simDict['Time advance'] == 'Transient':
                    os.system('cp ' + self.installpath + '/DictFile/5.0/buoyantPimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
                else:
                    os.system('cp ' + self.installpath + '/DictFile/5.0/buoyantSimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
            else:
                if self.simDict['Time advance'] == 'Transient':
                    os.system('cp ' + self.installpath + '/DictFile/5.0/pimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
                else:
                    os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')               

        elif value0 == 'Time advance':
            if what == 'Transient':
                if self.simDict['Energy'] == 'Off':
                    os.system('cp ' + self.installpath + '/DictFile/5.0/pimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
                else:
                    os.system('cp ' + self.installpath + '/DictFile/5.0/buoyantPimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
            else:
                if self.simDict['Energy'] == 'Off':
                    os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')
                else:
                    os.system('cp ' + self.installpath + '/DictFile/5.0/buoyantSimpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')

        keys = self.simDict.keys()
        if value0 in keys:
            self.simDict[value0] = what
        elif value0 in self.wallList:
            self.simDict['wallEmissivity'][value0] = what

        self.WFILE.turbulenceProperties(self.simDict)
        
        if self.simDict['Energy'] == 'Off' and self.simDict['Time advance'] == 'Steady':self.solver = 'simpleNFoam'
        elif self.simDict['Energy'] == 'Off' and self.simDict['Time advance'] == 'Transient':self.solver = 'pimpleNFoam'
        elif self.simDict['Energy'] == 'On' and self.simDict['Time advance'] == 'Steady':self.solver = 'buoyantSimpleNFoam'
        elif self.simDict['Energy'] == 'On' and self.simDict['Time advance'] == 'Transient':self.solver = 'buoyantPimpleNFoam'
        
        self.simDict['solver'] = self.solver

        if self.simDict['Energy'] == 'Off':
            self.WFILE.transportProperties(self.simDict)
        else:
            self.WFILE.thermophysicalProperties(self.simDict)
            self.WFILE.gravity(self.simDict)
            self.WFILE.operatingConditions('101325')

        if self.simDict['radiationModel'] == 'none':
            if glob.glob(self.caseDir + '/constant/radiationProperties'):
                os.system('rm ' + self.caseDir + '/constant/radiationProperties')
        else:            
            self.WFILE.radiationProperties(self.simDict)
            self.WFILE.radiationBCFile(self.simDict)
        
        self.checkNumber()        
        self.GEN.pickleDump(self.setFile,self.simDict)

        self.treestore.clear()
        self.makeTreeStore()

        self.treeview.expand_all()                
    #---------------------------------------------------------------------------------------------    
    def func1(self, column, cell, model, iter):
    
        what = model.get_value(iter, 1)
        path = model.get_path(iter)

        noneList = ['Physics', 'Material Properties', 'Radiation Properties',
                    'Radiation', 'wallEmissivity', 'absorptionEmission', 'fvDOMCoeffs']
        entryList = ['Prt', 'ReyStar', 'deltaRey',
                     'density', 'viscosity', 'conductivity', 'As', 'Ts', 'Cp',
                     'solverFrequency', 'absorptivity', 'emissivity', 'E', 'nPhi', 'nTheta', 'convergence', 'maxIter']
        comboList = ['Time advance', 'Energy', 'Turbulence model', 'Gravity', 'density_method',
                     'transport_method', 'radiationModel', 'cacheDiv']
        
        if what in noneList:
            self.ren1.set_property('visible', 0)
            
        elif what in entryList:
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            self.ren1.set_property('text',self.simDict[what])
        
        elif what in self.wallList:
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            self.ren1.set_property('text', self.simDict['wallEmissivity'][self.wallList[path[2]]])

        elif what in comboList:
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', self.storeDict[what])
            self.ren1.set_property('has-entry', False)
            self.ren1.set_property('text', self.simDict[what])
    #---------------------------------------------------------------------------------------------------------                
    def loadSimDict(self):   
   
        self.simDict = self.GEN.pickleLoad(self.setFile)        
        if self.simDict == None:
            dicts  =self.DEFAULT.defaultDict()
            self.simDict = dicts[0]
            for ii in self.wallList:
                self.simDict['wallEmissivity'][ii] = '1.0'
            self.GEN.pickleDump(self.setFile, self.simDict)
        else: # for the case : No. of patch is changed. ex) createBaffle
            if len(self.wallList) != len(self.simDict['wallEmissivity'].keys()):
                self.simDict['wallEmissivity'] = {}
                for ii in self.wallList:
                    self.simDict['wallEmissivity'][ii] = '1.0'
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        value0 = tree_model.get_value(tree_iter, 0)
        path = tree_model.get_path(tree_iter)

        self.treeviews = [self.treeview, self.treeview_prop, self.treeview_rad]
        for ii in self.treeviews:
            if treeview != ii:
                sel = ii.get_selection()
                sel.unselect_all()
        self.treebox.show_all() 
    #---------------------------------------------------------------------------------------------
    def setListStore(self):
        
        #turmodel = ['kEpsilon', 'realizableKE', 'RNGkEpsilon', 'kOmegaSST', 'laminar', 'realizableKEtwoLayer']
        turmodel = ['kEpsilon', 'realizableKE', 'RNGkEpsilon', 'kOmegaSST', 'laminar']
        time = ['Steady', 'Transient']
        energy = ['On', 'Off']
        density = ['Constant', 'Perfect gas']
        transport = ['Constant', 'Sutherland']
        gravity = ['None', '+x', '+y', '+z', '-x', '-y', '-z']
        radModel = ['none', 'P1', 'fvDOM']
        cacheDiv = ['true', 'false']

        liststore_turmodel = gtk.ListStore(str)
        for ii in turmodel:
            liststore_turmodel.append([ii])
        
        liststore_time = gtk.ListStore(str)
        for ii in time:
            liststore_time.append([ii])
        
        liststore_energy = gtk.ListStore(str)
        for ii in energy:
            liststore_energy.append([ii])
        
        liststore_density = gtk.ListStore(str)
        for ii in density:
            liststore_density.append([ii])
        
        liststore_transport = gtk.ListStore(str)
        for ii in transport:
            liststore_transport.append([ii])
        
        liststore_gravity = gtk.ListStore(str)
        for ii in gravity:
            liststore_gravity.append([ii])
        
        liststore_radModel = gtk.ListStore(str)
        for ii in radModel:
            liststore_radModel.append([ii])
        
        liststore_cacheDiv = gtk.ListStore(str)
        for ii in cacheDiv:
            liststore_cacheDiv.append([ii])
        
        self.storeDict = {}
        keys = ['Turbulence model', 'Time advance', 'Energy', 'density_method',
                'transport_method', 'Gravity', 'radiationModel', 'cacheDiv']
        values = [liststore_turmodel, liststore_time, liststore_energy, liststore_density, liststore_transport,
                  liststore_gravity, liststore_radModel, liststore_cacheDiv]
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]
    #---------------------------------------------------------------------------------------------
    def checkNumber(self):
    
        keys = ['density', 'viscosity', 'conductivity', 'As', 'Ts', 'Cp', 'molecular weight', 'solverFrequency',
                'absorptivity', 'emissivity', 'E', 'nPhi', 'nTheta', 'convergence', 'maxIter']
        for ii in keys:
            if self.GEN.isNumber(self.simDict[ii]) == False:
                self.GEN.makeDialog('Error!!! ' + ii + ' is not number')
        for i in range(len(self.wallList)):
            if self.GEN.isNumber(self.simDict['wallEmissivity'][self.wallList[i]]) == False:
                self.GEN.makeDialog('Error!!! wall emissivity of ' + self.wallList[i] + ' is not number')
        