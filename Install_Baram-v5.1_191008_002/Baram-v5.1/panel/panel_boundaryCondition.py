#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelBoundaryConditionClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.renderer = mainself.renderer
        
        self.GEN = generalClass(mainself)
        self.WFILE = writeFileClass(self.caseDir)
        self.DEFAULT = defaultValueClass(self)
        
        self.oldpatch = mainself.selectedPatch
        self.selectedPatch = self.oldpatch
        
        self.vtkActors = mainself.vtkActors
        self.vtkFeatureActors = mainself.vtkFeatureActors
        self.mainself = mainself
                
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')        
       
    def boundaryCondition(self, pickPath):
    
        self.pickPath = pickPath

        self.boundarybox = gtk.VBox()
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.boundarybox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Initial, Boundary Conditions  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox)           
                
        self.vpan = gtk.VPaned()
        self.boundarybox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1 = gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 30)

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
            self.simDict = dicts[0]
        
        self.bcNameList, self.polyPatchTypeList = self.GEN.getBCName()
        if self.bcNameList == False:
            self.bcNameList = []
            self.polyPatchTypeList = []
                   
        self.displayPatchDict = {}
        for ii in self.bcNameList:
            self.displayPatchDict[ii] = True
        #-------------------------------------------------------------------     
        self.setFileInitial = self.caseDir + '/system/settings/initialSettings'
        self.loadIniDict()
        self.getFields()
        self.getBCTypeList()                    
        
        self.setFileBC = self.caseDir + '/system/settings/boundaryTypes'
        self.setFileAMI = self.caseDir + '/system/settings/AMIConditions'
        self.loadAMIDict()        
        self.loadBCDict()
        
        self.liststore_types = gtk.ListStore(str)                   
        for ii in self.btypeList:
            self.liststore_types.append([ii])
        # treeview ------------------------------------------------------------                    
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str)

        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)
        
        self.treeview.connect('cursor-changed', self.selected, self.treeview)
        
        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1 = gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1_0 = gtk.CellRendererText()
        self.ren1_1 = gtk.CellRendererText()
        self.ren1_2 = gtk.CellRendererText()
        self.ren2 = gtk.CellRendererCombo()
        
        self.ren0.set_fixed_size(150, -1)
        self.ren1_0.set_fixed_size(40, -1)
        self.ren1_1.set_fixed_size(40, -1)
        self.ren1_2.set_fixed_size(40, -1)
        
        self.ren1_0.set_property("editable", True)
        self.ren1_1.set_property("editable", True)
        self.ren1_2.set_property("editable", True)
        self.ren2.set_property("editable", True)
        self.ren2.set_property('text-column', 0)
        
        self.ren1_0.connect('edited', self.changeValue, 'x')
        self.ren1_1.connect('edited', self.changeValue, 'y')
        self.ren1_2.connect('edited', self.changeValue, 'z')
        self.ren2.connect('edited', self.changeValue, 'x')
        
        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, text = 1)        
        
        self.tvcolumn1.pack_start(self.ren1_0, True)
        self.tvcolumn1.pack_start(self.ren1_1, True) 
        self.tvcolumn1.pack_start(self.ren1_2, True)
        self.tvcolumn1.pack_start(self.ren2, True)         
        self.tvcolumn1.set_cell_data_func(self.ren1_0, self.func)
        self.tvcolumn1.set_cell_data_func(self.ren2, self.func)

        self.treeview.expand_all()

        self.mainbox.pack_start(self.treeview, True, True, 0)
        
        self.setBCTreestore()
        
        # boundary value---------------------------------------------------------------
        self.setFileBCValue = self.caseDir + '/system/settings/boundaryValues'
        self.loadBCValueDict()
        
        self.treestore_bcvalue = gtk.TreeStore(str, str, str, str)
        
        self.treeview_bcvalue = gtk.TreeView(self.treestore_bcvalue)
        self.treeview_bcvalue.set_enable_tree_lines(True)

        self.tvcolumn0_bcvalue = gtk.TreeViewColumn('Variable')
        self.tvcolumnUnit_bcvalue = gtk.TreeViewColumn('Unit')
        self.tvcolumn1_bcvalue = gtk.TreeViewColumn('Value')
        
        self.treeview_bcvalue.append_column(self.tvcolumn0_bcvalue)
        self.treeview_bcvalue.append_column(self.tvcolumnUnit_bcvalue)
        self.treeview_bcvalue.append_column(self.tvcolumn1_bcvalue)
        
        self.ren0_bcvalue = gtk.CellRendererText()
        self.ren0_bcvalue.set_property("editable", False)
        
        self.renUnit_bcvalue = gtk.CellRendererText()
        self.renUnit_bcvalue.set_property("editable", False)
        
        self.ren1_bcvalue_0 = gtk.CellRendererCombo()
        self.ren1_bcvalue_1 = gtk.CellRendererCombo() 
        self.ren1_bcvalue_2 = gtk.CellRendererCombo()
        
        self.ren0_bcvalue.set_fixed_size(150,- 1)
        
        self.ren1_bcvalue_0.set_fixed_size(40, -1)
        self.ren1_bcvalue_1.set_fixed_size(40, -1)
        self.ren1_bcvalue_2.set_fixed_size(40, -1)
                 
        self.ren1_bcvalue_0.set_property("editable", True)
        self.ren1_bcvalue_1.set_property("editable", True)
        self.ren1_bcvalue_2.set_property("editable", True)
        
        self.ren1_bcvalue_0.set_property('text-column', 0)
        self.ren1_bcvalue_1.set_property('text-column', 0)
        self.ren1_bcvalue_2.set_property('text-column', 0)
        
        self.ren1_bcvalue_0.connect('edited', self.changeValue_bcvalue, 'x')
        self.ren1_bcvalue_1.connect('edited', self.changeValue_bcvalue, 'y')
        self.ren1_bcvalue_2.connect('edited', self.changeValue_bcvalue, 'z')
        
        self.tvcolumn0_bcvalue.pack_start(self.ren0_bcvalue, False)
        self.tvcolumn0_bcvalue.set_attributes(self.ren0_bcvalue, text = 0)
        
        self.tvcolumnUnit_bcvalue.pack_start(self.renUnit_bcvalue, False)
        
        self.tvcolumn1_bcvalue.pack_start(self.ren1_bcvalue_0, True)
        self.tvcolumn1_bcvalue.pack_start(self.ren1_bcvalue_1, True) 
        self.tvcolumn1_bcvalue.pack_start(self.ren1_bcvalue_2, True)         
        self.tvcolumn1_bcvalue.set_cell_data_func(self.ren1_bcvalue_0, self.func_bcvalue)

        self.valuebox.pack_end(self.treeview_bcvalue, True, True, 0) 

        self.mainself.freevbox.pack_start(self.boundarybox, True, True, 0)
               
        if self.pickPath:
            self.treeview.set_cursor(self.pickPath)
        
        self.mainself.window.show_all()
    #--------------------------------------------------------------------------------------------------------- 
    def setBCTreestore(self):
    
        self.treestore.clear()
        
        self.row_ini = self.treestore.append(None, [self.pixbuf_main, 'Initial Conditions', None, None])
        for i in range(len(self.fields)):
            self.treestore.append(self.row_ini, [self.pixbuf_first, self.fields[i], None, None])
        
        self.row_bc = self.treestore.append(None, [self.pixbuf_main, 'Boundary Conditions', None, None])

        self.bcNoAMI = []               
        amis = self.AMIDict.keys()
        notto = None
        for ii in self.bcNameList:
            if not ii in amis:
                self.bcNoAMI.append(ii)
                
        for ii in self.bcNameList:
            htconds = ['isoThermalWall', 'heatFluxWall', 'convectionWall']
            if self.simDict['Energy'] == 'Off':
                if self.boundaryTypeDict[ii] in htconds:
                    self.boundaryTypeDict[ii] = 'adiabaticWall'
            if ii != notto:
                patch = self.treestore.append(self.row_bc, [self.pixbuf_first, ii, self.boundaryTypeDict[ii], None])
                if ii in amis:
                    self.treestore.append(patch, [self.pixbuf_second, self.AMIDict[ii]['couplePatch'], self.boundaryTypeDict[ii], None])
                    notto = self.AMIDict[ii]['couplePatch']
            
        self.treeview.expand_all()    
    #--------------------------------------------------------------------------------------------------------- 
    def func(self, column, cell, model, iter):
    
        value0 = model.get_value(iter, 1)
        path = model.get_path(iter)
        
        if value0 == 'Initial Conditions' or value0 == 'Boundary Conditions':
            self.ren1_0.set_property('visible', 0) 
            self.ren1_1.set_property('visible', 0) 
            self.ren1_2.set_property('visible', 0)
            self.ren2.set_property('visible', 0)
            return
            
        if path[0] == 0:
            self.ren2.set_property('visible', 0)
            if value0 == 'Velocity [m/s]':
                self.ren1_0.set_property('visible', 1)
                self.ren1_0.set_property('text', self.iniDict['X-velocity'])
                self.ren1_1.set_property('visible', 1)
                self.ren1_1.set_property('text', self.iniDict['Y-velocity'])
                self.ren1_2.set_property('visible', 1)
                self.ren1_2.set_property('text', self.iniDict['Z-velocity']) 
            else:
                self.ren1_0.set_property('visible', 1)
                self.ren1_0.set_property('text', self.iniDict[value0])
                self.ren1_1.set_property('visible', 0)
                self.ren1_2.set_property('visible', 0)
 
        elif path[0] == 1:
            self.ren1_0.set_property('visible', 0)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren2.set_property('visible', 1)
            self.ren2.set_property('text', self.boundaryTypeDict[value0])
            ind = self.bcNameList.index(value0)
            if self.polyPatchTypeList[ind] == 'mappedWall':
                self.ren2.set_property('model', None)
                self.ren2.set_property('has-entry', True)
                self.ren2.set_property("editable",  False)
            else:
                self.ren2.set_property('model', self.liststore_types)
                self.ren2.set_property('has-entry', False)
                self.ren2.set_property("editable",  True)               
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what, xyz):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)

        if path[0] == '1':
            old = self.boundaryTypeDict[value0]
        else:
            old = None
        
        if what == old:
            return        

        if path[0] == '0':
            if self.GEN.checkNumber(value0, what):
                if value0 == 'Velocity [m/s]':
                    if xyz == 'x':
                        self.iniDict['X-velocity'] = what
                    elif xyz == 'y':
                        self.iniDict['Y-velocity'] = what
                    elif xyz == 'z':
                        self.iniDict['Z-velocity'] = what
                else:
                    self.iniDict[value0] = what
                self.GEN.pickleDump(self.setFileInitial, self.iniDict)
        else:
            if what == 'internalInterface' or what == 'rotationalPeriodic' or what == 'translationalPeriodic' or what == 'thermoCoupledWall':
                if old=='internalInterface' or old=='rotationalPeriodic' or old=='translationalPeriodic':
                    self.GEN.makeDialog('Sorry!!! Interface or periodic condition cannot be changed directly.  \n' + \
                                         'Change to other type first.')
                else:
                    self.cyclicAMIWindow(value0, what, old)
            elif what == 'empty':
                self.WFILE.changeDictionaryDictNoCyclicAMI(value0, what)
                os.system('changeDictionary -disablePatchGroups -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.changeDictionary')        
                self.boundaryTypeDict[value0] = what
                self.GEN.pickleDump(self.setFileBC, self.boundaryTypeDict)
                self.treestore[path][2] = what
                self.makeDetailTreeview(value0, what)
            else:
                if old == 'internalInterface' or old == 'rotationalPeriodic' or old == 'translationalPeriodic':
                    self.bcNoAMI.append(value0)
                    couplePatch = self.AMIDict[value0]['couplePatch']
                    self.bcNoAMI.append(couplePatch)
                    self.boundaryTypeDict[couplePatch] = what
                    del self.AMIDict[couplePatch]
                    del self.AMIDict[value0]
                    
                    self.GEN.pickleDump(self.setFileAMI, self.AMIDict)                    
                    
                    self.setBCTreestore()
            
                self.boundaryTypeDict[value0] = what
                self.GEN.pickleDump(self.setFileBC, self.boundaryTypeDict)
                self.treestore[path][2] = what
                self.makeDetailTreeview(value0, what)
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()        
        
        tree_model, tree_iter = self.selection.get_selected()
        value0 = tree_model.get_value(tree_iter, 1)
        value1 = tree_model.get_value(tree_iter, 2)
        path=tree_model.get_path(tree_iter)

        if path[0] == 1:
        
            if value0 in self.bcNameList:
        
                for ii in self.valuebox.get_children():
                    self.valuebox.remove(ii)
                self.valuebox.pack_start(self.treeview_bcvalue, True, True, 0)
                
                self.currentPatch = value0
                self.makeDetailTreeview(value0, value1)
                
                self.oldpatch = self.selectedPatch

                self.selectedPatch = value0           
                self.highlightColor()

        self.mainbox.show_all()
    #-----------------------------------------------------------------------------
    def highlightColor(self):
    
        if glob.glob(self.caseDir + '/VTK'):            
            self.displayMode = self.mainself.displayMode
            if self.oldpatch:
                oldind = self.bcNameList.index(self.oldpatch)
            if self.selectedPatch:
                newind = self.bcNameList.index(self.selectedPatch)                
            
            if self.displayMode == 'SurfaceEdge' or self.displayMode == 'Surface' or self.displayMode == 'Wireframe':
                for i in range(self.renderer.GetActors().GetNumberOfItems()):
                    self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetColor(1, 1, 1)
                self.vtkActors[newind].GetProperty().SetColor(0, 0, 1)
            else:
                for ii in self.vtkActors:
                    self.renderer.RemoveActor(ii)
                if self.displayPatchDict[self.selectedPatch] == True:                
                    self.renderer.AddActor(self.vtkActors[newind])
                    self.vtkActors[newind].GetProperty().SetColor(0, 0, 1)
        self.gvtk.Initialize() 
    #-----------------------------------------------------------------------------
    def func_bcvalue(self, column, cell, model, iter):
    
        value0 = model.get_value(iter, 0)
        
        velocityMode = ['noSlip', 'slip', 'rotating', 'translating']          
        liststore_velocityMode = gtk.ListStore(str)
        for ii in velocityMode:
            liststore_velocityMode.append([ii])        
        
        dic = self.boundaryValueDict[self.currentPatch]
        
        three = ['velocity', 'Origin', 'Axis', 'movingVelocity']
        inlfow = ['inflow totalTemperature', 'inflow turbulentIntensity', 'inflow viscosityRatio']
        
        if value0 == 'velocityMode':
            self.renUnit_bcvalue.set_property('text', '')
            self.ren1_bcvalue_0.set_property('has-entry', 0)
            self.ren1_bcvalue_0.set_property('model', liststore_velocityMode)
            self.ren1_bcvalue_0.set_property('text', dic['velocityMode'])
            self.ren1_bcvalue_1.set_property('visible', 0)
            self.ren1_bcvalue_2.set_property('visible', 0)
        elif value0 in three:
            self.ren1_bcvalue_0.set_property('visible', 1)
            self.ren1_bcvalue_1.set_property('visible', 1)
            self.ren1_bcvalue_2.set_property('visible', 1)                        
            self.ren1_bcvalue_0.set_property('model', None)
            self.ren1_bcvalue_0.set_property('has-entry', 1)
            self.ren1_bcvalue_1.set_property('model', None)
            self.ren1_bcvalue_1.set_property('has-entry', 1)
            self.ren1_bcvalue_2.set_property('model', None)
            self.ren1_bcvalue_2.set_property('has-entry', 1)
            if value0 == 'velocity':
                self.renUnit_bcvalue.set_property('text', '[m/s]')            
                self.ren1_bcvalue_0.set_property('text', dic['velocity_x'])
                self.ren1_bcvalue_1.set_property('text', dic['velocity_y'])
                self.ren1_bcvalue_2.set_property('text', dic['velocity_z'])            
            elif value0 == 'Origin':
                self.renUnit_bcvalue.set_property('text', '[-]')
                self.ren1_bcvalue_0.set_property('text', dic['rotatingOrigin_x'])
                self.ren1_bcvalue_1.set_property('text', dic['rotatingOrigin_y'])
                self.ren1_bcvalue_2.set_property('text', dic['rotatingOrigin_z'])
            elif value0 == 'Axis':
                self.renUnit_bcvalue.set_property('text', '[-]')
                self.ren1_bcvalue_0.set_property('text', dic['rotatingAxis_x'])
                self.ren1_bcvalue_1.set_property('text', dic['rotatingAxis_y'])
                self.ren1_bcvalue_2.set_property('text', dic['rotatingAxis_z'])
            elif value0 == 'movingVelocity':
                self.renUnit_bcvalue.set_property('text', '[m/s]') 
                self.ren1_bcvalue_0.set_property('text', dic['movingVelocity_x'])
                self.ren1_bcvalue_1.set_property('text', dic['movingVelocity_y'])
                self.ren1_bcvalue_2.set_property('text', dic['movingVelocity_z'])
        elif value0 in inlfow:
            self.ren1_bcvalue_0.set_property('visible', 1)            
            self.ren1_bcvalue_0.set_property('model', None)
            self.ren1_bcvalue_0.set_property('has-entry', 1)            
            self.ren1_bcvalue_1.set_property('visible', 0)
            self.ren1_bcvalue_2.set_property('visible', 0)        
            if value0 == 'inflow totalTemperature':
                self.ren1_bcvalue_0.set_property('text', dic['totalTemperature'])
                self.renUnit_bcvalue.set_property('text','[K]')
            elif value0 == 'inflow turbulentIntensity':
                self.ren1_bcvalue_0.set_property('text', dic['turbulentIntensity'])
                self.renUnit_bcvalue.set_property('text','[-]')
            elif value0 == 'inflow viscosityRatio':
                self.ren1_bcvalue_0.set_property('text', dic['viscosityRatio'])
                self.renUnit_bcvalue.set_property('text','[-]')
        else:
            self.ren1_bcvalue_0.set_property('visible', 1)
            self.ren1_bcvalue_0.set_property('text', dic[value0])
            self.ren1_bcvalue_0.set_property('model', None)
            self.ren1_bcvalue_0.set_property('has-entry', 1)            
            self.ren1_bcvalue_1.set_property('visible', 0)
            self.ren1_bcvalue_2.set_property('visible', 0)
            if value0 == 'turbulentIntensity':
                self.renUnit_bcvalue.set_property('text','[-]')
            elif value0 == 'viscosityRatio':
                self.renUnit_bcvalue.set_property('text','[-]')
            elif value0 == 'temperature':
                self.renUnit_bcvalue.set_property('text','[K]')
            elif value0 == 'Umag':
                self.renUnit_bcvalue.set_property('text','[m/s]')
            elif value0 == 'massFlowRate':
                self.renUnit_bcvalue.set_property('text','[kg/s]')
            elif value0 == 'rho':
                self.renUnit_bcvalue.set_property('text','[kg/m³]')
            elif value0 == 'totalTemperature':
                self.renUnit_bcvalue.set_property('text','[K]')
            elif value0 == 'volumeFlowRate':
                self.renUnit_bcvalue.set_property('text','[m³/s]')
            elif value0 == 'totalPressure':
                self.renUnit_bcvalue.set_property('text','[Pa]')
            elif value0 == 'heatFlux':
                self.renUnit_bcvalue.set_property('text','[W/m²]')
            elif value0 == 'h':
                self.renUnit_bcvalue.set_property('text','[W/m²K]')
            elif value0 == 'Ta':
                self.renUnit_bcvalue.set_property('text','[K]')
            elif value0 == 'RPM':
                self.renUnit_bcvalue.set_property('text','[-]')
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_bcvalue(self, widget, path, what, xyz):
    
        treeiter = self.treestore_bcvalue.get_iter(path)
        value0 = self.treestore_bcvalue.get_value(treeiter, 0)
        
        if value0 == 'velocity':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['velocity_' + xyz] = what
        elif value0 == 'movingVelocity':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['movingVelocity_' + xyz] = what
        elif value0 == 'Origin':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['rotatingOrigin_' + xyz] = what
        elif value0 == 'Axis':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['rotatingAxis_' + xyz] = what
        elif value0 == 'velocityMode':            
            if what == 'slip' or what == 'noSlip':
                if self.boundaryValueDict[self.currentPatch][value0] == 'translating':
                    self.treestore_bcvalue.remove(self.row_movingVelocity)                
                elif self.boundaryValueDict[self.currentPatch][value0] == 'rotating':
                    self.treestore_bcvalue.remove(self.row_origin)
                    self.treestore_bcvalue.remove(self.row_axis)
                    self.treestore_bcvalue.remove(self.row_rpm)
            elif what == 'translating':
                if self.boundaryValueDict[self.currentPatch][value0] == 'rotating':
                    self.treestore_bcvalue.remove(self.row_origin)
                    self.treestore_bcvalue.remove(self.row_axis)
                    self.treestore_bcvalue.remove(self.row_rpm)
                self.row_movingVelocity=self.treestore_bcvalue.append(None, ['movingVelocity', None, None, None])                       
            elif what == 'rotating':
                if self.boundaryValueDict[self.currentPatch][value0] == 'translating':
                    self.treestore_bcvalue.remove(self.row_movingVelocity)
                self.row_origin = self.treestore_bcvalue.append(None, ['Origin', None, None, None])
                self.row_axis = self.treestore_bcvalue.append(None, ['Axis', None, None, None])
                self.row_rpm = self.treestore_bcvalue.append(None, ['RPM', None, None, None])
            self.boundaryValueDict[self.currentPatch][value0] = what
        elif value0 == 'inflow totalTemperature':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['totalTemperature'] = what
        elif value0 == 'inflow turbulentIntensity':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['turbulentIntensity'] = what
        elif value0 == 'inflow viscosityRatio':
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch]['viscosityRatio'] = what        
        else:
            if self.GEN.checkNumber(value0, what):
                self.boundaryValueDict[self.currentPatch][value0] = what

        self.GEN.pickleDump(self.setFileBCValue, self.boundaryValueDict)                
    #---------------------------------------------------------------------------------------------------------        
    def makeDetailTreeview(self, value0, what):
    
        self.treestore_bcvalue.clear()
        
        turmodel = self.simDict['Turbulence model']

        if what == 'velocityInlet':
            self.treestore_bcvalue.append(None, ['velocity', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['temperature', None, None, None])
            if turmodel != 'laminar':
                self.treestore_bcvalue.append(None, ['turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['viscosityRatio', None, None, None])
                
        elif what == 'surfaceNormalVelocityInlet':
            self.treestore_bcvalue.append(None, ['Umag', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['temperature', None, None, None])
            if turmodel != 'laminar':
                self.treestore_bcvalue.append(None, ['turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['viscosityRatio', None, None, None])
                
        elif what == 'massFlowRateInlet':
            self.treestore_bcvalue.append(None, ['massFlowRate', None, None, None])
            self.treestore_bcvalue.append(None, ['rho', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['totalTemperature', None, None, None])
            if turmodel != 'laminar':
                self.treestore_bcvalue.append(None, ['turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['viscosityRatio', None, None, None])
                
        elif what == 'volumeFlowRateInlet':
            self.treestore_bcvalue.append(None, ['volumeFlowRate', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['temperature', None, None, None])
            if turmodel!='laminar':
                self.treestore_bcvalue.append(None, ['turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['viscosityRatio', None, None, None])
        
        elif what == 'pressureInlet':
            self.treestore_bcvalue.append(None, ['totalPressure', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['totalTemperature', None, None, None])
            if turmodel!='laminar':
                self.treestore_bcvalue.append(None, ['turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['viscosityRatio', None, None, None])
        
        elif what == 'pressureOutlet':
            self.treestore_bcvalue.append(None, ['totalPressure', None, None, None])
            if self.simDict['Energy'] == 'On':
                self.treestore_bcvalue.append(None, ['inflow totalTemperature', None, None, None])
            if turmodel!='laminar':
                self.treestore_bcvalue.append(None, ['inflow turbulentIntensity', None, None, None])
                self.treestore_bcvalue.append(None, ['inflow viscosityRatio', None, None, None])        
        elif what == 'pressureOutletExt':
            self.treestore_bcvalue.append(None, ['totalPressure', None, None, None])
        elif what == 'isoThermalWall':
            self.treestore_bcvalue.append(None, ['temperature', None, None, None])
        elif what == 'heatFluxWall':
            self.treestore_bcvalue.append(None, ['heatFlux', None, None, None])
                
        elif what == 'convectionWall':
            self.treestore_bcvalue.append(None, ['h', None, None, None])
            self.treestore_bcvalue.append(None, ['Ta', None, None, None])
            
        elif what == 'adiabaticWall':
            self.row_velocityMode = self.treestore_bcvalue.append(None, ['velocityMode', None, None, None])
            if self.boundaryValueDict[value0]['velocityMode'] == 'translating':
                self.row_movingVelocity = self.treestore_bcvalue.append(None, ['movingVelocity', None, None, None])
            elif self.boundaryValueDict[value0]['velocityMode'] == 'rotating':
                self.row_origin = self.treestore_bcvalue.append(None, ['Origin', None, None, None])
                self.row_axis = self.treestore_bcvalue.append(None,['Axis', None, None, None])
                self.row_rpm = self.treestore_bcvalue.append(None,['RPM', None, None, None])

        self.treeview_bcvalue.expand_all()
    #---------------------------------------------------------------------------------------------------------
    def loadIniDict(self):
    
        self.iniDict = self.GEN.pickleLoad(self.setFileInitial)
        if self.iniDict == None:
            DEFAULT = defaultValueClass(self)
            dicts = DEFAULT.defaultDict()
            self.iniDict = dicts[1]
    #---------------------------------------------------------------------------------------------------------        
    def loadBCDict(self):
    
        self.boundaryTypeDict = self.GEN.pickleLoad(self.setFileBC)
        
        if self.boundaryTypeDict == None:
            self.boundaryTypeDict = {}
            for i in range(len(self.bcNameList)):
                if self.polyPatchTypeList[i] == 'patch':
                    upper = self.bcNameList[i].upper()
                    if 'OUT' in upper:
                        self.boundaryTypeDict[self.bcNameList[i]] = 'pressureOutletExt' 
                    else:
                        self.boundaryTypeDict[self.bcNameList[i]] = 'surfaceNormalVelocityInlet'
                elif self.polyPatchTypeList[i] == 'wall':
                    self.boundaryTypeDict[self.bcNameList[i]] = 'adiabaticWall'
                elif self.polyPatchTypeList[i] == 'mappedWall':
                    match = self.GEN.getMappedWallType(self.bcNameList[i])
                    self.boundaryTypeDict[self.bcNameList[i]] = 'thermoCoupledWall'
                    dic = {}
                    dic['type'] = 'thermoCoupledWall'
                    dic['couplePatch'] = match
                    self.AMIDict[self.bcNameList[i]] = dic
                    self.GEN.pickleDump(self.setFileAMI, self.AMIDict)
                elif self.polyPatchTypeList[i] == 'cyclicAMI':
                    dic = {}
                    resultList = self.GEN.getAMIType(self.bcNameList[i])                                       
                    transform = resultList[0]
                    
                    if transform == 'rotational':
                        self.boundaryTypeDict[self.bcNameList[i]] = 'rotationalPeriodic'
                        dic['type'] = 'rotationalPeriodic'
                        axis='(' + resultList[2] + ' ' + resultList[3] + ' ' + resultList[4] + ')'
                        if axis == '(1 0 0)':
                            dic['rotationAxis'] = 'x'
                        elif axis == '(0 1 0)':
                            dic['rotationAxis'] = 'y'
                        elif axis == '(0 0 1)':
                            dic['rotationAxis'] = 'z'
                        else:
                            dic['rotationAxis'] = axis
                            print 'Error!!! Rotation Axis is not x/y/z'                            
                        dic['rotationCentre_x'] = resultList[5]
                        dic['rotationCentre_y'] = resultList[6]
                        dic['rotationCentre_z'] = resultList[7]
                        dic['couplePatch'] = resultList[1]
                        self.AMIDict[self.bcNameList[i]] = dic
                        self.GEN.pickleDump(self.setFileAMI, self.AMIDict)
                    elif transform == 'translational':
                        self.boundaryTypeDict[self.bcNameList[i]] = 'translationalPeriodic'
                        dic['type'] = 'translationalPeriodic'
                        dic['separationVector_x'] = resultList[2]
                        dic['separationVector_y'] = resultList[3]
                        dic['separationVector_z'] = resultList[4]
                        dic['couplePatch'] = resultList[1]
                        self.AMIDict[self.bcNameList[i]] = dic
                        self.GEN.pickleDump(self.setFileAMI, self.AMIDict)
                    elif transform == 'noOrdering' or transform == 'coincidentFullMatch':
                        self.boundaryTypeDict[self.bcNameList[i]] = 'internalInterface'
                        dic['type'] = 'internalInterface'
                        dic['couplePatch'] = resultList[1]
                        self.AMIDict[self.bcNameList[i]] = dic
                        self.GEN.pickleDump(self.setFileAMI, self.AMIDict)                    
                    elif transform == None:
                        self.boundaryTypeDict[self.bcNameList[i]] = 'adiabaticWall'                                                                          
                else:                
                    self.boundaryTypeDict[self.bcNameList[i]] = self.polyPatchTypeList[i]
            self.GEN.pickleDump(self.setFileBC, self.boundaryTypeDict)
    #---------------------------------------------------------------------------------------------------------
    def loadAMIDict(self):
    
        self.AMIDict = self.GEN.pickleLoad(self.setFileAMI)
        if self.AMIDict == None:
            self.AMIDict = {}            
    #--------------------------------------------------------------------------------------------------------- 
    def loadBCValueDict(self):
    
        self.boundaryValueDict = self.GEN.pickleLoad(self.setFileBCValue)
        if self.boundaryValueDict == None:
            self.boundaryValueDict = {}
            keys=['velocity_x', 'velocity_y', 'velocity_z', 'Umag', 'massFlowRate', 'rho', 'volumeFlowRate',
                  'totalPressure', 'staticPressure',
                  'temperature', 'heatFlux', 'h', 'Ta', 'totalTemperature',
                  'turbulentIntensity', 'viscosityRatio', 'nuTilda',
                  'velocityMode', 'movingVelocity_x', 'movingVelocity_y', 'movingVelocity_z',
                  'rotatingOrigin_x', 'rotatingOrigin_y', 'rotatingOrigin_z', 'rotatingAxis_x', 'rotatingAxis_y', 'rotatingAxis_z', 'RPM']
            
            values=['1', '0', '0', '1', '1', '1', '1',
                    '0', '0',
                    '300', '1000', '100', '300', '300',
                    '0.001', '10', '1e-8',
                    'noSlip', '0', '0', '0', '0', '0', '0', '0', '0', '1', '100']                      
                
            for i in range(len(self.bcNameList)):
                self.boundaryValueDict[self.bcNameList[i]] = {}
                for j in range(len(keys)):
                    self.boundaryValueDict[self.bcNameList[i]][keys[j]] = values[j]              
                
            self.GEN.pickleDump(self.setFileBCValue, self.boundaryValueDict)
    #---------------------------------------------------------------------------------------------------------
    def cyclicAMIWindow(self, patch, newtype, oldtype):
        
        def closeAMIWindow(widget):
            self.boundaryTypeDict[patch] = oldtype           
            window.destroy()
        
        def applythis(widget):
            for i in range(len(self.bcNoAMI)):
                if setName[i].get_active() == True:
                    selectedpatch = self.bcNoAMI[i]
            makeCouple(selectedpatch)
            
            window.destroy()

        def makeCouple(selectedpatch):
            dic = {}
            dic1 = {}
            dic['type'] = newtype
            dic1['type'] = newtype
            dic['couplePatch'] = selectedpatch
            dic1['couplePatch'] = patch

            self.AMIDict[patch] = dic
            self.AMIDict[selectedpatch] = dic1
            self.GEN.pickleDump(self.setFileAMI, self.AMIDict)
            
            self.boundaryTypeDict[selectedpatch] = newtype
            self.GEN.pickleDump(self.setFileBC, self.boundaryTypeDict)

            indPatch = self.bcNoAMI.index(patch)                            
            indSelected = self.bcNoAMI.index(selectedpatch)            
            
            self.bcNoAMI.remove(patch)
            self.bcNoAMI.remove(selectedpatch)
            
            self.setBCTreestore()
            
            self.boundaryTypeDict[patch] = newtype
            self.GEN.pickleDump(self.setFileBC, self.boundaryTypeDict)
            self.makeDetailTreeview(patch, newtype)
        
        target = None
        
        if patch[-1] == '1' or patch[-1] == '2':
            if patch[-1] == '1':
                target = patch[:-1] + '2'
            else:
                target = patch[:-1] + '1'
            
            if target in self.bcNoAMI:
                response = self.GEN.makeDialog_question('"' + target + '" is coupled patch. OK?' )                              
                if response == -8: # ok
                    if newtype == 'internalInterface':
                        makeCouple(target)
                        return
                    else:
                        pass
                elif response == -9:
                    pass

        self.bcNameList, polyPatchTypeList = self.GEN.getBCName()
        nametype = {}
        for i in range(len(self.bcNameList)):
            nametype[self.bcNameList[i]] = polyPatchTypeList[i]

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Select Interface')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Select coupled patch'), False, False, 15)            
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(5)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        mainbox.pack_start(swin, True, True, 5)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)
        scheight = len(self.bcNameList) * 38
        if scheight > 750:
            scheight = 750        
        swin.set_size_request(300, scheight)

        setName = []
        for i in range(len(self.bcNoAMI)):
            hbox1 = gtk.HBox(False, 5)
            itembox.pack_start(hbox1, False, False, 2)                
            setName.append(gtk.CheckButton(self.bcNoAMI[i], use_underline = False))
            setName[i].set_size_request(180, 28)
            
            if nametype[self.bcNoAMI[i]] != 'cyclicAMI' and self.bcNoAMI[i] != patch:
                hbox1.pack_start(setName[i], False, False, 0)
                
                if self.bcNoAMI[i] == target:
                    if response == -8:
                        setName[i].set_active(1)

        if newtype == 'rotationalPeriodic':        
            r1Entry = gtk.Entry()
            r2Entry = gtk.Entry()
            r3Entry = gtk.Entry()
            r1Entry.set_size_request(60, 28)
            r2Entry.set_size_request(60, 28)
            r3Entry.set_size_request(60, 28)
            r1Entry.set_text('0')
            r2Entry.set_text('0')
            r3Entry.set_text('0')
            
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('rotationCenter'), False, False, 5)
            hbox.pack_end(r3Entry, False, False, 5)
            hbox.pack_end(r2Entry, False, False, 0)
            hbox.pack_end(r1Entry, False, False, 5)

            axisCombo = gtk.combo_box_entry_new_text()
            axisCombo.set_size_request(120, 28)
            axisCombo.append_text('x')
            axisCombo.append_text('y')
            axisCombo.append_text('z')
            axisCombo.set_active(2)
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('rotationAxis'), False, False, 5)
            hbox.pack_end(axisCombo, False, False, 5)

        elif newtype == 'translationalPeriodic':
            c1Entry = gtk.Entry()
            c2Entry = gtk.Entry()
            c3Entry = gtk.Entry()
            c1Entry.set_size_request(60, 28)
            c2Entry.set_size_request(60, 28)
            c3Entry.set_size_request(60, 28)
            c1Entry.set_text('0')
            c2Entry.set_text('0')
            c3Entry.set_text('0')
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('Separation vector, 1st to 2nd'), False, False, 5)
            hbox.pack_end(c3Entry, False, False, 5)
            hbox.pack_start(c2Entry, False, False, 0)
            hbox.pack_end(c1Entry, False, False, 5)
        
        hbox2 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox2, False, False, 5)
        app = gtk.Button('Apply')
        app.set_size_request(100, 28)
        app.connect('clicked', applythis)
        cll = gtk.Button('Cancel')
        cll.set_size_request(100, 28)
        cll.connect('clicked', closeAMIWindow)
        hbox2.pack_end(cll, False, False, 5)
        hbox2.pack_end(app, False, False, 5)
        
        window.show_all()
    #-----------------------------------------------------------------------------------------------------------------------
    def getFields(self):
    
        if self.simDict['Turbulence model'] == 'laminar':
            if self.simDict['Energy'] == 'Off':
                self.fields = ['Velocity [m/s]', 'Pressure [Pa]']
            else:
                self.fields = ['Velocity [m/s]', 'Pressure [Pa]', 'Temperature [K]']            
        else:
            if self.simDict['Energy'] == 'Off':
                self.fields = ['Velocity [m/s]', 'Pressure [Pa]', 'velocityScale [m/s]', 'turbulentIntensity', 'viscosityRatio']
            else:
                self.fields = ['Velocity [m/s]', 'Pressure [Pa]', 'Temperature [K]', 'velocityScale [m/s]', 'turbulentIntensity', 'viscosityRatio']
    #-----------------------------------------------------------------------------------------------------------------------
    def getBCTypeList(self):
        
        if self.simDict['Energy'] == 'Off':
            self.btypeList = ['velocityInlet', 'surfaceNormalVelocityInlet', 'massFlowRateInlet', 'volumeFlowRateInlet',
                              'pressureInlet', 'pressureOutlet', 'pressureOutletExt',
                              'adiabaticWall', 'thermoCoupledWall',
                              'symmetry', 'internalInterface', 'rotationalPeriodic', 'translationalPeriodic',
                              'empty']       
        else:
            self.btypeList = ['velocityInlet', 'surfaceNormalVelocityInlet', 'massFlowRateInlet', 'volumeFlowRateInlet',
                              'pressureInlet', 'pressureOutlet', 'pressureOutletExt',
                              'adiabaticWall', 'isoThermalWall', 'heatFluxWall', 'convectionWall', 'thermoCoupledWall',
                              'symmetry', 'internalInterface', 'rotationalPeriodic', 'translationalPeriodic',
                              'empty']        




