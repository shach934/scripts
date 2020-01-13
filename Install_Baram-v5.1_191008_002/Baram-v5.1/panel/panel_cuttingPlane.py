#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelCuttingPlaneClass:
                
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
        
        self.planeList = []        
        self.scalarOrVector = None
        self.allActors = None
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')  
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')  
    #------------------------------------------------------------------------------------------
    def cuttingPlane(self):
        
        self.getPostReader()        
        self.colormapDict = self.colormapData()
        
        self.cuttingPlanebox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.cuttingPlanebox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Display cutPlane  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.cuttingPlanebox.pack_start(self.vpan, True, True, 0)
        
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
                  
        self.setFile = self.caseDir + '/system/settings/cuttingPlaneSet'
        self.loadCutDict()
        
        self.scalars = []
        self.times = []
        self.scalars = self.GEN.getScalars()
        self.scalars.append('mesh')
        if 'boundaryFields' in self.scalars:
            self.scalars.remove('boundaryFields')
        savedResult = self.GEN.getResult()                       
        if len(savedResult[0]) >= len(savedResult[1]):
            self.times = savedResult[0]
        else:
            self.times = savedResult[1]
        self.times.insert(0, '0')
        self.cutDict['time'] = self.times[-1]   
        # treeview plane ----------------------------------------------------------------
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)        
        self.row_plane = self.treestore.append(None, [self.pixbuf_main, 'Planes to display', None])

        keyList = self.cutDict.keys()
        for ii in keyList:
            if ii[:6] == 'plane-':
                self.planeList.append(ii)        
        self.planeList.sort()
        
        for ii in self.planeList:
            row_name = self.treestore.append(self.row_plane, [self.pixbuf_first, ii, None])
            row_axis = self.treestore.append(row_name, [self.pixbuf_second, 'Axis', None])
            row_cut = self.treestore.append(row_name, [self.pixbuf_second, 'Value', None])
        # -------------------------------------------------------------------------------
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
        self.ren1 = gtk.CellRendererCombo()
                          
        self.ren0.set_property('editable', False)
        self.ren1.set_property('editable', True)
        self.ren1.set_property('text-column', 0)

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
        self.treestore_common.append(None, ['Scalar', None, None])
        self.treestore_common.append(None, ['Time', None, None])
        self.treestore_common.append(None, ['Colormap', None, None])        
        self.treestore_common.append(None, ['Vector scale', None, None])
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
        
        self.tvcolumn0_common.set_attributes(self.ren0_common, text = 0)
        self.tvcolumn1_common.add_attribute(self.ren1_common, 'active', 1)        
        self.tvcolumn1_common.set_cell_data_func(self.ren2_common, self.func_common)

        self.valuebox.pack_start(self.treeview_common, True, True, 0) 
        
        # button
        addB = gtk.Button('Add plane')
        addB.set_size_request(100, 28)
        addB.connect('clicked', self.addPlane)
        delB = gtk.Button('Delete plane')
        delB.set_size_request(100, 28)
        delB.connect('clicked', self.deletePlane)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(addB, True, True, 0)
        hbox.pack_start(delB, True, True, 0)
        
        contourB = gtk.Button('Display contour')
        contourB.set_size_request(150, 28)
        contourB.connect('clicked', self.showCut, 'contour')
        vectorB = gtk.Button('Display vector')
        vectorB.set_size_request(150, 28)
        vectorB.connect('clicked', self.showCut, 'vector')
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(contourB, True, True, 0)
        hbox.pack_end(vectorB, True, True, 0)         

        return self.cuttingPlanebox 
    #--------------------------------------------------------   
    def togglePost(self,widget,path,model):
    
        model[path][1] = not model[path][1]                   
        self.cutDict['Overlay'] = model[path][1]        
        self.GEN.pickleDump(self.setFile, self.cutDict)      
    #---------------------------------------------------------------------------------------------------------        
    def changeValue(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 1)
        old = self.treestore[path][2]
        
        if old == what:
            return         
        
        domainRange = self.GEN.getDomainRange()
           
        if value0 == 'Axis':       
            planename = self.planeList[int(path[2])]
            self.cutDict[planename]['axis'] = what
        elif value0 == 'Value':        
            if self.GEN.checkNumber(value0, what):
                planename = self.planeList[int(path[2])]
                if self.cutDict[planename]['axis'] == 'x':
                    if float(what) < float(domainRange[0][0]) or float(what) > float(domainRange[1][0]):
                        self.GEN.makeDialog('Out of range!!! \n\n domain range of x : ' + domainRange[0][0] + ' ~ ' + domainRange[1][0])
                        return
                elif self.cutDict[planename]['axis'] == 'y':
                    if float(what) < float(domainRange[0][1]) or float(what) > float(domainRange[1][1]):
                        self.GEN.makeDialog('Out of range!!! \n\n domain range of y : ' + domainRange[0][1] + ' ~ ' + domainRange[1][1])
                        return
                elif self.cutDict[planename]['axis'] == 'z':
                    if float(what) < float(domainRange[0][2]) or float(what) > float(domainRange[1][2]):
                        self.GEN.makeDialog('Out of range!!! \n\n domain range of z : ' + domainRange[0][2] + ' ~ ' + domainRange[1][2])
                        return
                            
                self.cutDict[planename]['value'] = what

        self.GEN.pickleDump(self.setFile, self.cutDict)              
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what):
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)
        old = self.treestore_common[path][2]
        
        if old == what:
            return         
        
        if value0 == 'Scalar':
            self.cutDict['scalar'] = what
            if self.allActors:
                self.showCut(None, self.scalarOrVector)
        elif value0 == 'Time':
            self.cutDict['time'] = what
            if self.allActors:
                self.changeTime()
        elif value0 == 'Colormap':
            self.cutDict['colormap'] = what       
            if self.allActors:
                self.changeColormap()
        elif value0 == 'Vector scale':
            if self.GEN.checkNumber(value0, what):
                self.cutDict['scaleFactor'] = what            
                if self.allActors:
                    self.changeVectorScale()
        elif value0 == 'Data type':
            self.cutDict['dataType'] = what
            if self.allActors:
                self.changeDataType()
        
        self.treestore_common[path][2] = what
        self.GEN.pickleDump(self.setFile,self.cutDict)
    #---------------------------------------------------------------------------------------------    
    def func(self, column, cell, model, iter):
        what = model.get_value(iter, 1)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)
        
        if what == 'Planes to display' or what[:6] == 'plane-':
            self.ren1.set_property('visible', 0)
        elif what == 'Axis':
            self.ren1.set_property('visible', 1)
            self.ren1.set_property('model', dic['axis'])
            self.ren1.set_property('has-entry', False)
            planename = self.planeList[int(path[1])]
            self.ren1.set_property('text', self.cutDict[planename]['axis'])
        elif what == 'Value':
            self.ren1.set_property('visible', 1)
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            planename = self.planeList[int(path[1])]
            self.ren1.set_property('text', self.cutDict[planename]['value'])          
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model, iter):
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)        
        combo=['Scalar', 'Time', 'Colormap', 'Data type']

        if what in combo:
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)            
            self.ren2_common.set_property('has-entry', False)
            if what == 'Scalar':
                self.ren2_common.set_property('model', dic['scalars'])
                self.ren2_common.set_property('text', self.cutDict['scalar'])
            elif what == 'Time':
                self.ren2_common.set_property('model', dic['times'])
                self.ren2_common.set_property('text', self.cutDict['time'])
            elif what == 'Colormap':
                self.ren2_common.set_property('model', dic['colormap'])
                self.ren2_common.set_property('text', self.cutDict['colormap'])
            elif what == 'Data type':
                self.ren2_common.set_property('model', dic['dataType'])
                self.ren2_common.set_property('text', self.cutDict['dataType'])
        elif what == 'Vector scale':
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)
            self.ren2_common.set_property('model', None)
            self.ren2_common.set_property('has-entry', True)
            self.ren2_common.set_property('text', self.cutDict['scaleFactor'])
        elif what == 'Overlay':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0) 
    #---------------------------------------------------------------------------------------------    
    def liststore_post(self, scalars, times):

        colormap = ['blue to red', 'cool to warm', 'high_contrast', 'hot_to_cold', 'leaf_color', 'small_difference',
                    'hot', 'indigo_flame', 'land_color', 'spectrum_white']                      
        colorby = ['U', 'Scalar']
        axis = ['x', 'y', 'z']        

        liststore_scalars = gtk.ListStore(str)
        for ii in scalars:
            liststore_scalars.append([ii])
        
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
        
        liststore_dataType = gtk.ListStore(str)
        liststore_dataType.append(['point value'])
        liststore_dataType.append(['cell value'])
        
        storeDict = {}
        keys = ['scalars', 'times', 'colormap', 'colorby', 'axis', 'yesNo', 'dataType']
        values = [liststore_scalars, liststore_times, liststore_colormap, liststore_colorby, 
                  liststore_axis, liststore_yesNo, liststore_dataType]
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]
        
        return storeDict 
    # -------------------------------------------------------------------------
    def loadCutDict(self):
    
        self.cutDict = self.GEN.pickleLoad(self.setFile)        
        if self.cutDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.cutDict=dicts[5]     
        self.cutDict['displayContour'] = False
        self.cutDict['displayVector'] = False
        self.cutDict['Overlay'] = False
    # ----------------------------------------------------------------------------
    def addPlane(self, widget):
    
        nums = []
        for ii in self.planeList:
            aa = ii.split('-')            
            nums.append(int(aa[1]))
        if nums == []:
            name = 'plane-0'
        else:
            name = 'plane-' + str(max(nums) + 1)
        
        self.planeList.append(name)        
        self.row_name = self.treestore.append(self.row_plane, [self.pixbuf_first, name, None])
        self.row_axis = self.treestore.append(self.row_name, [self.pixbuf_second, 'Axis', None])
        self.row_cut = self.treestore.append(self.row_name, [self.pixbuf_second, 'Value', None])       
                       
        self.cutDict[name] = {}
        self.cutDict[name]['axis'] = 'x'
        self.cutDict[name]['value'] = '0'   
        self.GEN.pickleDump(self.setFile, self.cutDict)
        self.treeview.expand_all()
    #---------------------------------------------------------------------------------------------
    def deletePlane(self, widget):
    
        if self.selectToDel == []:
            self.GEN.makeDialog('Warning!!! Select name to delete')
            return
        else:       
            self.treestore.remove(self.selectToDel[1])
            self.planeList.remove(self.selectToDel[0])               
            if self.selectToDel[0] in self.cutDict.keys():
                del self.cutDict[self.selectToDel[0]]
            else:
                return
        self.treeview.expand_all()
        self.GEN.pickleDump(self.setFile, self.cutDict)
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
        self.cuttingPlanebox.show_all()
    #---------------------------------------------------------------------------------------------------------        
    def showCut(self, widget, oldDisplay):
    
        self.displayMode = self.mainself.displayMode
        POST = postProcessingClass(self)
        self.allActors, self.allCutters, self.allGlyph = POST.showCut(self.cutDict, self.planeList, self.reader, self.displayMode)
                        
        if self.cutDict['scalar'] == 'mesh':
            for ii in self.allActors:
                self.renderer.AddActor(ii[0])
        else:
            self.colorRange = self.fitRange()
            self.setColormap()
            
            self.Widget_ScalarBar = vtk.vtkScalarBarWidget()
            self.Widget_ScalarBar.SetScalarBarActor(self.allActors[0][2])
            self.Widget_ScalarBar.SetInteractor(self.gvtk)
            self.Widget_ScalarBar.GetRepresentation().SetPosition( 0.85, 0.46 )
            self.Widget_ScalarBar.GetRepresentation().SetPosition2( 0.08, 0.484 )           
            self.Widget_ScalarBar.On()
                
            if oldDisplay == 'contour':
                self.scalarOrVector = 'contour'                
                for ii in self.allActors:
                    self.renderer.AddActor(ii[0])
            elif oldDisplay == 'vector':
                self.scalarOrVector = 'vector'
                for ii in self.allActors:
                    self.renderer.AddActor(ii[1])

            for ii in self.allActors:
                if self.scalarOrVector == 'contour':
                    ii[0].GetMapper().SetLookupTable(self.colorFunction)
                    ii[0].GetMapper().SelectColorArray(self.cutDict['scalar'])
                else:
                    ii[1].GetMapper().SetLookupTable(self.colorFunction)
                    ii[1].GetMapper().SelectColorArray(self.cutDict['scalar'])

        for ii in self.vtkFeatureActors:
            self.renderer.AddActor(ii)
                
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------        
    def setColormap(self):
    
        scalarbar = self.allActors[0][2]
        scalarbar.SetTitle("%-7s"%self.cutDict['scalar'])
             
        self.colorFunction = scalarbar.GetLookupTable()
        self.colorFunction.RemoveAllPoints()

        if self.cutDict['colormap'] == 'blue to red':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.0, 0.0, 1.0)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 1.0, 0.0, 0.0)
            self.colorFunction.SetColorSpaceToHSV()
            self.colorFunction.HSVWrapOff()
        elif self.cutDict['colormap'] == 'cool to warm':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            self.colorFunction.SetColorSpaceToDiverging()           
        else:
            num = self.colormapDict[self.cutDict['colormap']][0]
            data = self.colormapDict[self.cutDict['colormap']][1]
            delta = self.colorRange[1]-self.colorRange[0]
            for i in range(num):
                self.colorFunction.AddRGBPoint(self.colorRange[0] + delta * (i) / (num - 1), data[i][0], data[i][1], data[i][2])
    #---------------------------------------------------------------------------------------------------------        
    def changeColormap(self):
    
        self.setColormap() 
        for ii in self.allActors:
            if self.scalarOrVector == 'contour':
                ii[0].GetMapper().SetLookupTable(self.colorFunction)
            else:
                ii[1].GetMapper().SetLookupTable(self.colorFunction)
        self.gvtk.Initialize()     
    #---------------------------------------------------------------------------------------------------------        
    def fitRange(self):
    
        mins = []
        maxs = []
        for ii in self.allCutters:
            if self.cutDict['dataType'] == 'cell value':
                drange = ii.GetOutput().GetCellData().GetArray(self.cutDict['scalar']).GetRange()
            else:
                drange = ii.GetOutput().GetPointData().GetArray(self.cutDict['scalar']).GetRange()
            mins.append(drange[0])
            maxs.append(drange[1])
        colorRange = [min(mins),max(maxs)]
        return colorRange            
    #---------------------------------------------------------------------------------------------------------        
    def changeTime(self):
                          
        plottime = float(self.cutDict['time'])
        self.reader.GetExecutive().SetUpdateTimeStep(0, plottime)
        self.reader.Modified()
        self.reader.Update()    
        self.gvtk.Initialize()             
    #---------------------------------------------------------------------------------------------------------        
    def changeVectorScale(self):
    
        for i in range(len(self.allActors)):
            if self.scalarOrVector == 'vector':
                self.allGlyph[i].SetScaleFactor(float(self.cutDict['scaleFactor']))	
        self.gvtk.Initialize()             
    #----------------------------------------------------------------------------------------------------
    def changeDataType(self):
    
        self.showCut(None, self.scalarOrVector)    
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


            
            
                    
