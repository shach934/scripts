#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelAdvancedClass:

    def __init__(self, mainself):
    
        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        self.installpath = mainself.installpath
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.displayOptCombo = mainself.displayOptCombo
        
        self.GEN = generalClass(mainself)

    def advanced(self):
        
        self.advbox = gtk.VBox(False, 0)
        
        frame = gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
                
        label = gtk.Label()
        label.set_markup('<b>  Mesh Quality Control / Advanced  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.advbox.pack_start(frame, True, True, 0)
        frame.add(ebox)
        ebox.add(label)
        # -----------------------------------------
        self.meshquality = ['maxNonOrtho', 'maxBoundarySkewness', 'maxInternalSkewness', 'maxConcave', 'minVol', 'minTetQuality',
                            'minArea', 'minTwist', 'minDeterminant', 'minFaceWeight', 'minVolRatio', 'minTriangleTwist',
                            'nSmoothScale', 'errorReduction', 'relaxedMaxNonOrtho', 'mergeTolerance']
        self.meshqualityvalue = ['65', '20', '4', '80', '1e-13', '1e-9', '-1', '0.05', '0.001', '0.05', '0.01', '-1', '4',
                                 '0.75', '75', '1e-6']

        swin1 = gtk.ScrolledWindow()
        swin1.set_border_width(0)
        swin1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.advbox.pack_start(swin1, True, True, 0)
        itembox1 = gtk.VBox(False, 0)
        swin1.add_with_viewport(itembox1)        
        swin1.set_size_request(200, 470)
        
        self.liststore1 = gtk.ListStore(str, str)
        for i in range(16):
            self.liststore1.append([self.meshquality[i], self.meshqualityvalue[i]])
                            
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

        applyB = gtk.Button('Apply')
        applyB.connect('clicked', self.applythis)        
        hbox = gtk.HBox(False, 5)
        self.advbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(applyB, True, True, 5)
       
        self.setSavedValue()

        return self.advbox

    #---------------------------------------------------------------------
    def applythis(self, widget):
        
        advDict = {}            
        model1 = self.treeview1.get_model()
        for i in range(len(self.meshquality)):
            iter = model1.get_iter(i)
            advDict[self.meshquality[i]] = model1.get_value(iter, 1)

        self.GEN.pickleDump(self.caseDir+'/system/settings/advancedSnappySetup', advDict)            
    #---------------------------------------------------------------------
    def setSavedValue(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/advancedSnappySetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            for i in range(len(self.meshquality)):
                self.liststore1[i][1] = dic[self.meshquality[i]]

                                    

