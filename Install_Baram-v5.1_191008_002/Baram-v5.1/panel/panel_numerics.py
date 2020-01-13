# -*-coding:utf8-*-

from common.fromAll     import *

class freepanelNumericsClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.solver = mainself.solver
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.terminal = mainself.terminal
        self.mainwindow = mainself.window        

        self.GEN = generalClass(mainself)
        
        self.WFILE = writeFileClass(self.caseDir)
        self.WFILEBC = writeBCFileClass(self)
        self.DEFAULT = defaultValueClass(self)
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')
        
    def numerics(self):

        self.numericbox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.numericbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Numerical Conditions  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.numericbox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, -1)

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
        
        if self.simDict['Energy'] == 'Off':
            self.fields = ['Pressure','Velocity']
        elif self.simDict['Energy'] == 'On':
            self.fields = ['Pressure','Velocity','Temperature']
        if self.simDict['Turbulence model'] != 'laminar':
            self.fields.append('Turbulence')

        self.setFileNume = self.caseDir + '/system/settings/numerixSetup'    
        self.loadNumeDict()        
        self.getStoreDict()
        
        # discretize --------------------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)

        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)

        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1 = gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererCombo()
        
        self.ren0.set_fixed_size(150, -1)
        
        self.ren0.set_property("editable", False)
        self.ren1.set_property("editable", True)
        self.ren1.set_property("text-column", 0)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn1.pack_start(self.ren1, False)
        
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        
        self.ren1.connect('edited', self.changeValue)
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func)
        
        self.getTreeStore()        
        self.treeview.expand_all()
        
        self.mainbox.pack_start(self.treeview, False, False, 0)        
        return self.numericbox
    #---------------------------------------------------------------------------------------------------------        
    def getTreeStore(self):
    
        self.treestore.clear()

        row_dis = self.treestore.append(None, [self.pixbuf_main, 'Discretization Schemes', None])
        
        if self.simDict['Time advance'] == 'Transient':
            self.treestore.append(row_dis, [self.pixbuf_first, 'Time', self.numeDict['discretize_time']])
        self.treestore.append(row_dis, [self.pixbuf_first, 'Momentum', self.numeDict['discretize_momentum']])        
        if self.simDict['Energy'] == 'On':
            self.treestore.append(row_dis, [self.pixbuf_first, 'Energy', self.numeDict['discretize_energy']])
        if self.simDict['Turbulence model'] != 'laminar':
            self.treestore.append(row_dis, [self.pixbuf_first, 'Turbulence', self.numeDict['discretize_turbulence']])
        
        row_relax = self.treestore.append(None, [self.pixbuf_main, 'Relaxation Factors', None])
        
        self.treestore.append(row_relax, [self.pixbuf_first, 'Pressure', self.numeDict['relax_pressure']])
        self.treestore.append(row_relax, [self.pixbuf_first, 'Momentum', self.numeDict['relax_momentum']])        
        if self.simDict['Energy'] == 'On':
            self.treestore.append(row_relax, [self.pixbuf_first, 'Energy', self.numeDict['relax_energy']])
        if self.simDict['Turbulence model'] != 'laminar':
            self.treestore.append(row_relax, [self.pixbuf_first, 'Turbulence', self.numeDict['relax_turbulence']])
        
        row_conv = self.treestore.append(None, [self.pixbuf_main, 'Convergence Criteria', None])
        
        self.treestore.append(row_conv, [self.pixbuf_first, 'Pressure', self.numeDict['conv_pressure']])
        self.treestore.append(row_conv, [self.pixbuf_first, 'Momentum', self.numeDict['conv_momentum']])        
        if self.simDict['Energy'] == 'On':
            self.treestore.append(row_conv, [self.pixbuf_first, 'Energy', self.numeDict['conv_energy']])
        if self.simDict['Turbulence model'] != 'laminar':
            self.treestore.append(row_conv, [self.pixbuf_first, 'Turbulence', self.numeDict['conv_turbulence']])
        if self.simDict['Time advance'] == 'Transient':
            self.treestore.append(row_conv, [self.pixbuf_first, 'Pressure_relative', self.numeDict['conv_pressure_relative']])
            self.treestore.append(row_conv, [self.pixbuf_first, 'Momentum_relative', self.numeDict['conv_momentum_relative']])        
            if self.simDict['Energy'] == 'On':
                self.treestore.append(row_conv, [self.pixbuf_first, 'Energy_relative', self.numeDict['conv_energy_relative']])
            if self.simDict['Turbulence model'] != 'laminar':
                self.treestore.append(row_conv, [self.pixbuf_first, 'Turbulence_relative', self.numeDict['conv_turbulence_relative']])
        
        if self.simDict['Time advance'] == 'Transient':    
            self.treestore.append(None, [self.pixbuf_main, 'Max iteration per dt', self.numeDict['nOuterCorrectors']])
    #---------------------------------------------------------------------------------------------------------        
    def func(self, column, cell, model, iter):
        
        what = model.get_value(iter, 1)
        path = model.get_path(iter)       

        if path[0] == 0: # discretize
            if what == 'Discretization Schemes':
                self.ren1.set_property('visible', 0)
            else:
                self.ren1.set_property('visible', True)
                self.ren1.set_property('has-entry', False)                
                if what == 'Time':
                    self.ren1.set_property("model", self.storeDict['ddts'])            
                    self.ren1.set_property('text', self.numeDict['discretize_time'])
                elif what == 'Momentum':
                    self.ren1.set_property("model", self.storeDict['discretizes'])            
                    self.ren1.set_property('text', self.numeDict['discretize_momentum'])
                elif what == 'Energy':
                    self.ren1.set_property("model", self.storeDict['discretizes'])            
                    self.ren1.set_property('text', self.numeDict['discretize_energy'])
                elif what == 'Turbulence':
                    self.ren1.set_property("model", self.storeDict['discretizes'])            
                    self.ren1.set_property('text', self.numeDict['discretize_turbulence'])

        elif path[0] == 1: # relax
            if what == 'Relaxation Factors':
                self.ren1.set_property('visible', 0)
            else:
                self.ren1.set_property('visible', True)
                self.ren1.set_property("model", None)
                self.ren1.set_property('has-entry', True)
                if what == 'Pressure':
                    self.ren1.set_property('text', self.numeDict['relax_pressure'])
                elif what == 'Momentum':
                    self.ren1.set_property('text', self.numeDict['relax_momentum'])
                elif what == 'Energy':
                    self.ren1.set_property('text', self.numeDict['relax_energy'])
                elif what == 'Turbulence':
                    self.ren1.set_property('text', self.numeDict['relax_turbulence'])

        elif path[0] == 2: # converge
            if what == 'Convergence Criteria':
                self.ren1.set_property('visible', 0)
            else:
                self.ren1.set_property('visible', True)
                self.ren1.set_property("model", None)
                self.ren1.set_property('has-entry', True)
                if what =='Momentum':
                    self.ren1.set_property('text', self.numeDict['conv_momentum'])
                elif what == 'Energy':
                    self.ren1.set_property('text', self.numeDict['conv_energy'])
                elif what == 'Turbulence':
                    self.ren1.set_property('text', self.numeDict['conv_turbulence'])
                elif what == 'Pressure':
                    self.ren1.set_property('text', self.numeDict['conv_pressure'])
                elif what == 'Pressure_relative':
                    self.ren1.set_property('text', self.numeDict['conv_pressure_relative'])
                elif what == 'Momentum_relative':
                    self.ren1.set_property('text', self.numeDict['conv_momentum_relative'])
                elif what == 'Energy_relative':
                    self.ren1.set_property('text', self.numeDict['conv_energy_relative'])
                elif what == 'Turbulence_relative':
                    self.ren1.set_property('text', self.numeDict['conv_turbulence_relative'])

        elif path[0] == 3: # nOuterCorrectors
            if what == 'Max iteration per dt':
                self.ren1.set_property('text', self.numeDict['nOuterCorrectors'])
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)
        old = self.treestore[path][2]
        
        if what == old:
            return
        if path[0] == '0': # discretize
            if value0 == 'Time':
                self.numeDict['discretize_time'] = what 
            elif value0 == 'Momentum':
                self.numeDict['discretize_momentum'] = what 
            elif value0 == 'Energy':
                self.numeDict['discretize_energy'] = what            
            elif value0 == 'Turbulence':
                self.numeDict['discretize_turbulence'] = what

        elif path[0] == '1': # relax
            if self.GEN.checkNumber(value0, what):
                if value0 == 'Momentum':
                    self.numeDict['relax_momentum'] = what
                elif value0 == 'Energy':
                    self.numeDict['relax_energy'] = what            
                elif value0 == 'Turbulence':
                    self.numeDict['relax_turbulence'] = what            
                elif value0 == 'Pressure':
                    self.numeDict['relax_pressure'] = what

        elif path[0] == '2': # converge        
            if self.GEN.checkNumber(value0, what):
                if value0 == 'Momentum':
                    self.numeDict['conv_momentum'] = what
                elif value0 == 'Energy':
                    self.numeDict['conv_energy'] = what            
                elif value0 == 'Turbulence':
                    self.numeDict['conv_turbulence'] = what            
                elif value0 == 'Pressure':
                    self.numeDict['conv_pressure'] = what                
                elif value0 == 'Pressure_relative':
                    self.numeDict['conv_pressure_relative'] = what        
                elif value0 == 'Momentum_relative':
                    self.numeDict['conv_momentum_relative'] = what
                elif value0 == 'Energy_relative':
                    self.numeDict['conv_energy_relative'] = what
                elif value0 == 'Turbulence_relative':
                    self.numeDict['conv_turbulence_relative'] = what
        elif path[0] == '3': # nOuterCorrectors        
            if value0 == 'Max iteration per dt':
                if self.GEN.checkNumber(value0, what):
                    self.numeDict['nOuterCorrectors'] = what
                    
        self.treestore[path][2] = what
            
        self.GEN.pickleDump(self.setFileNume, self.numeDict) 
        self.WFILEBC.numericConditions(self.numeDict, self.simDict)
    # -------------------------------------------------------------------------
    def loadNumeDict(self):
    
        self.numeDict = self.GEN.pickleLoad(self.setFileNume)
        if self.numeDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.numeDict = dicts[3]       
    #---------------------------------------------------------------------------------------------
    def getStoreDict(self):
    
        self.ddts = ['firstOrder', 'secondOrder']
        self.discretizes = ['firstOrder', 'secondOrder']

        self.liststore_ddts = gtk.ListStore(str)
        for ii in self.ddts:
            self.liststore_ddts.append([ii])
        
        self.liststore_discretizes = gtk.ListStore(str)
        for ii in self.discretizes:
            self.liststore_discretizes.append([ii])

        self.liststore_yesNo = gtk.ListStore(str)
        self.liststore_yesNo.append(['yes'])
        self.liststore_yesNo.append(['no'])
        
        self.storeDict = {}
        keys = ['ddts', 'discretizes', 'yesNo']
        values = [self.liststore_ddts, self.liststore_discretizes, self.liststore_yesNo]
        
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]
        
        
        

