#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelCfMeshClass:
                
    def __init__(self, mainself):

        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal

        self.renderer = mainself.renderer
        self.Widget_OriMarker = mainself.Widget_OriMarker
        
        self.GEN = generalClass(mainself)
        self.VTK_All = VTKStuff(mainself.caseDir)

        self.AllActors = None
        self.farActor = []
        self.objectActor = []
        self.selectToDel = []
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')  
    #------------------------------------------------------------------------------------------
    def cfMesh(self):

        self.cfmeshbox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.cfmeshbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Create Mesh with cfMesh  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.cfmeshbox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 300)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 20)

        self.underbox = gtk.VBox(False, 0)
                
        self.vpan.pack1(swin, False, True)
        self.vpan.pack2(self.underbox, False, True)
        
        self.underbox.pack_start(swin1)
        
        self.rangebox = gtk.VBox(False, 0)
        self.underbox.pack_start(self.rangebox, False, False, 0)

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
                  
        self.setFile = self.caseDir + '/system/settings/cfMeshSet'
        self.setFilePatch = self.caseDir + '/system/settings/cfMeshPatchSet'
        self.setFileObject = self.caseDir + '/system/settings/cfMeshObjectSet'
        self.loadCfMeshDict()

        # treeview plane ----------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool, str, bool)        

        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect('cursor-changed', self.selected, self.treeview)
        
        self.treeview.set_headers_visible(True)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(False)
        
        self.tvcolumn0 = gtk.TreeViewColumn('Item')
        self.tvcolumn1 = gtk.TreeViewColumn('Show')
        self.tvcolumn2 = gtk.TreeViewColumn('Value')
        self.tvcolumn3 = gtk.TreeViewColumn('Layer')
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        self.treeview.append_column(self.tvcolumn2)
        self.treeview.append_column(self.tvcolumn3)
                
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererToggle()
        self.ren2 = gtk.CellRendererCombo()
        self.ren3 = gtk.CellRendererToggle()
        
        self.ren1.set_fixed_size(50, -1)
        self.ren2.set_fixed_size(80, -1)
        self.ren3.set_fixed_size(50, -1)
                          
        self.ren0.set_property('editable', False)
        self.ren1.set_property("activatable", True)
        self.ren2.set_property('editable', True)
        self.ren2.set_property('text-column', 0)
        self.ren3.set_property('activatable', True)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn1.pack_start(self.ren1, False) 
        self.tvcolumn2.pack_start(self.ren2, True)
        self.tvcolumn3.pack_start(self.ren3, False)

        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        self.tvcolumn1.add_attribute(self.ren1, 'active', 2)
        self.tvcolumn3.add_attribute(self.ren3, 'active', 4)

        self.ren1.connect('toggled', self.toggleRen, self.treestore)
        self.ren2.connect('edited', self.changeValue)
        self.ren3.connect('toggled', self.toggleRen3, self.treestore)
        
        self.tvcolumn2.set_cell_data_func(self.ren2, self.func)
        
        self.makeTreeStore()
        
        self.treeview.expand_all()
        self.mainbox.add(self.treeview)

        self.initialRendering()
        # treeview common---------------------------------------------------------------
        self.treestore_common = gtk.TreeStore(str, str, str, str)        

        self.treeview_common = gtk.TreeView(self.treestore_common)
        self.treeview_common.set_enable_tree_lines(True)
        
        self.tvcolumn0_common = gtk.TreeViewColumn('    ITEMs')
        self.tvcolumn1_common = gtk.TreeViewColumn('  VALUE')
        
        self.treeview_common.append_column(self.tvcolumn0_common)
        self.treeview_common.append_column(self.tvcolumn1_common)
        
        self.ren0_common = gtk.CellRendererText()
        self.ren1_common = gtk.CellRendererCombo()
        self.ren2_common = gtk.CellRendererCombo()
        self.ren3_common = gtk.CellRendererCombo() 
        
        self.ren0_common.set_fixed_size(120, -1)

        self.ren0_common.set_property("editable", False)                 
        self.ren1_common.set_property("editable", True)
        self.ren2_common.set_property("editable", True)
        self.ren3_common.set_property("editable", True)

        self.ren1_common.set_property('text-column', 0)
        self.ren2_common.set_property('text-column', 0)
        self.ren3_common.set_property('text-column', 0)
                
        self.ren1_common.connect('edited', self.changeValue_common, 'x')
        self.ren2_common.connect('edited', self.changeValue_common, 'y')
        self.ren3_common.connect('edited', self.changeValue_common, 'z')
        
        self.tvcolumn0_common.pack_start(self.ren0_common, False)                        
        self.tvcolumn1_common.pack_start(self.ren1_common, True)        
        self.tvcolumn1_common.pack_start(self.ren2_common, True)
        self.tvcolumn1_common.pack_start(self.ren3_common, True)  
        
        self.tvcolumn0_common.set_attributes(self.ren0_common, text = 0)
        self.tvcolumn1_common.set_cell_data_func(self.ren1_common, self.func_common)

        self.valuebox.pack_start(self.treeview_common, True, True, 0) 
        
        self.makeButtonBox()

        return self.cfmeshbox 

    #--------------------------------------------------------   
    def makeTreeStore(self):
        
        self.treestore.clear()
        
        self.treestore.append(None, [self.pixbuf_main, 'Mesh type', None, None, None])
        
        self.treestore.append(None, [self.pixbuf_main, 'Max. cell size', None, None, None])
        
        self.row_patch = self.treestore.append(None, [self.pixbuf_main, 'Patch size level', None, None, None])        
        for ii in self.cfmeshDict['patches']:
            self.treestore.append(self.row_patch, [self.pixbuf_first, ii, True, None, True])
        
        self.row_obj = self.treestore.append(None, [self.pixbuf_main, 'Object refinement', None, None, None])
        
        for ii in self.cfmeshDict['objects']:
            self.treestore.append(self.row_obj, [self.pixbuf_first, ii, None, None, None])
            
        self.row_layer = self.treestore.append(None, [self.pixbuf_main, 'Boundary layer', None, None, None])
        self.treestore.append(self.row_layer, [self.pixbuf_first, 'No. of layers', None, None, None])
        self.treestore.append(self.row_layer, [self.pixbuf_first, 'Thickness ratio', None, None, None])
        self.treestore.append(self.row_layer, [self.pixbuf_first, 'First cell height', None, None, None])
        
        if self.cfmeshDict['allowDiscontinuity'] == True:
            self.treestore.append(self.row_layer, [self.pixbuf_first, 'Allow discontinuity', None, None, True])
        else:
            self.treestore.append(self.row_layer, [self.pixbuf_first, 'Allow discontinuity', None, None, False])

        if self.cfmeshDict['farfield']:
            self.row_far = self.treestore.append(None, [self.pixbuf_main, 'Farfield', None, None, None])
        
        self.treeview.expand_all()
    #--------------------------------------------------------   
    def makeTreeStoreCommon(self, objName, objType):
        
        self.treestore_common.clear()
        
        if objType == 'box' or objType == 'line' or objType == None:
            self.treestore_common.append(None, ['Point-1', None, None, None])
            self.treestore_common.append(None, ['Point-2', None, None, None])
            if objType == 'line':
                self.treestore_common.append(None, ['Thickness', None, None, None])
            if objName != 'Farfield':
                self.treestore_common.append(None, ['Size level', None, None, None])
            
        elif objType == 'sphere':
            self.treestore_common.append(None, ['Center', None, None, None])
            self.treestore_common.append(None, ['Radius', None, None, None])
            self.treestore_common.append(None, ['Thickness', None, None, None])
            self.treestore_common.append(None, ['Size level', None, None, None])

        elif objType == 'cone':
            self.treestore_common.append(None, ['Radius0', None, None, None])
            self.treestore_common.append(None, ['Radius1', None, None, None])
            self.treestore_common.append(None, ['Height', None, None, None])
            self.treestore_common.append(None, ['Direction', None, None, None])
            self.treestore_common.append(None, ['Center', None, None, None])
            self.treestore_common.append(None, ['Size level', None, None, None])
                    
        self.treeview_common.expand_all()
    #--------------------------------------------------------   
    def toggleRen(self, widget, path, model):
    
        model[path][2] = not model[path][2]
        value0 = model[path][1]
        value1 = model[path][2]
        
        if path[0] == '2':
            self.patchDict[value0]['display'] = value1
            self.resetDisplay()
        
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.GEN.pickleDump(self.setFilePatch, self.patchDict)
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
    #--------------------------------------------------------   
    def toggleRen3(self, widget, path, model):

        model[path][4] = not model[path][4]
        value0 = model[path][1]
        value1 = model[path][4]
        
        if path[0] == '2':
            self.patchDict[value0]['addLayer'] = value1
            
        elif path[0] == '4':
            self.cfmeshDict['allowDiscontinuity'] = value1
        
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.GEN.pickleDump(self.setFilePatch, self.patchDict)
        self.GEN.pickleDump(self.setFileObject, self.objectDict)       
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)
        old = self.treestore[path][3]
        
        if old == what:
            return
        
        self.treestore[path][3] = what
           
        if value0 == 'Mesh type':
            self.cfmeshDict['meshType'] = what
        
        elif value0 == 'Max. cell size':       
            if self.GEN.checkNumber(value0, what):
                self.cfmeshDict['maxCellSize'] = what
            
        elif value0 in self.cfmeshDict['patches']:
            self.patchDict[value0]['level'] = what
            
        elif value0 in self.cfmeshDict['objects']:
            self.objectDict[value0]['type'] = what
            self.makeTreeStoreCommon(value0, what)
            self.createObjectSurface()
            
        elif value0 == 'No. of layers':
            if self.GEN.checkNumber(value0, what):
                self.cfmeshDict['layerNo'] = what
            
        elif value0 == 'Thickness ratio':
            if self.GEN.checkNumber(value0, what):
                self.cfmeshDict['layerRatio'] = what
            
        elif value0 == 'First cell height':
            if self.GEN.checkNumber(value0, what):
                self.cfmeshDict['layerHeight'] = what

        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
        self.GEN.pickleDump(self.setFilePatch, self.patchDict)                
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what, xyz):
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)
        old = self.treestore_common[path][2]
        
        patch = self.selectToDel[0]
        
        if value0 == 'Point-1':
            if self.GEN.checkNumber(value0, what):
                if patch == 'Farfield':
                    if xyz == 'x':
                        self.cfmeshDict['farfield_point1'][0] = what
                    elif xyz == 'y':
                        self.cfmeshDict['farfield_point1'][1] = what
                    elif xyz == 'z':
                        self.cfmeshDict['farfield_point1'][2] = what
                    self.createFarSurface()
                else:
                    if xyz == 'x':
                        self.objectDict[patch]['minx'] = what
                    elif xyz == 'y':
                        self.objectDict[patch]['miny'] = what
                    elif xyz == 'z':
                        self.objectDict[patch]['minz'] = what
                    self.createObjectSurface()
        
        elif value0 == 'Point-2':
            if self.GEN.checkNumber(value0, what):
                if patch == 'Farfield':
                    if xyz == 'x':
                        self.cfmeshDict['farfield_point2'][0] = what
                    elif xyz == 'y':
                        self.cfmeshDict['farfield_point2'][1] = what
                    elif xyz == 'z':
                        self.cfmeshDict['farfield_point2'][2] = what
                    self.createFarSurface()
                else:
                    if xyz == 'x':
                        self.objectDict[patch]['maxx'] = what
                    elif xyz == 'y':
                        self.objectDict[patch]['maxy'] = what
                    elif xyz == 'z':
                        self.objectDict[patch]['maxz'] = what
                    self.createObjectSurface()

        elif value0 == 'Center':
            if self.GEN.checkNumber(value0, what):
                if xyz == 'x':
                    self.objectDict[patch]['centerx'] = what
                elif xyz == 'y':
                    self.objectDict[patch]['centery'] = what
                elif xyz == 'z':
                    self.objectDict[patch]['centerz'] = what
                self.createObjectSurface()

        elif value0 == 'Radius':
            if self.GEN.checkNumber(value0, what):
                self.objectDict[patch]['radius'] = what
                self.createObjectSurface()

        elif value0 == 'Thickness':
            if self.GEN.checkNumber(value0, what):
                self.objectDict[patch]['thick'] = what

        elif value0 == 'Size level':
            if self.GEN.checkNumber(value0, what):
                self.objectDict[patch]['level'] = what

        elif value0 == 'Direction':
            self.objectDict[patch]['direction'] = what 
            self.createObjectSurface()
            
        elif value0 == 'Radius0':
            self.objectDict[patch]['radius0'] = what            
            self.createObjectSurface()
            
        elif value0 == 'Radius1':
            self.objectDict[patch]['radius1'] = what
            self.createObjectSurface()
                        
        elif value0 == 'Height':
            self.objectDict[patch]['height'] = what
            self.createObjectSurface()
                        
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
        what = model.get_value(iter, 1)
        path = model.get_path(iter)
        
        dic = self.liststore_cfmesh()        
       
        nones = ['Patch size level', 'Object refinement', 'Boundary layer', 'Farfield']

        entrys = ['Max. cell size', 'No. of layers',
                  'Thickness ratio', 'First cell height']            
       
        if what in nones:
            self.ren1.set_property('visible', 0)
            self.ren2.set_property('visible', 0)
            self.ren3.set_property('visible', 0)
        
        elif what in self.cfmeshDict['patches']:
            if path[0] == 2:
                self.ren1.set_property('visible', 1)
                self.ren2.set_property('visible', 1)
                self.ren3.set_property('visible', 1)
                self.ren2.set_property('model', None)
                self.ren2.set_property('has-entry', True)
                self.ren2.set_property('text', self.patchDict[what]['level'])
            elif path[0] == 4:
                self.ren1.set_property('visible', 1)
                self.ren2.set_property('visible', 0)
                self.ren3.set_property('visible', 0)

        elif what == 'Mesh type':
            self.ren1.set_property('visible', 0)
            self.ren2.set_property('visible', 1)
            self.ren3.set_property('visible', 0)
            self.ren2.set_property('model', dic['meshType'])
            self.ren2.set_property('has-entry', False)
            self.ren2.set_property('text', self.cfmeshDict['meshType']) 
            
        elif what[:7] == 'object-':
            self.ren1.set_property('visible', 0)
            self.ren2.set_property('visible', 1)
            self.ren3.set_property('visible', 0)
            self.ren2.set_property('model', dic['objects'])
            self.ren2.set_property('has-entry', False)
            self.ren2.set_property('text', self.objectDict[what]['type'])        
            
        elif what in entrys:
            self.ren1.set_property('visible', 0)
            self.ren2.set_property('visible', 1)
            self.ren3.set_property('visible', 0)
            self.ren2.set_property('model', None)
            self.ren2.set_property('has-entry', True)
            if what == 'Max. cell size':
                self.ren2.set_property('text', self.cfmeshDict['maxCellSize'])
            elif what == 'No. of layers':
                self.ren2.set_property('text', self.cfmeshDict['layerNo'])
            elif what == 'Thickness ratio':
                self.ren2.set_property('text', self.cfmeshDict['layerRatio'])
            elif what == 'First cell height':
                self.ren2.set_property('text', self.cfmeshDict['layerHeight'])
                
        elif what == 'Allow discontinuity':        
            self.ren1.set_property('visible', 0)
            self.ren2.set_property('visible', 0)
            self.ren3.set_property('visible', 1)
                
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model, iter):
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        patch = self.selectToDel[0]

        direction = ['x', 'y', 'z']        
        liststore_direction = gtk.ListStore(str)
        for ii in direction:
            liststore_direction.append([ii])

        if what != 'Direction':
            self.ren1_common.set_property('has-entry', True)
            self.ren2_common.set_property('has-entry', True)
            self.ren3_common.set_property('has-entry', True)
            self.ren1_common.set_property('model', None)
            self.ren2_common.set_property('model', None)
            self.ren3_common.set_property('model', None)
                                
        if what == 'Point-1':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 1)
            self.ren3_common.set_property('visible', 1)
            if patch == 'Farfield':
                self.ren1_common.set_property('text', self.cfmeshDict['farfield_point1'][0])
                self.ren2_common.set_property('text', self.cfmeshDict['farfield_point1'][1])
                self.ren3_common.set_property('text', self.cfmeshDict['farfield_point1'][2])
            else:
                self.ren1_common.set_property('text', self.objectDict[patch]['minx'])
                self.ren2_common.set_property('text', self.objectDict[patch]['miny'])
                self.ren3_common.set_property('text', self.objectDict[patch]['minz'])
            
        elif what == 'Point-2':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 1)
            self.ren3_common.set_property('visible', 1)
            if patch == 'Farfield':
                self.ren1_common.set_property('text', self.cfmeshDict['farfield_point2'][0])
                self.ren2_common.set_property('text', self.cfmeshDict['farfield_point2'][1])
                self.ren3_common.set_property('text', self.cfmeshDict['farfield_point2'][2])
            else:
                self.ren1_common.set_property('text', self.objectDict[patch]['maxx'])
                self.ren2_common.set_property('text', self.objectDict[patch]['maxy'])
                self.ren3_common.set_property('text', self.objectDict[patch]['maxz'])
        elif what == 'Center':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 1)
            self.ren3_common.set_property('visible', 1)
            self.ren1_common.set_property('text', self.objectDict[patch]['centerx'])
            self.ren2_common.set_property('text', self.objectDict[patch]['centery'])
            self.ren3_common.set_property('text', self.objectDict[patch]['centerz'])
        elif what == 'Radius':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['radius'])
        elif what == 'Thickness':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['thick'])
        elif what == 'Size level':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['level'])
        elif what == 'Direction':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('has-entry', 0)
            self.ren1_common.set_property('model', liststore_direction)
            self.ren1_common.set_property('text', self.objectDict[patch]['direction'])            
        elif what == 'Radius0':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['radius0']) 
        elif what == 'Radius1':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['radius1']) 
        elif what == 'Height':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
            self.ren3_common.set_property('visible', 0)
            self.ren1_common.set_property('text', self.objectDict[patch]['height']) 
    #---------------------------------------------------------------------------------------------    
    def liststore_cfmesh(self):

        objects = ['box', 'sphere', 'line', 'cone']
        meshType = ['cartesian', 'cartesian2D', 'tetrahedral', 'polyhedral']      
        
        liststore_objects = gtk.ListStore(str)
        for ii in objects:
            liststore_objects.append([ii])
            
        liststore_meshType = gtk.ListStore(str)
        for ii in meshType:
            liststore_meshType.append([ii])
        
        storeDict = {}
        keys = ['objects', 'meshType']
        values = [liststore_objects, liststore_meshType]
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]
        
        return storeDict 
    # -------------------------------------------------------------------------
    def loadCfMeshDict(self):
    
        self.cfmeshDict = self.GEN.pickleLoad(self.setFile)        
        if self.cfmeshDict == None:
            self.cfmeshDict = {}
            self.cfmeshDict['maxCellSize'] = '0.05'
            self.cfmeshDict['layerNo'] = '0'
            self.cfmeshDict['layerRatio'] = '1.2'
            self.cfmeshDict['layerHeight'] = '0.001'
            self.cfmeshDict['allowDiscontinuity'] = False
            self.cfmeshDict['addLayerPatch'] = []
            self.cfmeshDict['farfield_point1'] = ['0', '0', '0']
            self.cfmeshDict['farfield_point2'] = ['10', '10', '10']
            self.cfmeshDict['farfield'] = False
            
            self.cfmeshDict['stlfiles'] = []
            self.cfmeshDict['patches'] = []
            self.cfmeshDict['objects'] = []
            
            self.cfmeshDict['meshType'] = 'cartesian'
            
            self.patchDict = {}
            self.objectDict = {}
        else:
            self.patchDict = self.GEN.pickleLoad(self.setFilePatch)
            self.objectDict = self.GEN.pickleLoad(self.setFileObject)
            
    #---------------------------------------------------------------------------------------------    
    def selectstl(self,widget):
    
        stls = self.GEN.selSTL()
        
        if stls == []:
            return
            
        if glob.glob(self.caseDir + '/system/settings/*.stl'):
            os.system('rm ' + self.caseDir + '/system/settings/*.stl')
            
        for ii in stls:
            rname = self.GEN.findSTLRegion(ii)
            if len(rname) == 1:
                self.GEN.renameSTLRegion(ii)            
        
        if len(stls) == 1:
            self.cfmeshDict['patches'] = []
            
            os.system('cp ' + stls[0] + ' ' + self.caseDir + '/mesh.stl')
            
            rname = self.GEN.findSTLRegion(stls[0])
            
            if len(rname) > 1:
                self.GEN.stlSplitRegions(stls[0])
                for rr in rname:
                    self.cfmeshDict['patches'].append(rr)
                    self.patchDict[rr] = {}
                    self.patchDict[rr]['level'] = '0'
                    self.patchDict[rr]['display'] = True
                    self.patchDict[rr]['addLayer'] = True                                    
            else:
                os.system('cp ' + stls[0] + ' ' + self.caseDir + '/system/settings/' + rname[0] + '.stl')
                
                self.cfmeshDict['patches'].append(rname[0])
                self.patchDict[rname[0]] = {}
                self.patchDict[rname[0]]['level'] = '0'
                self.patchDict[rname[0]]['display'] = True
                self.patchDict[rname[0]]['addLayer'] = True
                
        elif len(stls) > 1:
            self.cfmeshDict['patches'] = []
            self.GEN.mergeSTL(stls)
            for ii in stls:                
                rname = self.GEN.findSTLRegion(ii)
                
                if len(rname) > 1:
                    self.GEN.stlSplitRegions(ii)
                    for rr in rname:
                        self.cfmeshDict['patches'].append(rr)
                        self.patchDict[rr] = {}
                        self.patchDict[rr]['level'] = '0'
                        self.patchDict[rr]['display'] = True
                        self.patchDict[rr]['addLayer'] = True
                else:    
                    os.system('cp ' + ii + ' ' + self.caseDir + '/system/settings/' + rname[0] + '.stl')
                                               
                    self.cfmeshDict['patches'].append(rname[0]) 
                    self.patchDict[rname[0]] = {}
                    self.patchDict[rname[0]]['level'] = '0'
                    self.patchDict[rname[0]]['display'] = True
                    self.patchDict[rname[0]]['addLayer'] = True
            
        
        self.cfmeshDict['farfield'] = False
        
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
        self.GEN.pickleDump(self.setFilePatch, self.patchDict)
        
        self.makeTreeStore()

        self.initialRendering()

    #---------------------------------------------------------------------------------------------    
    def resetDisplay(self):
        
        self.renderer.RemoveAllViewProps()
        
        plist = self.cfmeshDict['patches']
        
        for i in range(len(plist)):
            if self.patchDict[plist[i]]['display']:
                self.renderer.AddActor(self.AllActors[i])
                
        if self.farActor:
            for ii in self.farActor:
                self.renderer.AddActor(ii)
        
        self.renderer.ResetCamera()
        self.gvtk.Initialize() 

    # ----------------------------------------------------------------------------
    def addObject(self, widget):
    
        olist = self.objectDict.keys()
        nums = []
        for ii in olist:
            aa = ii.split('-')            
            nums.append(int(aa[1]))
        if nums == []:
            name = 'object-0'
        else:
            name = 'object-' + str(max(nums) + 1)       
               
        self.treestore.append(self.row_obj, [self.pixbuf_first, name, None, None, None])     
                       
        self.objectDict[name] = {}
        self.objectDict[name]['type'] = 'box'
        self.objectDict[name]['level'] = '1'
        self.objectDict[name]['minx'] = '0'
        self.objectDict[name]['miny'] = '0'
        self.objectDict[name]['minz'] = '0'
        self.objectDict[name]['maxx'] = '1'
        self.objectDict[name]['maxy'] = '1'
        self.objectDict[name]['maxz'] = '1'
        self.objectDict[name]['centerx'] = '0'
        self.objectDict[name]['centery'] = '0'
        self.objectDict[name]['centerz'] = '0'
        self.objectDict[name]['radius'] = '1'
        self.objectDict[name]['thick'] = '1'

        self.objectDict[name]['radius0'] = '0.8'
        self.objectDict[name]['height'] = '0.3'
        self.objectDict[name]['radius1'] = '0.8'
        self.objectDict[name]['direction'] = 'z'
                
        self.cfmeshDict['objects'].append(name)
           
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        self.treeview.expand_all()

    #---------------------------------------------------------------------------------------------
    def deleteObject(self, widget):
        
        if self.selectToDel == []:
            self.GEN.makeDialog('Warning!!! Select name to delete')
            return
        else:       
            self.treestore.remove(self.selectToDel[1])
            if self.selectToDel[0] in self.objectDict.keys():
                del self.objectDict[self.selectToDel[0]]
                self.cfmeshDict['objects'].remove(self.selectToDel[0])
            else:
                return
        
        self.treeview.expand_all()
        self.GEN.pickleDump(self.setFileObject, self.objectDict)
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        
        for ii in self.valuebox.get_children():
            self.valuebox.remove(ii)
        self.selectToDel == []
        self.cfmeshbox.show_all()

        if self.objectActor:
            for ii in self.objectActor:
                self.renderer.RemoveActor(ii)
            self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        value0 = tree_model.get_value(tree_iter, 1)
        value1 = tree_model.get_value(tree_iter, 2)
        value2 = tree_model.get_value(tree_iter, 3)
        path=tree_model.get_path(tree_iter)
        
        if path[0] == 2:
        
            if value0 in self.cfmeshDict['patches']:  
                if self.patchDict[value0]['display']:
                    self.highlightColor(value0)
        
        elif path[0] == 3:

            if len(path) == 2:
            
                self.selectToDel = [value0, tree_iter]
                
                for ii in self.valuebox.get_children():
                    self.valuebox.remove(ii)
                self.valuebox.pack_start(self.treeview_common, True, True, 0)
                
                self.makeTreeStoreCommon(value0, value2)
                
                self.cfmeshbox.show_all()                
                   
                self.createObjectSurface()                
                
            else:
                self.selectToDel = []

        elif path[0] == 5:
        
            self.selectToDel = [value0, tree_iter]
            
            for ii in self.valuebox.get_children():
                self.valuebox.remove(ii)
            self.valuebox.pack_start(self.treeview_common, True, True, 0)

            self.makeTreeStoreCommon('Farfield', None)
            self.cfmeshbox.show_all()
    #-----------------------------------------------------------------------------
    def highlightColor(self, patchName):
    
        for i in range(self.renderer.GetActors().GetNumberOfItems()):
            self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetColor(1, 1, 1)
            
        ind = self.cfmeshDict['patches'].index(patchName)
        self.AllActors[ind].GetProperty().SetColor(0, 0, 1)
        
        self.gvtk.Initialize() 

    #---------------------------------------------------------------------------------------------
    def makeButtonBox(self):

        selStlB = gtk.Button('Select STL files')
        selStlB.set_size_request(100, 28)
        selStlB.connect('clicked', self.selectstl)
        
        farB = gtk.Button('Create farfield')
        farB.set_size_request(100, 28)
        farB.connect('clicked', self.createFarfield)
        
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(selStlB, True, True, 0)
        hbox.pack_start(farB, True, True, 0)

        addObjB = gtk.Button('Add object')
        addObjB.set_size_request(100, 28)
        addObjB.connect('clicked', self.addObject)
        
        delObjB = gtk.Button('Delete object')
        delObjB.set_size_request(100, 28)
        delObjB.connect('clicked', self.deleteObject)

        transB = gtk.Button('Translate STL')
        transB.set_size_request(100, 28)
        transB.connect('clicked', self.transformSTL, 'translate')
        
        rotateB = gtk.Button('Rotate STL')
        rotateB.set_size_request(100, 28)
        rotateB.connect('clicked', self.transformSTL, 'rotate')
        
        scaleB = gtk.Button('Scale STL')
        scaleB.set_size_request(100, 28)
        scaleB.connect('clicked', self.transformSTL, 'scale')   
        
        createMeshB = gtk.Button('Create Mesh')
        createMeshB.set_size_request(100, 28)
        createMeshB.connect('clicked', self.createMesh)
                
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(addObjB, True, True, 0)
        hbox.pack_start(delObjB, True, True, 0)    

        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(transB, True, True, 0)
        hbox.pack_start(rotateB, True, True, 0)
        hbox.pack_start(scaleB, True, True, 0)  
        
        hbox = gtk.HBox(False, 0)
        self.underbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(createMeshB, True, True, 0)
    #---------------------------------------------------------------------------------------------
    def createFarfield(self, widget):
    
        self.row_far = self.treestore.append(None, [self.pixbuf_main, 'Farfield', None, None, None])
        
        self.selectToDel = ['Farfield', self.row_far]
        self.cfmeshDict['farfield'] = True
        
        for ii in self.valuebox.get_children():
            self.valuebox.remove(ii)
        self.valuebox.pack_start(self.treeview_common, True, True, 0)
                
        self.makeTreeStoreCommon('Farfield', None)
        
        self.GEN.pickleDump(self.setFile, self.cfmeshDict)
        
        self.createFarSurface()
                
    #---------------------------------------------------------------------------------------------
    def createFarSurface(self):
    
        if self.farActor:
            for ii in self.farActor:
                self.renderer.RemoveActor(ii)
            
        minx = self.cfmeshDict['farfield_point1'][0]
        miny = self.cfmeshDict['farfield_point1'][1]
        minz = self.cfmeshDict['farfield_point1'][2]
        maxx = self.cfmeshDict['farfield_point2'][0]
        maxy = self.cfmeshDict['farfield_point2'][1]
        maxz = self.cfmeshDict['farfield_point2'][2]

        delx = float(maxx) - float(minx)
        dely = float(maxy) - float(miny)
        delz = float(maxz) - float(minz)
            
        unit = self.installpath + '/common/unitbox.stl'
        os.system("surfaceTransformPoints -scale '(" + str(delx) + " " + str(dely) + " " + str(delz) + ")' " \
                + unit + " " + self.caseDir + '/scaledbox.stl > /dev/null 2>&1')
        
        os.system("surfaceTransformPoints -translate '(" + minx + " " + miny + " " + minz + ")' " \
                + self.caseDir + "/scaledbox.stl" + " " + self.caseDir + '/system/settings/farfield.stl > /dev/null 2>&1')
                
        self.GEN.stlSplitRegions(self.caseDir + '/system/settings/farfield.stl')
        fars = [self.caseDir + '/system/settings/minx.stl', self.caseDir + '/system/settings/maxx.stl',
                self.caseDir + '/system/settings/miny.stl', self.caseDir + '/system/settings/maxy.stl',
                self.caseDir + '/system/settings/minz.stl', self.caseDir + '/system/settings/maxz.stl']
                
        #self.farActor = self.VTK_All.showSTL(self.caseDir + '/system/settings/farfield.stl')
        self.farActor = self.VTK_All.showSTLMulti(fars)
        #self.farActor.GetProperty().SetRepresentationToWireframe()
        #self.farActor.GetProperty().SetColor(1, 1, 0)
        
        for ii in self.farActor:
            self.renderer.AddActor(ii)
        
        self.renderer.ResetCamera()
        self.gvtk.Initialize()
    #--------------------------------------------------------------
    def showDomainRange(self, solids, stlRange):
        
        if solids == []:
            return
            
        for ii in self.rangebox.get_children():
            self.rangebox.remove(ii)
            
        minx = '%0.6f'%stlRange[0]
        maxx = '%0.6f'%stlRange[1]
        miny = '%0.6f'%stlRange[2]
        maxy = '%0.6f'%stlRange[3]
        minz = '%0.6f'%stlRange[4]
        maxz = '%0.6f'%stlRange[5]
        
        stringx = '    x range  :  ' + minx + '  ~  ' + maxx
        stringy = '    y range  :  ' + miny + '  ~  ' + maxy
        stringz = '    z range  :  ' + minz + '  ~  ' + maxz
        
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(gtk.Label(stringx), False, False, 5)
        self.rangebox.pack_start(hbox, False, False, 5)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(gtk.Label(stringy), False, False, 5)
        self.rangebox.pack_start(hbox, False, False, 0)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(gtk.Label(stringz), False, False, 5)
        self.rangebox.pack_start(hbox, False, False, 5)
    
        self.cfmeshbox.show_all()
    #---------------------------------------------------------------------------------------------
    def createObjectSurface(self):
    
        if self.objectActor:
            for ii in self.objectActor:
                self.renderer.RemoveActor(ii)
        
        objName = self.selectToDel[0]
        dic = self.objectDict[objName]        
        
        if self.objectDict[objName]['type'] == 'line':
            self.objectActor = self.VTK_All.showLine(dic['minx'], dic['miny'], dic['minz'], dic['maxx'], dic['maxy'], dic['maxz'])
        elif self.objectDict[objName]['type'] == 'box':
            self.objectActor = self.VTK_All.showObjectBox(dic['minx'], dic['miny'], dic['minz'], dic['maxx'], dic['maxy'], dic['maxz'])
        elif self.objectDict[objName]['type'] == 'sphere':
            self.objectActor = self.VTK_All.showSphere(dic['centerx'], dic['centery'], dic['centerz'], dic['radius'])
        elif self.objectDict[objName]['type'] == 'cone':
            self.objectActor = self.VTK_All.showCone(dic['centerx'], dic['centery'], dic['centerz'], dic['height'], dic['direction'], dic['radius0'], dic['radius1'])
            
        for ii in self.objectActor:
            ii.GetProperty().SetRepresentationToWireframe()
            ii.GetProperty().SetColor(1, 0, 0)
        
            self.renderer.AddActor(ii)
        
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------
    def createMesh(self, widget):
    
        if self.cfmeshDict['meshType'] == 'cartesian':
            mesher = 'cartesianMesh'
        elif self.cfmeshDict['meshType'] == 'cartesian2D':
            mesher = 'cartesian2DMesh'
        elif self.cfmeshDict['meshType'] == 'tetrahedral':
            mesher = 'tetMesh'
        elif self.cfmeshDict['meshType'] == 'polyhedral':
            mesher = 'pMesh'
                            
        os.system('cp ' + self.caseDir + '/mesh.stl ' + self.caseDir + '/mesh.stl.ori')
        
        if self.cfmeshDict['farfield']:
            
            stl = self.caseDir + '/mesh.stl'
            far = self.caseDir + '/system/settings/farfield.stl'                       
            
            if os.path.isfile(stl) == True and os.path.isfile(far) == True:
                self.GEN.mergeFarfield([self.caseDir + '/mesh.stl.ori', far])
    
        self.notebook.set_current_page(1)
        self.writeCfMeshDict()            
                
        cf = open(self.caseDir + '/cfMeshRun','w')
        cf.write('surfaceFeatureEdges -case ' + self.caseDir + ' -angle 30 ' + self.caseDir + '/mesh.stl ' + self.caseDir + '/mesh.fms\n')                                   
        
        cf.write('cp ' + self.caseDir + '/mesh.stl.ori ' + self.caseDir + '/mesh.stl\n')
        
        cf.write(mesher + ' -case ' + self.caseDir + '\n')                        
        #------------------------------------------------------------------------                       
        cf.write('foamToVTK -noInternal -noFaceZones -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.foamToVTK\n')
        cf.close()
        os.system('chmod +x ' + self.caseDir + '/cfMeshRun')
       
        time.sleep(1)
        
        cmd = self.caseDir + '/cfMeshRun\n'
        self.terminal.feed_child(cmd,len(cmd))
   
    #--------------------------------------------------------------
    def writeCfMeshDict(self):
    
        dic = self.cfmeshDict
        odic = self.objectDict
        pdic = self.patchDict
        
        patchNames = dic['patches']
        objectNames = self.cfmeshDict['objects']
    
        f=open(self.caseDir + '/system/meshDict', 'w')
        f.write('/*--------------------------------*- C++ -*----------------------------------*\\n')
        f.write('| =========                 |                                                |\n')
        f.write('| \\      /  F ield         | OpenFOAM GUI Project: creativeFields           |\n')
        f.write('|  \\    /   O peration     | Version:  0.8.9.0                              |\n')
        f.write('|   \\  /    A nd           | Web: www.c-fields.com                          |\n')
        f.write('|    \\/     M anipulation  |                                                |\n')
        f.write('\*---------------------------------------------------------------------------*/\n')
        f.write('\n')
        f.write('FoamFile\n')
        f.write('{\n')
        f.write('version	2;\n')
        f.write('format	ascii;\n')
        f.write('class	dictionary;\n')
        f.write('location	"system";\n')
        f.write('object	meshDict;\n')
        f.write('}\n')
        f.write('\n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')
        f.write('surfaceFile	"mesh.fms";\n')
        f.write('maxCellSize	' + dic['maxCellSize']+';\n')
        f.write('\n')
        #---------------------                
        f.write('localRefinement\n')
        f.write('{\n')
        
        for i in range(len(patchNames)):
            f.write('    ' + patchNames[i] + '\n')
            f.write('    {\n')
            f.write('        additionalRefinementLevels ' + self.patchDict[patchNames[i]]['level'] + ';\n')
            f.write('    }\n')           
        f.write('}\n')
        #---------------------        
        f.write('objectRefinements\n')
        f.write('{\n')
        
        for ii in objectNames:          

            f.write('    ' + ii + '\n')
            f.write('    {\n')
            f.write('        type ' + odic[ii]['type'] + ';\n')            
            f.write('        additionalRefinementLevels ' + odic[ii]['level'] + ';\n')

            if odic[ii]['type'] == 'box':            
                cfx = (float(odic[ii]['minx']) + float(odic[ii]['maxx'])) / 2
                cfy = (float(odic[ii]['miny']) + float(odic[ii]['maxy'])) / 2
                cfz = (float(odic[ii]['minz']) + float(odic[ii]['maxz'])) / 2
                lfx = float(odic[ii]['maxx']) - float(odic[ii]['minx'])
                lfy = float(odic[ii]['maxy']) - float(odic[ii]['miny'])
                lfz = float(odic[ii]['maxz']) - float(odic[ii]['minz'])
                f.write('        centre    (' + str(cfx) + ' ' + str(cfy) + ' ' + str(cfz) + ');\n')
                f.write('        lengthX   ' + str(lfx) + ';\n')
                f.write('        lengthY   ' + str(lfy) + ';\n')
                f.write('        lengthZ   ' + str(lfz) + ';\n')
            elif odic[ii]['type'] == 'line':            
                f.write('        p0    (' + odic[ii]['minx'] + ' ' + odic[ii]['miny'] + ' ' + odic[ii]['minz'] + ');\n')
                f.write('        p1    (' + odic[ii]['maxx'] + ' ' + odic[ii]['maxy'] + ' ' + odic[ii]['maxz'] + ');\n')                
                f.write('        refinementThickness    ' + odic[ii]['thick'] + ';\n')
            elif odic[ii]['type'] == 'sphere':
                f.write('        centre    (' + odic[ii]['centerx'] + ' ' + odic[ii]['centery'] + ' ' + odic[ii]['centerz'] + ');\n')
                f.write('        radius    ' + odic[ii]['radius'] + ';\n')
                f.write('        refinementThickness    ' + odic[ii]['thick'] + ';\n')
            elif odic[ii]['type'] == 'cone':                
                cx = float(odic[ii]['centerx'])
                cy = float(odic[ii]['centery'])
                cz = float(odic[ii]['centerz'])
                h = float(odic[ii]['height'])
                if odic[ii]['direction'] == 'x':
                    x0 = cx + h/2
                    x1 = cx - h/2
                    y0 = cy
                    y1 = cy
                    z0 = cz
                    z1 = cz
                elif odic[ii]['direction'] == 'y':
                    x0 = cx
                    x1 = cx
                    y0 = cy + h/2
                    y1 = cy - h/2
                    z0 = cz
                    z1 = cz
                elif odic[ii]['direction'] == 'z':
                    x0 = cx
                    x1 = cx
                    y0 = cy
                    y1 = cy
                    z0 = cz + h/2
                    z1 = cz - h/2                                       
                f.write('        p0    (' + str(x0) + ' ' + str(y0) + ' ' + str(z0) + ');\n')
                f.write('        radius0    ' + odic[ii]['radius0'] + ';\n')
                f.write('        p1    (' + str(x1) + ' ' + str(y1) + ' ' + str(z1) + ');\n')
                f.write('        radius1    ' + odic[ii]['radius1'] + ';\n')
                
            f.write('    }\n')

        f.write('}\n')

        #---------------------        
        f.write('boundaryLayers\n')
        f.write('{\n')
        if dic['layerNo'] != '0':
            f.write('    patchBoundaryLayers\n')
            f.write('    {\n')
            for ii in patchNames:
                if pdic[ii]['addLayer'] == True:
                    f.write('       "' + ii + '"\n')
                    f.write('       {\n')                           
                    f.write('           nLayers    ' + dic['layerNo'] + ';\n')
                    f.write('           thicknessRatio    ' + dic['layerRatio'] + ';\n')
                    f.write('           maxFirstLayerThickness    ' + dic['layerHeight'] + ';\n')
                    if dic['allowDiscontinuity'] == True:
                        f.write('           allowDiscontinuity    1;\n')
                    else:
                        f.write('           allowDiscontinuity    0;\n')
                    f.write('       }\n')
            f.write('    }\n')
            
        f.write('}\n')         

        f.close()

    #--------------------------------------------------------------
    def initialRendering(self):

        self.allSTLFiles = []
        plist = self.cfmeshDict['patches']
        for ii in plist:
            self.allSTLFiles.append(self.caseDir + '/system/settings/' + ii +'.stl')
        
        self.AllActors, self.stlRange = self.VTK_All.showSTLCfMesh(self.allSTLFiles)
        self.renderer.RemoveAllViewProps()
        for ii in self.AllActors:
            self.renderer.AddActor(ii)
        
        self.renderer.ResetCamera()
        self.gvtk.Initialize()              
      
        if self.stlRange != []:
            self.showDomainRange(self.cfmeshDict['patches'], self.stlRange)

        if self.cfmeshDict['farfield']:
            self.createFarSurface()
    #---------------------------------------------------------------------------------------------------------                
    def transformSTL(self, widget, what):

        def transform(wiget):
        
            orifiles = []
            plist = self.cfmeshDict['patches']
            for ii in plist:
                orifiles.append(self.caseDir + '/system/settings/' + ii +'.stl')

            if what == 'scale':
                os.system("surfaceTransformPoints -scale '(" + scalex.get_text() + ' ' + scaley.get_text() + ' ' + scalez.get_text() + ")' " + stlfile + ' ' + stlfile)
                for ii in  orifiles:
                    os.system("surfaceTransformPoints -scale '(" + scalex.get_text() + ' ' + scaley.get_text() + ' ' + scalez.get_text() + ")' " + ii + ' ' + ii)
            elif what == 'translate':
                os.system("surfaceTransformPoints -translate '(" + transx.get_text() + ' ' + transy.get_text() + ' ' + transz.get_text() + ")' " + stlfile + ' ' + stlfile)
                for ii in  orifiles:
                    os.system("surfaceTransformPoints -translate '(" + transx.get_text() + ' ' + transy.get_text() + ' ' + transz.get_text() + ")' " + ii + ' ' + ii)
            elif what == 'rotate':
                os.system("surfaceTransformPoints -rollPitchYaw '(" + rotatex.get_text() + ' ' + rotatey.get_text() + ' ' + rotatez.get_text() + ")' " + stlfile + ' ' + stlfile)
                for ii in  orifiles:
                    os.system("surfaceTransformPoints -rollPitchYaw '(" + rotatex.get_text() + ' ' + rotatey.get_text() + ' ' + rotatez.get_text() + ")' " + ii + ' ' + ii)
            self.initialRendering()
            window.destroy()
            
        def closethis(widget):
            window.destroy()
            
        stlfile = self.caseDir + '/mesh.stl'
            
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Transform mesh')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)

        selbox = gtk.VBox(False, 5)
        frame.add(selbox)

        if what == 'scale':
            scalebox = gtk.VBox(False, 5)
            selbox.pack_start(scalebox, False, False, 5)
            hbox = gtk.HBox(False, 5)
            scalebox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('Scale factors for x, y, z'), False, False, 5)
            scalex = gtk.Entry()
            scaley = gtk.Entry()
            scalez = gtk.Entry()
            scalex.set_size_request(80, 28)
            scaley.set_size_request(80, 28)
            scalez.set_size_request(80, 28)
            scalex.set_text('0.001')
            scaley.set_text('0.001')
            scalez.set_text('0.001')
            hbox = gtk.HBox(False, 5)
            scalebox.pack_start(hbox, False, False, 5)
            hbox.pack_end(scalez, False, False, 5)
            hbox.pack_end(scaley,False,False,0)
            hbox.pack_end(scalex, False, False, 5)

        elif what == 'translate':
            translatebox = gtk.VBox(False, 5)
            selbox.pack_start(translatebox, False, False, 5)
            hbox = gtk.HBox(False, 5)
            translatebox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('Translate factors for x, y, z [m]'), False, False, 5)
            transx = gtk.Entry()
            transy = gtk.Entry()
            transz = gtk.Entry()
            transx.set_size_request(80, 28)
            transy.set_size_request(80, 28)
            transz.set_size_request(80, 28)
            transx.set_text('1')
            transy.set_text('0')
            transz.set_text('0')
            hbox = gtk.HBox(False, 5)
            translatebox.pack_start(hbox, False, False, 5)
            hbox.pack_end(transz, False, False, 5)
            hbox.pack_end(transy,False,False,0)
            hbox.pack_end(transx, False, False, 5)

        elif what == 'rotate':
            rotatebox = gtk.VBox(False, 5)
            selbox.pack_start(rotatebox, False, False, 5)
            hbox = gtk.HBox(False, 5)
            rotatebox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('Rotate Angle for x, y, z [deg]'), False, False, 5)        
            rotatex = gtk.Entry()
            rotatey = gtk.Entry()
            rotatez = gtk.Entry()
            rotatex.set_size_request(80, 28)
            rotatey.set_size_request(80, 28)
            rotatez.set_size_request(80, 28)
            rotatex.set_text('90')
            rotatey.set_text('0')
            rotatez.set_text('0')
            hbox = gtk.HBox(False, 5)
            rotatebox.pack_start(hbox, False, False, 5)
            hbox.pack_end(rotatez, False, False, 5)
            hbox.pack_end(rotatey,False,False,0)
            hbox.pack_end(rotatex, False, False, 5)

        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', transform)
        clsB.connect('clicked', closethis)
        appB.set_size_request(100, 28)
        clsB.set_size_request(100, 28)
        bubox = gtk.HBox(False, 5)
        mainbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        
        window.show_all()                                   

