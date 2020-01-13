#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelPatchScalarClass:

    def __init__(self,mainself):
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
        
        self.cactor = None
        self.vactor = None
        self.scalarOrVector = None

        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')  
        
    def patchScalar(self):

        self.bcNameList, self.bcTypeList = self.GEN.getBCName()
        if self.bcNameList == False:
            self.bcNameList = [] 
        
        self.reader = self.VTK_All.unsgeometry(self.bcNameList, self.renderer)        
        self.colormapDict = self.colormapDapa()

        self.patchScalarbox = gtk.VBox()          

        frame = gtk.Frame()        
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.patchScalarbox.pack_start(frame,False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Display patch  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.patchScalarbox.pack_start(self.vpan, True, True, 0)
        
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
             
        self.setFile = self.caseDir + '/system/settings/patchFieldSet'
        self.loadPatchDict()
        
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
        self.times.insert(0,'0')
        self.patchDict['time'] = self.times[-1]     
        # treeview patch ----------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool)        
        
        self.bd = self.treestore.append(None, [self.pixbuf_main, 'Patches to display', None])       

        for ii in self.bcNameList:
            if ii in self.patchDict['patches']:
                self.treestore.append(self.bd, [self.pixbuf_first, ii, True])
            else:   
                self.treestore.append(self.bd, [self.pixbuf_first, ii, False])  
                
        self.treeview = gtk.TreeView(self.treestore)
        
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(False)
        
        self.tvcolumn0=gtk.TreeViewColumn(None)
        self.tvcolumn1=gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)

        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererToggle()                  
                          
        self.ren0.set_property('editable', False)
        self.ren1.set_property('activatable', True)
        
        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False) 
        self.tvcolumn1.pack_start(self.ren1, False)

        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)
        self.tvcolumn1.add_attribute(self.ren1, 'active', 2)  

        self.ren1.connect('toggled', self.togglePost, self.treestore)
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func)        

        self.treeview.expand_all()
        self.mainbox.add(self.treeview)
        # treeview common---------------------------------------------------------------
        self.treestore_common = gtk.TreeStore(str, bool, str)        
        self.treestore_common.append(None,['Scalar', None, None])
        self.treestore_common.append(None,['Time', None, None])
        self.treestore_common.append(None,['Colormap', None, None])        
        self.treestore_common.append(None,['Vector scale', None, None])
        self.treestore_common.append(None,['Overlay', False, None]) 
        # -------------------------------------------------------------------------------
        self.treeview_common = gtk.TreeView(self.treestore_common)
        self.treeview_common.set_enable_tree_lines(True)
        
        self.tvcolumn0_common = gtk.TreeViewColumn('  ITEMs')
        self.tvcolumn1_common = gtk.TreeViewColumn('  VALUE')
        
        self.treeview_common.append_column(self.tvcolumn0_common)
        self.treeview_common.append_column(self.tvcolumn1_common)
        
        self.ren0_common=gtk.CellRendererText()
        self.ren1_common=gtk.CellRendererToggle()
        self.ren2_common=gtk.CellRendererCombo() 
        
        self.ren0_common.set_fixed_size(150, -1)

        self.ren0_common.set_property("editable", False)                 
        self.ren1_common.set_property("activatable", True)
        self.ren2_common.set_property("editable", True)
        self.ren2_common.set_property('text-column', 0)
        
        self.ren1_common.connect('toggled', self.togglePost_common, self.treestore_common)
        self.ren2_common.connect('edited', self.changeValue_common)
        
        self.tvcolumn0_common.pack_start(self.ren0_common, False)                        
        self.tvcolumn1_common.pack_start(self.ren1_common, False)        
        self.tvcolumn1_common.pack_start(self.ren2_common, True) 
        
        self.tvcolumn0_common.set_attributes(self.ren0_common, text=0)
        self.tvcolumn1_common.add_attribute(self.ren1_common, 'active', 1)        
        self.tvcolumn1_common.set_cell_data_func(self.ren2_common, self.func_common)

        self.valuebox.pack_start(self.treeview_common, True, True, 0)                 
        self.makeButton()        
        return self.patchScalarbox
    #--------------------------------------------------------   
    def togglePost(self, widget, path, model):
    
        model[path][2] = not model[path][2]        
        value0 = model[path][1]
        value1 = model[path][2]

        if self.bcNameList == []:
            self.GEN.makeDialog('Warning!!! There is not mesh')
            return
                
        if value0 in self.bcNameList:
            if value1 == True:
                self.patchDict['patches'].append(value0)
            else:
                self.patchDict['patches'].remove(value0)
            self.showPatch(None, self.scalarOrVector)
            
        elif value0 == 'Overlay':
            self.patchDict['Overlay'] = value1
        
        self.GEN.pickleDump(self.setFile, self.patchDict)
    #--------------------------------------------------------   
    def togglePost_common(self,widget,path,model):
    
        model[path][1] = not model[path][1]                   
        self.patchDict['Overlay'] = model[path][1]        
        self.GEN.pickleDump(self.setFile, self.patchDict)  
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what):
    
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)        
        old = self.treestore_common[path][2] 
        
        if old == what:
            return              
        if value0 == 'Scalar':
            self.patchDict['scalar'] = what
            if self.cactor:
                self.changeScalar()
        elif value0 == 'Time':
            self.patchDict['time'] = what
            if self.cactor:
                self.changeTime()
        elif value0 == 'Colormap':
            self.patchDict['colormap'] = what
            if self.cactor:
                self.changeColormap()
        elif value0 == 'Vector scale':
            if self.GEN.checkNumber(value0, what):
                self.patchDict['scaleFactor'] = what                      
                self.changeVectorScale()
            
        self.treestore_common[path][2] = what
        self.GEN.pickleDump(self.setFile, self.patchDict)      
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
        what = model.get_value(iter, 1)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)

        if what == 'Patches to display':
            self.ren1.set_property('visible', 0)            
        elif what in self.bcNameList:
            self.ren1.set_property('visible', 1)       
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model, iter):
    
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)
        combo = ['Scalar', 'Time', 'Colormap']

        if what in combo:
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)            
            self.ren2_common.set_property('has-entry', False)
            if what == 'Scalar':
                self.ren2_common.set_property('model',dic['scalars'])
                self.ren2_common.set_property('text', self.patchDict['scalar'])
            elif what == 'Time':
                self.ren2_common.set_property('model',dic['times'])
                self.ren2_common.set_property('text', self.patchDict['time'])
            elif what == 'Colormap':
                self.ren2_common.set_property('model',dic['colormap'])
                self.ren2_common.set_property('text', self.patchDict['colormap'])
        elif what == 'Vector scale':
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)
            self.ren2_common.set_property('model', None)
            self.ren2_common.set_property('has-entry', True)
            self.ren2_common.set_property('text', self.patchDict['scaleFactor'])
        elif what == 'Overlay':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0) 
    #---------------------------------------------------------------------------------------------    
    def liststore_post(self, scalars, times):

        colormap = ['blue to red', 'cool to warm', 'high_contrast', 'hot_to_cold', 'leaf_color',
                    'small_difference', 'hot', 'indigo_flame', 'land_color', 'spectrum_white']                      
        colorby = ['U', 'Scalar']
        axis = ['x', 'y', 'z']
        
        scalars_cut = []
        for ii in scalars:
            scalars_cut.append(ii)
        scalars_cut.append('mesh')
                       
        liststore_scalars = gtk.ListStore(str)
        for ii in scalars:
            liststore_scalars.append([ii])
        
        liststore_scalars_cut = gtk.ListStore(str)
        for ii in scalars_cut:
            liststore_scalars_cut.append([ii])
        
        liststore_times = gtk.ListStore(str)
        for ii in times:
            liststore_times.append([ii])
        
        liststore_colormap = gtk.ListStore(str)
        for ii in colormap:
            liststore_colormap.append([ii])
       
        liststore_colorby = gtk.ListStore(str)
        for ii in colorby:
            liststore_colorby.append([ii])
        
        liststore_axis = gtk.ListStore(str)
        for ii in axis:
            liststore_axis.append([ii])
        
        liststore_yesNo = gtk.ListStore(str)
        liststore_yesNo.append(['yes'])
        liststore_yesNo.append(['no'])
        
        storeDict = {}
        keys = ['scalars', 'scalars_cut', 'times', 'colormap', 'colorby', 'axis', 'yesNo']
        values = [liststore_scalars, liststore_scalars_cut, liststore_times, liststore_colormap, 
                  liststore_colorby, liststore_axis, liststore_yesNo]
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]        
        return storeDict            
    #---------------------------------------------------------------------------------------------------------        
    def showPatch(self, widget, oldDisplay):
    
        if self.patchDict['patches'] == []:
            self.GEN.makeDialog('Select patch first!!!')
            return
    
        self.displayMode = self.mainself.displayMode
        POST = postProcessingClass(self)
        self.cactor, self.vactor, self.scalar_bar, self.compositeFilter, self.glyph = POST.showPatch(self.patchDict, self.reader, self.displayMode)
                       
        self.scalar_bar.SetTitle("%-7s"%self.patchDict['scalar'])
                       
        self.Widget_ScalarBar = vtk.vtkScalarBarWidget()
        self.Widget_ScalarBar.SetScalarBarActor(self.scalar_bar)
        self.Widget_ScalarBar.SetInteractor(self.gvtk)
        self.Widget_ScalarBar.GetRepresentation().SetPosition( 0.85, 0.46 )
        self.Widget_ScalarBar.GetRepresentation().SetPosition2( 0.08, 0.484 ) 
        self.Widget_ScalarBar.On()   
            
        if oldDisplay == 'contour':
            self.scalarOrVector = 'contour'                     
            self.renderer.AddActor(self.cactor)
        if oldDisplay == 'vector':
            self.scalarOrVector = 'vector'  
            self.renderer.AddActor(self.vactor)
        self.gvtk.Initialize()
    # -------------------------------------------------------------------------
    def loadPatchDict(self):    
    
        self.patchDict = self.GEN.pickleLoad(self.setFile)
        if self.patchDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.patchDict = dicts[4]
        self.patchDict['Overlay'] = False     
    #---------------------------------------------------------------------------------------------
    def makeButton(self):
    
        POST = postProcessingClass(self)
        contourB = gtk.Button('Display contour')
        vectorB = gtk.Button('Display vector')
        contourB.set_size_request(150, 28)
        vectorB.set_size_request(150, 28)
        contourB.connect('clicked', self.showPatch,'contour')
        vectorB.connect('clicked', self.showPatch,'vector')
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(contourB, True, True, 0)
        hbox.pack_end(vectorB, True, True, 0)            
    #---------------------------------------------------------------------------------------------------------        
    def setColormap(self):
    
        self.colorFunction = self.scalar_bar.GetLookupTable()
        self.colorFunction.RemoveAllPoints()
        
        self.colorRange = self.compositeFilter.GetOutput().GetCellData().GetArray(self.patchDict['scalar']).GetRange()

        if self.patchDict['colormap'] == 'blue to red':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.0, 0.0, 1.0)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 1.0, 0.0, 0.0)
            self.colorFunction.SetColorSpaceToHSV()
            self.colorFunction.HSVWrapOff()
        elif self.patchDict['colormap'] == 'cool to warm':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            self.colorFunction.SetColorSpaceToDiverging()           
        else:
            num=self.colormapDict[self.patchDict['colormap']][0]
            data=self.colormapDict[self.patchDict['colormap']][1]
            delta=self.colorRange[1] - self.colorRange[0]
            for i in range(num - 1):
                self.colorFunction.AddRGBPoint(self.colorRange[0] + delta*(i) / num, data[i][0], data[i][1], data[i][2])
        self.scalar_bar.SetTitle("%-7s"%self.patchDict['scalar'])
    #---------------------------------------------------------------------------------------------------------        
    def changeColormap(self):
    
        self.setColormap()
        if self.scalarOrVector == 'contour':
            self.cactor.GetMapper().SetLookupTable(self.colorFunction)
        else:
            self.vactor.GetMapper().SetLookupTable(self.colorFunction)
        self.gvtk.Initialize() 
    #---------------------------------------------------------------------------------------------------------        
    def changeScalar(self):
    
        self.setColormap()
        if self.scalarOrVector == 'contour':
            self.cactor.GetMapper().SetLookupTable(self.colorFunction)
            self.cactor.GetMapper().SelectColorArray(self.patchDict['scalar'])
            self.cactor.GetMapper().SetScalarRange(self.colorRange)
        else:
            self.vactor.GetMapper().SetLookupTable(self.colorFunction)
            self.vactor.GetMapper().SelectColorArray(self.patchDict['scalar'])
            self.vactor.GetMapper().SetScalarRange(self.colorRange)
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------        
    def changeTime(self):
                          
        plottime = float(self.patchDict['time'])
        self.reader.GetExecutive().SetUpdateTimeStep(0, plottime)
        self.reader.Modified()
        self.reader.Update()    
        self.gvtk.Initialize()             
    #---------------------------------------------------------------------------------------------------------        
    def changeVectorScale(self): 
    
        if self.scalarOrVector == 'vector':
            self.glyph.SetScaleFactor(float(self.patchDict['scaleFactor']))	
        self.gvtk.Initialize()                  
    #----------------------------------------------------------------------------------------------------
    def colormapDapa(self):
            
        cmaps = glob.glob(self.installpath + '/colormaps/*')        
        names = []
        nums = []
        datas = []
        for ii in cmaps:
            with open(ii, 'r') as f:
                ff=f.readlines()            
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
    #---------------------------------------------------------------------------------------------

        
                
               
