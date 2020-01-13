#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelReportClass:
                
    def __init__(self,mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.solver = mainself.solver
        self.terminal = mainself.terminal
        self.installpath=mainself.installpath
        self.renderer = mainself.renderer

        self.GEN = generalClass(self)        
        self.WFILE = writeFileClass(self.caseDir)
        self.DEFAULT = defaultValueClass(self)
        
        self.Renderer = mainself.renderer        
        self.VTK_All = VTKStuff(mainself.caseDir)
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png') 
        
        self.bcNameList, self.polyTypeList = self.GEN.getBCName()
        if self.bcNameList == False:
            self.bcNameList = []        
            self.polyTypeList = []
    #------------------------------------------------------------------------------------------
    def report(self):

        self.reportbox = gtk.VBox()
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.reportbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Extract Data  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox)          
        
        self.vpan = gtk.VPaned()
        self.reportbox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 15)
        
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
        
        self.wallList = []
        self.patchList = []        
        for i in range(len(self.bcNameList)):
            if self.polyTypeList[i] == 'wall' or self.polyTypeList[i] == 'mappedWall':
                self.wallList.append(self.bcNameList[i])
            elif self.polyTypeList[i] == 'patch':
                self.patchList.append(self.bcNameList[i])
        #-------------------------------------------------------------------------------------
        self.setFilePointReport = self.caseDir + '/system/settings/pointReport'
        self.setFileForceReport = self.caseDir + '/system/settings/forceReport'
        self.setFileSurfaceReport = self.caseDir + '/system/settings/surfaceReport'
        self.loadPointReportDict()
        self.loadForceReportDict()
        self.loadSurfaceReportDict()       

        self.getFields()
        self.getStoreDict()
        # treeview ----------------------------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool, str)                       
            
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)       
        self.treeview.set_enable_tree_lines(True)

        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn2 = gtk.TreeViewColumn(None)
            
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn2)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererToggle()
        self.ren2_0 = gtk.CellRendererCombo()
        self.ren2_1 = gtk.CellRendererCombo()
        self.ren2_2 = gtk.CellRendererCombo()

        self.ren2_0.set_fixed_size(40, -1)
        self.ren2_1.set_fixed_size(40, -1)
        self.ren2_2.set_fixed_size(40, -1)

        self.ren0.set_property('editable', False)
        self.ren1.set_property('activatable', True)
        self.ren2_0.set_property("editable", True)
        self.ren2_1.set_property("editable", True)
        self.ren2_2.set_property("editable", True)
        self.ren2_0.set_property('text-column', 0)
        self.ren2_1.set_property('text-column', 1)
        self.ren2_2.set_property('text-column', 2)       
       
        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn0.pack_start(self.ren1, False)  
        self.tvcolumn2.pack_start(self.ren2_0, True)
        self.tvcolumn2.pack_start(self.ren2_1, True)
        self.tvcolumn2.pack_start(self.ren2_2, True)

        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        self.tvcolumn0.add_attribute(self.ren1, 'active', 2)        

        self.ren1.connect('toggled', self.toggleReport, self.treestore)
        self.ren2_0.connect('edited', self.changeValue, 'x')
        self.ren2_1.connect('edited', self.changeValue, 'y')
        self.ren2_2.connect('edited', self.changeValue, 'z')              
        self.tvcolumn2.set_cell_data_func(self.ren2_0, self.func)

        self.treeview.expand_all()        
        self.mainbox.add(self.treeview)
        
        self.setTreeStore()              
        self.makeReportButton()        
        return self.reportbox
    #---------------------------------------------------------------------------------------------    
    def setTreeStore(self):
    
        self.treestore.clear()
        
        row_force = self.treestore.append(None, [self.pixbuf_main, 'Force', None, None])
        row_point = self.treestore.append(None, [self.pixbuf_main, 'Point', None, None])
        row_surface = self.treestore.append(None, [self.pixbuf_main, 'Surface', None, None])
        
        self.treestore.append(row_force, [self.pixbuf_first, 'Reference Area [m²]', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Reference Length [m]', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Reference Velocity [m/s]', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Reference Density [kg/m³]', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Drag Direction', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Lift Direction', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Pitch Axis', None, None])
        self.treestore.append(row_force, [self.pixbuf_first, 'Center of Rotation', None, None])        
        row_forcePatch=self.treestore.append(row_force,[self.pixbuf_first,'Patches', None, None])
        for ii in self.wallList:
            if ii in self.forceReportDict['Patches']:
                self.treestore.append(row_forcePatch, [self.pixbuf_second, ii, True, None])
            else:
                self.treestore.append(row_forcePatch, [self.pixbuf_second, ii, False, None]) 

        self.treestore.append(row_point, [self.pixbuf_first, 'Field', None, None])
        self.treestore.append(row_point, [self.pixbuf_first, 'Coordinate', None, None])

        self.treestore.append(row_surface, [self.pixbuf_first, 'Mode', None, None])
        if self.surfaceReportDict['Mode'] == 'Average' or self.surfaceReportDict['Mode'] == 'Integrate':
            self.treestore.append(row_surface, [self.pixbuf_first, 'Field', None, None])              
        self.treestore.append(row_surface, [self.pixbuf_first, 'Patch', None, None])                
        self.treeview.expand_all()           
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
    
        what = model.get_value(iter, 1)
        path = model.get_path(iter)

        entrys = ['Reference Area [m²]', 'Reference Length [m]', 'Reference Velocity [m/s]', 'Reference Density [kg/m³]']
        three = ['Drag Direction', 'Lift Direction', 'Pitch Axis', 'Center of Rotation', 'Coordinate']
        combo = ['Mode', 'Field', 'Patch']

        if what == 'Force' or what == 'Point' or what == 'Surface' or what == 'Patches':
            self.ren1.set_property('visible', 0)
            self.ren2_0.set_property('visible', 0)
            self.ren2_1.set_property('visible', 0)
            self.ren2_2.set_property('visible', 0)

        elif what in entrys:
            self.ren1.set_property('visible', 0)
            self.ren2_0.set_property('visible', 1)
            self.ren2_1.set_property('visible', 0)
            self.ren2_2.set_property('visible', 0)
            self.ren2_0.set_property('has-entry', 1)
            self.ren2_0.set_property('model', None)
            self.ren2_0.set_property('text', self.forceReportDict[what])

        elif what in three:
            self.ren1.set_property('visible', 0)
            self.ren2_0.set_property('visible', 1)
            self.ren2_1.set_property('visible', 1)
            self.ren2_2.set_property('visible', 1)
            self.ren2_0.set_property('has-entry', 1)
            self.ren2_0.set_property('model', None)            
            self.ren2_1.set_property('has-entry', 1)
            self.ren2_1.set_property('model', None)            
            self.ren2_2.set_property('has-entry', 1)
            self.ren2_2.set_property('model', None)
            if what == 'Center of Rotation':
                self.ren2_0.set_property('text', self.forceReportDict['CofR_x'])
                self.ren2_1.set_property('text', self.forceReportDict['CofR_y'])
                self.ren2_2.set_property('text', self.forceReportDict['CofR_z'])
            elif what == 'Drag Direction':
                self.ren2_0.set_property('text', self.forceReportDict['dragDir_x'])
                self.ren2_1.set_property('text', self.forceReportDict['dragDir_y'])
                self.ren2_2.set_property('text', self.forceReportDict['dragDir_z'])
            elif what == 'Lift Direction':
                self.ren2_0.set_property('text', self.forceReportDict['liftDir_x'])
                self.ren2_1.set_property('text', self.forceReportDict['liftDir_y'])
                self.ren2_2.set_property('text', self.forceReportDict['liftDir_z']) 
            elif what == 'Pitch Axis':
                self.ren2_0.set_property('text', self.forceReportDict['pitchAxis_x'])
                self.ren2_1.set_property('text', self.forceReportDict['pitchAxis_y'])
                self.ren2_2.set_property('text', self.forceReportDict['pitchAxis_z'])
            elif what == 'Coordinate':
                self.ren2_0.set_property('text', self.pointReportDict['x-coord'])
                self.ren2_1.set_property('text', self.pointReportDict['y-coord'])
                self.ren2_2.set_property('text', self.pointReportDict['z-coord'])          

        elif what in self.bcNameList:
            self.ren1.set_property('visible', 1)
            self.ren2_0.set_property('visible', 0)
            self.ren2_1.set_property('visible', 0)
            self.ren2_2.set_property('visible', 0)
       
        elif what in combo:
            self.ren1.set_property('visible', 0)
            self.ren2_0.set_property('visible', 1)
            self.ren2_1.set_property('visible', 0)
            self.ren2_2.set_property('visible', 0)
            self.ren2_0.set_property('has-entry', 0)                   
            if what == 'Field':
                self.ren2_0.set_property('model', self.storeDict['fields']) 
                if path[0] == 1:
                    self.ren2_0.set_property('text', self.pointReportDict['Field'])
                elif path[0] == 2:
                    self.ren2_0.set_property('text', self.surfaceReportDict['Field'])
            elif what == 'Mode':
                self.ren2_0.set_property('model', self.storeDict['modes'])        
                self.ren2_0.set_property('text', self.surfaceReportDict['Mode'])  
            elif what == 'Patch':
                if self.surfaceReportDict['Mode'] == 'Flowrate':
                    self.ren2_0.set_property('model', self.storeDict['patchPatches'])
                else:
                    self.ren2_0.set_property('model', self.storeDict['patches'])        
                self.ren2_0.set_property('text', self.surfaceReportDict['Patch'])                
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what, xyz):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)        
                
        entrys = ['Reference Area [m²]', 'Reference Length [m]', 'Reference Velocity [m/s]', 'Reference Density [kg/m³]']
        
        if value0 in entrys:
            if self.GEN.checkNumber(value0, what):
                self.forceReportDict[value0] = what
        
        elif value0 == 'Drag Direction':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.forceReportDict['dragDir_x'] = what
                elif xyz == 'y':
                    self.forceReportDict['dragDir_y'] = what
                elif xyz == 'z':
                    self.forceReportDict['dragDir_z'] = what        
        elif value0 == 'Lift Direction':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.forceReportDict['liftDir_x'] = what
                elif xyz == 'y':
                    self.forceReportDict['liftDir_y'] = what
                elif xyz == 'z':
                    self.forceReportDict['liftDir_z'] = what        
        elif value0 == 'Pitch Axis':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.forceReportDict['pitchAxis_x'] = what
                elif xyz == 'y':
                    self.forceReportDict['pitchAxis_y'] = what
                elif xyz == 'z':
                    self.forceReportDict['pitchAxis_z'] = what        
        elif value0 == 'Center of Rotation':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.forceReportDict['CofR_x'] = what
                elif xyz == 'y':
                    self.forceReportDict['CofR_y'] = what
                elif xyz == 'z':
                    self.forceReportDict['CofR_z'] = what        
        elif value0 == 'Field':
            if path[0]=='1':
                self.pointReportDict['Field'] = what      
            elif path[0]=='2':
                self.surfaceReportDict['Field'] = what 
        elif value0 == 'Coordinate':                
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.pointReportDict['x-coord'] = what
                elif xyz == 'y':
                    self.pointReportDict['y-coord'] = what
                elif xyz == 'z':
                    self.pointReportDict['z-coord'] = what            
        elif value0 == 'Mode':
            self.surfaceReportDict['Mode'] = what
            if what == 'Flowrate':
                if self.surfaceReportDict['Patch'] in self.patchList:
                    pass
                else:
                    self.surfaceReportDict['Patch'] = self.patchList[0]    
            self.setTreeStore()
        elif value0 == 'Patch':
            self.surfaceReportDict['Patch'] = what    
            
        self.GEN.pickleDump(self.setFileForceReport, self.forceReportDict)
        self.GEN.pickleDump(self.setFilePointReport, self.pointReportDict)
        self.GEN.pickleDump(self.setFileSurfaceReport, self.surfaceReportDict)               
    #--------------------------------------------------------   
    def toggleReport(self, widget, path, model):
    
        model[path][2] = not model[path][2]       
        value0 = model[path][1]
        value1 = model[path][2]
        
        if self.bcNameList == []:
            self.GEN.makeDialog('Warning!!! There is not mesh')
            return

        if value1 == True:
            self.forceReportDict['Patches'].append(value0)
        else:
            self.forceReportDict['Patches'].remove(value0)                
        self.GEN.pickleDump(self.setFileForceReport, self.forceReportDict)
    # -------------------------------------------------------------------------
    def loadForceReportDict(self):
    
        self.forceReportDict = self.GEN.pickleLoad(self.setFileForceReport)
        if self.forceReportDict == None:
            self.forceReportDict = {}
            self.forceReportDict['Reference Area [m²]'] = '1'
            self.forceReportDict['Reference Length [m]'] = '1'
            self.forceReportDict['Reference Velocity [m/s]'] = '1'
            self.forceReportDict['Reference Density [kg/m³]'] = '1'
            self.forceReportDict['dragDir_x'] = '1'
            self.forceReportDict['dragDir_y'] = '0'
            self.forceReportDict['dragDir_z'] = '0'
            self.forceReportDict['liftDir_x'] = '0'
            self.forceReportDict['liftDir_y'] = '0'
            self.forceReportDict['liftDir_z'] = '1'
            self.forceReportDict['pitchAxis_x'] = '0'
            self.forceReportDict['pitchAxis_y'] = '1'
            self.forceReportDict['pitchAxis_z'] = '0'
            self.forceReportDict['CofR_x'] = '0'
            self.forceReportDict['CofR_y'] = '0'
            self.forceReportDict['CofR_z'] = '0'
            self.forceReportDict['Patches'] = []
    # -------------------------------------------------------------------------
    def loadPointReportDict(self):
    
        self.pointReportDict = self.GEN.pickleLoad(self.setFilePointReport)
        if self.pointReportDict == None:
            self.pointReportDict = {}
            self.pointReportDict['Field'] = 'p'
            self.pointReportDict['x-coord'] = '0'
            self.pointReportDict['y-coord'] = '0'
            self.pointReportDict['z-coord'] = '0'
    # -------------------------------------------------------------------------
    def loadSurfaceReportDict(self):
        
        self.surfaceReportDict = self.GEN.pickleLoad(self.setFileSurfaceReport)
        if self.surfaceReportDict == None:
            self.surfaceReportDict = {}
            self.surfaceReportDict['Field'] = 'p'
            self.surfaceReportDict['Mode'] = 'Average'
            if self.bcNameList != []:
                self.surfaceReportDict['Patch'] = self.bcNameList[0]
            else:
                self.surfaceReportDict['Patch'] = 'None'
    #---------------------------------------------------------------------------------------------
    def makeReportButton(self):
    
        POST = postProcessingClass(self)
        forceReportB = gtk.Button('Force report')
        probePointB = gtk.Button('Probe point')
        forceReportB.set_size_request(150, 28)
        probePointB.set_size_request(150, 28)
        forceReportB.connect('clicked', POST.forceReport, self.forceReportDict, self.simDict)
        probePointB.connect('clicked', POST.pointReport, self.pointReportDict)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_end(probePointB, True, True, 0)
        hbox.pack_end(forceReportB, True, True, 0)            
        patchB = gtk.Button('Surface value')
        patchB.connect('clicked', POST.surfaceReport, self.surfaceReportDict)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False,0)
        hbox.pack_end(patchB, True, True, 0)        
    #---------------------------------------------------------------------------------------------
    def getFields(self):
    
        if self.simDict['Turbulence model'] == 'kOmegaSST':
            self.turfield = ['k', 'omega']
        elif self.simDict['Turbulence model'] == 'laminar':
            self.turfield = []
        else:
            self.turfield=['k', 'epsilon']
        
        if self.simDict['Energy'] == 'Off':
            self.fields=['Umag', 'p']
        else:
            self.fields=['Umag', 'p', 'p_rgh', 'T']
    #---------------------------------------------------------------------------------------------    
    def getStoreDict(self): 
           
        for ii in self.turfield:
            self.fields.append(ii)

        liststore_fields = gtk.ListStore(str)
        for ii in self.fields:
            liststore_fields.append([ii])
        
        liststore_num = gtk.ListStore(str)
        for i in range(11):
            liststore_num.append([str(i)])
        
        modes = ['Flowrate', 'Average', 'Integrate']
        liststore_modes = gtk.ListStore(str)
        for ii in modes:
            liststore_modes.append([ii])
        
        liststore_patches = gtk.ListStore(str)
        for ii in self.bcNameList:
            liststore_patches.append([ii])
        
        liststore_patchPatches = gtk.ListStore(str)
        for ii in self.patchList:
            liststore_patchPatches.append([ii])
        
        self.storeDict = {}
        keys = ['fields', 'number', 'modes', 'patches', 'patchPatches']
        values = [liststore_fields, liststore_num, liststore_modes, liststore_patches, liststore_patchPatches]
        
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]
        
        
