#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelSnapClass:

    def __init__(self, mainself):
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.displayOptCombo = mainself.displayOptCombo
        
        self.GEN = generalClass(mainself)
        
    def snap(self):
       
        # entry
        self.nsmoothEntry = gtk.Entry()
        self.nsmoothEntry.set_size_request(80, 28)      
        self.toleranceEntry = gtk.Entry()
        self.toleranceEntry.set_size_request(80, 28)      
        self.nsolveiterEntry = gtk.Entry()
        self.nsolveiterEntry.set_size_request(80, 28)      
        self.nrelaxiterEntry = gtk.Entry()
        self.nrelaxiterEntry.set_size_request(80, 28)   
        self.nfeaturesnapEntry = gtk.Entry()
        self.nfeaturesnapEntry.set_size_request(80, 28)

        self.entrys = [self.nsmoothEntry, self.toleranceEntry, self.nsolveiterEntry,
                       self.nrelaxiterEntry, self.nfeaturesnapEntry]
        self.entrykeys = ['nSmoothPatch', 'tolerance', 'nSolveIter',
                          'nRelaxIter', 'nFeatureSnapIter']

        # checkbutton
        self.implicitfeatureCB = gtk.CheckButton('implicitFeatureSnap')
        self.explicitfeatureCB = gtk.CheckButton('explicitFeatureSnap')
        self.multifeatureCB = gtk.CheckButton('multiRegionFeatureSnap')

        self.checkbuttons = [self.implicitfeatureCB, self.explicitfeatureCB, self.multifeatureCB]
        self.checkbuttonkeys = ['implicitFeatureSnap', 'explicitFeatureSnap', 'multiRegionFeatureSnap'] 
                
        # button
        applyB = gtk.Button('Apply')        
        #-----------------------------------------------------------------                                                                                                       
        self.snapbox = gtk.VBox(False, 5)

        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
                
        label = gtk.Label()
        label.set_markup('<b>  Snap mesh  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.snapbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)
                
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.nsmoothEntry, False, False, 5)
        hbox.pack_start(gtk.Label('nSmoothPatch'), False, False, 5)        
        
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.toleranceEntry, False, False, 5)
        hbox.pack_start(gtk.Label('tolerance'), False, False, 5)  
        
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.nsolveiterEntry, False, False, 5)
        hbox.pack_start(gtk.Label('nSolveIter'), False, False, 5) 
        
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.nrelaxiterEntry, False, False, 5)
        hbox.pack_start(gtk.Label('nRelaxIter'), False, False, 5) 
        
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_end(self.nfeaturesnapEntry, False, False, 5)
        hbox.pack_start(gtk.Label('nFeatureSnapIter'), False, False, 5)                 
        
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.implicitfeatureCB, False, False, 5)
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.explicitfeatureCB, False, False, 5)       
        hbox = gtk.HBox(False, 5)
        self.snapbox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.multifeatureCB, False, False, 5)  
                
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.snapbox.pack_start(separator, False, True, 5)                                    

        hbox = gtk.HBox(False, 5);self.snapbox.pack_start(hbox, False, False, 5);hbox.pack_end(applyB, True, True, 5)
       
        # connect
        applyB.connect('clicked', self.applythis)
        
        self.setSavedValue()

        return self.snapbox        
    #---------------------------------------------------------------------
    def applythis(self, widget):
        
        snapDict = {}
        for i in range(len(self.entrykeys)):
            snapDict[self.entrykeys[i]] = self.entrys[i].get_text()
        for i in range(len(self.checkbuttons)):
            if self.checkbuttons[i].get_active() == 1:
                snapDict[self.checkbuttonkeys[i]] = 'true'
            else:
                snapDict[self.checkbuttonkeys[i]] = 'false'
        self.GEN.pickleDump(self.caseDir+'/system/settings/snapSetup', snapDict)
    #---------------------------------------------------------------------
    def setSavedValue(self):
        
        aa = glob.glob(self.caseDir + '/system/settings/snapSetup')
        if aa:
            dic = self.GEN.pickleLaod(aa[0])
            for i in range(len(self.entrykeys)):
                self.entrys[i].set_text(dic[self.entrykeys[i]])              
            for i in range(len(self.checkbuttons)):
                if dic[self.checkbuttonkeys[i]] == 'true':
                    self.checkbuttons[i].set_active(1)
                else:
                    self.checkbuttons[i].set_active(0)
        else:
            self.setDefaultValue()
    #---------------------------------------------------------------------
    def setDefaultValue(self):
    
        self.nsmoothEntry.set_text('3')       
        self.toleranceEntry.set_text('3')       
        self.nsolveiterEntry.set_text('30')       
        self.nrelaxiterEntry.set_text('5')       
        self.nfeaturesnapEntry.set_text('15')               
        self.implicitfeatureCB.set_active(0)
        self.explicitfeatureCB.set_active(1)
        self.multifeatureCB.set_active(0)        
        
        
