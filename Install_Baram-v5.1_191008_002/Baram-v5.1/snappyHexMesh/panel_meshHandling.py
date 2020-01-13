#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelMeshSnappyClass:

    def __init__(self, mainself):

        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.renderer = mainself.renderer
        self.VTK_All = VTKStuff(mainself.caseDir)        
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.displayOptCombo = mainself.displayOptCombo
        
        self.GEN = generalClass(mainself)
        
    def mesh(self):
    
        self.meshbox = gtk.VBox(False, 5)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                
        label = gtk.Label()
        label.set_markup('<b>  Mesh Manipulation  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.meshbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)
        # --- display boundary -----------------------------------------
        label = gtk.Label('Display patch')
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        self.viewbox = gtk.VBox(False, 5)
        self.meshbox.pack_start(self.viewbox, False, False, 5)
        
        self.scwin = gtk.ScrolledWindow()
        self.scwin.set_border_width(0)
        self.scwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scwin.set_size_request(250, 300)
        self.smbox = gtk.VBox(False, 0)
        self.bdbox = gtk.HBox(False, 5)

        self.viewbox.pack_start(self.smbox, True, True, 0)
        self.smbox.pack_start(self.scwin, True, True, 0)
        self.scwin.add_with_viewport(self.bdbox)    

        self.displaybutton = gtk.Button('Display')
        self.displaybutton.connect('clicked', self.showpatch)
        self.displaybutton.set_size_request(120, 28)
        hbox = gtk.HBox(False, 5)
        self.viewbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.displaybutton, True, True, 5)
        
        self.patchzone = self.viewbc(self.bdbox)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.meshbox.pack_start(separator, False, True, 2)
        #--------------------------------------------------
        label = gtk.Label('Display cut plane')
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('Axis normal')
        self.axisCombo=gtk.combo_box_entry_new_text()
        self.axisCombo.set_size_request(120, 28)
        self.axisList = ['x', 'y', 'z']
        for jj in self.axisList:
            self.axisCombo.append_text(jj)
        self.axisCombo.set_active(0)
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 2)
        hbox.pack_end(self.axisCombo, False, False, 5)
        hbox.pack_end(label, False, False, 5)    
        
        label = gtk.Label('value')
        self.vEntry=gtk.Entry()
        self.vEntry.set_size_request(120, 28)
        self.vEntry.set_text('0')
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 2)
        hbox.pack_end(self.vEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)
        
        self.cutbutton = gtk.Button(label='Display')
        self.cutbutton.connect('clicked', self.showcut)
        self.cutbutton.set_size_request(120, 28)
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.cutbutton, True, True,  5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.meshbox.pack_start(separator, False, True, 2)
        #--------------------------------------------------
        label = gtk.Label('Mesh manipulate')
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)              
        
        self.checkB = gtk.Button('Check mesh')
        self.checkB.connect('clicked', self.checkMesh)
        self.checkB.set_size_request(120, 28)
        self.scaleB = gtk.Button('Scale mesh')
        self.scaleB.connect('clicked', self.scaleMesh)
        self.scaleB.set_size_request(120, 28)
        self.transB = gtk.Button('Translate mesh')
        self.transB.connect('clicked', self.translateMesh)
        self.transB.set_size_request(120, 28)
        self.patchB = gtk.Button('Split boundary')
        self.patchB.connect('clicked', self.autoPatch)
        self.patchB.set_size_request(120, 28)
        self.topoB = gtk.Button('Create cellSet')
        self.topoB.connect('clicked', self.topoSet)
        self.topoB.set_size_request(120, 28)
        self.refineB = gtk.Button('Refine mesh')
        self.refineB.connect('clicked', self.refineMesh)
        self.refineB.set_size_request(120, 28)
        
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.checkB, True, True,  5)
        hbox.pack_end(self.patchB, True, True,  5)
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.scaleB, True, True,  5)
        hbox.pack_end(self.transB, True, True,  5)
        hbox = gtk.HBox(False, 5)
        self.meshbox.pack_start(hbox, False, False, 2)
        hbox.pack_start(self.topoB, True, True,  5)
        hbox.pack_end(self.refineB, True, True,  5)

        return self.meshbox
    #---------------------------------------------------------------------------------------------------------
    def showpatch(self, widget):
        
        cellzones = self.GEN.getCellZones()
        patchnzone = self.bcname + cellzones 
        
        viewposition = [1, 1, 1]
        self.renderer.RemoveAllViewProps()
        actor = self.VTK_All.showMeshSnappy(patchnzone, self.onOff, viewposition, self.displayOptCombo.child.get_text())
        self.renderer.AddActor(actor)
        self.gvtk.Initialize()
        
        self.notebook.set_current_page(0)
    #---------------------------------------------------------------------------------------------------------                    
    def showcut(self, widget):

        ax = self.axisCombo.child.get_text()
        vv = self.vEntry.get_text()
        
        if ax == 'x':
            originlist = [vv,0,0];normallist = [1,0,0]                
        elif ax == 'y':
            originlist = [0,vv,0];normallist = [0,1,0]
        elif ax == 'z':
            originlist = [0,0,vv];normallist = [0,0,1]
                
        caseType = 1

        viewposition = [1, 1, 1]
        self.renderer.RemoveAllViewProps()
        outlineActor, actor = self.VTK_All.cutPlaneSnappy(normallist, originlist, caseType, 'latestTime',
                                viewposition, self.displayOptCombo.child.get_text())
        self.renderer.AddActor(outlineActor)
        self.renderer.AddActor(actor)
        self.gvtk.Initialize()

        self.notebook.set_current_page(0)
    #---------------------------------------------------------------------------------------------------------                    
    def viewbc(self, bdbox):       
   
        if glob.glob(self.caseDir+'/constant/polyMesh/boundary'):        
            self.bcname, bctype = self.GEN.getBCName()
            cellzones = self.GEN.getCellZones()
            patchzone = self.bcname + cellzones
            
            for ii in bdbox.get_children():
                bdbox.remove(ii)
            
            def get_model(tree_store):
                if tree_store:
                    return tree_store 
                else:
                    return None
                                    
            def col1_toggled_cb(cell, path, model):
                model[path][1] = not model[path][1]
                for i in range(len(patchzone)):
                    if model[path][0] == patchzone[i]:
                        if model[path][1] == True:
                            self.onOff[i] = 1
                        else:
                            self.onOff[i] = 0
            
            def changeValue(widget, path, text, model):
                old = model[path][0]
                model[path][0] = text
                self.changeName(patchzone, old, text, bdbox)
                                    
            def make_view(model):
                view = gtk.TreeView(model)
                renderer = gtk.CellRendererText()
                renderer.set_property("editable", True)
                renderer.connect('edited', changeValue, model)                
                renderer1 = gtk.CellRendererToggle()
                renderer1.set_property('activatable', True)
                renderer1.connect('toggled', col1_toggled_cb, model)

                column0 = gtk.TreeViewColumn("Boundary Name", renderer, text = 0)
                column1 = gtk.TreeViewColumn("          Display", renderer1 )
                column1.add_attribute(renderer1, "active", 1)
                view.append_column(column0)
                view.append_column(column1)
                return view

            self.onOff = []
            for i in range(len(patchzone)):
                self.onOff.append(0)            
            tree_store = gtk.TreeStore(str, bool)
            for item in patchzone:
                parent = tree_store.append(None, (item, None))
            mdl = get_model(tree_store)
            view = make_view(mdl)        
            
            bdbox.pack_start(view, True, True, 5)
            
            self.meshbox.show_all()

        else:
            patchzone = 'none'  
            
        return patchzone 
    #---------------------------------------------------------------------------------------------------------            
    def changeName(self, patchzone, oldname, newname, bdbox):
    
        WFILE = writeFileClassSnappy(self.caseDir)
        
        bcnames, bctypes = self.GEN.getBCName()
        ind = bcnames.index(oldname)
        patchtype = bctypes[ind]       

        WFILE.createPatch(oldname, newname, patchtype)
        
        os.system('createPatch -overwrite -case ' + self.caseDir)
        
        for i in range(len(self.bcname)):
            if self.bcname[i] == oldname:
                self.bcname[i] = newname
            
        self.viewbc(bdbox)
    #---------------------------------------------------------------------------------------------------------            
    def scaleMesh(self, widget):       
   
        def closethis(widget):            
            window.destroy()

        def applythis(widget):
            xscale = scalex.get_text()
            yscale = scaley.get_text()
            zscale = scalez.get_text()
            
            if self.GEN.isNumber(xscale) == False:
                self.GEN.makeDialog('Error!!! x-scale is not number')
                return
            if self.GEN.isNumber(yscale) == False:
                self.GEN.makeDialog('Error!!! y-scale is not number')
                return
            if self.GEN.isNumber(zscale) == False:
                self.GEN.makeDialog('Error!!! z-scale is not number') 
                return

            f = open(self.caseDir + '/system/settings/runscalemesh', 'w')
            f.write("transformPoints -case " + self.caseDir + " -scale '(" + xscale + ' ' + yscale + ' ' + zscale + ")'" + '\n')
            f.write('foamToVTK  -noInternal -noFaceZones -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.foamToVTK' + '\n')
            f.close()
            os.system('chmod +x ' + self.caseDir + '/system/settings/runscalemesh')
            cmd = self.caseDir+'/system/settings/runscalemesh\n'
            self.terminal.feed_child(cmd,len(cmd))
                        
            window.destroy()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Scale mesh')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        label = gtk.Label('Set scale factor for x,y,z')
        labelbox = gtk.HBox(False, 5)
        vbox.pack_start(labelbox, False, False, 5)
        labelbox.pack_start(label, False, False, 5)

        scalex = gtk.Entry()
        scalex.set_size_request(80, 28)
        scalex.set_text('0.001')
        scaley = gtk.Entry()
        scaley.set_size_request(80, 28)
        scaley.set_text('0.001')
        scalez = gtk.Entry()
        scalez.set_size_request(80, 28)
        scalez.set_text('0.001')
        scalebox = gtk.HBox(False, 5)
        vbox.pack_start(scalebox, False, False, 5)
        scalebox.pack_start(scalex, False, False, 5)
        scalebox.pack_start(scaley, False, False, 5)
        scalebox.pack_start(scalez, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        vbox.pack_start(separator, False, True, 2)
        
        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', applythis)
        clsB.connect('clicked', closethis)
        appB.set_size_request(100,28)
        clsB.set_size_request(100,28)
        bubox = gtk.HBox(False, 5)
        vbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        window.show_all()       
    #---------------------------------------------------------------------------------------------------------            
    def translateMesh(self, widget):

        def closethis(widget):
            window.destroy()

        def applythis(widget):
            xscale = scalex.get_text()
            yscale = scaley.get_text()
            zscale = scalez.get_text()
            
            if self.GEN.isNumber(xscale) == False:
                self.GEN.makeDialog('Error!!! vector-x is not number')
                return
            if self.GEN.isNumber(yscale) == False:
                self.GEN.makeDialog('Error!!! vector-y is not number')
                return
            if self.GEN.isNumber(zscale) == False:
                self.GEN.makeDialog('Error!!! vector-z is not number') 
                return

            f = open(self.caseDir + '/system/settings/runtranslatemesh', 'w')
            f.write("transformPoints -case " + self.caseDir + " -translate '(" + xscale + ' ' + yscale + ' ' + zscale + ")'" + '\n')
            f.write('foamToVTK -noInternal -noFaceZones -case '+ self.caseDir + ' > ' + self.caseDir + '/logfiles/logfiles/log.foamToVTK' + '\n')
            f.close()
            os.system('chmod +x ' + self.caseDir +'/system/settings/runtranslatemesh')
            cmd = self.caseDir + '/system/settings/runtranslatemesh\n'
            self.terminal.feed_child(cmd,len(cmd))
                                        
            window.destroy()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Translate mesh')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        label = gtk.Label('Set vector for x,y,z [m]')
        labelbox = gtk.HBox(False, 5)
        vbox.pack_start(labelbox, False, False, 5)
        labelbox.pack_start(label, False, False, 5)

        scalex = gtk.Entry()
        scalex.set_size_request(80, 28)
        scalex.set_text('1')
        scaley = gtk.Entry()
        scaley.set_size_request(80, 28)
        scaley.set_text('0')
        scalez = gtk.Entry()
        scalez.set_size_request(80, 28)
        scalez.set_text('0')
        scalebox = gtk.HBox(False, 5)
        vbox.pack_start(scalebox, False, False, 5)
        scalebox.pack_start(scalex, False, False, 5)
        scalebox.pack_start(scaley, False, False, 5)
        scalebox.pack_start(scalez, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        vbox.pack_start(separator, False, True, 2)
        
        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', applythis)
        clsB.connect('clicked', closethis)
        appB.set_size_request(100, 28)
        clsB.set_size_request(100, 28)
        bubox = gtk.HBox(False, 5)
        vbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        window.show_all()
    #---------------------------------------------------------------------------------------------------------                            
    def checkMesh(self, widget):
    
        cmd = 'checkMesh -case ' + self.caseDir + '\n'
        self.terminal.feed_child(cmd,len(cmd))
        self.notebook.set_current_page(1)
            
        az = self.caseDir + '/constant/polyMesh/boundary'
        with open(az, 'r') as filea:
            lines = filea.readlines()
        line1 = []  
        for i in range(16, len(lines)):
            a = (lines[i]).strip()
            if a == '{':
                line1.append(i)
        for i in line1:
            bb = (lines[i - 1]).strip()
            b = bb[0]
            if self.GEN.isNumber(b):
                self.GEN.makeDialoge('Warning!!! Some patch name begin with number\n It might have some problem')           
    #---------------------------------------------------------------------------------------------------------            
    def autoPatch(self, widget):
    
        def closethis(widget):            
            window.destroy()
            os.system('rm -r ' + self.caseDir + '/1')

        def applythis(widget):
        
            aa = self.GEN.getResult()
            res = aa[0]
            for ii in res:
                os.system('rm -r ' + self.caseDir + '/' + ii)
            
            angle = angleEntry.get_text()
            if self.GEN.isNumber(angle) == False:
                self.GEN.makeDialog('Error!!! Feature angle is not number')
                return
            
            WFILE.creatPatchNone()

            os.system('autoPatch -overwrite -case ' + self.caseDir + ' ' + angle)
            os.system('createPatch -overwrite -case ' + self.caseDir)

            self.patchzone = self.viewbc(self.bdbox)
                        
            window.destroy()
                
        def testrun(widget):
            WFILE.creatPatchNone()
            
            angle = angleEntry.get_text()
            aa = self.GEN.getResult()
            res = aa[0]
            for ii in res:
                os.system('rm -r ' + self.caseDir + '/' + ii)
                
            os.system('autoPatch -case ' + self.caseDir + ' ' + angle)
            os.system('createPatch -overwrite -case ' + self.caseDir)
            self.patchzoneAutoPatch = self.viewbcAutoPatch(bdbox1, window)            
            
        def testdisplay(widget):
            viewposition = [1, 1, 1]
            self.renderer.RemoveAllViewProps()
            actor = self.VTK_All.showMeshAutoPatch(self.patchzoneAutoPatch, self.onOffAutoPatch, viewposition, 'surface')
            self.renderer.AddActor(actor)
            self.gvtk.Initialize()
            
            self.notebook.set_current_page(0)        
            
        WFILE = writeFileClassSnappy(self.caseDir)
        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('autoPatch')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)
        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        label = gtk.Label('Feature angle [deg]')
        angleEntry = gtk.Entry()
        angleEntry.set_size_request(80, 28)
        angleEntry.set_text('60')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(angleEntry, False, False, 5)
           
        viewbox1=gtk.VBox(False, 5)
        vbox.pack_start(viewbox1, False, False, 5)
           
        scwin1 = gtk.ScrolledWindow()
        scwin1.set_border_width(0)
        scwin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scwin1.set_size_request(250, 300)
        smbox1=gtk.VBox(False, 0)
        bdbox1=gtk.HBox(False, 5)

        viewbox1.pack_start(smbox1, True, True, 0)
        smbox1.pack_start(scwin1, True, True, 0)
        scwin1.add_with_viewport(bdbox1) 
         
        testB = gtk.Button('Test')
        testB.set_size_request(120, 28)
        testB.connect('clicked', testrun)            
        testdisbutton = gtk.Button('Display')
        testdisbutton.connect('clicked', testdisplay)
        testdisbutton.set_size_request(120, 28)
        hbox = gtk.HBox(False, 5)
        viewbox1.pack_start(hbox, False, False, 0)
        hbox.pack_end(testdisbutton, False, False, 5)
        hbox.pack_end(testB, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        vbox.pack_start(separator, False, True, 2)
            
        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', applythis)
        clsB.connect('clicked', closethis)
        appB.set_size_request(120, 28)
        clsB.set_size_request(120, 28)
        bubox = gtk.HBox(False, 5)
        vbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        window.show_all()
    #---------------------------------------------------------------------------------------------------------                    
    def viewbcAutoPatch(self, bdbox1, win):    

        def getBCName():
            aa = self.caseDir + '/1/polyMesh/boundary'
            if glob.glob(aa) == []:
                return
            else:
                with open(aa, 'r') as filea:
                    lines = filea.readlines()
                for ii in lines:
	            if ii == '\n':
	                lines.remove(ii)
                line1 = []
                bcname = []
                f = open(aa, 'r')
                for i in range(15, len(lines)):
                    a = (lines[i]).strip()
                    if a == '{':
                        line1.append(i)            
                for i in line1:
                    b = (lines[i - 1]).strip()
                    bcname.append(b)
                return bcname
                           
        if glob.glob(self.caseDir + '/1/polyMesh/boundary'):        
            bcname = getBCName()
            patchzone = bcname
            aa = bdbox1.get_children()
            for ii in aa:
                bdbox1.remove(ii)
            
            def get_model(tree_store):
                if tree_store:
                    return tree_store 
                else:
                    return None                

            def col1_toggled_cb(cell, path, model):
                model[path][1] = not model[path][1]
                for i in range(len(patchzone)):
                    if model[path][0] == patchzone[i]:
                        if model[path][1] == True:
                            self.onOffAutoPatch[i] = 1
                        else:
                            self.onOffAutoPatch[i] = 0
                                    
            def make_view(model):
                view = gtk.TreeView(model)
                renderer = gtk.CellRendererText()
                renderer1 = gtk.CellRendererToggle()
                renderer1.set_property('activatable', True)
                renderer1.connect('toggled', col1_toggled_cb, model)

                column0 = gtk.TreeViewColumn("Boundary Name", renderer, text = 0)
                column1 = gtk.TreeViewColumn("          Display", renderer1)
                column1.add_attribute( renderer1, "active", 1)
                view.append_column(column0)
                view.append_column(column1)
                return view

            self.onOffAutoPatch = []
            for i in range(len(patchzone)):
                self.onOffAutoPatch.append(0)            
            tree_store = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
            for item in patchzone:
                parent = tree_store.append(None, (item, None))
            mdl = get_model(tree_store)
            view = make_view(mdl)        
            
            bdbox1.pack_start(view, True, True, 5)
            
            win.show_all()

        else:
            patchzone = 'none'  
            
        return patchzone
    #---------------------------------------------------------------------------------------------------------            
    def topoSet(self, widget):
        
        WFILE=writeFileClassSnappy(self.caseDir)
    
        def closethis(widget):            
            window.destroy();

        def applythis(widget):
            name = nameEntry.get_text()
            minx = minxEntry.get_text()
            miny = minyEntry.get_text()
            minz = minzEntry.get_text()
            maxx = maxxEntry.get_text()
            maxy = maxyEntry.get_text()
            maxz = maxzEntry.get_text()
            
            if self.GEN.isNumber(minx) == False:
                self.GEN.makeDialog('Error!!! min.x is not number');return
            if self.GEN.isNumber(miny) == False:
                self.GEN.makeDialog('Error!!! min.y is not number');return
            if self.GEN.isNumber(minz) == False:
                self.GEN.makeDialog('Error!!! min.z is not number');return
            if self.GEN.isNumber(maxx) == False:
                self.GEN.makeDialog('Error!!! max.x is not number');return                
            if self.GEN.isNumber(maxy) == False:
                self.GEN.makeDialog('Error!!! max.y is not number');return 
            if self.GEN.isNumber(maxz) == False:
                self.GEN.makeDialog('Error!!! max.z is not number');return 
                                
            topodic = {}
            topodic['name'] = name
            topodic['min'] = [minx, miny, minz]
            topodic['max'] = [maxx, maxy, maxz]
            self.GEN.pickleDump(self.caseDir+'/system/settings/topoSetDictSetup', topodic)
            
            WFILE.topoSetDict(topodic)
            
            time.sleep(0.5)
            
            cmd = 'topoSet -case ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd,len(cmd))
                        
            window.destroy()

        def setSavedValue():
            aa = glob.glob(self.caseDir + '/system/settings/topoSetDictSetup')
            if aa:
                dic = self.GEN.pickleLoad(aa[0])
                nameEntry.set_text(dic['name'])
                minxEntry.set_text(dic['min'][0])
                minyEntry.set_text(dic['min'][1])
                minzEntry.set_text(dic['min'][2])   
                maxxEntry.set_text(dic['max'][0])
                maxyEntry.set_text(dic['max'][1])
                maxzEntry.set_text(dic['max'][2])   
        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('topoSet')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        label = gtk.Label('Create cellSet inside box')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)        
        
        label = gtk.Label('Name')
        nameEntry = gtk.Entry()
        nameEntry.set_size_request(100,28)
        nameEntry.set_text('c0')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(nameEntry, False, False, 5)
        
        label = gtk.Label('Define box with 2 point')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)        
        
        label = gtk.Label('Min. x,y,z')
        minxEntry = gtk.Entry()
        minxEntry.set_size_request(80, 28)
        minxEntry.set_text('0')
        minyEntry = gtk.Entry()
        minyEntry.set_size_request(80, 28)
        minyEntry.set_text('0')
        minzEntry = gtk.Entry()
        minzEntry.set_size_request(80, 28)
        minzEntry.set_text('0')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(minzEntry, False, False, 5)
        hbox.pack_end(minyEntry, False, False, 5)
        hbox.pack_end(minxEntry, False, False, 5)

        label = gtk.Label('Max. x,y,z')        
        maxxEntry = gtk.Entry()
        maxxEntry.set_size_request(80, 28)
        maxxEntry.set_text('1')
        maxyEntry = gtk.Entry()
        maxyEntry.set_size_request(80, 28)
        maxyEntry.set_text('1')
        maxzEntry = gtk.Entry()
        maxzEntry.set_size_request(80, 28)
        maxzEntry.set_text('1')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(maxzEntry, False, False, 5)
        hbox.pack_end(maxyEntry, False, False, 5)
        hbox.pack_end(maxxEntry, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        vbox.pack_start(separator, True, True, 10)

        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', applythis)
        clsB.connect('clicked', closethis)
        appB.set_size_request(100, 28)
        clsB.set_size_request(100, 28)
        bubox = gtk.HBox(False, 5)
        vbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        
        setSavedValue()
                
        window.show_all()             
    #---------------------------------------------------------------------------------------------------------            
    def refineMesh(self, widget):
        
        WFILE=writeFileClassSnappy(self.caseDir)
    
        def closethis(widget):            
            window.destroy()

        def applythis(widget):
            cellset = setCombo.child.get_text()
            if usehexCB.get_active() == 1:
                usehex = 'true'
            else:
                usehex = 'false'
            if geocutCB.get_active() == 1:
                geocut = 'true'
            else:
                geocut = 'false'
            if writemeshCB.get_active() == 1:
                writemesh = 'true'
            else:
                writemesh = 'false'
            
            dic = {}
            dic['cellset'] = cellset
            dic['useHexTopology'] = usehex
            dic['geometricCut'] = geocut
            dic['writeMesh'] = writemesh                                            
            self.GEN.pickleDump(self.caseDir+'/system/settings/refineMeshSetup', dic)
            
            WFILE.refineMeshDict(dic)
            
            time.sleep(0.5)
            
            cmd = 'refineMesh -overwrite -case ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd,len(cmd))
                        
            window.destroy()

        def setSavedValue():
            aa = glob.glob(self.caseDir + '/system/settings/refineMeshSetup')
            if aa:
                dic = self.GEN.pickleLoad(aa[0])
                if dic['cellset'] in sets:
                    setCombo.child.set_text(dic['cellset'])
                if dic['useHexTopology'] == 'true':
                    usehexCB.set_active(1)
                else:
                    usehexCB.set_active(0)
                
                if dic['geometricCut'] == 'true':
                    geocutCB.set_active(1)
                else:
                    geocutCB.set_active(0)
                    
                if dic['writeMesh'] == 'true':
                    writemeshCB.set_active(1)
                else:
                    writemeshCB.set_active(0)                                

        aa = glob.glob(self.caseDir + '/constant/polyMesh/sets/*')
        if aa == []:
            self.GEN.makeDialog('Error!!! There is not cellSets')
            return
        else:
            sets = []
            for ii in aa:
                a1 = ii.split('/')
                sets.append(a1[-1])
        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Refine mesh')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        mainbox.pack_start(frame, False, False, 5)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        label = gtk.Label('Refine mesh using cellSet')
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('cellSet')
        setCombo=gtk.combo_box_entry_new_text()
        setCombo.set_size_request(160,28)
        for ii in sets:
            setCombo.append_text(ii)
        setCombo.set_active(0)                              
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(setCombo, False, False, 5) 
        
        usehexCB = gtk.CheckButton('useHexTopology')
        usehexCB.set_active(0)                              
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(usehexCB, False, False, 5)

        geocutCB = gtk.CheckButton('geometricCut')
        geocutCB.set_active(1)                              
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(geocutCB, False, False, 5)
        
        writemeshCB = gtk.CheckButton('writeMesh')
        writemeshCB.set_active(0)                              
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(writemeshCB, False, False, 5)                        
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        vbox.pack_start(separator, True, True, 10)

        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        appB.connect('clicked', applythis)
        clsB.connect('clicked', closethis)
        appB.set_size_request(100, 28)
        clsB.set_size_request(100, 28)
        bubox = gtk.HBox(False, 5)
        vbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        
        setSavedValue()
        
        window.show_all()                      
