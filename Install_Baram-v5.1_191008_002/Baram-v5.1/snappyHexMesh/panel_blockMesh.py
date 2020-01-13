#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class freepanelBlockMeshClass:

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
                
    def blockMesh(self):

        # entry
        self.minxEntry = gtk.Entry()
        self.minxEntry.set_size_request(60, 28)
        self.minxEntry.set_text('0')
        self.minyEntry = gtk.Entry()
        self.minyEntry.set_size_request(60, 28)
        self.minyEntry.set_text('0')
        self.minzEntry = gtk.Entry()
        self.minzEntry.set_size_request(60, 28)
        self.minzEntry.set_text('0')
        
        self.maxxEntry = gtk.Entry()
        self.maxxEntry.set_size_request(60, 28)
        self.maxxEntry.set_text('10')
        self.maxyEntry = gtk.Entry()
        self.maxyEntry.set_size_request(60, 28)
        self.maxyEntry.set_text('10')
        self.maxzEntry = gtk.Entry()
        self.maxzEntry.set_size_request(60, 28)
        self.maxzEntry.set_text('10')
        
        self.noxEntry = gtk.Entry()
        self.noxEntry.set_size_request(60, 28)
        self.noxEntry.set_text('10')
        self.noyEntry = gtk.Entry()
        self.noyEntry.set_size_request(60, 28)
        self.noyEntry.set_text('10')
        self.nozEntry = gtk.Entry()
        self.nozEntry.set_size_request(60, 28)
        self.nozEntry.set_text('10')

        self.entrys = [self.minxEntry, self.minyEntry, self.minzEntry, self.maxxEntry, self.maxyEntry,
                       self.maxzEntry, self.noxEntry, self.noyEntry, self.nozEntry]
        self.entrykeys = ['minx', 'miny', 'minz', 'maxx', 'maxy', 'maxz', 'nodex', 'nodey', 'nodez']
        
        # button
        self.domainB = gtk.Button('Set Domain Range')
        self.domainB.set_size_request(180, 28)
        self.runBM = gtk.Button('blockMesh')
        #-----------------------------------------------------------------                                                                                                       
        self.blockbox = gtk.VBox(False, 5)
        
        frame=gtk.Frame()
        
        ebox = gtk.EventBox()
        ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        
        label = gtk.Label()
        label.set_markup('<b>  blockMesh  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(50, 45)
        
        self.blockbox.pack_start(frame, True, True, 0)
        frame.add(ebox)        
        ebox.add(label)

        label = gtk.Label('  Define background domain')
        label.set_alignment(0, 0.5)
        self.blockbox.pack_start(label, False, False, 2)       
                
        label = gtk.Label('Min. x/y/z')
        label.set_alignment(0, 0.5)       
        hbox = gtk.HBox(False, 5)
        self.blockbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(self.minzEntry, False, False, 5)
        hbox.pack_end(self.minyEntry, False, False, 0)
        hbox.pack_end(self.minxEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)        
        
        label = gtk.Label('Max. x/y/z')
        label.set_alignment(0, 0.5)       
        hbox = gtk.HBox(False, 5)
        self.blockbox.pack_start(hbox, False, False, 5)  
        hbox.pack_end(self.maxzEntry, False, False, 5)
        hbox.pack_end(self.maxyEntry, False, False, 0)
        hbox.pack_end(self.maxxEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)
        
        hbox = gtk.HBox(False, 5)
        self.blockbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(self.domainB, False, False, 5)
        
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.blockbox.pack_start(separator, False, True, 5)

        label = gtk.Label('  Define background mesh size ')
        label.set_alignment(0, 0.5)
        self.blockbox.pack_start(label, False, False, 2)       
        
        label = gtk.Label('No. x/y/z')
        label.set_alignment(0, 0.5)       
        hbox = gtk.HBox(False, 5)
        self.blockbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(self.nozEntry, False, False, 5)
        hbox.pack_end(self.noyEntry, False, False, 0)
        hbox.pack_end(self.noxEntry, False, False, 5)
        hbox.pack_end(label, False, False, 5)          

        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        self.blockbox.pack_start(separator,False,True,5)                    
       
        hbox = gtk.HBox(False, 5)
        self.blockbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(self.runBM, True, True, 5)
        
        # connect
        self.domainB.connect('clicked', self.setDomainRange)
        self.runBM.connect('clicked', self.runBlockMesh)
                               
        self.setSavedValue()

        return self.blockbox
    #-------------------------------------------------------------------------------------------------
    def runBlockMesh(self, widget):
    
        blockDict = {}
        for i in range(len(self.entrykeys)):
            blockDict[self.entrykeys[i]] = self.entrys[i].get_text()
        
        self.GEN.pickleDump(self.caseDir + '/system/settings/blockMeshSetup', blockDict)

        self.makeBlockMeshDict(blockDict)

        cmd = 'blockMesh -case ' + self.caseDir + '\n'
        self.terminal.feed_child(cmd,len(cmd))
        
        self.displayBlockMesh()
        self.notebook.set_current_page(0)
    #-------------------------------------------------------------------------------------------------
    def setSavedValue(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/blockMeshSetup')
        if aa:
            dic = self.GEN.pickleLoad(aa[0])
            for i in range(len(self.entrykeys)):
                self.entrys[i].set_text(dic[self.entrykeys[i]])              
    #-------------------------------------------------------------------------------------------------    
    def displayBlockMesh(self):
    
        while True:
            aa = glob.glob(self.caseDir + '/constant/polyMesh/boundary')
            if aa:
                break
            time.sleep(1)

        viewposition = [1, 1, 1]
        self.renderer.RemoveAllViewProps()
        actor, stlactors = self.VTK_All.blockMesh()
        self.renderer.AddActor(actor)
        for ii in stlactors:
            self.renderer.AddActor(ii)
        self.gvtk.Initialize()
        
        self.notebook.set_current_page(0)
    #-------------------------------------------------------------------------------------------------        
    def setDomainRange(self, widget):
    
        stls = glob.glob(self.caseDir + '/constant/triSurface/*.stl')

        if len(stls) == 1:
            os.system('cp ' + stls[0] + ' ' + self.caseDir + '/mesh.stl')
        elif len(stls) == 0:
            return
        else:
            self.GEN.mergeSTL(stls)
        
        stlrange = self.GEN.getSTLRange(self.caseDir + '/mesh.stl')
            
        minx = stlrange[0][0]
        miny = stlrange[0][1]
        minz = stlrange[0][2]
        maxx = stlrange[1][0]
        maxy = stlrange[1][1]
        maxz = stlrange[1][2]
        
        dx = float(maxx) - float(minx)
        dy = float(maxy) - float(miny)
        dz = float(maxz) - float(minz)            
        minix = float(minx) - dx * 0.01
        miniy = float(miny) - dy * 0.01
        miniz = float(minz) - dz * 0.01
        maxix = float(maxx) + dx * 0.01
        maxiy = float(maxy) + dy * 0.01
        maxiz = float(maxz) + dz * 0.01
            
        self.minxEntry.set_text(str(minix))
        self.minyEntry.set_text(str(miniy))
        self.minzEntry.set_text(str(miniz))                
        self.maxxEntry.set_text(str(maxix))
        self.maxyEntry.set_text(str(maxiy))
        self.maxzEntry.set_text(str(maxiz))      
    #-------------------------------------------------------------------------------------------------
    def makeBlockMeshDict(self, dic):
    
        aa = glob.glob(self.caseDir + '/system')
        if aa == []:
            os.system('mkdir ' + self.caseDir + '/system')
        f = open(self.caseDir + '/system/blockMeshDict', 'w')
        
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.2.0                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      blockMeshDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

        f.write('convertToMeters 1; \n')
        f.write('vertices \n')
        f.write('( \n')
        f.write('   ( ' + dic['minx'] + ' ' + dic['miny'] + ' ' + dic['minz'] + ' ) \n') 
        f.write('   ( ' + dic['maxx'] + ' ' + dic['miny'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['maxx'] + ' ' + dic['maxy'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['minx'] + ' ' + dic['maxy'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['minx'] + ' ' + dic['miny'] + ' ' + dic['maxz'] + ' ) \n')         
        f.write('   ( ' + dic['maxx'] + ' ' + dic['miny'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write('   ( ' + dic['maxx'] + ' ' + dic['maxy'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write('   ( ' + dic['minx'] + ' ' + dic['maxy'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write(');\n')
        f.write('blocks\n')
        f.write('(\n')
        f.write('    hex (0 1 2 3 4 5 6 7) (' + dic['nodex'] + ' ' + dic['nodey'] + ' ' + dic['nodez'] + ') simpleGrading (1 1 1)\n')
        f.write(');\n')
        f.write('edges\n')
        f.write('(\n')
        f.write(');\n')
        f.write('boundary\n')
        f.write('(\n')
        
        f.write('    minX \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 3 7 4) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxX \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (1 2 6 5) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    minY \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 1 5 4) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxY \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (3 7 6 2) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    minZ \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (0 1 2 3) \n')
        f.write('        ); \n')
        f.write('    } \n')

        f.write('    maxZ \n')
        f.write('    { \n')
        f.write('        type patch; \n')
        f.write('        faces \n')
        f.write('        ( \n')
        f.write('            (4 5 6 7) \n')
        f.write('        ); \n')
        f.write('    } \n')
        
        f.write('); \n')
           
        f.close() 
    #-------------------------------------------------------------------------------------------------
    def makeBlockMeshDict_ori(self, dic):
    
        aa = glob.glob(self.caseDir + '/system')
        if aa == []:
            os.system('mkdir ' + self.caseDir + '/system')
        f = open(self.caseDir + '/system/blockMeshDict','w')
        
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.2.0                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      blockMeshDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

        f.write('convertToMeters 1; \n')
        f.write('vertices \n')
        f.write('( \n')
        f.write('   ( ' + dic['minx'] + ' ' + dic['miny'] + ' ' + dic['minz'] + ' ) \n') 
        f.write('   ( ' + dic['maxx'] + ' ' + dic['miny'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['maxx'] + ' ' + dic['maxy'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['minx'] + ' ' + dic['maxy'] + ' ' + dic['minz'] + ' ) \n')         
        f.write('   ( ' + dic['minx'] + ' ' + dic['miny'] + ' ' + dic['maxz'] + ' ) \n')         
        f.write('   ( ' + dic['maxx'] + ' ' + dic['miny'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write('   ( ' + dic['maxx'] + ' ' + dic['maxy'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write('   ( ' + dic['minx'] + ' ' + dic['maxy'] + ' ' + dic['maxz'] + ' ) \n') 
        f.write(');\n')
        f.write('blocks\n')
        f.write('(\n')
        f.write('    hex (0 1 2 3 4 5 6 7) (' + dic['nodex'] + ' ' + dic['nodey'] + ' ' + dic['nodez'] + ') simpleGrading (1 1 1)\n')
        f.write(');\n')
        f.write('edges\n')
        f.write('(\n')
        f.write(');\n')
        f.write('boundary\n')
        f.write('(\n')
        if dic['sym']=='min.X':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (0 3 7 4) \n')
            f.write('        ); \n')
            f.write('    } \n')
        elif dic['sym']=='max.X':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (1 2 6 5) \n')
            f.write('        ); \n')
            f.write('    } \n')
        elif dic['sym']=='min.Y':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (0 1 5 4) \n')
            f.write('        ); \n')
            f.write('    } \n')
        elif dic['sym']=='max.Y':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (3 7 6 2) \n')
            f.write('        ); \n')
            f.write('    } \n')
        elif dic['sym']=='min.Z':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (0 1 2 3) \n')
            f.write('        ); \n')
            f.write('    } \n')
        elif dic['sym']=='max.Z':
            f.write('    symmetry \n')
            f.write('    { \n')
            f.write('        type patch; \n')
            f.write('        faces \n')
            f.write('        ( \n')
            f.write('            (4 5 6 7) \n')
            f.write('        ); \n')
            f.write('    } \n')
        f.write('); \n')
           
        f.close() 
        #---------------------------------------------------------------------------------------------------------         
                                    

