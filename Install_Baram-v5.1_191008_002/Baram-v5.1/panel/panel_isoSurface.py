#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelIsoSurfaceClass:
                
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
        
        self.isoSurfaceList = []
        self.multiSurfaceList = []        
        self.allActors = None
        self.isoSurfaceActors = []
        self.multiSurfaceActors = []
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')         
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png') 
    #------------------------------------------------------------------------------------------
    def isoSurface(self):
        
        self.getPostReader()                
        self.colormapDict = self.colormapData()

        self.isoSurfacebox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.isoSurfacebox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Display Iso-Surface  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.isoSurfacebox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 70)

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

        self.setFile = self.caseDir + '/system/settings/isoSurfaceSet'
        self.loadIsoDict()
        
        self.getTimeList()
        self.getArrayName()        
        # treeview isoSurface-------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)        
        self.row_surface = self.treestore.append(None, [self.pixbuf_main, 'isoSurfaces/value', None])
        self.row_multiSurface = self.treestore.append(None, [self.pixbuf_main, 'multiSurfaces', None])

        keyList = self.isoDict.keys()
        for ii in keyList:
            if ii[:11] == 'isoSurface-':
                self.isoSurfaceList.append(ii)
            if ii[:13] == 'multiSurface-':
                self.multiSurfaceList.append(ii)
        
        self.isoSurfaceList.sort()
        
        for ii in self.isoSurfaceList:
            self.treestore.append(self.row_surface, [self.pixbuf_first, ii, None])
        for ii in self.multiSurfaceList:
            row_name = self.treestore.append(self.row_multiSurface, [self.pixbuf_first, ii, None])
            self.treestore.append(row_name, [self.pixbuf_first, 'from', self.isoDict[ii]['from']])
            self.treestore.append(row_name, [self.pixbuf_first, 'to', self.isoDict[ii]['to']])
            self.treestore.append(row_name, [self.pixbuf_first, 'steps', self.isoDict[ii]['steps']])
                
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect('cursor-changed', self.selected, self.treeview)
        
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_grid_lines(False)
        
        self.tvcolumn0 = gtk.TreeViewColumn(None)
        self.tvcolumn1 = gtk.TreeViewColumn(None)
        self.tvcolumn2 = gtk.TreeViewColumn(None)
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.renbuf = gtk.CellRendererPixbuf()
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererText()
                          
        self.ren0.set_property('editable', False)
        self.ren1.set_property('editable', True)

        self.tvcolumn0.pack_start(self.renbuf, False)
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn1.pack_start(self.ren1, False) 
        self.tvcolumn0.set_attributes(self.renbuf, pixbuf = 0)
        self.tvcolumn0.set_attributes(self.ren0, markup = 1)

        self.ren1.connect('edited', self.changeValue)
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func)
                    
        self.treeview.expand_all()
        self.mainbox.add(self.treeview)
        # treeview common---------------------------------------------------------------
        self.treestore_common = gtk.TreeStore(str, bool, str)        
        self.treestore_common.append(None, ['isoField', None, None])
        self.treestore_common.append(None, ['Scalar', None, None])
        self.treestore_common.append(None, ['Time', None, None])
        self.treestore_common.append(None, ['Colormap', None, None])        
        self.treestore_common.append(None, ['Overlay', False, None])
        self.treestore_common.append(None, ['Data type', None, None]) 
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
        
        self.tvcolumn0_common.set_attributes(self.ren0_common, text=0)
        self.tvcolumn1_common.add_attribute(self.ren1_common,'active', 1)
        self.tvcolumn1_common.set_cell_data_func(self.ren2_common, self.func_common)

        self.valuebox.pack_start(self.treeview_common, True, True, 0) 

        # label
        self.rangeLabel = gtk.Label()
        field = self.isoDict['isoField']
        if self.isThereData() == True:
            text='  Range of ' + field + ' : ' + str(self.fullRange[field][0]) + ' ~ ' + str(self.fullRange[field][1])
        else:
            text=''
        
        self.rangeLabel.set_text(text)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 15)
        hbox.pack_start(self.rangeLabel, False, False, 0)
        
        # button
        addB = gtk.Button('isoSurface')
        addB.set_size_request(100, 28)
        addB.connect('clicked', self.addSurface)
        addMultiB = gtk.Button('multi-Surface')
        addMultiB.set_size_request(100, 28)
        addMultiB.connect('clicked', self.addMultiSurface)
        delB = gtk.Button('Delete')
        delB.set_size_request(100, 28)
        delB.connect('clicked', self.deleteSurface)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(addB, True, True, 0)
        hbox.pack_start(addMultiB, True, True, 0)
        hbox.pack_start(delB, True, True, 0)
        
        contourB = gtk.Button('Display contour')
        contourB.set_size_request(150, 28)
        contourB.connect('clicked', self.showIso)
        hbox = gtk.HBox(False,0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(contourB, True, True, 0)

        return self.isoSurfacebox 
    #--------------------------------------------------------   
    def togglePost(self, widget, path, model):
    
        model[path][1] = not model[path][1]                   
        self.isoDict['Overlay'] = model[path][1]        
        self.GEN.pickleDump(self.setFile, self.isoDict)
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)
        old = self.treestore[path][2]
        
        if old == what:
            return         
        
        if self.GEN.checkNumber(value0, what):
            if value0[:10] == 'isoSurface':        
                surfacename = self.isoSurfaceList[int(path[2])]
                self.isoDict[surfacename]['value'] = what
                self.showIso(None)
            elif value0 == 'from':
                surfacename = self.multiSurfaceList[int(path[2])]
                self.isoDict[surfacename]['from'] = what
            elif value0 == 'to':
                surfacename = self.multiSurfaceList[int(path[2])]
                self.isoDict[surfacename]['to'] = what
            elif value0 == 'steps':
                surfacename = self.multiSurfaceList[int(path[2])]
                self.isoDict[surfacename]['steps'] = what
            
            self.GEN.pickleDump(self.setFile, self.isoDict)              
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what):
    
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)
        old = self.treestore_common[path][2]
        
        if old == what:
            return

        if value0 == 'isoField':
            self.isoDict['isoField'] = what
            text='  Range of ' + what + ' : ' + str(self.fullRange[what][0]) + ' ~ ' + str(self.fullRange[what][1])
            self.rangeLabel.set_text(text)            
            for ii in self.multiSurfaceList:
                self.isoDict[ii]['from'] = str(self.fullRange[what][0])
                self.isoDict[ii]['to'] = str(self.fullRange[what][1])
        elif value0 == 'Scalar':
            self.isoDict['scalar'] = what
            if self.allActors:
                self.showIso(None)
        elif value0 == 'Time':
            self.isoDict['time'] = what
            if self.allActors:
                self.changeTime()            
            self.getArrayName()
            text='  Range of ' + self.isoDict['isoField'] + ' : ' + str(self.fullRange[self.isoDict['isoField']][0]) + ' ~ ' + str(self.fullRange[self.isoDict['isoField']][1])
            self.rangeLabel.set_text(text)
        elif value0 == 'Colormap':
            self.isoDict['colormap'] = what       
            if self.allActors:
                self.changeColormap()
        elif value0 == 'Data type':
            self.isoDict['dataType'] = what
            if self.allActors:
                self.changeDataType()
        
        self.treestore_common[path][2] = what
        self.GEN.pickleDump(self.setFile, self.isoDict)
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
    
        what = model.get_value(iter, 1)
        path = model.get_path(iter)        
       
        if what == 'isoSurfaces/value':
            self.ren1.set_property('visible', 0)
        elif what[:10] == 'isoSurface':   
            self.ren1.set_property('visible', 1)
            surfacename = self.isoSurfaceList[int(path[1])]
            self.ren1.set_property('text', self.isoDict[surfacename]['value'])
        elif what[:12] == 'multiSurface':   
            self.ren1.set_property('visible', 0)
        elif what == 'from':
            self.ren1.set_property('visible', 1)
            surfacename = self.multiSurfaceList[int(path[1])]
            self.ren1.set_property('text', self.isoDict[surfacename]['from'])
        elif what == 'to':
            self.ren1.set_property('visible', 1)
            surfacename = self.multiSurfaceList[int(path[1])]
            self.ren1.set_property('text', self.isoDict[surfacename]['to'])
        elif what == 'steps':
            self.ren1.set_property('visible', 1)
            surfacename = self.multiSurfaceList[int(path[1])]
            self.ren1.set_property('text', self.isoDict[surfacename]['steps'])
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model,iter):
    
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)        
        combo = ['isoField', 'Scalar', 'Time', 'Colormap', 'Data type']
        
        if what in combo:
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)            
            self.ren2_common.set_property('has-entry', False)
            if what == 'isoField':            
                self.ren2_common.set_property('model',dic['scalars'])
                self.ren2_common.set_property('text', self.isoDict['isoField'])
            elif what == 'Scalar':
                self.ren2_common.set_property('model',dic['scalars'])
                self.ren2_common.set_property('text', self.isoDict['scalar'])
            elif what == 'Time':
                self.ren2_common.set_property('model',dic['times'])
                self.ren2_common.set_property('text', self.isoDict['time'])
            elif what == 'Colormap':
                self.ren2_common.set_property('model',dic['colormap'])
                self.ren2_common.set_property('text', self.isoDict['colormap'])
            elif what == 'Data type':
                self.ren2_common.set_property('model', dic['dataType'])
                self.ren2_common.set_property('text', self.isoDict['dataType'])
        elif what == 'Overlay':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0) 
    #---------------------------------------------------------------------------------------------    
    def liststore_post(self, scalars, times):

        colormap = ['blue to red', 'cool to warm', 'high_contrast', 'hot_to_cold', 'leaf_color',
                    'small_difference', 'hot', 'indigo_flame', 'land_color', 'spectrum_white']                      

        isoField = []
        for ii in scalars:
            isoField.append(ii)

        liststore_scalars = gtk.ListStore(str)
        for ii in scalars:
            liststore_scalars.append([ii])
        
        liststore_times = gtk.ListStore(str)
        for ii in times:
            liststore_times.append([ii])
        
        liststore_colormap = gtk.ListStore(str)
        for ii in colormap:
            liststore_colormap.append([ii])
       
        liststore_isoField = gtk.ListStore(str)
        for ii in isoField:
            liststore_isoField.append([ii])
        
        liststore_yesNo = gtk.ListStore(str)
        liststore_yesNo.append(['yes'])
        liststore_yesNo.append(['no'])
        
        liststore_dataType = gtk.ListStore(str)
        liststore_dataType.append(['point value'])
        liststore_dataType.append(['cell value'])
        
        storeDict = {}
        keys = ['scalars', 'times', 'colormap', 'isoField', 'yesNo', 'dataType']
        values = [liststore_scalars, liststore_times, liststore_colormap,
                  liststore_isoField, liststore_yesNo, liststore_dataType]
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]
        
        return storeDict 
    # -------------------------------------------------------------------------
    def loadIsoDict(self):
        
        self.isoDict = self.GEN.pickleLoad(self.setFile)        
        if self.isoDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.isoDict = dicts[6]     
        self.isoDict['displayContour'] = False
        self.isoDict['Overlay'] = False
    # ----------------------------------------------------------------------------
    def addSurface(self, widget):
    
        nums = []
        for ii in self.isoSurfaceList:
            aa = ii.split('-')            
            nums.append(int(aa[1]))
        if nums == []:
            name = 'isoSurface-0'
        else:
            name = 'isoSurface-' + str(max(nums) + 1)
        
        self.isoSurfaceList.append(name)        
        self.treestore.append(self.row_surface, [self.pixbuf_first, name, '0'])
                               
        self.isoDict[name] = {}
        self.isoDict[name]['value'] = '0'   
        self.GEN.pickleDump(self.setFile, self.isoDict)
        self.treeview.expand_all()
    # ----------------------------------------------------------------------------
    def addMultiSurface(self, widget):     
    
        nums = []
        for ii in self.multiSurfaceList:
            aa = ii.split('-')            
            nums.append(int(aa[1]))
        if nums == []:
            name = 'multiSurface-0'
        else:
            name = 'multiSurface-' + str(max(nums) + 1)        
        
        self.multiSurfaceList.append(name)        
        row_name = self.treestore.append(self.row_multiSurface, [self.pixbuf_first, name, None])
        self.treestore.append(row_name, [self.pixbuf_second, 'from', str(self.fullRange[self.isoDict['isoField']][0])])
        self.treestore.append(row_name, [self.pixbuf_second, 'to', str(self.fullRange[self.isoDict['isoField']][0])])
        self.treestore.append(row_name, [self.pixbuf_second, 'steps', '10'])
                       
        self.isoDict[name] = {}
        self.isoDict[name]['from'] = str(self.fullRange[self.isoDict['isoField']][0])  
        self.isoDict[name]['to'] = str(self.fullRange[self.isoDict['isoField']][1]) 
        self.isoDict[name]['steps'] = '10'
        self.GEN.pickleDump(self.setFile, self.isoDict)
        self.treeview.expand_all()
    #---------------------------------------------------------------------------------------------
    def deleteSurface(self, widget):
    
        if self.selectToDel == []:
            self.GEN.makeDialog('Warning!!! Select name to delete')
            return
        else:       
            self.treestore.remove(self.selectToDel[1])
            if self.selectToDel[0][:10] == 'isoSurface':
                self.isoSurfaceList.remove(self.selectToDel[0])               
            elif self.selectToDel[0][:12] == 'multiSurface':
                self.multiSurfaceList.remove(self.selectToDel[0])               
                
            if self.selectToDel[0] in self.isoDict.keys():
                del self.isoDict[self.selectToDel[0]]
            else:
                return
        self.treeview.expand_all()
        self.GEN.pickleDump(self.setFile, self.isoDict)
    #---------------------------------------------------------------------------------------------------------        
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        if tree_iter:
            path = tree_model.get_path(tree_iter)
            value0 = tree_model.get_value(tree_iter, 1)
            value1 = tree_model.get_value(tree_iter, 2)
            if len(path) == 2:
                self.selectToDel = [value0, tree_iter]
            else:
                self.selectToDel = []
        self.isoSurfacebox.show_all()
    #---------------------------------------------------------------------------------------------------------        
    def showIso(self, widget):
    
        if self.isoSurfaceList == [] and self.multiSurfaceList == []:
            return
    
        self.displayMode = self.mainself.displayMode
        POST = postProcessingClass(self)
        self.allActors, self.allIsos = POST.showIso(self.isoDict, self.isoSurfaceList, self.multiSurfaceList, 
                                                    self.isoSurfaceActors, self.reader, self.displayMode)
           
        self.allActors[0][1].SetTitle("%-7s"%self.isoDict['scalar'])
        
        self.Widget_ScalarBar = vtk.vtkScalarBarWidget()
        self.Widget_ScalarBar.SetScalarBarActor(self.allActors[0][1])
        self.Widget_ScalarBar.SetInteractor(self.gvtk)
        self.Widget_ScalarBar.GetRepresentation().SetPosition( 0.85, 0.46 )
        self.Widget_ScalarBar.GetRepresentation().SetPosition2( 0.08, 0.484 )
        self.Widget_ScalarBar.On()   
                
        for ii in self.allActors:
            self.renderer.AddActor(ii[0])
            self.isoSurfaceActors.append(ii[0])
            self.isoSurfaceActors.append(ii[1])

        self.gvtk.Initialize()
        self.fitRange()       
        self.setColormap()
        
        for ii in self.allActors:
            ii[0].GetMapper().SetLookupTable(self.colorFunction)
            ii[0].GetMapper().SelectColorArray(self.isoDict['scalar'])
            ii[0].GetProperty().EdgeVisibilityOff()            
        
        for ii in self.vtkFeatureActors:
            self.renderer.AddActor(ii)
        
        self.gvtk.Initialize()                  
    #---------------------------------------------------------------------------------------------------------        
    def setColormap(self):
    
        scalarbar = self.allActors[0][1]        
        self.colorFunction = scalarbar.GetLookupTable()
        self.colorFunction.RemoveAllPoints()

        if self.isoDict['colormap'] == 'blue to red':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.0, 0.0, 1.0)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 1.0, 0.0, 0.0)
            self.colorFunction.SetColorSpaceToHSV()
            self.colorFunction.HSVWrapOff()
        elif self.isoDict['colormap'] == 'cool to warm':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            self.colorFunction.SetColorSpaceToDiverging()           
        else:
            num = self.colormapDict[self.isoDict['colormap']][0]
            data = self.colormapDict[self.isoDict['colormap']][1]
            delta = self.colorRange[1] - self.colorRange[0]
            for i in range(num - 1):
                self.colorFunction.AddRGBPoint(self.colorRange[0] + delta*(i) / num, data[i][0], data[i][1], data[i][2])

        scalarbar.SetTitle("%-7s"%self.isoDict['scalar'])
    #---------------------------------------------------------------------------------------------------------        
    def changeColormap(self):
    
        self.setColormap()         
        for ii in self.allActors:
            ii[0].GetMapper().SetLookupTable(self.colorFunction)
        self.gvtk.Initialize()     
    #---------------------------------------------------------------------------------------------------------        
    def fitRange(self):
    
        mins = []
        maxs = []
        for i in range(len(self.isoSurfaceList)):                        
            iso = self.allIsos[i]
            if self.isoDict['dataType'] == 'cell value':
                drange = iso.GetOutput().GetCellData().GetArray(self.isoDict['scalar']).GetRange()
            else:
                drange = iso.GetOutput().GetPointData().GetArray(self.isoDict['scalar']).GetRange()
            mins.append(drange[0])
            maxs.append(drange[1])
            
        for i in range(len(self.multiSurfaceList)):                        
            iso = self.allIsos[len(self.isoSurfaceList) + i]
            if self.isoDict['dataType'] == 'cell value':
                drange = iso.GetOutput().GetCellData().GetArray(self.isoDict['scalar']).GetRange()
            else:
                drange = iso.GetOutput().GetPointData().GetArray(self.isoDict['scalar']).GetRange()
            mins.append(drange[0])
            maxs.append(drange[1])           
                
        self.colorRange = [min(mins), max(maxs)]
    #---------------------------------------------------------------------------------------------------------        
    def changeTime(self):
                          
        plottime = float(self.isoDict['time'])
        self.reader.GetExecutive().SetUpdateTimeStep(0, plottime)
        self.reader.Modified()
        self.reader.Update()    
        self.gvtk.Initialize()             
    #----------------------------------------------------------------------------------------------------
    def changeDataType(self):
    
        self.showIso(None)
    #----------------------------------------------------------------------------------------------------
    def colormapData(self):
    
        cmaps = glob.glob(self.installpath + '/colormaps/*')        
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
    def getTimeList(self):
    
        if glob.glob(self.caseDir + '/constant/polyMesh')==[]:
            self.times = []
            return
        
        outInfo = self.reader.GetExecutive().GetOutputInformation(0)
        timeStepsKey = vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
        nTimeSteps = outInfo.Length(timeStepsKey)
        
        self.times = []
        for i in range(nTimeSteps):
            self.times.append(outInfo.Get(timeStepsKey, i))

        self.isoDict['time'] = str(max(self.times))
    #---------------------------------------------------------------------------------------------------------                            
    def getArrayName(self):
    
        if glob.glob(self.caseDir + '/constant/polyMesh') == []:
            self.scalars = []
            return
        
        self.reader.GetExecutive().SetUpdateTimeStep(0, float(self.isoDict['time']))
        self.reader.Modified()
        self.reader.Update()           
       
        vtkunsgrid = self.reader.GetOutput().GetBlock(0)
        numArray = vtkunsgrid.GetPointData().GetNumberOfArrays()
        self.scalars = []
        for i in range(numArray):
            name = vtkunsgrid.GetPointData().GetArray(i).GetName()
            if name != 'U':
                self.scalars.append(name)

        self.fullRange = {}
        for ii in self.scalars:
            drange = vtkunsgrid.GetCellData().GetArray(ii).GetRange()
            self.fullRange[ii] = drange

        self.scalars.append('coordsX')
        self.scalars.append('coordsY')
        self.scalars.append('coordsZ')
        self.fullRange['coordsX'] = vtkunsgrid.GetPoints().GetData().GetRange(0)
        self.fullRange['coordsY'] = vtkunsgrid.GetPoints().GetData().GetRange(1)
        self.fullRange['coordsZ'] = vtkunsgrid.GetPoints().GetData().GetRange(2)        

    #---------------------------------------------------------------------------------------------------------                            
    def getPostReader(self):
        
        fileName = self.caseDir + "/ "
        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:caseType = 1

        self.reader = vtk.vtkPOpenFOAMReader()
        self.reader.SetFileName(fileName)
        self.reader.SetCaseType(caseType)
        self.reader.CreateCellToPointOn()
        self.reader.DecomposePolyhedraOn()
        self.reader.Update()

    #---------------------------------------------------------------------------------------------
    def isThereData(self):
    
        if glob.glob(self.caseDir + '/constant/polyMesh'):
            if glob.glob(self.caseDir + '/0/p'):
                answer = True
            else:
                answer = False
        else:
            answer = False
        return answer
            
            
                    
