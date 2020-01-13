#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelMonitoringClass:
                
    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.solver = mainself.solver
        self.terminal = mainself.terminal
        self.installpath = mainself.installpath
        self.renderer = mainself.renderer

        self.GEN = generalClass(self)        
        self.WFILE = writeFileClass(self.caseDir)
        self.DEFAULT = defaultValueClass(self)
        self.POST = postProcessingClass(self)
        
        self.Renderer = mainself.renderer        
        self.VTK_All = VTKStuff(mainself.caseDir)
        
        self.bcNameList, self.polyTypeList = self.GEN.getBCName()
        if self.bcNameList == False:
            self.bcNameList = []
            self.polyTypeList = []        
            
        self.selectedItem = None
        self.selectedName = None
            
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png') 
    #------------------------------------------------------------------------------------------
    def monitoring(self):

        self.monitorbox = gtk.VBox()
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.monitorbox.pack_start(frame, False, False, 0)
        label=gtk.Label()
        label.set_markup('<b>  Monitoring  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox)           
        
        self.vpan = gtk.VPaned()
        self.monitorbox.pack_start(self.vpan, True, True, 0)

        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 100)
        
        self.underbox = gtk.VBox(False, 0)

        self.vpan.pack1(swin, False, True)
        self.vpan.pack2(self.underbox, False, True)
        
        self.underbox.pack_start(swin1)
        
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

        self.setFileMonitor = self.caseDir + '/system/settings/monitorSetup'
        self.loadMonitorDict()
        self.getFields()        
        self.getStoreDict()
        
        # treeview-----------------------------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str)

        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_visible(False)       
        self.treeview.set_enable_tree_lines(True)
        
        self.treeview.connect('cursor-changed', self.selected, self.treeview)

        self.tvcolumn0 = gtk.TreeViewColumn(None)
            
        self.treeview.append_column(self.tvcolumn0)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()

        self.ren0.set_property('editable', False)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)

        self.treeview.expand_all()
        
        self.mainbox.add(self.treeview)

        self.setMonitorTreestore()
        
        # value -------------------------------------------------------------------------------------
        self.treestore_value = gtk.TreeStore(str, bool, str)
        
        self.treeview_value = gtk.TreeView(self.treestore_value)
        self.treeview_value.set_enable_tree_lines(True)        
      
        self.tvcolumn0_value = gtk.TreeViewColumn('Variable       ')
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
        self.ren2_1_value.set_property('text-column', 1)
        self.ren2_2_value.set_property('text-column', 2)
        
        self.tvcolumn0_value.pack_start(self.ren0_value, False)
        self.tvcolumn0_value.pack_start(self.ren1_value, True)
        self.tvcolumn2_value.pack_start(self.ren2_0_value, True)
        self.tvcolumn2_value.pack_start(self.ren2_1_value, True)
        self.tvcolumn2_value.pack_start(self.ren2_2_value, True)

        self.tvcolumn0_value.set_attributes(self.ren0_value, markup = 0)
        self.tvcolumn0_value.add_attribute(self.ren1_value, 'active', 1)

        self.ren1_value.connect('toggled', self.toggleMonitor, self.treestore_value)
        self.ren2_0_value.connect('edited', self.changeValue, 'x')
        self.ren2_1_value.connect('edited', self.changeValue, 'y')
        self.ren2_2_value.connect('edited', self.changeValue, 'z')              
        self.tvcolumn2_value.set_cell_data_func(self.ren2_0_value, self.func)
        
        self.treeview_value.expand_all()
        
        self.valuebox.add(self.treeview_value)
        self.makeMonitorButton()
        
        return self.monitorbox

    #---------------------------------------------------------------------------------------------------------
    def setMonitorTreestore(self):
    
        self.treestore.clear()
        
        row_force = self.treestore.append(None, [self.pixbuf_main, 'Force'])
        row_point = self.treestore.append(None, [self.pixbuf_main, 'Point'])
        row_surface = self.treestore.append(None, [self.pixbuf_main, 'Surface'])
        
        keys = self.monitorDict.keys()        
        keys.sort()

        forces = []
        points = []
        surfaces = []
        for ii in keys:
            if self.monitorDict[ii]['type'] == 'force':forces.append(ii)
            elif self.monitorDict[ii]['type'] == 'point':points.append(ii)
            elif self.monitorDict[ii]['type'] == 'surface':surfaces.append(ii)
        
        for ii in forces:self.treestore.append(row_force, [self.pixbuf_first, ii])
        for ii in points:self.treestore.append(row_point, [self.pixbuf_first, ii])
        for ii in surfaces:self.treestore.append(row_surface, [self.pixbuf_first, ii])
        
        self.treeview.expand_all()
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
    
        what = model.get_value(iter, 0)
        path = model.get_path(iter)
        
        if self.selectedName == None:
            return
        
        name = self.selectedName             
         
        entrys = ['Reference Area [m²]', 'Reference Length [m]', 'Reference Velocity [m/s]', 'Reference Density [kg/m³]', 'Interval']
        three = ['Drag Direction', 'Lift Direction', 'Pitch Axis', 'Center of Rotation', 'Coordinate']
        combo = ['Mode', 'Field', 'Patch']

        if what == 'Patches':
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 0)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
        elif what in entrys:
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 1)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
            self.ren2_0_value.set_property('has-entry', 1)
            self.ren2_0_value.set_property('model', None)
            if what == 'Reference Area [m²]':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Reference Area [m²]'])
            elif what == 'Reference Length [m]':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Reference Length [m]'])
            elif what == 'Reference Velocity [m/s]':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Reference Velocity [m/s]'])
            elif what == 'Reference Density [kg/m³]':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Reference Density [kg/m³]'])
            elif what == 'Interval':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Interval'])
        elif what in three:
            self.ren1_value.set_property('visible', 0)
            self.ren2_0_value.set_property('visible', 1)
            self.ren2_1_value.set_property('visible', 1)
            self.ren2_2_value.set_property('visible', 1)
            self.ren2_0_value.set_property('has-entry', 1)
            self.ren2_0_value.set_property('model', None)
            self.ren2_1_value.set_property('has-entry', 1)
            self.ren2_1_value.set_property('model', None)
            self.ren2_2_value.set_property('has-entry', 1)
            self.ren2_2_value.set_property('model', None)
            if what == 'Drag Direction':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['dragDir_x'])
                self.ren2_1_value.set_property('text', self.monitorDict[name]['dragDir_y'])
                self.ren2_2_value.set_property('text', self.monitorDict[name]['dragDir_z'])
            elif what == 'Lift Direction':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['liftDir_x'])
                self.ren2_1_value.set_property('text', self.monitorDict[name]['liftDir_y'])
                self.ren2_2_value.set_property('text', self.monitorDict[name]['liftDir_z'])
            elif what == 'Pitch Axis':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['pitchAxis_x'])
                self.ren2_1_value.set_property('text', self.monitorDict[name]['pitchAxis_y'])
                self.ren2_2_value.set_property('text', self.monitorDict[name]['pitchAxis_z'])
            elif what == 'Center of Rotation':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['CofR_x'])
                self.ren2_1_value.set_property('text', self.monitorDict[name]['CofR_y'])
                self.ren2_2_value.set_property('text', self.monitorDict[name]['CofR_z'])
            elif what == 'Coordinate':
                self.ren2_0_value.set_property('text', self.monitorDict[name]['x-coord'])
                self.ren2_1_value.set_property('text', self.monitorDict[name]['y-coord'])
                self.ren2_2_value.set_property('text', self.monitorDict[name]['z-coord'])       
        elif what in self.bcNameList:
            self.ren1_value.set_property('visible', 1)
            self.ren2_0_value.set_property('visible', 0)
            self.ren2_1_value.set_property('visible', 0)
            self.ren2_2_value.set_property('visible', 0)
        elif what in combo:
            self.ren1_value.set_property('visible', False)
            self.ren2_0_value.set_property('visible', True)
            self.ren2_1_value.set_property('visible', False)
            self.ren2_2_value.set_property('visible', False)
            self.ren2_0_value.set_property('has-entry', False)
            if what == 'Field':                
                self.ren2_0_value.set_property('model', self.storeDict['fields'])        
                if self.selectedItem == 'point':
                    self.ren2_0_value.set_property('text', self.monitorDict[name]['Field_point'])
                elif self.selectedItem == 'surface':
                    self.ren2_0_value.set_property('text', self.monitorDict[name]['Field_surface'])
            elif what == 'Mode':
                self.ren2_0_value.set_property('model', self.storeDict['modes'])        
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Mode'])
            elif what == 'Patch':
                if self.monitorDict[name]['Mode'] == 'Flowrate':
                    self.ren2_0_value.set_property('model', self.storeDict['patchPatches'])
                else:
                    self.ren2_0_value.set_property('model', self.storeDict['patches'])      
                self.ren2_0_value.set_property('text', self.monitorDict[name]['Patch'])                  
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what, xyz):
    
        treeiter = self.treestore_value.get_iter(path)
        value0 = self.treestore_value.get_value(treeiter, 0)

        name = self.selectedName

        if value0 == 'Drag Direction':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.monitorDict[name]['dragDir_x'] = what
                elif xyz == 'y':
                    self.monitorDict[name]['dragDir_y'] = what
                elif xyz == 'z':
                    self.monitorDict[name]['dragDir_z'] = what
        elif value0 == 'Lift Direction':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.monitorDict[name]['liftDir_x'] = what
                elif xyz == 'y':
                    self.monitorDict[name]['liftDir_y'] = what
                elif xyz == 'z':
                    self.monitorDict[name]['liftDir_z'] = what
        elif value0 == 'Pitch Axis':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.monitorDict[name]['pitchAxis_x'] = what
                elif xyz == 'y':
                    self.monitorDict[name]['pitchAxis_y'] = what
                elif xyz == 'z':
                    self.monitorDict[name]['pitchAxis_z'] = what
        elif value0 == 'Center of Rotation':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.monitorDict[name]['CofR_x'] = what
                elif xyz == 'y':
                    self.monitorDict[name]['CofR_y'] = what
                elif xyz == 'z':
                    self.monitorDict[name]['CofR_z'] = what
        elif value0 == 'Coordinate':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.monitorDict[name]['x-coord'] = what
                elif xyz == 'y':
                    self.monitorDict[name]['y-coord'] = what
                elif xyz == 'z':
                    self.monitorDict[name]['z-coord'] = what
        elif value0 == 'Field':
            if self.selectedItem == 'point':
                self.monitorDict[name]['Field_point'] = what
            elif self.selectedItem == 'surface':
                self.monitorDict[name]['Field_surface'] = what
        elif value0 == 'Mode':
            self.monitorDict[name]['Mode'] = what
            if what == 'Flowrate':
                if self.monitorDict[name]['Patch'] in self.patchList:
                    pass
                else:
                    self.monitorDict[name]['Patch'] = self.patchList[0]
        elif value0 == 'Interval':
            if self.GEN.checkNumber(value0, what):
                self.monitorDict[name]['Interval'] = what
        else:
            self.monitorDict[name][value0] = what            
       
        self.makeDetailTreeview(name)
            
        self.GEN.pickleDump(self.setFileMonitor, self.monitorDict)
        self.writeFiles()
    #--------------------------------------------------------   
    def toggleMonitor(self, widget, path, model):

        model[path][1] = not model[path][1]               
        value0 = model[path][0]
        value1 = model[path][1]

        name = self.selectedName
              
        if value1 == True:
            self.monitorDict[name]['Patches_force'].append(value0)
        else:
            self.monitorDict[name]['Patches_force'].remove(value0)
        
        self.GEN.pickleDump(self.setFileMonitor, self.monitorDict)
        self.writeFiles()
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        value0 = tree_model.get_value(tree_iter,1)
        path = tree_model.get_path(tree_iter)
            
        if tree_iter:
            if len(path) == 2:
                self.selectedName = value0
                if path[0] == 0:
                    self.selectedItem = 'force'
                elif path[0] == 1:
                    self.selectedItem = 'point'
                elif path[0] == 2:
                    self.selectedItem = 'surface'                    
                self.makeDetailTreeview(value0)
            else:
                self.selectedName=None
                if path[0] == 0:
                    self.selectedItem = 'force'
                elif path[0] == 1:
                    self.selectedItem = 'point'
                elif path[0] == 2:
                    self.selectedItem = 'surface'        
    #---------------------------------------------------------------------------------------------
    def makeDetailTreeview(self, name):   
    
        self.treestore_value.clear()
        
        if self.selectedItem == 'force':
            self.treestore_value.append(None, ['Reference Area [m²]', None, None])
            self.treestore_value.append(None, ['Reference Length [m]', None, None])
            self.treestore_value.append(None, ['Reference Velocity [m/s]', None, None])
            self.treestore_value.append(None, ['Reference Density [kg/m³]', None, None])
            self.treestore_value.append(None, ['Drag Direction', None, None])
            self.treestore_value.append(None, ['Lift Direction', None, None])
            self.treestore_value.append(None, ['Pitch Axis', None, None])
            self.treestore_value.append(None, ['Center of Rotation', None, None])
            row_patch = self.treestore_value.append(None, ['Patches', None, None])
            for ii in self.wallList:
                if ii in self.monitorDict[self.selectedName]['Patches_force']:
                    self.treestore_value.append(row_patch, [ii, True, None])
                else:
                    self.treestore_value.append(row_patch, [ii, False, None])
        elif self.selectedItem == 'point':
            self.treestore_value.append(None, ['Field', None, None])
            self.treestore_value.append(None, ['Interval', None, None])
            self.treestore_value.append(None, ['Coordinate', None, None])
        elif self.selectedItem == 'surface':
            self.treestore_value.append(None, ['Mode', None, None])
            if self.monitorDict[self.selectedName]['Mode'] == 'Integrate' or self.monitorDict[self.selectedName]['Mode'] == 'Average':
                self.treestore_value.append(None, ['Field', None, None])
            self.treestore_value.append(None, ['Patch', None, None])
            
        self.treeview_value.expand_all()
    # -------------------------------------------------------------------------
    def loadMonitorDict(self):
    
        self.monitorDict = self.GEN.pickleLoad(self.setFileMonitor)
        if self.monitorDict == None:
            self.monitorDict = {}           
    #---------------------------------------------------------------------------------------------
    def makeMonitorButton(self):
    
        POST = postProcessingClass(self)        
        
        addButton = gtk.Button('Add')
        delButton = gtk.Button('Delete')
        addButton.set_size_request(100, 28)
        delButton.set_size_request(100, 28)
        addButton.connect('clicked', self.addButton)
        delButton.connect('clicked', self.deleteButton)
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(addButton, True, True, 0)
        hbox.pack_start(delButton, True, True, 0)                 
        
        plotForceB = gtk.Button('Plot force')
        plotPointB = gtk.Button('Plot point')
        plotSurfaceB = gtk.Button('Plot surface')
        plotForceB.set_size_request(100, 28)
        plotPointB.set_size_request(100, 28)
        plotSurfaceB.set_size_request(100, 28)
        plotForceB.connect('clicked', self.POST.plotForce, self.monitorDict)
        plotPointB.connect('clicked', self.POST.plotPoint, self.monitorDict)
        plotSurfaceB.connect('clicked', self.POST.plotSurface, self.monitorDict)                
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(plotForceB, True, True, 0)
        hbox.pack_start(plotPointB, True, True, 0)
        hbox.pack_start(plotSurfaceB, True, True, 0)
        
        saveForceB = gtk.Button('Save force')
        savePointB = gtk.Button('Save point')
        saveSurfaceB = gtk.Button('Save surface')
        saveForceB.set_size_request(100, 28)
        savePointB.set_size_request(100, 28)
        saveSurfaceB.set_size_request(100, 28)
        saveForceB.connect('clicked', self.saveForce)
        savePointB.connect('clicked', self.savePoint)
        saveSurfaceB.connect('clicked', self.saveSurface)                
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(saveForceB, True, True, 0)
        hbox.pack_start(savePointB, True, True, 0)
        hbox.pack_start(saveSurfaceB, True, True, 0)

        plotResidualB = gtk.Button('Plot residual')
        plotResidualB.set_size_request(100, 28)
        plotResidualB.connect('clicked', self.POST.plotResidual)                
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(plotResidualB, True, True, 0)
    #---------------------------------------------------------------------------------------------
    def addButton(self, widget):
    
        if self.selectedItem == None:
            self.GEN.makeDialog('Warning!!! Select "Force" or "Point" or "Surface"')
            return
        name = self.getNewName() 

        self.monitorDict[name] = {}
        self.monitorDict[name]['Reference Area [m²]'] = '1'
        self.monitorDict[name]['Reference Length [m]'] = '1'
        self.monitorDict[name]['Reference Velocity [m/s]'] = '1'
        self.monitorDict[name]['Reference Density [kg/m³]'] = '1'
        self.monitorDict[name]['dragDir_x'] = '1'
        self.monitorDict[name]['dragDir_y'] = '0'
        self.monitorDict[name]['dragDir_z'] = '0'
        self.monitorDict[name]['liftDir_x'] = '0'
        self.monitorDict[name]['liftDir_y'] = '0'
        self.monitorDict[name]['liftDir_z'] = '1'
        self.monitorDict[name]['pitchAxis_x'] = '0'
        self.monitorDict[name]['pitchAxis_y'] = '1'
        self.monitorDict[name]['pitchAxis_z'] = '0'
        self.monitorDict[name]['CofR_x'] = '0'
        self.monitorDict[name]['CofR_y'] = '0'
        self.monitorDict[name]['CofR_z'] = '0'
        self.monitorDict[name]['Patches_force'] = []
            
        self.monitorDict[name]['x-coord'] = '0'
        self.monitorDict[name]['y-coord'] = '0'
        self.monitorDict[name]['z-coord'] = '0'
        self.monitorDict[name]['Field_point'] = 'p'
        self.monitorDict[name]['Interval'] = '1'
            
        self.monitorDict[name]['Field_surface'] = 'p'
        self.monitorDict[name]['Patch'] = self.bcNameList[0]
        self.monitorDict[name]['Mode'] = 'Average'

        self.monitorDict[name]['type'] = self.selectedItem
  
        self.setMonitorTreestore()

        self.GEN.pickleDump(self.setFileMonitor, self.monitorDict)
        
        self.writeFiles()
        self.modifyControlDict()
    #---------------------------------------------------------------------------------------------
    def deleteButton(self, widget):
    
        if self.selectedName == None:
            self.GEN.makeDialog('Warning!!! Select name to delete')
            return
        else:
            if self.monitorDict[self.selectedName]['type'] == 'point':
                os.system('rm ' + self.caseDir + '/system/pointProbe_' + self.selectedName)
            elif self.monitorDict[self.selectedName]['type'] == 'surface':
                os.system('rm ' + self.caseDir + '/system/surfaceProbe_' + self.selectedName)
            elif self.monitorDict[self.selectedName]['type'] == 'force':
                os.system('rm ' + self.caseDir + '/system/forces_' + self.selectedName)
                os.system('rm ' + self.caseDir + '/system/forceCoeffs_' + self.selectedName)

            del self.monitorDict[self.selectedName]            
            self.setMonitorTreestore()
            self.treestore_value.clear()
        self.treeview.expand_all()              
    #----------------------------------------------------------------------------------------------    
    def modifyControlDict(self):
           
        setFile = self.caseDir + '/system/settings/runConditions'
        runDict = self.GEN.pickleLoad(setFile)
        if runDict == None:
            DEFAULT = defaultValueClass(self)
            dicts = DEFAULT.defaultDict()
            runDict = dicts[2]
            if self.solver == 'pimpleDyMNFoam' or self.solver == 'interPhaseChangeNFoam':
                runDict['endTime'] = '1'
                runDict['deltaT'] = '0.001'
        self.WFILE.controlDictFile(runDict, self.solver)      
    #----------------------------------------------------------------------------------------------    
    def getFields(self):
    
        if self.simDict['Turbulence model'] == 'kOmegaSST':
            self.turfield = ['k', 'omega']
        elif self.simDict['Turbulence model'] == 'SpalartAllmaras':
            self.turfield = ['nuTilda']
        elif self.simDict['Turbulence model'] == 'laminar':
            self.turfield = []
        else:
            self.turfield=['k', 'epsilon']
        
        if self.simDict['Energy'] == 'Off':
            self.fields = ['Umag', 'p']
        elif self.simDict['Energy'] == 'On':
            self.fields = ['Umag', 'p', 'p_rgh', 'T']
        
        for ii in self.turfield:
            self.fields.append(ii)
    #----------------------------------------------------------------------------------------------    
    def getStoreDict(self):
    
        self.liststore_fields = gtk.ListStore(str)
        for ii in self.fields:
            self.liststore_fields.append([ii])
        
        self.liststore_patchPatches = gtk.ListStore(str)
        for ii in self.patchList:
            self.liststore_patchPatches.append([ii])
        
        modes = ['Flowrate', 'Average', 'Integrate']
        self.liststore_modes = gtk.ListStore(str)
        for ii in modes:
            self.liststore_modes.append([ii])
        
        self.liststore_patches = gtk.ListStore(str)
        for ii in self.bcNameList:
            self.liststore_patches.append([ii])
        
        self.storeDict = {}
        keys = ['fields', 'patchPatches', 'modes', 'patches']
        values = [self.liststore_fields, self.liststore_patchPatches, self.liststore_modes, self.liststore_patches]
        
        for i in range(len(keys)):
            self.storeDict[keys[i]] = values[i]        
    #---------------------------------------------------------------------------------------------
    def getNewName(self):
    
        names = self.monitorDict.keys()
        forces = []
        points = []
        surfaces = []
        for ii in names:
            if ii[:5] == 'force':forces.append(ii)
            elif ii[:5] == 'point':points.append(ii)
            elif ii[:7] == 'surface':surfaces.append(ii)

        if self.selectedItem == 'force':
            nums = []
            for ii in forces:
                aa = ii.split('-')            
                nums.append(int(aa[1]))
            if nums == []:
                name = 'force-0'
            else:
                name = 'force-' + str(max(nums) + 1)

        elif self.selectedItem == 'point':
            nums = []
            for ii in points:
                aa = ii.split('-')            
                nums.append(int(aa[1]))
            if nums == []:
                name = 'point-0'
            else:
                name = 'point-' + str(max(nums) + 1)    
            
        elif self.selectedItem == 'surface':
            nums = []
            for ii in surfaces:
                aa = ii.split('-')            
                nums.append(int(aa[1]))
            if nums == []:
                name = 'surface-0'
            else:
                name = 'surface-' + str(max(nums) + 1)            
        return name  
    #---------------------------------------------------------------------------------------------
    def writeFiles(self):
    
        names = self.monitorDict.keys()
        forces = []
        points = []
        surfaces = []
        for ii in names:
            if ii[:5] == 'force':forces.append(ii)
            elif ii[:5] == 'point':points.append(ii)
            elif ii[:7] == 'surface':surfaces.append(ii)
            
        for ii in forces:
            self.WFILE.forceFile(self.monitorDict[ii], ii, self.simDict)
            
        for ii in points:
            self.WFILE.pointProbeFile(self.monitorDict[ii], ii)
            
        for ii in surfaces:
            self.WFILE.surfaceProbeFile(self.monitorDict[ii], ii)
    #---------------------------------------------------------------------------------------------
    def saveForce(self,widget):
    
        if self.selectedName == None:
            self.GEN.makeDialog('Warning!!! Select force to save')
            return
        else:
            if self.selectedItem != 'force':
                self.GEN.makeDialog('Warning!!! Select force to save')
                return
            else:
                self.POST.saveForce(self.selectedName, self.monitorDict)
    #---------------------------------------------------------------------------------------------
    def savePoint(self, widget):
    
        if self.selectedName == None:
            self.GEN.makeDialog('Warning!!! Select point to save')
            return
        else:
            if self.selectedItem != 'point':
                self.GEN.makeDialog('Warning!!! Select point to save')
                return
            else:
                self.POST.savePoint(self.selectedName, self.monitorDict)    
    #---------------------------------------------------------------------------------------------
    def saveSurface(self, widget):
    
        if self.selectedName == None:
            self.GEN.makeDialog('Warning!!! Select surface to save')
            return
        else:
            if self.selectedItem != 'surface':
                self.GEN.makeDialog('Warning!!! Select surface to save')
                return
            else:
                self.POST.saveSurface(self.selectedName, self.monitorDict)  
    
        
