#!/bin/bash
#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class mainWindowSnappy:

    def delete_event(self, widget, event):    
        gtk.main_quit()
        home = expanduser("~")         
        if self.caseDir == home + '/.OpenFOAM/Baram_snappy_temporary':
            os.system('rm -rf ' + self.caseDir)
        elif self.caseDir[:-1] == home + '/.OpenFOAM/Baram_snappy_temporary':
            os.system('rm -rf ' + self.caseDir)

    def destroy(self, widget):
        gtk.main_quit()
        
    def __init__(self, caseDir, installpath):
    
        self.caseDir = caseDir
        self.installpath = installpath
        
        self.VTK_All = VTKStuff(self.caseDir)
        
        self.mode = 'New'
        self.rr = 0.32
        self.gg = 0.34
        self.bb = 0.43
        self.solver = 'snappyHexMesh'
        self.culling = False
        
        self.gvtk = GtkGLExtVTKRenderWindowInteractor()

    def mainWindowGUI(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Baram-snappy-v5.0')
        self.window.set_border_width(2)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event", self.delete_event)
        
        GEN = generalClass(self)
        winsize = GEN.pickleLoad(expanduser("~") + '/.OpenFOAM/windowSize')
        if winsize == None:
            winsize = (800, 500)
        self.window.set_default_size(winsize[0], winsize[1])
        
        self.mainbox = gtk.VBox(False, 0)
        self.window.add(self.mainbox)
        
        self.menubox = gtk.HBox(False, 0)
        self.mainbox.pack_start(self.menubox, False, False, 0)
        self.mb = gtk.MenuBar()
        self.menubox.pack_start(self.mb, False, False, 0)

        self.toolframe = gtk.Frame()
        self.toolframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(self.toolframe, False, False, 0)
        hbox = gtk.HBox(False, 0)
        self.toolframe.add(hbox)
        self.toolbarbox = gtk.HBox(False, 0)
        hbox.pack_start(self.toolbarbox, True, True, 0)
        
        self.hpan = gtk.HPaned()
        self.mainbox.pack_start(self.hpan, True, True, 0)
        self.leftbox = gtk.VBox(False, 0)
        self.graphicbox = gtk.HBox(False, 0)
        self.hpan.add(self.leftbox)
        self.hpan.add(self.graphicbox)
        
        freeswin = gtk.ScrolledWindow()
        freeswin.set_border_width(0)
        freeswin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        freeswin.set_size_request(350, -1)
        self.leftbox.add(freeswin)
        self.freevbox = gtk.VBox(False, 0)
        freeswin.add_with_viewport(self.freevbox)
        
        self.tailbox = gtk.HBox(False, 5)
        self.mainbox.pack_start(self.tailbox, False, False, 0)
        self.tailbox.pack_end(gtk.Label('Baram v5.0 : OpenFOAM v5 based snappyHexMesh Graphic UI of NEXTFOAM'), False, False, 5)
        #------------------------------------------------------------------------------------------------------------------------------
        self.renderbox = gtk.VBox(False, 0)
        self.gvtk.set_size_request(300, 200)
        
        self.viewToolbox = gtk.HBox()
        self.renderbox.pack_start(self.viewToolbox, False, False, 0)
        self.makeToolbar_view()
        
        # background color
        vvvbox = gtk.EventBox()
        self.viewToolbox.pack_start(vvvbox, False, False, 0)
        self.bgbox = gtk.VBox(False, 0)
        vvvbox.add(self.bgbox)
        self.bgCombo = gtk.combo_box_entry_new_text()
        self.bgCombo.set_size_request(160, 28)
        bgList = ['background color', 'black', 'white', 'paraview']
        for ii in bgList:
            self.bgCombo.append_text(ii)
        self.bgCombo.set_active(0)
        self.bgbox.pack_end(self.bgCombo, True, True, 10)
        self.bgCombo.connect('changed', self.chbg)                 
        
        self.renderbox.pack_start(self.gvtk, True, True, 0)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.rr, self.gg, self.bb)
        self.gvtk.GetRenderWindow().AddRenderer(self.renderer)

        self.Actor_Axes = vtk.vtkAxesActor()
        self.Actor_Axes.SetNormalizedLabelPosition(1.5, 1.5, 1.5)
        self.Actor_Axes.SetNormalizedTipLength(0.3, 0.3, 0.3)
        self.Widget_OriMarker = vtk.vtkOrientationMarkerWidget()
        self.Widget_OriMarker.SetOrientationMarker(self.Actor_Axes)
        self.Widget_OriMarker.SetInteractor(self.gvtk)
        self.Widget_OriMarker.EnabledOn()
        self.Widget_OriMarker.InteractiveOff()

        self.shellbox = gtk.VBox(False, 0)
        self.terminal = vte.Terminal()
        self.terminal.fork_command()

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.graphicbox.pack_start(self.notebook, True, True, 0)
        self.notebook.append_page(self.renderbox,gtk.Label('Graphic window'))
        self.notebook.append_page(self.shellbox,gtk.Label('shell window'))
        
        self.makeTerminal()
        self.makeToolbar()
        self.createMenu()
        #------------------------------------------------------------------------------------------------------------------------------
        self.freepanelbox = gtk.VBox(False, 0)
        FREECAD = freepanelCADClass(self)
        self.cadbox = FREECAD.CAD()
        self.freevbox.pack_start(self.cadbox, False, False, 0)

        self.window.show_all()
        
        self.setfolder()
    #--------------------------------------------------------------------------------------
    def createMenu(self):
        
        files=['New', 'Open', 'Save As', 'Exit']
        stls=['Scale', 'Translate', 'Split solids', 'Merge files', 'surfaceAutoPatch']
        posts=['paraFoam', 'paraFoam -builtin']
        help = ['Snappy User Guide', 'Snappy Tutorial']
        
        fmenu = gtk.Menu()
        stlmenu = gtk.Menu()
        pmenu = gtk.Menu()
        hmenu = gtk.Menu()

        for i in range(len(files)):
            mi = gtk.MenuItem(files[i])
            fmenu.append(mi)
            mi.connect('activate', self.menuitem_response,files[i])
        for i in range(len(stls)):
            mi = gtk.MenuItem(stls[i])
            stlmenu.append(mi)
            mi.connect('activate', self.menuitem_response,stls[i])
        for i in range(len(posts)):
            mi = gtk.MenuItem(posts[i])
            pmenu.append(mi)
            mi.connect('activate', self.menuitem_response,posts[i])
        for i in range(len(help)):
            mi = gtk.MenuItem(help[i])
            hmenu.append(mi)
            mi.connect('activate', self.menuitem_response,help[i])

        filemenuitem = gtk.MenuItem('File  ')
        filemenuitem.set_submenu(fmenu)
        surfacemenuitem = gtk.MenuItem('Surface  ')
        surfacemenuitem.set_submenu(stlmenu)
        postmenuitem = gtk.MenuItem('PostProcessing  ')
        postmenuitem.set_submenu(pmenu)
        helpmenuitem = gtk.MenuItem('Help  ')
        helpmenuitem.set_submenu(hmenu)

        self.mb.append(filemenuitem)
        self.mb.append(surfacemenuitem)
        self.mb.append(postmenuitem)
        self.mb.append(helpmenuitem)        
    #------------------------------------------------------------------------------------------
    def menuitem_response(self, widget, string):
    
        if string == 'New':
            self.newcase()
        elif string == 'Open':
            self.readcase()
        elif string == 'Save As':
            self.saveAs()
        elif string == 'Exit':
            self.closedialog()
        elif string == 'createCylinder':
            self.createCylinder()
        elif string == 'Scale':
            self.surfaceScale()
        elif string == 'Translate':
            self.surfaceTranslate()
        elif string == 'Split solids':
            self.splitSolids()
        elif string == 'Merge files':
            self.mergeSTLs()
        elif string == 'surfaceAutoPatch':
            self.surfaceAutoPatch()
        elif string == 'paraFoam':
            os.system('paraFoam -case ' + self.caseDir + '&')
        elif string == 'paraFoam -builtin':
            os.system('paraFoam -builtin -case ' + self.caseDir + '&')
        elif string == 'Snappy User Guide':
            os.system('evince ' + self.installpath + '/Help/Baram-snappy-v5.0-usersGuide.pdf &')
        elif string == 'Snappy Tutorial':
            os.system('evince ' + self.installpath + '/Help/Baram-snappy-v5.0-tutorial.pdf &')
    #----------------------------------------------------------------------------------------            
    def makeTerminal(self):
    
        self.terminal.set_scrollback_lines(-1)
        self.terminal.set_scroll_on_output(True)
        self.terminal.set_scroll_on_keystroke(True)
        self.terminal.set_word_chars("-A-Za-z0-9,./?%&#:_")

        foreground = gtk.gdk.Color('#bbbbbb')
        background = gtk.gdk.Color('#222222')

        user_palette = []
        user_palette.append(gtk.gdk.Color('#000000'))
        user_palette.append(gtk.gdk.Color('#cc0000'))
        user_palette.append(gtk.gdk.Color('#4e9a06'))
        user_palette.append(gtk.gdk.Color('#c4a000'))
        user_palette.append(gtk.gdk.Color('#3465a4'))
        user_palette.append(gtk.gdk.Color('#75507b'))
        user_palette.append(gtk.gdk.Color('#06989a'))
        user_palette.append(gtk.gdk.Color('#d3d7cf'))
        user_palette.append(gtk.gdk.Color('#555753'))
        user_palette.append(gtk.gdk.Color('#ef2929'))
        user_palette.append(gtk.gdk.Color('#8ae234'))
        user_palette.append(gtk.gdk.Color('#fce94f'))
        user_palette.append(gtk.gdk.Color('#729fcf'))
        user_palette.append(gtk.gdk.Color('#ad7fa8'))
        user_palette.append(gtk.gdk.Color('#34e2e2'))
        user_palette.append(gtk.gdk.Color('#eeeeec'))

        self.terminal.set_colors(foreground, background, user_palette)

        self.terminal.feed_child("PS1= '\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\w\\[\\033[00m\\]${text}$\[\e[m\] ';\
                               history -d $((HISTCMD-1))\n")
        self.terminal.feed_child('reset\n')

        self.scroller = gtk.ScrolledWindow()
        self.scroller.set_border_width(2)
        self.scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scroller.add(self.terminal)
        self.shellbox.pack_start(self.scroller, True, True, 0)
        
        cmd= 'unset PROMPT_COMMAND'+'\n'
        self.terminal.feed_child(cmd, len(cmd))
        
        cmd= 'cd ' + self.caseDir + '\n'
        self.terminal.feed_child(cmd, len(cmd))        
    #----------------------------------------------------------------------------------------    
    def makeToolbar(self):
        
        self.toolbox = gtk.HBox(False, 0)
        self.toolbarbox.pack_start(self.toolbox, True, True, 0)
        self.toolbar=gtk.Toolbar()
        self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)        
        self.toolbox.add(self.toolbar)            
        
        self.displayOptCombo = gtk.combo_box_entry_new_text()
        self.displayOptCombo.set_size_request(180, 28)
        self.displayOptCombo.connect('changed',self.changeDisplayMode)
        self.displayoptList=['surface', 'surfaceEdge', 'wireframe']
        for ii in self.displayoptList:
            self.displayOptCombo.append_text(ii)
        self.displayOptCombo.set_size_request(130, 28)
        self.displayOptCombo.set_active(0)
        hbox3 = gtk.HBox()
        self.toolbarbox.pack_start(hbox3, False, False, 0)
        
        hhhbox = gtk.HBox(False, 5)
        hhvbox = gtk.VBox(False, 5)
        hhvbox.pack_start(hhhbox, True, True, 10)
        hhhbox.pack_end(self.displayOptCombo, False, False, 5)
        hbox3.add(hhvbox)        
        hbox3.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
        
        self.logo = gtk.Image()
        self.logo.set_from_file(self.installpath + "/pic/logo_baram.png")
        logohbox = gtk.HBox(False, 5)
        logohbox.pack_start(self.logo, False, False, 5)
        self.toolbarbox.pack_start(logohbox, False, False, 0)

        self.projectToolItems = ['New Project', 'Open Project']
        self.projectPic = ['new.png', 'open.png']

        self.solverToolItems = ['Geometry', 'blockMesh', 'castellate mesh', 'snap mesh', 'add layer', 'advanced',
                                'Run SnappyHexMesh', 'Mesh manipulation', 'paraFoam', 'Exit']
        self.solverPic = ['geom.png', 'blockmesh.png', 'castel.png', 'snapp.png', 'layer.png', 'advance.png',
                          'run.png', 'Mesh.png', 'para.png', 'close.png']
        
        for i in range(2):
            self.createtoolbar(self.installpath + '/pic/' + self.projectPic[i], self.projectToolItems[i], i)        
        sep = gtk.SeparatorToolItem()
        self.toolbar.insert(sep, 2)
        
        for i in range(10):
            self.createtoolbar(self.installpath + '/pic/' + self.solverPic[i], self.solverToolItems[i], i + 3)
        sep = gtk.SeparatorToolItem()
        self.toolbar.insert(sep, 13)
    #----------------------------------------------------------------------------------------    
    def makeToolbar_view(self):
            
        self.toolbox1 = gtk.HBox(False, 5)
        self.viewToolbox.pack_start(self.toolbox1, True, True, 0)

        self.toolbar1 = gtk.Toolbar()
        self.toolbar1.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.toolbar1.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar1.set_border_width(0)
        self.toolbox1.add(self.toolbar1)

        self.cameraToolItems = ['Reset', 'view dir. +X', 'view dir. -X', 'view dir. +Y', 'view dir. -Y',
                                'view dir. +Z', 'view dir. -Z', 'Surface culling']
        self.cameraPic = ['reset.png', 'plusx.png', 'minusx.png', 'plusy.png', 'minusy.png',
                          'plusz.png', 'minusz.png', 'culling.png']
        
        for i in range(8):
            self.createtoolbar_view(self.installpath + '/pic/' + self.cameraPic[i], self.cameraToolItems[i], i)        
    #------------------------------------------------------------------------------------------------------                  
    def createtoolbar(self, pic, text, num):
    
        icon = gtk.Image()
        icon.set_from_file(pic)
        button = gtk.ToolButton(icon)
        button.set_icon_widget(icon)
        button.set_tooltip_text(text)
        button.connect('clicked', self.runToolbar, text)
        self.toolbar.insert(button, num)
    #------------------------------------------------------------------------------------------------------                  
    def createtoolbar_view(self, pic, text, num):
    
        icon = gtk.Image()
        icon.set_from_file(pic)
        button = gtk.ToolButton(icon)
        button.set_icon_widget(icon)
        button.set_tooltip_text(text)
        button.connect('clicked', self.runToolbar, text)
        self.toolbar1.insert(button, num)         
    #------------------------------------------------------------------------------------------------------
    def runToolbar(self, widget, text):
      
        if text == 'New Project':
            self.newcase()
        elif text == 'Open Project':
            self.readcase()
        elif text == 'paraFoam':
            os.system('paraFoam -builtin -case ' + self.caseDir + '&')
        elif text == 'Reset':
            self.resetSize()
        elif text == 'view dir. +X':
            self.resetview([-1,0,0], [0,0,0], [0,0,1])
        elif text == 'view dir. -X':
            self.resetview([1,0,0], [0,0,0], [0,0,1])
        elif text == 'view dir. +Y':
            self.resetview([0,-1,0], [0,0,0], [0,0,1])
        elif text == 'view dir. -Y':
            self.resetview([0, 1, 0], [0,0,0], [0,0,1])
        elif text == 'view dir. +Z':
            self.resetview([0,0,-1], [0,0,0], [0,1,0])
        elif text == 'view dir. -Z':
            self.resetview([0, 0, 1], [0,0,0], [0,1,0])
        elif text == 'Surface culling':
            self.surfaceCulling()        
        elif text == 'Exit':
            self.closedialog()
        else:
            self.chfreepanel(text)       
    #------------------------------------------------------------------------------------------
    def setfolder(self):
    
        WFILE = writeFileClassSnappy(self.caseDir)
        
        if not os.path.isdir(self.caseDir + '/0'):
            os.system('mkdir ' + self.caseDir + '/0')
        if not os.path.isdir(self.caseDir + '/constant'):
            os.system('mkdir ' + self.caseDir + '/constant')
        if not os.path.isdir(self.caseDir + '/system'):
            os.system('mkdir ' + self.caseDir + '/system')
        if not os.path.isdir(self.caseDir + '/system/settings'):
            os.system('mkdir ' + self.caseDir + '/system/settings')
        if not os.path.isdir(self.caseDir + '/logfiles'):
            os.system('mkdir ' + self.caseDir + '/logfiles')
        if self.mode == 'New':
            WFILE.basicfvsolution()
            WFILE.basicfvschemes()
        else:
            if not os.path.isfile(self.caseDir + '/system/fvSolution'):
                WFILE.basicfvsolution()
            if not os.path.isfileb(self.caseDir + '/system/fvSchemes'):
                WFILE.basicfvschemes()
        WFILE.basiccontroldict()
    #------------------------------------------------------------------------------------------
    def chfreepanel(self, whatitem):        
        
        if whatitem == 'paraFoam':
            return
        
        for ii in self.freevbox.get_children():
            self.freevbox.remove(ii)
        
        if whatitem == 'Geometry':
            self.FREECAD = freepanelCADClass(self)
            self.cadbox = self.FREECAD.CAD()
            self.freevbox.pack_start(self.cadbox, False, False, 0)
        elif whatitem == 'blockMesh':
            self.FREEBLOCKMESH = freepanelBlockMeshClass(self)
            self.blockbox = self.FREEBLOCKMESH.blockMesh()
            self.freevbox.pack_start(self.blockbox, False, False, 0)
        elif whatitem == 'castellate mesh':
            self.FREECASTEL = freepanelCastellateClass(self)
            self.castelbox = self.FREECASTEL.castellate()
            self.freevbox.pack_start(self.castelbox, False, False, 0)
        elif whatitem == 'snap mesh':
            self.FREESNAP = freepanelSnapClass(self)
            self.snapbox = self.FREESNAP.snap()
            self.freevbox.pack_start(self.snapbox, False, False, 0)
        elif whatitem == 'add layer':
            self.FREELAYER = freepanelLayerClass(self)
            self.layerbox = self.FREELAYER.addLayer()
            self.freevbox.pack_start(self.layerbox, False, False, 0)
        elif whatitem == 'advanced':
            self.FREEADVANCED = freepanelAdvancedClass(self)
            self.advbox = self.FREEADVANCED.advanced()
            self.freevbox.pack_start(self.advbox, False, False, 0)
        elif whatitem == 'Run SnappyHexMesh':
            self.FREERUNSNAPPY = freepanelRunSnappyClass(self)
            self.runbox = self.FREERUNSNAPPY.runSnappy()
            self.freevbox.pack_start(self.runbox, False, False, 0)
        elif whatitem == 'Mesh manipulation':
            self.FREEMESH = freepanelMeshSnappyClass(self)
            self.meshbox = self.FREEMESH.mesh()
            self.freevbox.pack_start(self.meshbox, False, False, 0)
        self.window.show_all()
    #-----------------------------------------------------------------------------------------#
    def newcase(self):
    
        GEN = generalClass(self)
        returnedname = GEN.newcase()
        
        if returnedname != 'None':
            self.caseDir = returnedname
            self.setfolder()
            self.window.set_title('Baram-snappy-v5.0     ' + self.caseDir)
            for ii in self.freevbox.get_children():
                self.freevbox.remove(ii)
            self.FREECAD = freepanelCADClass(self)
            self.cadbox = self.FREECAD.CAD()
            self.freevbox.pack_start(self.cadbox, False, False, 0)
            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd, len(cmd))
            self.window.show_all()
            
            self.renderer.RemoveAllViewProps()                               
            
            return self.caseDir
    #-------------------------------------------------------------------------------------------------    
    def readcase(self):
    
        GEN = generalClass(self)
        returnedname = GEN.readcase()
        
        if returnedname != 'None':
            self.caseDir = returnedname
            self.setfolder()
            self.window.set_title('Baram-snappy-v5.0     ' + self.caseDir)
            for ii in self.freevbox.get_children():
                self.freevbox.remove(ii)
            self.FREECAD = freepanelCADClass(self)
            self.cadbox = self.FREECAD.CAD()
            self.freevbox.pack_start(self.cadbox, False, False, 0)
            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd, len(cmd))
            self.window.show_all()

            for ii in glob.glob(self.caseDir + '/system/settings/openSubWindow'):
                os.system('rm '+ii)
            
            if os.path.isdir(self.caseDir + '/VTK'):
                VTK = VTKStuff(self.caseDir)
                GEN = generalClass(self)
                bcname, bctype = GEN.getBCName()
                onOff = []
                for ii in bcname:
                    onOff.append(1)
                onOff.append(0)
                viewposition = [1, 1, 1]
                displayOpt = self.displayOptCombo.child.get_text()
                self.notebook.set_current_page(0)
            else:
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
                                    
            return self.caseDir              
    #------------------------------------------------------------------------------------------           
    def saveAs(self):
    
        MENU = menuClass(self)
        clonename = MENU.saveas()
        
        if clonename != 'None':        
            self.caseDir = clonename
            self.window.set_title('Baram-snappy-v5.0     ' + self.caseDir)

            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd, len(cmd))
            self.window.show_all()
            
            for ii in glob.glob(self.caseDir + '/system/settings/openSubWindow'):
                os.system('rm '+ii)
                                          
            return self.caseDir
    #------------------------------------------------------------------------------------------
    def createCylinder(self):
        SURF = surfaceClass(self)
        SURF.createCylinder()

    def surfaceScale(self):
        SURF = surfaceClass(self)
        SURF.surfaceScale()          

    def surfaceTranslate(self):
        SURF = surfaceClass(self)
        SURF.surfaceTranslate()
          
    def splitSolids(self):
        SURF = surfaceClass(self)
        SURF.splitSolids()  
        
    def mergeSTLs(self):
        SURF = surfaceClass(self)
        SURF.mergeSTLs()
        
    def surfaceAutoPatch(self):
        SURF = surfaceClass(self)
        SURF.surfaceAutoPatch()
    #----------------------------------------------------------------------------------------------------
    def resetview(self, viewposition, target, up):
    
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(viewposition[0], viewposition[1], viewposition[2])
        camera.SetFocalPoint(target[0], target[1], target[2])
        camera.SetViewUp(up[0], up[1], up[2])

        self.renderer.SetActiveCamera(camera)
        self.renderer.ResetCamera()
        self.gvtk.Initialize()
    #----------------------------------------------------------------------------------------------------
    def surfaceCulling(self):
    
        num = self.renderer.GetActors().GetNumberOfItems()
        if self.culling == True:
            for i in range(num):
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().FrontfaceCullingOff()
            self.culling = False
        else:
            for i in range(num):
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().FrontfaceCullingOn()
            self.culling = True
        self.gvtk.Initialize() 
    #----------------------------------------------------------------------------------------------------
    def resetSize(self):
    
        ggg = self.gvtk.GetRenderWindow().GetRenderers()
        g1 = ggg.GetFirstRenderer()            
        camera = g1.GetActiveCamera()
        g1.SetActiveCamera(camera)
        g1.ResetCamera()
        self.gvtk.GetRenderWindow().AddRenderer(g1)
        self.gvtk.Initialize()
        self.window.show_all()  
    #--------------------------------------------------------------------------------------
    def chbg(self, widget):
    
        color = self.bgCombo.child.get_text()
        if color == 'white':
            self.rr = 1
            self.gg = 1
            self.bb = 1
        elif color == 'black':
            self.rr = 0
            self.gg = 0
            self.bb = 0
        elif color == 'paraview':
            self.rr = 0.32
            self.gg = 0.34
            self.bb = 0.43
        self.renderer.SetBackground(self.rr, self.gg, self.bb)
        self.window.show_all()
    #---------------------------------------------------------------------------------------------------------            
    def changeDisplayMode(self, widget):
    
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
    #------------------------------------------------------------------------------------------------------                  
    def closedialog(self):
    
        def applythis(widget):
            win.destroy()
            size = self.window.get_size()
            GEN = generalClass(self)
            GEN.pickleDump(expanduser("~") + '/.OpenFOAM/windowSize', size)
            self.window.destroy()
            gtk.main_quit()
            home = expanduser("~")             
            if self.caseDir == home + '/.OpenFOAM/Baram_snappy_temporary':
                os.system('rm -rf ' + self.caseDir)
            elif self.caseDir[:-1] == home + '/.OpenFOAM/Baram_snappy_temporary':
                os.system('rm -rf ' + self.caseDir)
        
        def closethis(widget):
            win.destroy()
            
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_border_width(5)
        win.set_position(gtk.WIN_POS_CENTER)
        
        mbox = gtk.VBox(False, 0)
        win.add(mbox)
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        mbox.pack_start(frame, False, False, 5)
        hbox = gtk.HBox(False, 5)
        frame.add(hbox)
        ibox = gtk.VBox(False, 5)
        hbox.pack_start(ibox, False, False, 5)
        pic = gtk.Image()
        pic.set_from_file(self.installpath + '/pic/question.png')
        ibox.pack_start(pic, False, False, 0)
        lbox = gtk.HBox(False, 5)
        hbox.pack_start(lbox, False, False, 5)
        lbox.pack_start(gtk.Label('Exit this program ?'), False, False, 0)
        bbox = gtk.HBox(False, 5)
        mbox.pack_start(bbox, False, False, 5)
        
        appB = gtk.Button('Exit')
        appB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        clsB = gtk.Button('Cancel')
        clsB.set_size_request(100, 28)
        clsB.connect('clicked', closethis)
        bbox.pack_end(clsB, True, True, 5)
        bbox.pack_end(appB, True, True, 5)	
        win.show_all()
             
