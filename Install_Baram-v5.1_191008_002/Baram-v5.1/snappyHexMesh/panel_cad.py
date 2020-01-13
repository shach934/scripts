#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelCADClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        
        self.renderer = mainself.renderer
        self.VTK_All = VTKStuff(mainself.caseDir)
        self.GEN = generalClass(mainself)
        
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.displayOptCombo = mainself.displayOptCombo
        
        self.selectedPatch = None
        
        self.stlFileSetup = self.caseDir + '/system/settings/stlFileSetup'
        self.stlNameSetup = self.caseDir + '/system/settings/stlNameSetup'
        
    def CAD(self):
    
        self.loadSTLFileDict()
        self.loadSTLNameList()
        self.displaySTL()

        self.cadbox = gtk.VBox(False, 5)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()        
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        
        label = gtk.Label()
        label.set_markup('<b>  Geometry  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.cadbox.pack_start(frame, True, True, 0)
        frame.add(ebox)       
        ebox.add(label)
      
        self.selAddB = gtk.Button('Add STL')
        self.selDelB = gtk.Button('Delete STL')

        self.selAddB.connect('clicked', self.AddSTL)
        self.selDelB.connect('clicked', self.DelSTL)

        hbox = gtk.HBox(False, 5)
        self.cadbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.selAddB, True, True, 5)
        hbox.pack_start(self.selDelB, True, True, 5)
        # --- display boundary -----------------------------------------
        self.viewbox = gtk.VBox(False, 5)
        self.cadbox.pack_start(self.viewbox, False, False, 0)        
        self.scwin = gtk.ScrolledWindow()
        self.scwin.set_border_width(0)
        self.scwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scwin.set_size_request(250, 250)
        self.smbox = gtk.VBox(False, 0)
        self.bdbox = gtk.VBox(False, 0)
        self.viewbox.pack_start(self.smbox, True, True, 0)
        self.smbox.pack_start(self.scwin, True, True, 0)
        self.scwin.add_with_viewport(self.bdbox)
        # --- feature angle --------------------------------------------        
        label = gtk.Label('Feature Angle')
        self.featureAngleEntry = gtk.Entry()
        self.featureAngleEntry.set_text('150')
        self.featureAngleEntry.set_size_request(80,28)
        hbox = gtk.HBox(False, 5)
        self.cadbox.pack_start(hbox, False, False,  5)
        hbox.pack_start(label, False, False,  5)
        hbox.pack_end(self.featureAngleEntry, False, False,  5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.cadbox.pack_start(separator, False, True, 2)
        # --- Domain range ---------------------------------------------
        label = gtk.Label('  Domain Range')
        label.set_alignment(0, 0.5)
        self.cadbox.pack_start(label, False, False, 2)  
        
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(200, 60)
        textview = gtk.TextView()
        self.rangebuffer = textview.get_buffer()
        sw.add(textview)
        hbox = gtk.VBox(False, 5)
        self.cadbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(sw, False, False,  5)
        # --- Create searchableBox --------------------------------------
        label = gtk.Label('  Create searchableBox')
        label.set_alignment(0,0.5)
        self.cadbox.pack_start(label, False, False, 2)       
                
        label = gtk.Label('       Number of Boxes')
        label.set_alignment(0,0.5)
        self.nobjCombo=gtk.combo_box_entry_new_text()
        self.nobjList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  
        for ii in self.nobjList:
            self.nobjCombo.append_text(ii)
        self.nobjCombo.set_active(0)
        self.nobjCombo.set_size_request(80, 28)
        self.nobjCombo.connect('changed', self.changeObjNo)        
        self.nobjCombo.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))        

        hbox = gtk.HBox(False, 5)
        self.cadbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False,  5)
        hbox.pack_end(self.nobjCombo, False, False,  5)

        scwinobj = gtk.ScrolledWindow()
        scwinobj.set_border_width(0)
        scwinobj.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        scwinobj.set_size_request(250, 120)
        hbox = gtk.HBox(False, 5)
        self.cadbox.pack_start(hbox, False, False,  5)
        hbox.pack_start(scwinobj, True, True, 0)

        self.vboxobj = gtk.VBox(False, 0)
        scwinobj.add_with_viewport(self.vboxobj)
        #-------------------------------------------------------------------------        
        self.appB = gtk.Button('Apply')
        self.appB.connect('clicked', self.applythis)
        hbox = gtk.HBox(False, 5)
        self.cadbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.appB, True, True, 5)        

        self.setSavedValue()

        return self.cadbox
    #------------------------------------------------------------------------------------------
    def applythis(self, widget):
    
        featureAng = self.featureAngleEntry.get_text()
        f = open(self.caseDir + '/system/settings/featureAngle', 'w')
        f.write(featureAng)
        f.close() 
        self.GEN.pickleDump(self.stlFileSetup, self.stlFileDict)
    #------------------------------------------------------------
    def setSavedValue(self):
    
        self.showitembox()                
            
        aa = glob.glob(self.caseDir + '/system/settings/objectRefine-*')
        if aa:
            nobj = str(len(aa))
            self.nobjCombo.child.set_text(nobj)
            
        aa = glob.glob(self.caseDir + '/system/settings/featureAngle')
        if aa:
            with open(aa[0], 'r') as f:
                angle = f.read()
            self.featureAngleEntry.set_text(angle)
    #------------------------------------------------------------
    def AddSTL(self, widget):
    
        # Receive File List
        aa = glob.glob(self.caseDir + '/constant/triSurface')
        if aa == []:
            os.system('mkdir ' + self.caseDir + '/constant/triSurface')        
        
        stlfilelist = self.GEN.selSTL()
        for ii in stlfilelist:
            numRegion = self.GEN.findSTLRegion(ii)
            if numRegion > 1:
                regions = self.makeSolidSTLFile(ii)
                for jj in regions:
                    self.stlnames.append(jj)
            elif numRegion == 1:
                aa = ii.split('/')
                nameonly.append(aa[-1][:-4]) 
                os.system('cp ' + ii + ' ' + self.caseDir + '/constant/triSurface/' + nameonly + '.stl')
                self.stlnames.append(nameonly)
            else:
                return
                                            
        for ii in self.stlnames:
            self.stlFileDict[ii] = {'type':'wall', 'mode':'inside', 'level':'1', 'distance':'1e-5'}
        self.GEN.pickleDump(self.stlFileSetup, self.stlFileDict)
        self.GEN.pickleDump(self.stlNameSetup, self.stlnames)
        
        self.showitembox()             
        self.notebook.set_current_page(0)           

        # Model Display        
        selectedstl = []
        for i in range(len(self.stlnames)):
            selectedstl.append(self.caseDir + '/constant/triSurface/' + self.stlnames[i] + '.stl')
                
        self.renderer.RemoveAllViewProps()
        self.actors = self.VTK_All.showSTLMultiForSnappy(selectedstl)
        for ii in self.actors:
            self.renderer.AddActor(ii)
        self.gvtk.Initialize()
        self.resetSize()
        
        aa = glob.glob(self.caseDir + '/system/settings/castellateSetup')
        if aa:
            os.system('rm ' + aa[0])
        
        aa = glob.glob(self.caseDir + '/system/settings/layerSetup')
        if aa:
            os.system('rm ' + aa[0])
    #------------------------------------------------------------
    def DelSTL(self, widget):
    
        os.system('rm ' + self.caseDir + '/constant/triSurface/' + self.selectedPatch + '.stl')
        self.stlnames.remove(self.selectedPatch)
        del self.stlFileDict[self.selectedPatch]
        self.GEN.pickleDump(self.stlFileSetup, self.stlFileDict)
        self.GEN.pickleDump(self.stlNameSetup, self.stlnames)       
        self.showitembox()        
        
        selectedstl = []
        for i in range(len(self.stlnames)):
            selectedstl.append(self.caseDir + '/constant/triSurface/' + self.stlnames[i] + '.stl')
            
        self.renderer.RemoveAllViewProps()
        self.actors = self.VTK_All.showSTLMultiForSnappy(selectedstl)
        for ii in self.actors:
            self.renderer.AddActor(ii)
        self.gvtk.Initialize()
        return
    # ------------------------------------------------------------
    def showitembox(self):
    
        self.liststore_type = gtk.ListStore(str)
        types=['wall', 'patch', 'cellZone', 'baffle']
        for ii in types:
            self.liststore_type.append([ii])
        
        self.liststore_zoneMode = gtk.ListStore(str)
        zoneMode=['inside', 'outside', 'distance']
        for ii in zoneMode:
            self.liststore_zoneMode.append([ii])
        
        self.treestore = gtk.TreeStore(str, str)
        
        self.makeTreeStore()
                    
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect('cursor-changed', self.selected, self.treeview)

        self.tvcolumn0 = gtk.TreeViewColumn('Name         ')
        self.tvcolumn1 = gtk.TreeViewColumn(' Type')
        
        self.treeview.append_column(self.tvcolumn0)
        self.treeview.append_column(self.tvcolumn1)
        
        self.ren0 = gtk.CellRendererText()
        self.ren1 = gtk.CellRendererCombo() 

        self.ren0.set_property('editable', False)
        self.ren1.set_property('editable', True)
        self.ren1.set_property('text-column', 0)
        
        self.tvcolumn0.pack_start(self.ren0, False)
        self.tvcolumn1.pack_start(self.ren1, True) 
        
        self.tvcolumn0.set_attributes(self.ren0, markup = 0)
        
        self.ren1.connect('edited', self.changeType)        
        self.tvcolumn1.set_cell_data_func(self.ren1, self.func1)
        
        self.treeview.expand_all()
        
        aa = self.bdbox.get_children()
        for ii in aa:
            self.bdbox.remove(ii)
        self.bdbox.pack_start(self.treeview, True, True, 0)
        
        self.bdbox.show_all()
    #---------------------------------------------------------------------------------------------    
    def makeTreeStore(self):
    
        self.treestore.clear()
        self.iters = []
        for i in range(len(self.stlnames)):
            self.iters.append(self.treestore.append(None, [self.stlnames[i], 'wall']))                        
            if self.stlFileDict[self.stlnames[i]]['type'] == 'cellZone':
                self.treestore.append(self.iters[i], ['mode', self.stlFileDict[self.stlnames[i]]['mode']])
                self.treestore.append(self.iters[i], ['level', self.stlFileDict[self.stlnames[i]]['level']])
                if self.stlFileDict[self.stlnames[i]]['mode'] == 'distance':
                    self.treestore.append(self.iters[i], ['distance', self.stlFileDict[self.stlnames[i]]['distance']])
    #---------------------------------------------------------------------------------------------    
    def func1(self, column, cell, model, iter):
    
        what = model.get_value(iter, 1)
        path = model.get_path(iter)
        value0 = model.get_value(iter, 0)        
        
        if value0 == 'mode':
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', self.liststore_zoneMode)
            self.ren1.set_property('has-entry', False)
            self.ren1.set_property('text', self.stlFileDict[self.stlnames[path[0]]]['mode'])
        elif value0 == 'level':
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            self.ren1.set_property('text', self.stlFileDict[self.stlnames[path[0]]]['level'])
        elif value0 == 'distance':
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', None)
            self.ren1.set_property('has-entry', True)
            self.ren1.set_property('text', self.stlFileDict[self.stlnames[path[0]]]['distance'])
        else:
            self.ren1.set_property('visible', 1)            
            self.ren1.set_property('model', self.liststore_type)
            self.ren1.set_property('has-entry', False)
            self.ren1.set_property('text', self.stlFileDict[value0]['type'])
    #---------------------------------------------------------------------------------------------
    def changeType(self, widget, path, what):
    
        treeiter = self.treestore.get_iter(path)
        value0 = self.treestore.get_value(treeiter, 0)        
        old = self.treestore[path][1]
        
        if what == old:
            return
        
        if value0 in self.stlnames:
            self.stlFileDict[value0]['type'] = what
        elif value0 == 'mode':
            self.stlFileDict[self.stlnames[int(path[0])]]['mode'] = what                
        elif value0 == 'level':
            self.stlFileDict[self.stlnames[int(path[0])]]['level'] = what
        elif value0 == 'distance':
            self.stlFileDict[self.stlnames[int(path[0])]]['distance'] = what            
        
        self.treestore[path][1] = what          
        self.makeTreeStore()        
        self.treeview.expand_all()        
        self.GEN.pickleDump(self.stlFileSetup, self.stlFileDict) 
    #---------------------------------------------------------------------------------------------------------             
    def selected(self, widget, treeview):
    
        self.selection = treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        path = tree_model.get_path(tree_iter)
        if tree_iter == None:
            return
        if len(path) == 1:
            self.oldpatch = self.selectedPatch
            self.selectedPatch=tree_model.get_value(tree_iter, 0)
            self.highlightColor()
            self.setRange()
    #-----------------------------------------------------------------------------
    def highlightColor(self):   
     
        if self.selectedPatch != None:
            newind=self.stlnames.index(self.selectedPatch)                       
        for i in range(self.renderer.GetActors().GetNumberOfItems()):
            if i == newind:
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetColor(0,0,1)
            else: 
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetColor(1,1,1)          
        self.gvtk.Initialize()  
    #------------------------------------------------------------
    def changeObjNo(self, widget):
    
        def setbox(widget, i):
            self.openObjectWindow(self.boxnameEntry[i].get_text())               
           
        def delbox(widget, i):                                
            delname = self.boxnameEntry[i].get_text()
            aa = glob.glob(self.caseDir + '/system/settings/objectRefine-' + delname)
            if aa != []:
                os.system('rm ' + aa[0])
            
            self.vboxobj.remove(self.objhbox[i])
            
            curno = self.nobjCombo.child.get_text()
            newno = int(curno) - 1
            self.nobjCombo.child.set_text(str(newno))
            self.cadbox.show_all()                
    
        nobj = widget.child.get_text()
                                          
        bb = self.vboxobj.get_children()
        for ii in bb:
            self.vboxobj.remove(ii)
                    
        self.objhbox = []
        self.boxnameEntry = []
        self.boxdelButton = []
        self.boxsetButton = []
        for i in range(int(nobj)):
            self.objhbox.append(gtk.HBox(False, 5))
            self.boxnameEntry.append(gtk.Entry())
            self.boxnameEntry[i].set_text('box' + str(i + 1))
            self.boxdelButton.append(gtk.Button('delete'))
            self.boxdelButton[i].set_size_request(80, 28)
            self.boxdelButton[i].connect('clicked', delbox, i)
            self.boxsetButton.append(gtk.Button('Set'))
            self.boxsetButton[i].set_size_request(80, 28)
            self.boxsetButton[i].connect('clicked', setbox, i)
            self.vboxobj.pack_start(self.objhbox[i], False, False, 0)
            self.objhbox[i].pack_start(self.boxnameEntry[i], True, True, 5)
            self.objhbox[i].pack_end(self.boxdelButton[i], False, False,  5)                                
            self.objhbox[i].pack_end(self.boxsetButton[i], False, False, 0)
            
        aa = glob.glob(self.caseDir + '/system/settings/objectRefine-*')
        for i in range(int(nobj)):
            if i + 1 <= len(aa):
                dic=self.GEN.pickleLoad(aa[i])
                self.boxnameEntry[i].set_text(dic['objectname'])
        
        if int(nobj) < len(aa):
            for i in range(len(aa)):                    
                if i + 1 > int(nobj):
                    os.system('rm ' + aa[i])

        self.cadbox.show_all()
    #---------------------------------------------------------------------------------------------------------                    
    def openObjectWindow(self, objectname):
    
        def applythis(widget):
            objectDict = {}
            objectDict['objectname'] = objectname
            objectDict['minx'] = minxEntry.get_text()
            objectDict['miny'] = minyEntry.get_text()
            objectDict['minz'] = minzEntry.get_text()
            objectDict['maxx'] = maxxEntry.get_text()
            objectDict['maxy'] = maxyEntry.get_text()
            objectDict['maxz'] = maxzEntry.get_text()           
                        
            self.GEN.pickleDump(self.caseDir + '/system/settings/objectRefine-' + objectname, objectDict)
            window.destroy()
            
        def closethis(widget):
            window.destroy()
        
        def displayobj(widget):
            minx = minxEntry.get_text()
            miny = minyEntry.get_text()
            minz = minzEntry.get_text()
            maxx = maxxEntry.get_text()
            maxy = maxyEntry.get_text()
            maxz = maxzEntry.get_text()            
            
            self.notebook.set_current_page(0)
            
            stlfullnames = []
            for ii in self.stlnames:
                stlfullnames.append(self.caseDir + '/constant/triSurface/' + ii + '.stl')
            
            viewposition = [1, 1, 1]
            self.renderer.RemoveAllViewProps()
            actor, stlactors = self.VTK_All.showBox(minx, miny, minz, maxx, maxy, maxz, viewposition, stlfullnames)
            self.renderer.AddActor(actor)
            for ii in stlactors:
                self.renderer.AddActor(ii)
            self.gvtk.Initialize()
            
        def setSavedValue():
            aa = glob.glob(self.caseDir + '/system/settings/objectRefine-' + objectname)
            if aa:
                dic = self.GEN.pickleLoad(self.caseDir + '/system/settings/objectRefine-' + objectname)
                minxEntry.set_text(dic['minx'])
                minyEntry.set_text(dic['miny'])
                minzEntry.set_text(dic['minz'])
                maxxEntry.set_text(dic['maxx'])
                maxyEntry.set_text(dic['maxy'])
                maxzEntry.set_text(dic['maxz'])                
        # -----------------------------------    
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        window.set_title('Object setup window')
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mbox=gtk.VBox(False, 5)
        window.add(mbox)      
    
        label = gtk.Label('Set 2 point of Box')
        label.set_alignment(0, 0.5)
        hbox = gtk.HBox(False, 5)
        mbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False,  5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mbox.pack_start(separator, False, True, 5)                    
                
        label = gtk.Label('Min.')
        label.set_alignment(0, 0.5)
        minxEntry = gtk.Entry()
        minxEntry.set_size_request(60, 28)
        minxEntry.set_text('0') 
        minyEntry = gtk.Entry()
        minyEntry.set_size_request(60, 28)
        minyEntry.set_text('0') 
        minzEntry = gtk.Entry()
        minzEntry.set_size_request(60, 28)
        minzEntry.set_text('0')        
        hbox = gtk.HBox(False, 5)
        mbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False,  5)
        hbox.pack_end(minzEntry, False, False,  5)
        hbox.pack_end(minyEntry, False, False, 0)
        hbox.pack_end(minxEntry, False, False,  5)
                    
        label = gtk.Label('Max.')
        label.set_alignment(0, 0.5)
        maxxEntry = gtk.Entry()
        maxxEntry.set_size_request(60, 28)
        maxxEntry.set_text('0') 
        maxyEntry = gtk.Entry()
        maxyEntry.set_size_request(60, 28)
        maxyEntry.set_text('0') 
        maxzEntry = gtk.Entry()
        maxzEntry.set_size_request(60, 28)
        maxzEntry.set_text('0')
        
        hbox = gtk.HBox(False, 5)
        mbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(label, False, False,  5)
        hbox.pack_end(maxzEntry, False, False,  5)
        hbox.pack_end(maxyEntry, False, False, 0)
        hbox.pack_end(maxxEntry, False, False,  5) 

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mbox.pack_start(separator, False, True, 5)                                
        # -----------------------------------    
        dispB = gtk.Button('Show Box')
        dispB.connect('clicked', displayobj)
        hbox = gtk.HBox(False, 5)
        mbox.pack_start(hbox, False, False, 2)
        hbox.pack_end(dispB, True, True, 0)
        
        applyB = gtk.Button('Apply')
        applyB.connect('clicked', applythis)
        closeB = gtk.Button('Close')
        closeB.connect('clicked', closethis)        
        hbox = gtk.HBox(False, 5)
        mbox.pack_start(hbox, False, False, 2)
        hbox.pack_end(closeB, True, True, 0)
        hbox.pack_end(applyB, True, True, 0)   
        
        setSavedValue()
        
        window.show_all()
    #---------------------------------------------------------------------------------------------------------
    def resetSize(self):
    
        camera = self.renderer.GetActiveCamera()
        self.renderer.SetActiveCamera(camera)
        self.renderer.ResetCamera()
        self.gvtk.Initialize()
        self.mainwindow.show_all()              
    #---------------------------------------------------------------------------------------------------------                    
    def setRange(self):
    
        if glob.glob(self.caseDir + '/constant/triSurface/' + self.selectedPatch + '.stl'):        
            stlrange = self.GEN.getSTLRange(self.caseDir + '/constant/triSurface/' + self.selectedPatch + '.stl')
        else:
            stlrange = self.GEN.getSTLRange(self.caseDir + '/constant/triSurface/' + self.stlnames[i] + '.stl')
        string = '    Range of '+self.selectedPatch
        string = string + '\n        Min. : (' + stlrange[0][0] + ' ' + stlrange[0][1] + ' ' + stlrange[0][2] + ') \n'
        string = string + '        Max. : (' + stlrange[1][0] + ' ' + stlrange[1][1] + ' ' + stlrange[1][2] + ')'
        self.rangebuffer.set_text(string)
    #---------------------------------------------------------------------------------------------------------                    
    def makeSolidSTLFile(self, filename):
    
        with open(filename, 'r') as f:
            ff = f.readlines()
        
        regionnames = []
        startlines = []
        for i in range(len(ff)):
            if ff[i][:5] == 'solid':
                a1 = ff[i].split(' ')
                regionnames.append(a1[1][:-1])
                startlines.append(i + 1)
        nlines = []
        for k in range(len(regionnames) - 1):
            cc = int(startlines[k + 1]) - int(startlines[k])
            nlines.append(cc)
        nlines.append(len(ff) - int(startlines[-1]) + 1)
                                
        for j in range(len(regionnames)):
            g = open(self.caseDir + '/constant/triSurface/' + regionnames[j] + '.stl','w')
            for ii in range(nlines[j]):
                jj = startlines[j] - 1 + ii
                g.write(ff[jj])
            g.close()    
        return regionnames
    #---------------------------------------------------------------------------------------------------------                    
    def loadSTLFileDict(self):
    
        self.stlFileDict = self.GEN.pickleLoad(self.stlFileSetup)        
        if self.stlFileDict == None:
            self.stlFileDict = {}
    #---------------------------------------------------------------------------------------------------------                    
    def loadSTLNameList(self):
    
        self.stlnames = self.GEN.pickleLoad(self.stlNameSetup)        
        if self.stlnames == None:
            self.stlnames = []
    #---------------------------------------------------------------------------------------------------------                    
    def displaySTL(self):
                
        stls = glob.glob(self.caseDir + '/constant/triSurface/*')
        stllist = []
        for ii in stls:
            if ii[-3:].upper() == 'STL':
                stllist.append(ii)
        self.renderer.RemoveAllViewProps()
        self.actors = self.VTK_All.showSTLMultiForSnappy(stllist)
        for ii in self.actors:
            self.renderer.AddActor(ii)
        self.gvtk.Initialize()
        self.resetSize()
        
        self.displayMode = self.displayOptCombo.child.get_text()
        num = self.renderer.GetActors().GetNumberOfItems()                        
        for i in range(num):
            if self.displayMode == 'surfaceEdge':            
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().EdgeVisibilityOn()
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentation(2)
            elif self.displayMode == 'surface':
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().EdgeVisibilityOff()
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentation(2)
            elif self.displayMode == 'wireframe':
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentationToWireframe()
        self.gvtk.Initialize()                    
        
        
