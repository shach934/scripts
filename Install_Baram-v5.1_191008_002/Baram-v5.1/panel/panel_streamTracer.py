#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelStreamTracerClass:
                
    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window        
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.solver = mainself.solver
        self.terminal = mainself.terminal
        self.installpath = mainself.installpath
        self.mainself = mainself        
        self.vtkFeatureActors = mainself.vtkFeatureActors        
        
        self.renderer = mainself.renderer
        self.VTK_All = VTKStuff(mainself.caseDir)
        self.GEN = generalClass(mainself)
        self.DEFAULT = defaultValueClass(self)
        
        self.seedList = []        
        self.allActors = None
        self.seedActors = {}
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')  
    #------------------------------------------------------------------------------------------
    def streamTracer(self):
        
        self.getPostReader()        
        self.colormapDict = self.colormapData()
        
        self.streambox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.streambox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Display streamline  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.streambox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 60)

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
                  
        self.setFile = self.caseDir + '/system/settings/streamTracerSet'
        self.loadStreamDict()
        self.loadSeedActors()
        
        self.scalars = []
        self.times = []
        self.scalars = self.GEN.getScalars()
        if 'boundaryFields' in self.scalars:
            self.scalars.remove('boundaryFields')
        savedResult = self.GEN.getResult()                       
        if len(savedResult[0]) >= len(savedResult[1]):
            self.times = savedResult[0]
        else:
            self.times = savedResult[1]
        self.times.insert(0, '0')
        self.streamDict['time'] = self.times[-1]   
        
        # treeview ---------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, str)
        self.treeview = gtk.TreeView(self.treestore)
        
        self.treeview.connect('cursor-changed', self.selected, self.treeview)
        
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(False)
        
        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1 = gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1_0 = gtk.CellRendererCombo()
        self.ren1_1 = gtk.CellRendererCombo()
        self.ren1_2 = gtk.CellRendererCombo()
        
        self.ren1_0.set_fixed_size(50, -1)
        self.ren1_1.set_fixed_size(50, -1)
        self.ren1_2.set_fixed_size(50, -1)
                          
        self.ren0.set_property('editable', False)
        self.ren1_0.set_property('editable', True)
        self.ren1_1.set_property('editable', True)
        self.ren1_2.set_property('editable', True)
        
        self.ren1_0.set_property('text-column', 0)
        self.ren1_1.set_property('text-column', 0)
        self.ren1_2.set_property('text-column', 0)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn1.pack_start(self.ren1_0, True)
        self.tvcolumn1.pack_start(self.ren1_1, True)
        self.tvcolumn1.pack_start(self.ren1_2, True) 

        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        self.ren1_0.connect('edited', self.changeValue, 'x')
        self.ren1_1.connect('edited', self.changeValue, 'y')
        self.ren1_2.connect('edited', self.changeValue, 'z')
        self.tvcolumn1.set_cell_data_func(self.ren1_0, self.func)
            
        
        #self.treeview.expand_all()
        self.mainbox.add(self.treeview)

        self.makeTreeStore()
                
        # treeview common---------------------------------------------------------------
        self.treestore_common = gtk.TreeStore(str, bool, str)        
        self.treestore_common.append(None, ['Scalar', None, None])
        self.treestore_common.append(None, ['Time', None, None])
        self.treestore_common.append(None, ['Colormap', None, None])        
        self.treestore_common.append(None, ['Overlay', False, None])
        self.treestore_common.append(None, ['Show seed', True, None])

        # -------------------------------------------------------------------------------
        self.treeview_common = gtk.TreeView(self.treestore_common)
        self.treeview_common.set_enable_tree_lines(True)
        
        self.tvcolumn0_common = gtk.TreeViewColumn('  ITEMs')
        self.tvcolumn1_common = gtk.TreeViewColumn('  VALUE')
        
        self.treeview_common.append_column(self.tvcolumn0_common)
        self.treeview_common.append_column(self.tvcolumn1_common)
        
        self.ren0_common = gtk.CellRendererText()
        self.ren1_common = gtk.CellRendererToggle()
        self.ren2_common = gtk.CellRendererCombo() 
        
        self.ren0_common.set_fixed_size(150, -1)

        self.ren0_common.set_property("editable", False)                 
        self.ren1_common.set_property("activatable", True)
        self.ren2_common.set_property("editable", True)
        self.ren2_common.set_property('text-column', 0)
        
        self.ren1_common.connect('toggled', self.togglePost, self.treestore_common)
        self.ren2_common.connect('edited', self.changeValue_common)
        
        self.tvcolumn0_common.pack_start(self.ren0_common, False)                        
        self.tvcolumn1_common.pack_start(self.ren1_common, False)        
        self.tvcolumn1_common.pack_start(self.ren2_common, True) 
        
        self.tvcolumn0_common.set_attributes(self.ren0_common, text = 0)
        self.tvcolumn1_common.add_attribute(self.ren1_common, 'active', 1)        
        self.tvcolumn1_common.set_cell_data_func(self.ren2_common, self.func_common)

        self.valuebox.pack_start(self.treeview_common, True, True, 0) 
        
        # button
        addB = gtk.Button('Add seed')
        addB.set_size_request(100, 28)
        addB.connect('clicked', self.addSeed)
        delB = gtk.Button('Delete seed')
        delB.set_size_request(100, 28)
        delB.connect('clicked', self.deleteSeed)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(addB, True, True, 0)
        hbox.pack_start(delB, True, True, 0)
        
        contourB = gtk.Button('Display')
        contourB.set_size_request(150, 28)
        contourB.connect('clicked', self.showStream)

        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(contourB, True, True, 0)

        self.mainself.freevbox.pack_start(self.streambox, True, True, 0)
        self.mainself.window.show_all()
        
        self.showAllSeedActor()
        
        #return self.streambox 
    #--------------------------------------------------------   
    def makeTreeStore(self):
    
        self.treestore.clear()
    
        self.row_seed = self.treestore.append(None, [self.pixbuf_main, 'Seeds', None, None, None])
        
        for ii in self.seedList:
            row_name = self.treestore.append(self.row_seed, [self.pixbuf_first, ii, None, None, None])
            if self.streamDict[ii]['seedType'] == 'line':
                self.treestore.append(row_name, [self.pixbuf_second, 'point1', None, None, None])
                self.treestore.append(row_name, [self.pixbuf_second, 'point2', None, None, None])
            elif self.streamDict[ii]['seedType'] == 'plane':
                self.treestore.append(row_name, [self.pixbuf_second, 'point1', None, None, None])
                self.treestore.append(row_name, [self.pixbuf_second, 'point2', None, None, None])
                self.treestore.append(row_name, [self.pixbuf_second, 'point3', None, None, None])
            elif self.streamDict[ii]['seedType'] == 'sphere':
                self.treestore.append(row_name, [self.pixbuf_second, 'center', None, None, None])
                self.treestore.append(row_name, [self.pixbuf_second, 'radius', None, None, None])
            self.treestore.append(row_name, [self.pixbuf_second, 'resolution', None, None, None])
        
        self.row_opt = self.treestore.append(None, [self.pixbuf_main, 'Options', None, None, None])
        self.treestore.append(self.row_opt, [self.pixbuf_first, 'integrator', None, None, None])
        self.treestore.append(self.row_opt, [self.pixbuf_first, 'direction', None, None, None])
        self.treestore.append(self.row_opt, [self.pixbuf_first, 'max. length', None, None, None])
        
        self.row_shape = self.treestore.append(None, [self.pixbuf_main, 'Shape', None, None, None])
        if self.streamDict['shape'] == 'line':
            self.treestore.append(self.row_shape, [self.pixbuf_first, 'line width', None, None, None])
        elif self.streamDict['shape'] == 'tube':
            self.treestore.append(self.row_shape, [self.pixbuf_first, 'tube radius', None, None, None])
        elif self.streamDict['shape'] == 'ribbon':
            self.treestore.append(self.row_shape, [self.pixbuf_first, 'ribbon width', None, None, None])
            self.treestore.append(self.row_shape, [self.pixbuf_first, 'ribbon angle', None, None, None])
            
        self.treeview.expand_all()
    #--------------------------------------------------------   
    def togglePost(self,widget,path,model):
    
        model[path][1] = not model[path][1]
        
        item = model[path][0]
        if item == 'Overlay':
            self.streamDict['Overlay'] = model[path][1]
        elif item == 'Show seed':
            self.streamDict['showSeed'] = model[path][1]
            if model[path][1] == False:
                self.removeAllSeedActor()
            else:
                self.showAllSeedActor()
        self.GEN.pickleDump(self.setFile, self.streamDict)      
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what, xyz):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)
        old = self.treestore[path][2]
        
        if old == what:
            return         

        if value0[:5] == 'seed-':       
            self.streamDict[value0]['seedType'] = what
            self.makeTreeStore()
            
            seedname = self.seedList[int(path[2])]
            self.renderer.RemoveActor(self.seedActors[seedname])
            self.seedActors[seedname] = self.getSeedActor(seedname, self.streamDict)
            self.renderer.AddActor(self.seedActors[seedname])
            
        elif value0 == 'point1' or value0 == 'point2' or value0 == 'point3' or value0 == 'center':
            if self.GEN.checkNumber(value0, what):
                seedname = self.seedList[int(path[2])]
                if xyz == 'x':
                    self.streamDict[seedname][value0][0] = what
                elif xyz == 'y':
                    self.streamDict[seedname][value0][1] = what
                elif xyz == 'z':
                    self.streamDict[seedname][value0][2] = what
                    
                self.renderer.RemoveActor(self.seedActors[seedname])
                self.seedActors[seedname] = self.getSeedActor(seedname, self.streamDict)
                self.renderer.AddActor(self.seedActors[seedname])
                               
        elif value0 == 'radius' or value0 == 'resolution':
            if self.GEN.checkNumber(value0, what):
                seedname = self.seedList[int(path[2])]
                self.streamDict[seedname][value0] = what
                
                self.renderer.RemoveActor(self.seedActors[seedname])
                self.seedActors[seedname] = self.getSeedActor(seedname, self.streamDict)
                self.renderer.AddActor(self.seedActors[seedname])
                            
        elif value0 == 'integrator' or value0 == 'direction':
            self.streamDict[value0] = what
            
        elif value0 == 'max. length':        
            if self.GEN.checkNumber(value0, what):
                self.streamDict['maxLength'] = what

        elif value0 == 'Shape':        
            self.streamDict['shape'] = what
            self.makeTreeStore()
            
        elif value0 == 'line width':        
            if self.GEN.checkNumber(value0, what):
                self.streamDict['lineWidth'] = what
        
        elif value0 == 'tube radius':        
            if self.GEN.checkNumber(value0, what):
                self.streamDict['tubeRadius'] = what
            
        elif value0 == 'ribbon width':        
            if self.GEN.checkNumber(value0, what):
                self.streamDict['ribbonWidth'] = what
            
        elif value0 == 'ribbon angle':        
            if self.GEN.checkNumber(value0, what):
                self.streamDict['ribbonAngle'] = what
            
        self.GEN.pickleDump(self.setFile, self.streamDict)              
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what):
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)
        old = self.treestore_common[path][2]
        
        if old == what:
            return         
        
        if value0 == 'Scalar':
            self.streamDict['scalar'] = what
            if self.allActors:
                self.showStream(None)
        elif value0 == 'Time':
            self.streamDict['time'] = what
            if self.allActors:
                self.changeTime()
        elif value0 == 'Colormap':
            self.streamDict['colormap'] = what       
            if self.allActors:
                self.changeColormap()

        self.treestore_common[path][2] = what
        self.GEN.pickleDump(self.setFile,self.streamDict)
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
        what = model.get_value(iter, 1)
        path = model.get_path(iter) 

        dic = self.liststore_post(self.scalars, self.times)
        
        if what == 'Seeds' or what == 'Options':
            self.ren1_0.set_property('visible', 0)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
        elif what[:5] == 'seed-':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', dic['seedType'])
            self.ren1_0.set_property('has-entry', False)
            seedname = self.seedList[int(path[1])]  
            self.ren1_0.set_property('text', self.streamDict[seedname]['seedType'])
        elif what[:5] == 'point':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 1)
            self.ren1_2.set_property('visible', 1)
            self.ren1_0.set_property('model', None)
            self.ren1_1.set_property('model', None)
            self.ren1_2.set_property('model', None)
            self.ren1_0.set_property('has-entry', True)
            self.ren1_1.set_property('has-entry', True)
            self.ren1_2.set_property('has-entry', True)
            seedname = self.seedList[int(path[1])]  
            if what == 'point1':
                self.ren1_0.set_property('text', self.streamDict[seedname]['point1'][0])
                self.ren1_1.set_property('text', self.streamDict[seedname]['point1'][1])
                self.ren1_2.set_property('text', self.streamDict[seedname]['point1'][2])
            elif what == 'point2':
                self.ren1_0.set_property('text', self.streamDict[seedname]['point2'][0])
                self.ren1_1.set_property('text', self.streamDict[seedname]['point2'][1])
                self.ren1_2.set_property('text', self.streamDict[seedname]['point2'][2])
            elif what == 'point3':
                self.ren1_0.set_property('text', self.streamDict[seedname]['point3'][0])
                self.ren1_1.set_property('text', self.streamDict[seedname]['point3'][1])
                self.ren1_2.set_property('text', self.streamDict[seedname]['point3'][2])
        elif what == 'center':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 1)
            self.ren1_2.set_property('visible', 1)
            self.ren1_0.set_property('model', None)
            self.ren1_1.set_property('model', None)
            self.ren1_2.set_property('model', None)
            self.ren1_0.set_property('has-entry', True)
            self.ren1_1.set_property('has-entry', True)
            self.ren1_2.set_property('has-entry', True)
            seedname = self.seedList[int(path[1])]  
            self.ren1_0.set_property('text', self.streamDict[seedname]['center'][0])
            self.ren1_1.set_property('text', self.streamDict[seedname]['center'][1])
            self.ren1_2.set_property('text', self.streamDict[seedname]['center'][2])
        elif what == 'radius' or what == 'resolution':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', None)
            self.ren1_0.set_property('has-entry', True)
            seedname = self.seedList[int(path[1])]  
            self.ren1_0.set_property('text', self.streamDict[seedname][what])
        elif what == 'max. length':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', None)
            self.ren1_0.set_property('has-entry', True)
            self.ren1_0.set_property('text', self.streamDict['maxLength'])
        elif what == 'integrator' or what == 'direction':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', dic[what])
            self.ren1_0.set_property('has-entry', False)
            self.ren1_0.set_property('text', self.streamDict[what])
        elif what == 'Shape':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', dic['shape'])
            self.ren1_0.set_property('has-entry', False)
            self.ren1_0.set_property('text', self.streamDict['shape'])
        elif what == 'line width' or what == 'tube radius' or what == 'ribbon width' or what == 'ribbon angle':
            self.ren1_0.set_property('visible', 1)
            self.ren1_1.set_property('visible', 0)
            self.ren1_2.set_property('visible', 0)
            self.ren1_0.set_property('model', None)
            self.ren1_0.set_property('has-entry', True)
            if what == 'line width':
                self.ren1_0.set_property('text', self.streamDict['lineWidth'])
            elif what == 'tube radius':
                self.ren1_0.set_property('text', self.streamDict['tubeRadius'])
            elif what == 'ribbon width':
                self.ren1_0.set_property('text', self.streamDict['ribbonWidth'])            
            elif what == 'ribbon angle':
                self.ren1_0.set_property('text', self.streamDict['ribbonAngle'])
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model, iter):
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)        
        combo=['Scalar', 'Time', 'Colormap']

        if what in combo:
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)            
            self.ren2_common.set_property('has-entry', False)
            if what == 'Scalar':
                self.ren2_common.set_property('model', dic['scalars'])
                self.ren2_common.set_property('text', self.streamDict['scalar'])
            elif what == 'Time':
                self.ren2_common.set_property('model', dic['times'])
                self.ren2_common.set_property('text', self.streamDict['time'])
            elif what == 'Colormap':
                self.ren2_common.set_property('model', dic['colormap'])
                self.ren2_common.set_property('text', self.streamDict['colormap'])

        elif what == 'Overlay' or what == 'Show seed':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0) 
    #---------------------------------------------------------------------------------------------    
    def liststore_post(self, scalars, times):

        colormap = ['blue to red', 'cool to warm', 'high_contrast', 'hot_to_cold', 'leaf_color', 'small_difference',
                    'hot', 'indigo_flame', 'land_color', 'spectrum_white']                      
        seedType = ['line', 'plane', 'sphere']
        integrator = ['RungeKutta2', 'RungeKutta4', 'RungeKutta45']
        direction = ['forward', 'backward', 'both']
        shape = ['line', 'tube', 'ribbon']
                

        liststore_scalars = gtk.ListStore(str)
        for ii in scalars:
            liststore_scalars.append([ii])
        
        liststore_times = gtk.ListStore(str)
        for ii in times:
            liststore_times.append([ii])
        
        liststore_colormap = gtk.ListStore(str)
        for ii in colormap:
            liststore_colormap.append([ii])
        
        liststore_integrator = gtk.ListStore(str)
        for ii in integrator:
            liststore_integrator.append([ii])
        
        liststore_direction = gtk.ListStore(str)
        for ii in direction:
            liststore_direction.append([ii])
            
        liststore_shape = gtk.ListStore(str)
        for ii in shape:
            liststore_shape.append([ii])
        
        liststore_yesNo = gtk.ListStore(str)
        liststore_yesNo.append(['yes'])
        liststore_yesNo.append(['no'])
        
        liststore_seedType = gtk.ListStore(str)
        for ii in seedType:
            liststore_seedType.append([ii])
        
        storeDict = {}
        keys = ['scalars', 'times', 'colormap', 'integrator', 'direction', 'yesNo', 'seedType', 'shape']
        values = [liststore_scalars, liststore_times, liststore_colormap, liststore_integrator, 
                  liststore_direction, liststore_yesNo, liststore_seedType, liststore_shape]
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]
        
        return storeDict 
    # -------------------------------------------------------------------------
    def loadStreamDict(self):
    
        self.streamDict = self.GEN.pickleLoad(self.setFile)        
        if self.streamDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.streamDict=dicts[8]     
        
        keyList = self.streamDict.keys()
        for ii in keyList:
            if ii[:5] == 'seed-':
                self.seedList.append(ii)        
        self.seedList.sort()
    # -------------------------------------------------------------------------
    def loadSeedActors(self):
        
        keyList = self.streamDict.keys()
        for ii in keyList:
            if ii[:5] == 'seed-':
                self.seedActors[ii] = self.getSeedActor(ii, self.streamDict) 
    
    
    # ----------------------------------------------------------------------------
    def addSeed(self, widget):
            
        nums = []
        for ii in self.seedList:
            aa = ii.split('-')            
            nums.append(int(aa[1]))
        if nums == []:
            name = 'seed-0'
        else:
            name = 'seed-' + str(max(nums) + 1)
            
        self.seedList.append(name)
                       
        self.streamDict[name] = {}
        self.streamDict[name]['seedType'] = 'line'
        self.streamDict[name]['point1'] = ['0', '0', '0']
        self.streamDict[name]['point2'] = ['0', '0', '1']
        self.streamDict[name]['resolution'] = '10'   
        self.streamDict[name]['point3'] = ['0', '0', '0']
        self.streamDict[name]['center'] = ['0', '0', '0']
        self.streamDict[name]['radius'] = '1'
      
        self.GEN.pickleDump(self.setFile, self.streamDict)

        self.makeTreeStore()                      

        seedActor = self.getSeedActor(name, self.streamDict)
        self.seedActors[name] = seedActor
        
        self.renderer.AddActor(seedActor)

    #---------------------------------------------------------------------------------------------
    def deleteSeed(self, widget):
    
        if self.selectToDel == []:
            self.GEN.makeDialog('Warning!!! Select name to delete')
            return
        else:       
            self.treestore.remove(self.selectToDel[1])
            self.seedList.remove(self.selectToDel[0])               
            if self.selectToDel[0] in self.streamDict.keys():
                del self.streamDict[self.selectToDel[0]]
                del self.seedActors[self.selectToDel[0]]
            else:
                return
        self.treeview.expand_all()
        self.GEN.pickleDump(self.setFile, self.streamDict)
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        if tree_iter != None:
            path = tree_model.get_path(tree_iter)
            value0 = tree_model.get_value(tree_iter, 1)
            if len(path) == 2:
                self.selectToDel = [value0, tree_iter]
            else:
                self.selectToDel = []
        self.streambox.show_all()
    #---------------------------------------------------------------------------------------------------------        
    def showStream(self, widget):
    
        POST = postProcessingClass(self)
        self.allActors = POST.showStream(self.streamDict, self.seedList, self.reader)

        readergetblock = self.reader.GetOutput().GetBlock(0)
        self.colorRange = readergetblock.GetPointData().GetArray(self.streamDict['scalar']).GetRange()
            
        self.setColormap()
            
        self.Widget_ScalarBar = vtk.vtkScalarBarWidget()
        self.Widget_ScalarBar.SetScalarBarActor(self.allActors[0][2])
        self.Widget_ScalarBar.SetInteractor(self.gvtk)
        self.Widget_ScalarBar.GetRepresentation().SetPosition( 0.85, 0.46 )
        self.Widget_ScalarBar.GetRepresentation().SetPosition2( 0.08, 0.484 )  
        self.Widget_ScalarBar.On()   
             
        for ii in self.allActors:
            self.renderer.AddActor(ii[0])

        for ii in self.allActors:
            ii[0].GetMapper().SetLookupTable(self.colorFunction)
            ii[0].GetMapper().SelectColorArray(self.streamDict['scalar'])

        for ii in self.vtkFeatureActors:
            self.renderer.AddActor(ii)
            
        if self.streamDict['showSeed'] == True:
            self.showAllSeedActor()
                
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------        
    def setColormap(self):
    
        scalarbar = self.allActors[0][2]        
        self.colorFunction = scalarbar.GetLookupTable()
        self.colorFunction.RemoveAllPoints()

        if self.streamDict['colormap'] == 'blue to red':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.0, 0.0, 1.0)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 1.0, 0.0, 0.0)
            self.colorFunction.SetColorSpaceToHSV()
            self.colorFunction.HSVWrapOff()
        elif self.streamDict['colormap'] == 'cool to warm':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            self.colorFunction.SetColorSpaceToDiverging()           
        else:
            num = self.colormapDict[self.streamDict['colormap']][0]
            data = self.colormapDict[self.streamDict['colormap']][1]
            delta = self.colorRange[1]-self.colorRange[0]
            for i in range(num):
                self.colorFunction.AddRGBPoint(self.colorRange[0] + delta * (i) / (num - 1), data[i][0], data[i][1], data[i][2])
		
        scalarbar.SetTitle("%-7s"%self.streamDict['scalar'])
    #---------------------------------------------------------------------------------------------------------        
    def changeColormap(self):
    
        self.setColormap() 
        for ii in self.allActors:
            ii[0].GetMapper().SetLookupTable(self.colorFunction)
        self.gvtk.Initialize()     
    #---------------------------------------------------------------------------------------------------------        
    def fitRange(self):
    
        readergetblock = self.reader.GetOutput().GetBlock(0)
        drange = readergetblock.GetPointData().GetArray(self.streamDict['scalar']).GetRange()
        
        colorRange = [drange[0], drange[1]]
        return colorRange  
           
    #---------------------------------------------------------------------------------------------------------        
    def changeTime(self):
                          
        plottime = float(self.streamDict['time'])
        self.reader.GetExecutive().SetUpdateTimeStep(0, plottime)
        self.reader.Modified()
        self.reader.Update()    
        self.gvtk.Initialize()             
   
    #----------------------------------------------------------------------------------------------------
    def colormapData(self):
    
        cmaps = glob.glob(self.installpath+'/colormaps/*')        
        names = []
        nums = []
        datas = []
        for ii in cmaps:
            with open(ii, 'r') as f:
                ff = f.readlines()
            names.append(ff[0].strip())            
            nums.append(int(ff[2].strip()))
            vvs = []
            for i in range(len(ff) - 3):
                aa = ff[i + 3].split()
                lis = [float(aa[0]), float(aa[1]), float(aa[2])]
                vvs.append(lis)
            datas.append(vvs)            
        cmapdic = {}
        for i in range(len(names)):
            cmapdic[names[i]] = [nums[i], datas[i]]            
        return cmapdic    
    #---------------------------------------------------------------------------------------------------------                            
    def getPostReader(self):
    
        fileName = self.caseDir+"/ "
        if glob.glob(self.caseDir+'/processor*'):
            caseType = 0
        else:
            caseType = 1

        self.reader = vtk.vtkPOpenFOAMReader()
        self.reader.SetFileName(fileName)
        self.reader.SetCaseType(caseType)
        self.reader.CreateCellToPointOn()
        self.reader.DecomposePolyhedraOn()
        self.reader.Update()
    #---------------------------------------------------------------------------------------------
    def getSeedActor(self, seedName, dic):
        
        if dic[seedName]['seedType'] == 'line':
            point1 = dic[seedName]['point1']
            point2 = dic[seedName]['point2']
            resolution = dic[seedName]['resolution']
            actor = self.VTK_All.seed_line(point1, point2, resolution)
            return actor

        elif dic[seedName]['seedType'] == 'plane':
            point1 = dic[seedName]['point1']
            point2 = dic[seedName]['point2']
            point3 = dic[seedName]['point3']
            resolution = dic[seedName]['resolution']
            actor = self.VTK_All.seed_plane(point1, point2, point3, resolution)
            return actor

        elif dic[seedName]['seedType'] == 'sphere':
            center = dic[seedName]['center']
            radius = dic[seedName]['radius']
            resolution = dic[seedName]['resolution']
            actor = self.VTK_All.seed_sphere(center, radius, resolution)
            return actor
    #---------------------------------------------------------------------------------------------
    def showAllSeedActor(self):        
        names = self.seedActors.keys()
        for ii in names:
            self.renderer.AddActor(self.seedActors[ii])
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------
    def removeAllSeedActor(self):        
        names = self.seedActors.keys()
        for ii in names:
            self.renderer.RemoveActor(self.seedActors[ii])
        self.gvtk.Initialize()
            
                    
