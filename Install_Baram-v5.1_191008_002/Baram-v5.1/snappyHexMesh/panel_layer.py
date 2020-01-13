#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelLayerClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.displayOptCombo = mainself.displayOptCombo
        
        self.GEN = generalClass(mainself)
        
    def addLayer(self):
        
        # entry
        self.nlayerEntry = gtk.Entry()
        self.nlayerEntry.set_size_request(80, 28)    
        self.expansionEntry = gtk.Entry()
        self.expansionEntry.set_size_request(80, 28)           
        self.finalthickEntry = gtk.Entry()
        self.finalthickEntry.set_size_request(80, 28)
        self.firstthickEntry = gtk.Entry()
        self.firstthickEntry.set_size_request(80, 28)
        self.overallthickEntry = gtk.Entry()
        self.overallthickEntry.set_size_request(80, 28)
        self.minthickEntry = gtk.Entry()
        self.minthickEntry.set_size_request(80, 28)
        self.ngrowEntry = gtk.Entry()
        self.ngrowEntry.set_size_request(80, 28)       
        
        self.entrys = [self.nlayerEntry, self.expansionEntry, self.finalthickEntry, self.firstthickEntry,
                       self.overallthickEntry, self.minthickEntry, self.ngrowEntry]
        self.entrykeys = ['nlayers', 'expansionRatio', 'finalthick', 'firstthick',
                          'overallthick','minThickness','nGrow']
                                        
        # combo
        self.thickCombo = gtk.combo_box_entry_new_text()
        self.thickCombo.set_size_request(110, 28)
        self.thickList = ['firstLayer', 'finalLayer', 'overall']  
        for ii in self.thickList:
            self.thickCombo.append_text(ii)
                
        self.combos = [self.thickCombo]
        self.combokeys = ['thickmethod']
        
        # checkbutton
        self.relativesizeCB = gtk.CheckButton('Use relative sizes')
        
        self.checkbuttons = [self.relativesizeCB]
        self.checkbuttonkeys = ['relativesize']        
                
        # button
        self.layerCalB = gtk.Button('layer size calculator')
        self.layerCalB.set_size_request(180, 28)
        self.applyB = gtk.Button('Apply')        
        #---------------------------------------------------------------------------------------------
        self.layerbox = gtk.VBox(False, 5)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                
        label = gtk.Label()
        label.set_markup('<b>  Add boundary layers  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.layerbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)

        label = gtk.Label('No.of layers')
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.nlayerEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('expansionRatio')
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.expansionEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)

        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.relativesizeCB, False, False, 5)

        label = gtk.Label('Thickness difine method')     
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.thickCombo, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        self.methodbox = gtk.VBox(False, 0)
        self.layerbox.pack_start(self.methodbox, False, False, 0) 
                                
        finallabel = gtk.Label('finalLayerThickness')
        self.finalhbox = gtk.HBox(False, 5)
        self.methodbox.pack_start(self.finalhbox, False, False, 0)
        self.finalhbox.pack_end(self.finalthickEntry, False, False, 5)
        self.finalhbox.pack_start(finallabel, False, False, 5)

        firstlabel = gtk.Label('firstLayerThickness')
        self.firsthbox = gtk.HBox(False, 5)
        self.firsthbox.pack_end(self.firstthickEntry, False, False, 5)
        self.firsthbox.pack_start(firstlabel, False, False, 5)

        overalllabel = gtk.Label('overallLayerThickness')
        self.overallhbox = gtk.HBox(False, 5)
        self.overallhbox.pack_end(self.overallthickEntry, False, False, 5)
        self.overallhbox.pack_start(overalllabel, False, False, 5)

        label = gtk.Label('minThickness')
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.minthickEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)        

        label = gtk.Label('nGrow')
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.ngrowEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5) 
        
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.layerCalB, False, False, 5)                
                        
        aa = glob.glob(self.caseDir+'/system/settings/stlFileSetup')
        if aa:
            stlDict = self.GEN.pickleLoad(aa[0])
        else:
            stlDict = {}                
        self.stlnames = stlDict.keys()
        self.stlnames.sort()
            
        self.viewbox = gtk.VBox(False, 0)
        self.layerbox.pack_start(self.viewbox, False, False, 0)        
        self.scwin=gtk.ScrolledWindow()
        self.scwin.set_border_width(0)
        self.scwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scwin.set_size_request(250,180)
        self.smbox = gtk.VBox(False,0)
        self.bdbox = gtk.HBox(False,0)
        self.viewbox.pack_start(self.smbox, True, True, 0)
        self.smbox.pack_start(self.scwin, True, True, 0)
        self.scwin.add_with_viewport(self.bdbox)                           
        self.showitembox(self.stlnames)      
        # -----------------------------------------
        label = gtk.Label('  Advanced settings ')
        label.set_alignment(0, 0.5)
        self.layerbox.pack_start(label, False, False, 2)       

        self.advlayer = ['featureAngle', 'slipFeatureAngle', 'nRelaxIter', 'nSmoothSurfaceNormals',
                         'nSmoothNormals', 'nSmoothThickness', 'maxFaceThicknessRatio', 'maxThicknessToMedialRatio',
                         'minMedianAxisAngle', 'nBufferCellsNoExtrude', 'nLayerIter', 'nRelaxedIter',]
        self.advlayervalue = ['60', '30', '10', '1', '3', '10', '0.5', '0.3', '90', '0', '50', '20']

        swin1 = gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.layerbox.pack_start(swin1, True, True, 0)
        itembox1=gtk.VBox(False, 0)
        swin1.add_with_viewport(itembox1)        
        swin1.set_size_request(200, 250)
        
        self.liststore1 = gtk.ListStore(str,str)
        for i in range(12):
            self.liststore1.append([self.advlayer[i], self.advlayervalue[i]])
                            
        self.treeview1 = gtk.TreeView(self.liststore1)        
        
        def changeValue1(widget, path, text):
            self.liststore1[path][1] = text
            
        self.rcell = gtk.CellRendererText()
        self.rcell1 = gtk.CellRendererText()
        self.rcell1.set_property("editable", True)
        self.rcell1.connect('edited', changeValue1)

        self.rtvcolumn = gtk.TreeViewColumn('Items                                ', self.rcell, text = 0)
        self.rtvcolumn1 = gtk.TreeViewColumn('Value', self.rcell1, text = 1)
        self.treeview1.append_column(self.rtvcolumn)
        self.treeview1.append_column(self.rtvcolumn1)               
        itembox1.pack_start(self.treeview1, True, True, 0)  
        # -----------------------------------------
        hbox = gtk.HBox(False, 5)
        self.layerbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(self.applyB, True, True, 5)

        # connect
        self.thickCombo.connect('changed', self.changeThick)
        self.layerCalB.connect('clicked', self.layerCalculator)
        self.applyB.connect('clicked', self.applythis)
        
        self.setSavedValue()

        return self.layerbox        
    #---------------------------------------------------------------------
    def applythis(self, widget):

        layerDict = {}
        
        for i in range(len(self.entrykeys)):
            layerDict[self.entrykeys[i]] = self.entrys[i].get_text()
        for i in range(len(self.combokeys)):
            layerDict[self.combokeys[i]] = self.combos[i].child.get_text()            
        for i in range(len(self.checkbuttons)):
            if self.checkbuttons[i].get_active() == 1:
                layerDict[self.checkbuttonkeys[i]] = 'true'
            else:
                layerDict[self.checkbuttonkeys[i]] = 'false'
        
        layerDict['stlnames'] = self.stlnames
        layerDict['layerOnOff'] = self.onOff
        
        model1 = self.treeview1.get_model()
        for i in range(len(self.advlayer)):
            iter = model1.get_iter(i)
            layerDict[self.advlayer[i]] = model1.get_value(iter, 1)

        self.GEN.pickleDump(self.caseDir+'/system/settings/layerSetup', layerDict)
    #---------------------------------------------------------------------
    def setSavedValue(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/layerSetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            for i in range(len(self.entrykeys)):
                self.entrys[i].set_text(dic[self.entrykeys[i]])              
            for i in range(len(self.combokeys)):
                self.combos[i].child.set_text(dic[self.combokeys[i]])
            for i in range(len(self.checkbuttons)):
                if dic[self.checkbuttonkeys[i]] == 'true':
                    self.checkbuttons[i].set_active(1)
                else:
                    self.checkbuttons[i].set_active(0)
            
            for i in range(len(self.advlayer)):
                self.liststore1[i][1] = dic[self.advlayer[i]]
        else:
            self.setDefaultValue()
    #---------------------------------------------------------------------------------------------
    def setDefaultValue(self):
    
        self.nlayerEntry.set_text('5')       
        self.expansionEntry.set_text('1.2')               
        self.finalthickEntry.set_text('0.3')       
        self.firstthickEntry.set_text('0.3')       
        self.overallthickEntry.set_text('0.3')       
        self.minthickEntry.set_text('0.2')
        self.ngrowEntry.set_text('0')               
        self.thickCombo.set_active(1)
        self.relativesizeCB.set_active(1)
    #---------------------------------------------------------------------
    def changeThick(self, widget):
    
        method = widget.child.get_text()
        aa = self.methodbox.get_children()
        for ii in aa:
            self.methodbox.remove(ii)
        if method == 'firstLayer':
            self.methodbox.pack_start(self.firsthbox, False, False, 0)
        elif method == 'finalLayer':
            self.methodbox.pack_start(self.finalhbox, False, False, 0)
        elif method == 'overall':
            self.methodbox.pack_start(self.overallhbox, False, False, 0)
        self.layerbox.show_all()
    #------------------------------------------------------------
    def showitembox(self, stlnames):
    
        bb = self.bdbox.get_children()
        for ii in bb:
            self.bdbox.remove(ii)            
        
        def get_model(tree_store):
            if tree_store:
                return tree_store 
            else:
                return None                
        
        def col1_toggled_cb( cell, path, model ):
            model[path][1] = not model[path][1]
            for i in range(len(stlnames)):
                if model[path][0] == stlnames[i]:
                    if model[path][1] == True:
                        self.onOff[i] = 1
                    else:
                        self.onOff[i] = 0
                        
        def make_view( model ):
            view = gtk.TreeView( model )
            renderer = gtk.CellRendererText()
            renderer1 = gtk.CellRendererToggle()
            renderer1.set_property('activatable', True)
            renderer1.connect('toggled', col1_toggled_cb, model)
            column0 = gtk.TreeViewColumn("Boundary Name         ", renderer, text = 0)
            column1 = gtk.TreeViewColumn("Add layer", renderer1)
            column1.add_attribute( renderer1, "active", 1)
            view.append_column(column0)
            view.append_column(column1)
            return view

        aa = glob.glob(self.caseDir + '/system/settings/layerSetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            self.onOff = dic['layerOnOff']            
        else:            
            self.onOff = []
            for i in range(len(stlnames)):
                self.onOff.append(1)

        tree_store = gtk.TreeStore(str, bool)
        for i in range(len(stlnames)):
            parent = tree_store.append(None, (stlnames[i], self.onOff[i]))

        mdl = get_model(tree_store)
        view = make_view(mdl)
        
        self.bdbox.pack_start(view, True, True, 0)            
        self.layerbox.show_all()
    #---------------------------------------------------------------------
    def layerCalculator(self, widget):

        def calculate(widget):
            nn = float(nEntry.get_text())
            first = float(firstEntry.get_text())
            ratio = float(expanEntry.get_text())
            last = first * ratio**(nn - 1)
            
            overall = 0.
            for i in range(int(nEntry.get_text())):
                overall = overall + first * ratio**(i)

            lastEntry.set_text(str("%0.6f" %last))
            overEntry.set_text(str("%0.6f" %overall))
        
        def closethis(widget):
            calwin.destroy()

        calwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        calwin.set_title('Layer size calculator')
        calwin.set_border_width(10)
        calwin.set_position(gtk.WIN_POS_CENTER)
        calwin.set_transient_for(self.mainwindow)
            
        mainvbox = gtk.VBox(False, 5)
        calwin.add(mainvbox)
        
        label = gtk.Label('Conditions')
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('No. of layers      ')
        nEntry = gtk.Entry()
        nEntry.set_text('3')
        nEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(nEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)
        
        label = gtk.Label('First cell height')
        firstEntry = gtk.Entry()
        firstEntry.set_text('0.001')
        firstEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(firstEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)
                
        label = gtk.Label('Expansion ratio')
        expanEntry = gtk.Entry()
        expanEntry.set_text('1.0')
        expanEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(expanEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)
       
        calB = gtk.Button('Calculate')
        calB.set_size_request(150, 28)
        calB.connect('clicked', calculate)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(calB, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 5) 
        
        label = gtk.Label('Result')
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)        
        
        label = gtk.Label('Last cell height')
        lastEntry = gtk.Entry()
        lastEntry.set_size_request(100, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(lastEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        
        label = gtk.Label('Overall layer thickness')
        overEntry = gtk.Entry()
        overEntry.set_size_request(100, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(overEntry, False, False, 5)
        hbox.pack_start(label, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 5) 
                
        closeB = gtk.Button('Close')
        closeB.set_size_request(150, 28)
        closeB.connect('clicked', closethis)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(closeB, False, False, 5)
        
        
        calwin.show_all()
         
                                    

