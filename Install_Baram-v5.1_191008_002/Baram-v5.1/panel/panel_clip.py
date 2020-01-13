#-*-coding:utf8-*-

from common.fromAll     import *

class freepanelClipClass:
                
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
        
        self.allActors = None
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')         
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png') 
    #------------------------------------------------------------------------------------------
    def clip(self):
        
        self.getPostReader()                
        self.colormapDict = self.colormapData()

        self.clipbox = gtk.VBox()          

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.clipbox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Clip  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox) 
                
        self.vpan = gtk.VPaned()
        self.clipbox.pack_start(self.vpan, True, True, 0)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(400, 100)
        swin1=gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin1.set_size_request(400, 70)

        self.vpan.pack2(swin1, False, True)

        ebox1 = gtk.EventBox()
        ebox1.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        swin1.add_with_viewport(ebox1)

        self.valuebox = gtk.VBox(False, 0)
        ebox1.add(self.valuebox)

        self.setFile = self.caseDir + '/system/settings/clipSet'
        self.loadClipDict()
        
        self.getTimeList()
        self.getArrayName()        

        # treeview common---------------------------------------------------------------
        self.treestore_common = gtk.TreeStore(str, bool, str)        
        self.treestore_common.append(None, ['Clip by', None, None])
        self.treestore_common.append(None, ['Value', None, None])
        self.treestore_common.append(None, ['Scalar', None, None])
        self.treestore_common.append(None, ['Time', None, None])
        self.treestore_common.append(None, ['Colormap', None, None])        
        self.treestore_common.append(None, ['Inside Out', False, None])
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
        
        field = self.clipDict['clipBy']
        text='  Range of ' + field + ' : ' + str(self.fullRange[field][0]) + ' ~ ' + str(self.fullRange[field][1])
        
        self.rangeLabel.set_text(text)
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 15)
        hbox.pack_start(self.rangeLabel, False, False, 0)
        
        contourB = gtk.Button('Display Clip')
        contourB.set_size_request(150, 28)
        contourB.connect('clicked', self.showClip)
        hbox = gtk.HBox(False,0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(contourB, True, True, 0)

        return self.clipbox 
    #--------------------------------------------------------   
    def togglePost(self, widget, path, model):
    
        model[path][1] = not model[path][1]        
        value0 = model[path][0]

        try:
            self.clippers
            for ii in self.clippers:
                ii.SetInsideOut(model[path][1])
        except:
            pass
                    
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------        
    def changeValue_common(self, widget, path, what):
    
        treeiter = self.treestore_common.get_iter(path)
        value0 = self.treestore_common.get_value(treeiter, 0)
        old = self.treestore_common[path][2]
        
        if old == what:
            return

        if value0 == 'Clip by':
            self.clipDict['clipBy'] = what
            text='  Range of ' + what + ' : ' + str(self.fullRange[what][0]) + ' ~ ' + str(self.fullRange[what][1])
            self.rangeLabel.set_text(text)            

        elif value0 == 'Value':
            if self.GEN.checkNumber(value0, what):
                self.clipDict['value'] = what
                if self.allActors:
                    self.showClip(None)
                
        elif value0 == 'Scalar':
            self.clipDict['scalar'] = what
            if self.allActors:
                self.showClip(None)
        
        elif value0 == 'Time':
            self.clipDict['time'] = what
            if self.allActors:
                self.changeTime()            
            self.getArrayName()
            text='  Range of ' + self.clipDict['clipBy'] + ' : ' + str(self.fullRange[self.clipDict['clipBy']][0]) + ' ~ ' + str(self.fullRange[self.clipDict['clipBy']][1])
            self.rangeLabel.set_text(text)
        
        elif value0 == 'Colormap':
            self.clipDict['colormap'] = what       
            if self.allActors:
                self.changeColormap()

        self.treestore_common[path][2] = what
        self.GEN.pickleDump(self.setFile, self.clipDict)
    #---------------------------------------------------------------------------------------------    
    def func_common(self, column, cell, model,iter):
    
        what = model.get_value(iter, 0)
        path = model.get_path(iter)        

        dic = self.liststore_post(self.scalars, self.times)        
        combo = ['Clip by', 'Scalar', 'Time', 'Colormap']
        
        if what in combo:
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)            
            self.ren2_common.set_property('has-entry', False)
            if what == 'Clip by':            
                self.ren2_common.set_property('model',dic['clipBys'])
                self.ren2_common.set_property('text', self.clipDict['clipBy'])
            elif what == 'Scalar':
                self.ren2_common.set_property('model',dic['scalars'])
                self.ren2_common.set_property('text', self.clipDict['scalar'])
            elif what == 'Time':
                self.ren2_common.set_property('model',dic['times'])
                self.ren2_common.set_property('text', self.clipDict['time'])
            elif what == 'Colormap':
                self.ren2_common.set_property('model',dic['colormap'])
                self.ren2_common.set_property('text', self.clipDict['colormap'])
        elif what == 'Inside Out':
            self.ren1_common.set_property('visible', 1)
            self.ren2_common.set_property('visible', 0)
        elif what == 'Value':
            self.ren1_common.set_property('visible', 0)
            self.ren2_common.set_property('visible', 1)
            self.ren2_common.set_property('has-entry', True)
            self.ren2_common.set_property('text', self.clipDict['value'])
    #---------------------------------------------------------------------------------------------    
    def liststore_post(self, scalars, times):

        colormap = ['blue to red', 'cool to warm', 'high_contrast', 'hot_to_cold', 'leaf_color',
                    'small_difference', 'hot', 'indigo_flame', 'land_color', 'spectrum_white']                      

        clipBy = []
        for ii in scalars:
            clipBy.append(ii)

        liststore_clipBys = gtk.ListStore(str)
        for ii in scalars:
            liststore_clipBys.append([ii])
            
        liststore_scalars = gtk.ListStore(str)
        for ii in scalars:
            if ii != 'coordsX' and ii != 'coordsY' and ii != 'coordsZ': 
                liststore_scalars.append([ii])
        
        liststore_times = gtk.ListStore(str)
        for ii in times:
            liststore_times.append([ii])
        
        liststore_colormap = gtk.ListStore(str)
        for ii in colormap:
            liststore_colormap.append([ii])
       
        liststore_clipBy = gtk.ListStore(str)
        for ii in clipBy:
            liststore_clipBy.append([ii])
        
        liststore_yesNo = gtk.ListStore(str)
        liststore_yesNo.append(['yes'])
        liststore_yesNo.append(['no'])
        
        liststore_dataType = gtk.ListStore(str)
        liststore_dataType.append(['point value'])
        liststore_dataType.append(['cell value'])
        
        storeDict = {}
        keys = ['clipBys','scalars', 'times', 'colormap', 'clipBy', 'yesNo']
        values = [liststore_clipBys, liststore_scalars, liststore_times, liststore_colormap,
                  liststore_clipBy, liststore_yesNo]
        
        for i in range(len(keys)):
            storeDict[keys[i]] = values[i]
        
        return storeDict 
    # -------------------------------------------------------------------------
    def loadClipDict(self):
        
        self.clipDict = self.GEN.pickleLoad(self.setFile)        
        if self.clipDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.clipDict = dicts[7]     
    #---------------------------------------------------------------------------------------------------------        
    def showClip(self, widget):
    
        self.displayMode = self.mainself.displayMode
        POST = postProcessingClass(self)
        
        num = self.renderer.GetActors().GetNumberOfItems()
        bcNameList, bcTypelist = self.GEN.getBCName()

        self.allActors, self.clippers = POST.showClip(self.clipDict, self.reader, self.displayMode)
           
        self.renderer.RemoveAllViewProps()

        for ii in self.allActors[0]:
            self.renderer.AddActor(ii)

        if num != len(bcNameList):
            self.Widget_ScalarBar = vtk.vtkScalarBarWidget()
            self.Widget_ScalarBar.SetScalarBarActor(self.allActors[1])
            self.Widget_ScalarBar.SetInteractor(self.gvtk)
            self.Widget_ScalarBar.GetRepresentation().SetPosition( 0.85, 0.46 )
            self.Widget_ScalarBar.GetRepresentation().SetPosition2( 0.08, 0.484 )
            self.Widget_ScalarBar.On()   

            self.fitRange()
            self.setColormap()
        
            self.allActors[0][0].GetMapper().SetLookupTable(self.colorFunction)
            self.allActors[0][0].GetMapper().SelectColorArray(self.clipDict['scalar'])
            self.allActors[0][0].GetProperty().EdgeVisibilityOff()            
          
        self.gvtk.Initialize()                  
    #---------------------------------------------------------------------------------------------------------        
    def setColormap(self):
    
        scalarbar = self.allActors[1]        
        self.colorFunction = scalarbar.GetLookupTable()
        self.colorFunction.RemoveAllPoints()

        if self.clipDict['colormap'] == 'blue to red':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.0, 0.0, 1.0)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 1.0, 0.0, 0.0)
            self.colorFunction.SetColorSpaceToHSV()
            self.colorFunction.HSVWrapOff()
        elif self.clipDict['colormap'] == 'cool to warm':
            self.colorFunction.AddRGBPoint(self.colorRange[0], 0.23137254902, 0.298039215686, 0.752941176471)
            self.colorFunction.AddRGBPoint(self.colorRange[1], 0.705882352941, 0.0156862745098, 0.149019607843)
            self.colorFunction.SetColorSpaceToDiverging()           
        else:
            num = self.colormapDict[self.clipDict['colormap']][0]
            data = self.colormapDict[self.clipDict['colormap']][1]
            delta = self.colorRange[1] - self.colorRange[0]
            for i in range(num - 1):
                self.colorFunction.AddRGBPoint(self.colorRange[0] + delta*(i) / num, data[i][0], data[i][1], data[i][2])

        scalarbar.SetTitle("%-7s"%self.clipDict['scalar'])
        
    #---------------------------------------------------------------------------------------------------------        
    def changeColormap(self):
    
        self.setColormap()         
        self.allActors[0][0].GetMapper().SetLookupTable(self.colorFunction)
        self.gvtk.Initialize()     
    #---------------------------------------------------------------------------------------------------------        
    def fitRange(self): # this is global range. how to fit range???

        scalar = self.clipDict['scalar']

        rangeList = []
        for ii in self.clippers:
            if scalar == 'coordsX':
                rangeList.append(ii.GetInput().GetPoints().GetData().GetRange(0))
            elif scalar == 'coordsY':
                rangeList.append(ii.GetInput().GetPoints().GetData().GetRange(1))
            elif scalar == 'coordsZ':
                rangeList.append(ii.GetInput().GetPoints().GetData().GetRange(2))
            else:           
                rangeList.append(ii.GetInput().GetPointData().GetArray(self.clipDict['scalar']).GetRange())
        
        mins = []
        maxs = []
        for ii in rangeList:
            mins.append(ii[0])
            maxs.append(ii[1])
            
        self.colorRange = [min(mins), max(maxs)]
    #---------------------------------------------------------------------------------------------------------        
    def changeTime(self):
                          
        plottime = float(self.clipDict['time'])
        self.reader.GetExecutive().SetUpdateTimeStep(0, plottime)
        self.reader.Modified()
        self.reader.Update()    
        self.gvtk.Initialize()             
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

        self.clipDict['time'] = str(max(self.times))
    #---------------------------------------------------------------------------------------------------------                            
    def getArrayName(self):
    
        if glob.glob(self.caseDir + '/constant/polyMesh') == []:
            self.scalars = []
            return
        
        self.reader.GetExecutive().SetUpdateTimeStep(0, float(self.clipDict['time']))
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

            
            
                    
