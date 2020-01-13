#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelCellZoneClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.solver = mainself.solver
        self.renderer = mainself.renderer
        self.vtkFeatureActors = mainself.vtkFeatureActors        
        self.mainself = mainself
        
        self.GEN = generalClass(mainself)
        self.WFILE = writeFileClass(self.caseDir)
        self.DEFAULT = defaultValueClass(self)
        self.VTK_All = VTKStuff(self.caseDir)
                
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath+'/pic/treeIcon/second.png')
               
    def cellZone(self):        

        self.cellzonebox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.cellzonebox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  CellZone Conditions  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.cellzonebox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1 = gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 100)

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
        #---------------------------------------------------------------------        
        self.simDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')        
        if self.simDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.simDict=dicts[0]
        
        self.getNonConstraintPatch()
        self.cellZones = self.GEN.getCellZones()

        self.setFileZone = self.caseDir + '/system/settings/cellZoneSetup'
        self.loadCellZoneDict()
        self.getStoreDict()
        
        # cellzone ---------------------------------------------------------------------        
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)       
        
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)       
        self.treeview.set_enable_tree_lines(True)
        
        self.treeview.connect('cursor-changed', self.selected, self.treeview)

        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1=gtk.TreeViewColumn(None)
                        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererCombo()
        self.ren1.connect('edited', self.changeValue) 

        self.ren0.set_property('editable', False)
        self.ren1.set_property("editable", True)
        self.ren1.set_property('text-column', 0)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, text = 1) 
         
        self.tvcolumn1.pack_start(self.ren1, False)        
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func)
        
        self.treeview.expand_all()
        
        self.mainbox.pack_start(self.treeview, True, True, 0)            
        self.setZoneTreestore()        
        # value ---------------------------------------------------------------------        
        self.treestore_value = gtk.TreeStore(str, bool, str)
                           
        self.treeview_value = gtk.TreeView(self.treestore_value)
        self.treeview_value.set_enable_tree_lines(True)

        self.tvcolumn0_value = gtk.TreeViewColumn('Variable')
        self.tvcolumn2_value = gtk.TreeViewColumn('Value')

        self.tvcolumn0_value.set_resizable(True)
                        
        self.treeview_value.append_column(self.tvcolumn0_value)
        self.treeview_value.append_column(self.tvcolumn2_value)
        
        self.ren0_value = gtk.CellRendererText()
        self.ren1_value = gtk.CellRendererToggle()                  
        self.ren2_0_value = gtk.CellRendererCombo() 
        self.ren2_1_value = gtk.CellRendererCombo()          
        self.ren2_2_value = gtk.CellRendererCombo()                  
        
        self.ren2_0_value.set_fixed_size(40, -1)
        self.ren2_1_value.set_fixed_size(40, -1)
        self.ren2_2_value.set_fixed_size(40, -1)

        self.ren0_value.set_property('editable', False)
        self.ren1_value.set_property('activatable', True)
        self.ren2_0_value.set_property("editable", True)
        self.ren2_1_value.set_property("editable", True)
        self.ren2_2_value.set_property("editable", True)
        self.ren2_0_value.set_property('text-column', 0)
        self.ren2_1_value.set_property('text-column', 0)
        self.ren2_2_value.set_property('text-column', 0)
        
        self.tvcolumn0_value.pack_start(self.ren0_value, False) 
        self.tvcolumn2_value.pack_start(self.ren1_value, False)
        
        self.tvcolumn2_value.pack_start(self.ren2_0_value, True)
        self.tvcolumn2_value.pack_start(self.ren2_1_value, True)
        self.tvcolumn2_value.pack_start(self.ren2_2_value, True)
        
        self.tvcolumn0_value.set_attributes(self.ren0_value, markup = 0)
        self.tvcolumn2_value.add_attribute(self.ren1_value, 'active', 1)
        
        self.ren1_value.connect('toggled', self.togglePatch_value, self.treestore_value)
        self.ren2_0_value.connect('edited', self.changeValue_value, 'x')
        self.ren2_1_value.connect('edited', self.changeValue_value, 'y')
        self.ren2_2_value.connect('edited', self.changeValue_value, 'z')        
        self.tvcolumn2_value.set_cell_data_func(self.ren2_0_value, self.func_value)
        
        self.treeview_value.expand_all()
        
        self.valuebox.pack_start(self.treeview_value, True, True, 0)    
        
        return self.cellzonebox

    #---------------------------------------------------------------------------------------------------------
    def setZoneTreestore(self):

        for i in range(len(self.cellZones)):
            self.treestore.append(None, [self.pixbuf_main, self.cellZones[i], self.cellZoneDict['types'][i]])
        self.treeview.expand_all()
    #---------------------------------------------------------------------------------------------------------
    def togglePatch_value(self,widget,path,model):
    
        model[path][1] = not model[path][1]
       
        dic = self.cellZoneDict['dict'][self.index]
        patchlist = dic['StaticPatch']
        value = self.treestore_value[path][1]
        patch = model[path][0]

        if value == True:
            patchlist.append(patch)
        else:
            if patch in patchlist:
                patchlist.remove(patch)            

        dic['StaticPatch'] = patchlist

        self.GEN.pickleDump(self.setFileZone, self.cellZoneDict) 
        self.WFILE.MRFProperties(self.cellZoneDict)
    #--------------------------------------------------------------------------
    def changeValue(self, widget, path, what):    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)        

        ind = int(path[0])
        self.cellZoneDict['types'][ind] = what        
        
        self.makeDetailTreeview(self.cellZones[ind], self.cellZoneDict['types'][ind])        
        self.GEN.pickleDump(self.setFileZone, self.cellZoneDict)
        
        if os.path.isfile(self.caseDir + '/constant/MRFProperties'):
            os.system('rm ' + self.caseDir + '/constant/MRFProperties')
        self.WFILE.MRFProperties(self.cellZoneDict)
        
        porousfile = glob.glob(self.caseDir + '/system/cellZoneConditions_Porous*')
        for ii in porousfile:
            os.system('rm ' + ii)
        self.WFILE.porousFile(self.cellZoneDict)
        
        heatsourcefile = glob.glob(self.caseDir + '/system/cellZoneConditions_heatsource*')
        for ii in heatsourcefile:
            os.system('rm ' + ii)
        self.WFILE.heatsourceFile(self.cellZoneDict)
        
        self.WFILE.fvOptions()  
    #--------------------------------------------------------------------------
    def changeValue_value(self, widget, path, what, xyz):
    
        treeiter = self.treestore_value.get_iter(path)
        value0 = self.treestore_value.get_value(treeiter, 0)
        old = self.treestore_value[path][2] 
        
        dic = self.cellZoneDict['dict'][self.index]
        
        if what == old:
            return
                 
        if value0 == 'Origin':
            if self.GEN.checkNumber(value0, what):
                dic['ori'+xyz] = what
        elif value0 == 'Axis':
            if self.GEN.checkNumber(value0, what):
                dic['axis'+xyz] = what
        elif value0 == 'RPM':
            if self.GEN.checkNumber(value0, what):
                dic['RPM'] = what            
        elif value0 == 'Method':
            dic['porousType'] = what               
            self.makeDetailTreeview(self.currentZone, 'Porous')
        elif value0 == 'Dir-1':
            if self.GEN.checkNumber(value0, what):
                dic['e1' + xyz] = what
        elif value0 == 'Dir-2':
            if self.GEN.checkNumber(value0, what):
                dic['e2' + xyz] = what
        elif value0 == 'd':
            if self.GEN.checkNumber(value0, what):
                dic['d' + xyz] = what
        elif value0 == 'f':
            if self.GEN.checkNumber(value0, what):
                dic['f' + xyz] = what
        elif value0 == 'c0':
            if self.GEN.checkNumber(value0, what):
                dic['c0'] = what
        elif value0 == 'c1':
            if self.GEN.checkNumber(value0, what):
                dic['c1'] = what
        elif value0 == 'Heat source':
            dic['sourceType'] = what
            self.makeDetailTreeview(self.currentZone, self.cellZoneDict['types'][self.index])
        elif value0 == 'Value [W/m³]' or value0 == 'Value [W]' or value0 == 'Value [K]':
            if self.GEN.checkNumber(value0, what):
                dic['sourceValue'] = what
        
        self.GEN.pickleDump(self.setFileZone, self.cellZoneDict)        
        self.WFILE.MRFProperties(self.cellZoneDict)
        
        porousfile = glob.glob(self.caseDir + '/system/cellZoneConditions_Porous*')
        for ii in porousfile:
            os.system('rm ' + ii)
        self.WFILE.porousFile(self.cellZoneDict)
        
        heatsourcefile = glob.glob(self.caseDir + '/system/cellZoneConditions_heatsource*')
        for ii in heatsourcefile:
            os.system('rm ' + ii)
        self.WFILE.heatsourceFile(self.cellZoneDict)
        
        self.WFILE.fvOptions() 
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
    
        what = model.get_value(iter, 1)
        path = model.get_path(iter)
        
        self.ren1.set_property('visible', 1)
        self.ren1.set_property('has-entry', False)
        self.ren1.set_property('model', self.storeDict['types'])
        self.ren1.set_property('text', self.cellZoneDict['types'][path[0]])
    #---------------------------------------------------------------------------------------------    
    def func_value(self, column, cell, model, iter):
    
        what = model.get_value(iter, 0)
        path = model.get_path(iter)

        dic = self.cellZoneDict['dict'][self.index]
        
        coord = ['Origin', 'Axis', 'Dir-1', 'Dir-2', 'd', 'f']
        singleInput = ['RPM', 'c0', 'c1', 'Value [W/m³]', 'Value [W]', 'Value [K]']
        combo = ['Method', 'Heat source']
        
        if what in coord:
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 1)
            self.ren2_1_value.set_property('visible', 1)
            self.ren2_2_value.set_property('visible', 1)
            self.ren2_0_value.set_property('editable', 1)
            self.ren2_1_value.set_property('editable', 1) 
            self.ren2_2_value.set_property('editable', 1)
            self.ren2_0_value.set_property('has-entry', True)
            self.ren2_1_value.set_property('has-entry', True)
            self.ren2_2_value.set_property('has-entry', True)
            self.ren2_0_value.set_property('model', None)
            self.ren2_1_value.set_property('model', None)
            self.ren2_2_value.set_property('model', None)
            if what == 'Origin':
                self.ren2_0_value.set_property('text', dic['orix'])
                self.ren2_1_value.set_property('text', dic['oriy'])
                self.ren2_2_value.set_property('text', dic['oriz'])
            elif what == 'Axis':
                self.ren2_0_value.set_property('text', dic['axisx'])
                self.ren2_1_value.set_property('text', dic['axisy'])
                self.ren2_2_value.set_property('text', dic['axisz'])
            elif what == 'Dir-1':
                self.ren2_0_value.set_property('text', dic['e1x'])
                self.ren2_1_value.set_property('text', dic['e1y'])
                self.ren2_2_value.set_property('text', dic['e1z'])
            elif what == 'Dir-2':
                self.ren2_0_value.set_property('text', dic['e2x'])
                self.ren2_1_value.set_property('text', dic['e2y'])
                self.ren2_2_value.set_property('text', dic['e2z'])
            elif what == 'd':
                self.ren2_0_value.set_property('text', dic['dx'])
                self.ren2_1_value.set_property('text', dic['dy'])
                self.ren2_2_value.set_property('text', dic['dz'])
            elif what == 'f':
                self.ren2_0_value.set_property('text', dic['fx'])
                self.ren2_1_value.set_property('text', dic['fy'])
                self.ren2_2_value.set_property('text', dic['fz'])
                     
        elif what in singleInput:
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 1)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
            self.ren2_0_value.set_property('editable', 1)
            self.ren2_1_value.set_property('editable', 0) 
            self.ren2_2_value.set_property('editable', 0)
            self.ren2_0_value.set_property('has-entry', True)
            self.ren2_0_value.set_property('model', None)             
            if what == 'RPM':
                self.ren2_0_value.set_property('text', dic['RPM'])
            elif what == 'c0':
                self.ren2_0_value.set_property('text', dic['c0'])
            elif what == 'c1':
                self.ren2_0_value.set_property('text', dic['c1'])
            elif what == 'Value [W/m³]' or what == 'Value [W]' or what == 'Value [K]':
                self.ren2_0_value.set_property('text', dic['sourceValue'])
            
        elif what in combo:
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 1)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
            self.ren2_0_value.set_property('has-entry', False)
            self.ren2_0_value.set_property('editable', 1)
            self.ren2_1_value.set_property('editable', 0) 
            self.ren2_2_value.set_property('editable', 0)             
            if what == 'Method':
                self.ren2_0_value.set_property("model", self.storeDict['poroustype'])
                self.ren2_0_value.set_property('text', dic['porousType'])
            elif what == 'Heat source':
                self.ren2_0_value.set_property("model", self.storeDict['heatsource'])
                self.ren2_0_value.set_property('text', dic['sourceType'])
            
        elif what == 'StaticPatch':
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 0)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
            self.ren2_0_value.set_property('editable', 0)
            self.ren2_1_value.set_property('editable', 0) 
            self.ren2_2_value.set_property('editable', 0)
        elif what in self.bcnameList:
            self.ren1_value.set_property('visible', 1)
            self.ren2_0_value.set_property('visible', 0)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
            self.ren2_0_value.set_property('editable', 0)
            self.ren2_1_value.set_property('editable', 0) 
            self.ren2_2_value.set_property('editable', 0)
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()        
        
        tree_model, tree_iter = self.selection.get_selected()
        value0 = tree_model.get_value(tree_iter, 1)
        value1 = tree_model.get_value(tree_iter, 2)###
        path = tree_model.get_path(tree_iter)
        
        for ii in self.valuebox.get_children():
            self.valuebox.remove(ii)
        self.valuebox.pack_start(self.treeview_value, True, True, 0)
        
        self.currentZone = value0
        self.index = self.cellZones.index(self.currentZone)
        
        self.makeDetailTreeview(self.currentZone, value1)###

        self.valuebox.show_all()
    #---------------------------------------------------------------------------------------------
    def makeDetailTreeview(self, zone, what):   
    
        self.treestore_value.clear()
        
        ind = self.cellZones.index(zone)
        dic = self.cellZoneDict['dict'][ind]
        
        if what == 'MRF':
            self.treestore_value.append(None, ['RPM', None, None])
            self.treestore_value.append(None, ['Origin', None, None])
            self.treestore_value.append(None, ['Axis', None, None])          
            row_static = self.treestore_value.append(None, ['StaticPatch', None, None])               
            for ii in self.bcnameList:            
                if ii in dic['StaticPatch']:            
                    self.treestore_value.append(row_static, [ii, True, None])
                else:
                    self.treestore_value.append(row_static, [ii, False, None])                              

        elif what == 'Porous':
            row_method=self.treestore_value.append(None, ['Method', None, None])
            if dic['porousType']=='Darcy':
                self.treestore_value.append(row_method, ['Dir-1', None, None])
                self.treestore_value.append(row_method, ['Dir-2', None, None])
                self.treestore_value.append(row_method, ['d', None, None])
                self.treestore_value.append(row_method, ['f', None, None])
            else:
                self.treestore_value.append(row_method, ['c0', None, None])
                self.treestore_value.append(row_method, ['c1', None, None])
        
        if self.simDict['Energy'] == 'On':###
            row_hs = self.treestore_value.append(None, ['Heat source', None, None])
            if dic['sourceType'] == 'absolute':
                self.treestore_value.append(row_hs, ['Value [W]', None, None])
            elif dic['sourceType'] == 'specific':
                self.treestore_value.append(row_hs, ['Value [W/m³]', None, None])
            elif dic['sourceType'] == 'fixed.T':
                self.treestore_value.append(row_hs, ['Value [K]', None, None])
            
        displaybutton = gtk.Button('Display Zone')
        displaybutton.connect('clicked', self.displayZone, zone)
        hbox = gtk.HBox()
        hbox.pack_start(displaybutton, True, True, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        
        self.treeview_value.expand_all()
    #---------------------------------------------------------------------------------------------
    def displayZone(self, widget, zoneName):
    
        if not os.path.isdir(self.caseDir + '/VTK/' + zoneName):
            f = open(self.caseDir + '/setSetBatch', 'w')
            f.write('cellSet ' + zoneName + ' new zoneToCell ' + zoneName)
            f.close()
            
            os.system('setSet -case ' + self.caseDir + ' -batch ' + self.caseDir + '/setSetBatch > /dev/null 2>&1')
        
        self.renderer.RemoveAllViewProps()
        for ii in self.vtkFeatureActors:
            self.renderer.AddActor(ii)
            
        zoneActor = self.VTK_All.displayZone(zoneName)
        self.renderer.AddActor(zoneActor)
        
        if self.mainself.discombo.child.get_text() == 'Surface':
            zoneActor.GetProperty().EdgeVisibilityOff()
            zoneActor.GetProperty().SetRepresentation(2)
        elif self.mainself.discombo.child.get_text() == 'SurfaceEdge':
            zoneActor.GetProperty().EdgeVisibilityOn()
            zoneActor.GetProperty().SetRepresentation(2)
        elif self.mainself.discombo.child.get_text() == 'Wireframe':
            zoneActor.GetProperty().SetRepresentationToWireframe()                
                
        self.notebook.set_current_page(0)        
    #---------------------------------------------------------------------------------------------
    def basicDict(self):
    
        baseDict = {}
        keys = ['orix', 'oriy', 'oriz', 'axisx', 'axisy', 'axisz', 'RPM', 'StaticPatch',
                'e1x', 'e1y', 'e1z', 'e2x', 'e2y', 'e2z', 'porousType', 'dx', 'dy', 'dz', 'fx', 'fy', 'fz', 'c0', 'c1',
                'sourceType', 'sourceValue']
        values = ['0', '0', '0', '0', '0', '1', '100', [],
                  '1', '0', '0', '0', '1', '0', 'Darcy', '500', '1e10', '1e10', '0', '0', '0', '1', '2',
                  'None', '100']
        for i in range(len(keys)):
            baseDict[keys[i]] = values[i]
        return baseDict
    #---------------------------------------------------------------------------------------------------------
    def loadCellZoneDict(self):
    
        self.cellZoneDict = self.GEN.pickleLoad(self.setFileZone)
        if self.cellZoneDict == None:
            self.cellZoneDict = {}
            self.cellZoneDict['cellZones'] = self.cellZones
            self.cellZoneDict['types'] = []
            self.cellZoneDict['dict'] = []
            
            for ii in self.cellZones:
                self.cellZoneDict['types'].append('None')
                self.cellZoneDict['dict'].append(self.basicDict())
        else:
            self.cellZones = self.cellZoneDict['cellZones']               
    #-----------------------------------------------------------------------------------------------------------------------
    def getStoreDict(self):
    
        self.liststore_cellZones = gtk.ListStore(str)
        for ii in self.cellZones:
            self.liststore_cellZones.append([ii])
        
        self.liststore_zone_types = gtk.ListStore(str)
        self.typeList = ['None', 'Porous', 'MRF']                                    
        for ii in self.typeList:
            self.liststore_zone_types.append([ii])
        
        self.liststore_poroustypes = gtk.ListStore(str)
        self.poroustypeList = ['Darcy', 'powerLaw']                                    
        for ii in self.poroustypeList:
            self.liststore_poroustypes.append([ii])
        
        self.liststore_heatsource = gtk.ListStore(str)
        self.heatsourceList = ['None', 'specific', 'absolute', 'fixed.T']                                    
        for ii in self.heatsourceList:
            self.liststore_heatsource.append([ii])
        
        self.storeDict = {}
        keys = ['cellZones', 'types', 'poroustype', 'heatsource']
        values = [self.liststore_cellZones, self.liststore_zone_types, self.liststore_poroustypes, self.liststore_heatsource]
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]
    #-----------------------------------------------------------------------------------------------------------------------
    def getNonConstraintPatch(self):
    
        self.bcnameListOri, self.polyPatchTypeListOri = self.GEN.getBCName()
        self.bcnameList = []
        if self.bcnameListOri == False:
            self.bcnameList = []
        for i in range(len(self.bcnameListOri)):
            if self.polyPatchTypeListOri[i] != 'empty' and self.polyPatchTypeListOri[i] != 'wedge':
                self.bcnameList.append(self.bcnameListOri[i])

        
         

