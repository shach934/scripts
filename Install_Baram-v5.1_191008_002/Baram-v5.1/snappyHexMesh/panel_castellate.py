#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelCastellateClass:

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
        
    def castellate(self):

        # entry
        self.maxlocalcellsEntry = gtk.Entry()
        self.maxlocalcellsEntry.set_size_request(80, 28)     
        self.maxglobalcellsEntry = gtk.Entry()
        self.maxglobalcellsEntry.set_size_request(80, 28)  
        self.minrefinecellsEntry = gtk.Entry()
        self.minrefinecellsEntry.set_size_request(80, 28)
        self.maxloadEntry = gtk.Entry()
        self.maxloadEntry.set_size_request(80, 28)
        self.ncellsbetweenEntry = gtk.Entry()
        self.ncellsbetweenEntry.set_size_request(80, 28)
        self.resolvefeatureEntry = gtk.Entry()
        self.resolvefeatureEntry.set_size_request(80, 28)
        self.locxEntry = gtk.Entry()
        self.locxEntry.set_size_request(60, 28)
        self.locyEntry = gtk.Entry()
        self.locyEntry.set_size_request(60, 28)            
        self.loczEntry = gtk.Entry()
        self.loczEntry.set_size_request(60, 28)

        self.entrys = [self.maxlocalcellsEntry, self.maxglobalcellsEntry, self.minrefinecellsEntry, self.maxloadEntry,
                       self.ncellsbetweenEntry, self.resolvefeatureEntry, self.locxEntry, self.locyEntry, self.loczEntry]
        self.entrykeys = ['maxLocalCells', 'maxGlobalCells', 'minRefinementCells', 'maxLoadUnbalance', 'nCellsBetweenLevels',
                          'resolveFeatureAngle', 'locationInMeshx', 'locationInMeshy', 'locationInMeshz']

        # checkbutton
        self.freestandCB = gtk.CheckButton('allowFreeStandingZoneFaces')
        
        self.checkbuttons = [self.freestandCB]
        self.checkbuttonkeys = ['allowFreeStandingZoneFaces']         
        
        # button
        showPointB = gtk.Button('Display point')
        showPointB.set_size_request(180, 28)
        levelCalB = gtk.Button('Size level calculator')
        levelCalB.set_size_request(180, 28)       
        applyB = gtk.Button('Apply')        
        #----------------------------------------------------------------------------------                                                                                             
        self.castellbox = gtk.VBox(False,0)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        
        label = gtk.Label()
        label.set_markup('<b>  Castellate mesh  </b>')
        label.set_alignment(0,0.5)
        label.set_size_request(50,45)
        
        self.castellbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)
                        
        label = gtk.Label('maxLocalCells')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.maxlocalcellsEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)        
        
        label = gtk.Label('maxGlobalCells')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.maxglobalcellsEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)  
        
        label = gtk.Label('minRefinementCells')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.minrefinecellsEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5) 
        
        label = gtk.Label('maxLoadUnbalance')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.maxloadEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5) 
        
        label = gtk.Label('nCellsBetweenLevels')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.ncellsbetweenEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)                 
        
        label = gtk.Label('resolveFeatureAngle')
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.resolvefeatureEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)   
        
        label = gtk.Label('locationInMesh')                    
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(label, False, False, 5)   
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.loczEntry, False, False, 5)
        hbox.pack_end(self.locyEntry, False, False, 0)
        hbox.pack_end(self.locxEntry, False, False, 5)
        
        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(showPointB, False, False, 5)               

        hbox = gtk.HBox(False,5)
        self.castellbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.freestandCB, False, False, 5)                      

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.castellbox.pack_start(separator, False, True, 5)                                    
        # -----------------------------------------
        label = gtk.Label('  Surface & Feature refinement level ')
        label.set_alignment(0, 0.5)
        self.castellbox.pack_start(label, False, False, 2)       

        aa = glob.glob(self.caseDir + '/system/settings/stlFileSetup')
        if aa:
            self.stlDict = self.GEN.pickleLoad(aa[0])
        else:
            self.stlDict = {}
        
        self.stlnames = self.stlDict.keys()
        self.stlnames.sort()
            
        self.stlvalues = []
        self.featurevalues = []
        for ii in self.stlnames:
            self.stlvalues.append('1')
            self.featurevalues.append('1')

        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.castellbox.pack_start(swin, True, True, 0)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)        
        hh = 31 + len(self.stlnames) * 30        
        swin.set_size_request(200, hh)
        
        self.liststore = gtk.ListStore(str, str, str)
        for i in range(len(self.stlnames)):
            self.liststore.append([self.stlnames[i], self.stlvalues[i], self.featurevalues[i]])
                            
        self.treeview = gtk.TreeView(self.liststore)        
        
        def changeValue(widget, path, text):
            self.liststore[path][1] = text
        def changeValuefeature(widget, path, text):
            self.liststore[path][2] = text
            
        self.cell = gtk.CellRendererText()
        self.cell1 = gtk.CellRendererText()
        self.cell1.set_property("editable", True)
        self.cell1.connect('edited', changeValue)
        self.cell2 = gtk.CellRendererText()
        self.cell2.set_property("editable", True)
        self.cell2.connect('edited', changeValuefeature)

        self.tvcolumn = gtk.TreeViewColumn('Name                      ', self.cell, text = 0)
        self.tvcolumn1 = gtk.TreeViewColumn('STL          ', self.cell1, text = 1)
        self.tvcolumn2 = gtk.TreeViewColumn('Feature', self.cell2, text = 2)
        self.treeview.append_column(self.tvcolumn)
        self.treeview.append_column(self.tvcolumn1)
        self.treeview.append_column(self.tvcolumn2)               
        itembox.pack_start(self.treeview, True, True, 0)
        # -----------------------------------------
        label = gtk.Label('  Region refinement level ')
        label.set_alignment(0, 0.5)
        self.castellbox.pack_start(label, False, False, 5)       

        self.objnames = []
        self.regvalues = []
        aa = glob.glob(self.caseDir + '/system/settings/objectRefine-*')
        for i in range(len(aa)):
            dic = self.GEN.pickleLoad(aa[i])
            self.objnames.append(dic['objectname'])
            self.regvalues.append('1')

        swin1 = gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        self.castellbox.pack_start(swin1, True, True, 0)
        itembox1 = gtk.VBox(False,0)
        swin1.add_with_viewport(itembox1)        
        hh = 35 + len(self.objnames) * 30        
        swin1.set_size_request(200, hh)
        
        self.liststore1 = gtk.ListStore(str, str)
        for i in range(len(self.objnames)):
            self.liststore1.append([self.objnames[i], self.regvalues[i]])
                            
        self.treeview1 = gtk.TreeView(self.liststore1)        
        
        def changeValue1(widget, path, text):
            self.liststore1[path][1] = text
            
        self.rcell = gtk.CellRendererText()
        self.rcell1 = gtk.CellRendererText()
        self.rcell1.set_property("editable", True)
        self.rcell1.connect('edited', changeValue1)

        self.rtvcolumn = gtk.TreeViewColumn('Region                                ', self.rcell, text = 0)
        self.rtvcolumn1 = gtk.TreeViewColumn('Value', self.rcell1, text = 1)
        self.treeview1.append_column(self.rtvcolumn)
        self.treeview1.append_column(self.rtvcolumn1)               
        itembox1.pack_start(self.treeview1, True, True, 0)        

        hbox = gtk.HBox(False, 5)
        self.castellbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(levelCalB, False, False, 5)       
        hbox = gtk.HBox(False, 5)
        self.castellbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(applyB, True, True, 5)
        
        # connect
        levelCalB.connect('clicked', self.sizeLevelCalculator)        
        applyB.connect('clicked', self.applythis)
        showPointB.connect('clicked', self.showPoint)          
       
        self.setSavedValue()

        return self.castellbox        
    #---------------------------------------------------------------------
    def applythis(self, widget):
    
        castellDict = {}
        for i in range(len(self.entrykeys)):
            castellDict[self.entrykeys[i]] = self.entrys[i].get_text()
        for i in range(len(self.checkbuttons)):
            if self.checkbuttons[i].get_active() == 1:
                castellDict[self.checkbuttonkeys[i]] = 'true'
            else:
                castellDict[self.checkbuttonkeys[i]] = 'false'
        
        model1 = self.treeview.get_model()
        for i in range(len(self.stlnames)):
            iter = model1.get_iter(i)
            castellDict['stllevel-' + self.stlnames[i]] = model1.get_value(iter, 1)
            castellDict['featurelevel-' + self.stlnames[i]] = model1.get_value(iter, 2)
            
        model2 = self.treeview1.get_model()
        for i in range(len(self.objnames)):
            iter = model2.get_iter(i)
            castellDict['regionlevel-' + self.objnames[i]] = model2.get_value(iter, 1)
            
        self.GEN.pickleDump(self.caseDir + '/system/settings/castellateSetup', castellDict)
    #---------------------------------------------------------------------
    def setSavedValue(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/castellateSetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            for i in range(len(self.entrykeys)):
                self.entrys[i].set_text(dic[self.entrykeys[i]])              
            for i in range(len(self.checkbuttons)):
                if dic[self.checkbuttonkeys[i]] == 'true':
                    self.checkbuttons[i].set_active(1)
                else:
                    self.checkbuttons[i].set_active(0)
            
            for i in range(len(self.stlnames)):
                self.liststore[i][1] = dic['stllevel-' + self.stlnames[i]]
                self.liststore[i][2] = dic['featurelevel-' + self.stlnames[i]]

            for i in range(len(self.objnames)):
                keys = dic.keys()
                if 'regionlevel-' + self.objnames[i] in keys:
                    self.liststore1[i][1] = dic['regionlevel-' + self.objnames[i]]
        else:
            self.setDefaultValue()
    #---------------------------------------------------------------------
    def setDefaultValue(self):
    
        self.maxlocalcellsEntry.set_text('100000')       
        self.maxglobalcellsEntry.set_text('3000000')               
        self.minrefinecellsEntry.set_text('0')       
        self.maxloadEntry.set_text('0.1')       
        self.ncellsbetweenEntry.set_text('3')       
        self.resolvefeatureEntry.set_text('30')       
        self.locxEntry.set_text('0')
        self.locyEntry.set_text('0')               
        self.loczEntry.set_text('0')
        self.freestandCB.set_active(1)
    #---------------------------------------------------------------------    
    def sizeLevelCalculator(self, widget):

        def calculate(widget):
            NN = float(levelcombo.child.get_text())
            sizex = size0x * (0.5**NN)
            sizey = size0y * (0.5**NN)
            sizez = size0z * (0.5**NN)
            resxEntry.set_text(str("%0.6f" %sizex))
            resyEntry.set_text(str("%0.6f" %sizey))
            reszEntry.set_text(str("%0.6f" %sizez))
        
        def closethis(widget):
            calwin.destroy()
                
        aa = glob.glob(self.caseDir + '/system/settings/blockMeshSetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            minx = dic['minx']
            miny = dic['miny']
            minz = dic['minz']
            maxx = dic['maxx']
            maxy = dic['maxy']
            maxz = dic['maxz']
            nodex = dic['nodex']
            nodey = dic['nodey']
            nodez = dic['nodez']
            lengthx = float(maxx) - float(minx)
            lengthy = float(maxy) - float(miny)
            lengthz = float(maxz) - float(minz)
            size0x = lengthx / float(nodex)
            size0y = lengthy / float(nodey)
            size0z = lengthz / float(nodez)
        else:
            self.GEN.makeDialog('Set blockMesh first')
            return

        calwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        calwin.set_title('Size level calculator')
        calwin.set_border_width(10)
        calwin.set_position(gtk.WIN_POS_CENTER)
            
        mainvbox = gtk.VBox(False,5)
        calwin.add(mainvbox)
        
        label = gtk.Label('Block Mesh Conditions')
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('Domain length, x / y / z')
        xlengEntry = gtk.Entry()
        xlengEntry.set_text(str(lengthx))
        xlengEntry.set_size_request(80, 28)
        ylengEntry = gtk.Entry()
        ylengEntry.set_text(str(lengthy))
        ylengEntry.set_size_request(80, 28)
        zlengEntry = gtk.Entry()
        zlengEntry.set_text(str(lengthz))
        zlengEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(zlengEntry, False, False, 5)
        hbox.pack_end(ylengEntry, False, False, 0)
        hbox.pack_end(xlengEntry, False, False, 5)
        
        label = gtk.Label('Size of Level 0, x / y / z')
        xzeroEntry = gtk.Entry()
        xzeroEntry.set_text(str(size0x))
        xzeroEntry.set_size_request(80, 28)
        yzeroEntry = gtk.Entry()
        yzeroEntry.set_text(str(size0y))
        yzeroEntry.set_size_request(80, 28)
        zzeroEntry = gtk.Entry()
        zzeroEntry.set_text(str(size0z))
        zzeroEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(zzeroEntry, False, False, 5)
        hbox.pack_end(yzeroEntry, False, False, 0)
        hbox.pack_end(xzeroEntry, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 5) 
        
        label = gtk.Label('Level to calculate')
        levelcombo=gtk.combo_box_entry_new_text()
        levelcombo.set_size_request(100, 28)
        for i in range(16):
            levelcombo.append_text(str(i))
        levelcombo.set_active(0)                              
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(levelcombo, False, False, 5)          
        
        calB = gtk.Button('Calculate')
        calB.set_size_request(150, 28)
        calB.connect('clicked', calculate)
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(calB, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 5) 
        
        label = gtk.Label('Result, x / y /z')
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)        

        resxEntry = gtk.Entry()
        resxEntry.set_size_request(100,28)
        resxEntry.set_text(str(size0x))
        resyEntry = gtk.Entry()
        resyEntry.set_size_request(100,28)
        resyEntry.set_text(str(size0y))
        reszEntry = gtk.Entry()
        reszEntry.set_size_request(100,28)
        reszEntry.set_text(str(size0z))
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(reszEntry, False, False, 5)
        hbox.pack_end(resyEntry, False, False, 5)
        hbox.pack_end(resxEntry, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 5) 
                
        closeB = gtk.Button('Close')
        closeB.set_size_request(150, 28)
        closeB.connect('clicked', closethis)
        hbox = gtk.HBox(False,5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(closeB, False, False, 5)
        
        calwin.show_all()
    #---------------------------------------------------------------------    
    def showPoint(self, widget):
    
        xx = self.locxEntry.get_text()
        yy = self.locyEntry.get_text()
        zz = self.loczEntry.get_text()

        viewposition = [1, 1, 1]
        self.renderer.RemoveAllViewProps()
        actor, coneActor = self.VTK_All.showPointSnappy(xx, yy, zz)
        self.renderer.AddActor(actor)
        self.renderer.AddActor(coneActor)        
        self.gvtk.Initialize()
        
        self.notebook.set_current_page(0)
        
        

