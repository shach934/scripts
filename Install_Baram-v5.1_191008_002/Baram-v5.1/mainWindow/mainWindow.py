#!/bin/bash
#-*-coding:utf8-*-

from common.fromAll     import *

# -----------------------------------------------------------------------------------------------------
class mainWindow:

    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        home = expanduser("~")         
        if self.caseDir == home + '/.OpenFOAM/Baram_temporary':
            os.system('rm -rf ' + self.caseDir)
        elif self.caseDir[:-1] == home + '/.OpenFOAM/Baram_temporary':
            os.system('rm -rf '+self.caseDir)

    def destroy(self,widget,data=None):
        self.window.destroy()
        gtk.main_quit()

    def __init__(self, caseDir, installpath, solver):
        self.caseDir = caseDir
        self.solver = solver
        self.installpath = installpath        
        self.rr = 0.32
        self.gg = 0.34
        self.bb = 0.43
        self.ver = 'Baram-v5.1'
        
        self.gvtk = GtkGLExtVTKRenderWindowInteractor()
        
        self.gvtk.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        
        self.cellPicker=vtk.vtkCellPicker()
        self.cellPicker.SetTolerance(0.005)

        self.displayPatchDict = {}
        self.displayMode = 'Surface'
        self.selectedPatch = None
        self.culling = False
        self.backgroudColor = 'paraview'
        
        self.nowPanel = 'Mesh Manipulation'
        
        self.pixbuf_main = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/mainItem.png')
        self.pixbuf_first = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/first.png')        
        self.pixbuf_second = gtk.gdk.pixbuf_new_from_file(self.installpath + '/pic/treeIcon/second.png')        
        
        gtk.gdk.threads_init()                
        
    def mainWindowGUI(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.ver)
        self.window.set_border_width(2)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event", self.delete_event)
        
        GEN = generalClass(self)
        winsize = GEN.pickleLoad(expanduser("~") + '/.OpenFOAM/windowSize')
        if winsize == None:winsize = (800,500)
        self.window.set_default_size(winsize[0], winsize[1])

        self.mainbox = gtk.VBox(False,0)
        self.window.add(self.mainbox)
        
        self.menubox = gtk.HBox(False,0)
        self.mainbox.pack_start(self.menubox,False,False,0)
        self.mb = gtk.MenuBar()
        self.menubox.pack_start(self.mb,False,False,0)

        self.toolframe = gtk.Frame()
        self.toolframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(self.toolframe,False,False,0)
        hbox = gtk.HBox(False,0)
        self.toolframe.add(hbox)
        self.toolbarbox = gtk.HBox(False,0)
        hbox.pack_start(self.toolbarbox,True,True,0)
        
        self.hpan = gtk.HPaned()
        self.mainbox.pack_start(self.hpan,True,True,0)
        self.freepanelbox = gtk.VBox(False,0)
        self.graphicbox = gtk.HBox(False,0)
        self.hpan.add(self.freepanelbox)
        self.hpan.add(self.graphicbox)

        self.tailbox = gtk.HBox(False,5)
        self.mainbox.pack_start(self.tailbox,False,False,0)
        label = self.ver + ' : OpenFOAM v5 based flow solver and Graphic UI of NEXTFOAM'
        self.tailbox.pack_end(gtk.Label(label),False,False,5)
        #------------------------------------------------------------------------------------------------------------------------------
        self.renderbox = gtk.VBox()
        self.gvtk.set_size_request(300,200)

        self.toolEvent = gtk.EventBox()
        self.viewToolbox = gtk.HBox(False,0)
        self.toolEvent.add(self.viewToolbox)
        
        self.renderbox.pack_start(self.toolEvent,False,False,0)
        self.makeToolbar_view()

        # display mode
        disbox = gtk.VBox(False,0)
        self.viewToolbox.pack_start(disbox,False,False,5)
        self.discombo = gtk.combo_box_entry_new_text()
        self.discombo.set_size_request(150,28)
        self.displayModeList = ['Surface','SurfaceEdge','Wireframe','Feature']
        for ii in self.displayModeList:
            self.discombo.append_text(ii)
        self.discombo.set_active(0)
        self.discombo.connect('changed',self.changeDisplayMode)
        disbox.pack_end(self.discombo,True,True,10)
        
        # background color
        bgbox = gtk.VBox(False,0)
        self.viewToolbox.pack_start(bgbox,False,False,5)
        self.bgCombo=gtk.combo_box_entry_new_text()
        self.bgCombo.set_size_request(160,28)
        bgList = ['background color','black','white','paraview']
        for ii in bgList:
            self.bgCombo.append_text(ii)
        self.bgCombo.set_active(0)
        bgbox.pack_end(self.bgCombo,True,True,10)
        self.bgCombo.connect('changed',self.chbg)         
        #
        self.renderbox.pack_start(self.gvtk, True, True, 0)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.rr, self.gg, self.bb)
        self.gvtk.GetRenderWindow().AddRenderer(self.renderer)

        self.Actor_Axes = vtk.vtkAxesActor()
        self.Actor_Axes.SetNormalizedLabelPosition(1.5, 1.5, 1.5)
        self.Actor_Axes.SetNormalizedTipLength(0.3, 0.3, 0.3)

        xAxisLabel = self.Actor_Axes.GetXAxisCaptionActor2D()
        xAxisLabel.GetTextActor().SetTextScaleModeToNone()
        xAxisLabel.GetCaptionTextProperty().SetColor(1,0,0)        
        yAxisLabel = self.Actor_Axes.GetYAxisCaptionActor2D()
        yAxisLabel.GetTextActor().SetTextScaleModeToNone()
        yAxisLabel.GetCaptionTextProperty().SetColor(0,1,0)        
        zAxisLabel = self.Actor_Axes.GetZAxisCaptionActor2D()
        zAxisLabel.GetTextActor().SetTextScaleModeToNone()
        zAxisLabel.GetCaptionTextProperty().SetColor(0,0,1)

        self.Widget_OriMarker = vtk.vtkOrientationMarkerWidget()
        self.Widget_OriMarker.SetOrientationMarker(self.Actor_Axes)
        self.Widget_OriMarker.SetInteractor(self.gvtk)
        self.Widget_OriMarker.EnabledOn()
        self.Widget_OriMarker.InteractiveOff()

        self.shellbox = gtk.VBox(False,0)
        self.terminal = vte.Terminal()
        self.terminal.fork_command()

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.graphicbox.add(self.notebook)
        self.notebook.append_page(self.renderbox,gtk.Label('Graphic window'))
        self.notebook.append_page(self.shellbox,gtk.Label('shell window'))

        self.makeTerminal()
        self.makeToolbar()       
        self.createMenu()

        self.freevbox = gtk.VBox(False,0)
        self.freepanelbox.pack_start(self.freevbox,True,True,0)
        
        self.meshPart()
        self.freevbox.pack_start(self.meshbox,True,True,0)        
        
        self.window.show_all()
        
        self.resetNewCase()
    #--------------------------------------------------------------------------------------
    def createMenu(self):
    
        filesmenuitems = ['New simulation','Open simulation','Save As','Clone Case','reconstructPar','Load setting','Exit']
        #stlsmenuitems = ['Scale','Translate','Split solid','Merge files','surfaceAutoPatch']
        stlsmenuitems = ['surfaceAutoPatch']
        postsmenuitems = ['paraFoam','paraFoam -builtin']
        fieldsmenuitems = ['mapFields','setFields','yPlus','Q','vorticity']
        helpmenuitems = ['User Guide', 'Tutorial Guide','About']

        filemenu = gtk.Menu()
        stlmenu = gtk.Menu()
        meshmenu = gtk.Menu()
        postmenu = gtk.Menu()
        fieldmenu = gtk.Menu()
        reportmenu = gtk.Menu()
        helpmenu = gtk.Menu()

        for i in range(len(filesmenuitems)):
            mi = gtk.MenuItem(filesmenuitems[i])
            filemenu.append(mi)
            mi.connect('activate',self.menuitem_response,filesmenuitems[i])
        for i in range(len(stlsmenuitems)):
            mi = gtk.MenuItem(stlsmenuitems[i])
            stlmenu.append(mi)
            mi.connect('activate',self.menuitem_response,stlsmenuitems[i])
        for i in range(len(postsmenuitems)):
            mi = gtk.MenuItem(postsmenuitems[i])
            postmenu.append(mi)
            mi.connect('activate',self.menuitem_response,postsmenuitems[i])
        for i in range(len(fieldsmenuitems)):
            mi = gtk.MenuItem(fieldsmenuitems[i])
            fieldmenu.append(mi)
            mi.connect('activate',self.menuitem_response,fieldsmenuitems[i])
        for i in range(len(helpmenuitems)):
            mi = gtk.MenuItem(helpmenuitems[i])
            helpmenu.append(mi)
            mi.connect('activate',self.menuitem_response,helpmenuitems[i])

        filemenuitem = gtk.MenuItem('File  ')
        filemenuitem.set_submenu(filemenu)
        stlmenuitem = gtk.MenuItem('Surface  ')
        stlmenuitem.set_submenu(stlmenu)
        fieldmenuitem = gtk.MenuItem('Fields  ')
        fieldmenuitem.set_submenu(fieldmenu)
        postmenuitem = gtk.MenuItem('PostProcessing  ')
        postmenuitem.set_submenu(postmenu)
        helpmenuitem = gtk.MenuItem('Help  ')
        helpmenuitem.set_submenu(helpmenu)

        self.mb.append(filemenuitem)
        self.mb.append(stlmenuitem)
        self.mb.append(fieldmenuitem)
        self.mb.append(postmenuitem)
        self.mb.append(helpmenuitem)
    #------------------------------------------------------------------------------------------
    def menuitem_response(self,widget,string):
        
        MENU = menuClass(self)
        GEN = generalClass(self)
        SURFACE = surfaceClass(self)    
        simDict = GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')         
        if simDict != None:
            self.solver = simDict['solver']
        
        if string == 'New simulation':self.newcase()
        elif string == 'Open simulation':self.readcase()
        elif string == 'Save As':self.saveAs() 
        elif string == 'Clone Case':self.cloneCase()
        elif string == 'reconstructPar':MENU.reconstructPar()
        elif string == 'Load setting':MENU.readSetting()
        elif string == 'Exit':self.closedialog()

        elif string == 'surfaceAutoPatch':SURFACE.surfaceAutoPatch()  
                                        
        elif string == 'paraFoam -builtin':os.system('paraFoam -builtin -case '+self.caseDir+'&')
        elif string == 'paraFoam':os.system('paraFoam -case '+self.caseDir+'&')
        elif string == 'mapFields':MENU.mapFields()
        elif string == 'setFields': MENU.setFields(self.gvtk,self.renderer,simDict)

        elif string == 'yPlus':MENU.yPlusRAS()
        elif string == 'Q': MENU.QCriterion()
        elif string == 'vorticity': MENU.vorticity()

        elif string == 'User Guide':os.system('evince ' + self.installpath + '/Help/Baram-v5-usersGuide.pdf'+'&')
        elif string == 'Tutorial Guide':os.system('evince ' + self.installpath + '/Help/Baram-v5-tutorials.pdf'+'&') 
        elif string == 'About':MENU.about(self.window,self.installpath)                
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

        self.terminal.feed_child("PS1='\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\w\\[\\033[00m\\]${text}$\[\e[m\] ';history -d $((HISTCMD-1))\n")
        self.terminal.feed_child('reset\n')

        self.scroller = gtk.ScrolledWindow()
        self.scroller.set_border_width(2)
        self.scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scroller.add(self.terminal)
        self.shellbox.pack_start(self.scroller,True,True,0)
        
        cmd='unset PROMPT_COMMAND'+'\n'
        self.terminal.feed_child(cmd,len(cmd))        
        cmd='cd '+self.caseDir+'\n'
        self.terminal.feed_child(cmd,len(cmd))
        cmd='reset'+'\n'
        self.terminal.feed_child(cmd,len(cmd))
    #----------------------------------------------------------------------------------------    
    def makeToolbar(self):
        
        self.toolbox = gtk.HBox(False,5)
        self.toolbarbox.pack_start(self.toolbox,True,True,0)
        self.handlebox = gtk.HandleBox()
        self.toolbox.pack_start(self.handlebox,True,True,0)

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.toolbar.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar.set_border_width(0)
        self.handlebox.add(self.toolbar)            

        self.logo = gtk.Image()
        self.logo.set_from_file(self.installpath + "/pic/logo_baram.png")
        hbox4 = gtk.EventBox()
        self.toolbarbox.pack_start(hbox4, False, False, 0)
        
        logohbox = gtk.HBox(False, 5)
        logohbox.pack_start(self.logo, False, False, 5)
        hbox4.add(logohbox)

        self.projectToolItems = ['New Project','Open Project']
        self.projectPic = ['new.png','open.png']
        self.solverToolItems = ['CfMesh', 'Mesh Manipulation', 'Flow Conditions', 'Boundary Conditions',
                                'Cell Zone Conditions', 'Numerical Conditions', 'Monitoring', 'Run Conditions',
                                'Stop', 'Extract Data', 'Patch Display', 'Cutting Plane', 'Iso Surfaces', 'Clip', 'Streamline',
                                'ParaFoam', 'Exit']
        self.solverPic = ['cfmesh.png', 'mesh.png', 'sim.png', 'bc.png', 'cellzone.png', 'nume.png', 'monitor.png',
                          'run.png', 'stop.png', 'report.png', 'patchscalar.png', 'cutplane.png', 'isoSurface.png', 'clip.png', 'stream.png',
                          'para.png', 'close.png']

        
        for i in range(2):
            self.createtoolbar(self.installpath + '/pic/' + self.projectPic[i],self.projectToolItems[i],i)        
        sep=gtk.SeparatorToolItem()
        self.toolbar.insert(sep,2)
        
        for i in range(17):
            self.createtoolbar(self.installpath + '/pic/' + self.solverPic[i],self.solverToolItems[i],i+3)   
    #----------------------------------------------------------------------------------------    
    def makeToolbar_view(self):
        
        self.toolbox1 = gtk.HBox(False,5)
        self.viewToolbox.pack_start(self.toolbox1,True,True,0)
        self.handlebox1 = gtk.HandleBox()
        self.toolbox1.pack_start(self.handlebox1,True,True,0)

        self.toolbar1 = gtk.Toolbar()
        self.toolbar1.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.toolbar1.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar1.set_border_width(0)
        self.handlebox1.add(self.toolbar1)

        self.cameraToolItems = ['Reset','view dir. +X','view dir. -X','view dir. +Y','view dir. -Y','view dir. +Z',
                                'view dir. -Z','Surface culling']
        self.cameraPic = ['reset.png','plusx.png','minusx.png','plusy.png','minusy.png','plusz.png','minusz.png',
                          'culling.png']
        
        for i in range(8):
            self.createtoolbar_view(self.installpath+'/pic/'+self.cameraPic[i],self.cameraToolItems[i],i)
    #------------------------------------------------------------------------------------------------------                  
    def createtoolbar(self,pic,text,num):
    
        icon = gtk.Image()
        icon.set_from_file(pic)
        button = gtk.ToolButton(icon)
        button.set_icon_widget(icon)
        button.set_tooltip_text(text)
        button.connect('clicked',self.runToolbar,text)
        self.toolbar.insert(button,num)
    #------------------------------------------------------------------------------------------------------                  
    def createtoolbar_view(self,pic,text,num):
    
        icon = gtk.Image()
        icon.set_from_file(pic)
        button = gtk.ToolButton(icon)
        button.set_icon_widget(icon)
        button.set_tooltip_text(text)
        button.connect('clicked',self.runToolbar,text)
        self.toolbar1.insert(button,num)           
    #------------------------------------------------------------------------------------------------------
    def runToolbar(self,widget,text):  
    
        GEN = generalClass(self)
        if text == 'New Project':self.newcase()
        elif text == 'Open Project':self.readcase()
        elif text == 'ParaFoam':os.system('paraFoam -builtin -case ' + self.caseDir + '&')
        elif text == 'Stop':GEN.savestop()
        elif text == 'Exit':self.closedialog()
        elif text == 'Reset':self.resetSize()
        elif text == 'view dir. +X': self.resetview([-1,0,0],[0,0,0],[0,0,1])
        elif text == 'view dir. -X': self.resetview([1,0,0],[0,0,0],[0,0,1])
        elif text == 'view dir. +Y': self.resetview([0,-1,0],[0,0,0],[0,0,1])
        elif text == 'view dir. -Y': self.resetview([0, 1, 0],[0,0,0],[0,0,1])
        elif text == 'view dir. +Z': self.resetview([0,0,-1],[0,0,0],[0,1,0])
        elif text == 'view dir. -Z': self.resetview([0, 0, 1],[0,0,0],[0,1,0])
        elif text == 'Surface culling':self.surfaceCulling()
        
        for ii in self.solverToolItems:
            if text==ii:
                self.chfreepanel(text)
    #-----------------------------------------------------------------------------------------------------
    def chfreepanel(self,whatitem):
    
        woMesh = ['Flow Conditions', 'Boundary Conditions', 'Cell Zone Conditions', 'Numerical Conditions',
                  'Monitoring', 'Run Conditions', 'Extract Data', 'Patch Display', 'Cutting Plane', 'Iso Surfaces', 'Clip', 'Streamline']
        self.displayPanel = ['Cutting Plane', 'Iso Surfaces', 'Patch Display', 'Cell Zone Conditions', 'Streamline']

        if whatitem in woMesh:
            if glob.glob(self.caseDir+'/constant/polyMesh')==[]:
                GEN = generalClass(self)
                GEN.makeDialog('Warning!!! There is not Mesh. Load mesh first')
                return
        
        if whatitem!='ParaFoam' and whatitem!='Stop' and whatitem!='Exit' and whatitem!='New Project' and whatitem!='Open Project':                    
            self.Widget_OriMarker.InteractiveOff()
            for ii in self.freevbox.get_children():
                self.freevbox.remove(ii)

        if whatitem == 'Flow Conditions':
            self.FREESIMULATION = freepanelSimulationClass(self)
            self.simulationbox = self.FREESIMULATION.simulation()
            self.freevbox.pack_start(self.simulationbox,True,True,0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'CfMesh':
            self.FREECFMESH = freepanelCfMeshClass(self)
            self.cfmeshbox = self.FREECFMESH.cfMesh()
            self.freevbox.pack_start(self.cfmeshbox,True,True,0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Mesh Manipulation':
            self.freevbox.pack_start(self.meshbox,True,True,0)
            self.displayMesh()
            self.initWin()
            self.notebook.set_current_page(0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Boundary Conditions':
            self.FREEBOUNDARY = freepanelBoundaryConditionClass(self)            
            self.FREEBOUNDARY.boundaryCondition(None)

            self.notebook.set_current_page(0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Cell Zone Conditions':
            self.FREECELLZONE = freepanelCellZoneClass(self)
            self.cellzonebox = self.FREECELLZONE.cellZone()
            self.freevbox.pack_start(self.cellzonebox,True,True,0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)

        elif whatitem == 'Numerical Conditions':
            self.FREENUMERICS = freepanelNumericsClass(self)
            self.numericbox = self.FREENUMERICS.numerics()
            self.freevbox.pack_start(self.numericbox, True, True, 0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Run Conditions':
            self.FREERUNCONDITION = freepanelRunConditionClass(self)
            self.runbox = self.FREERUNCONDITION.runCondition()
            self.freevbox.pack_start(self.runbox, True, True, 0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Monitoring':
            self.FREEMONITORING = freepanelMonitoringClass(self)
            self.monitorbox = self.FREEMONITORING.monitoring()
            self.freevbox.pack_start(self.monitorbox,True,True,0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem
            
        elif whatitem == 'Extract Data':
            self.FREEREPORT = freepanelReportClass(self)
            self.reportbox = self.FREEREPORT.report()
            self.freevbox.pack_start(self.reportbox,True,True,0)
            if self.nowPanel in self.displayPanel:
                self.discombo.append_text('Feature')
            self.nowPanel = whatitem

        elif whatitem == 'Cutting Plane':
            self.FREECUTTINGPLANE = freepanelCuttingPlaneClass(self)
            self.cuttingPlanebox = self.FREECUTTINGPLANE.cuttingPlane()
            self.freevbox.pack_start(self.cuttingPlanebox,True,True,0)
            self.notebook.set_current_page(0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)
            
        elif whatitem == 'Iso Surfaces':
            self.FREEISOSURFACE = freepanelIsoSurfaceClass(self)
            self.isoSurfacebox = self.FREEISOSURFACE.isoSurface()
            self.freevbox.pack_start(self.isoSurfacebox,True,True,0)
            self.notebook.set_current_page(0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)

        elif whatitem == 'Patch Display':
            self.FREEPATCHSCALAR = freepanelPatchScalarClass(self)
            self.patchScalarbox = self.FREEPATCHSCALAR.patchScalar()
            self.freevbox.pack_start(self.patchScalarbox, True, True, 0)
            self.notebook.set_current_page(0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)
            
        elif whatitem == 'Clip':
            self.FREECLIP = freepanelClipClass(self)
            self.clipbox = self.FREECLIP.clip()
            self.freevbox.pack_start(self.clipbox,True,True,0)
            self.notebook.set_current_page(0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)

        elif whatitem == 'Streamline':
            self.FREESTREAM = freepanelStreamTracerClass(self)
            #self.streambox = self.FREESTREAM.streamTracer()
            self.FREESTREAM.streamTracer()
            #self.freevbox.pack_start(self.streambox,True,True,0)
            self.notebook.set_current_page(0)
            self.nowPanel = whatitem
            if self.discombo.child.get_text() == 'Feature':
                self.discombo.child.set_text('Surface')
            self.discombo.remove_text(3)
            
        self.window.show_all()                
    #------------------------------------------------------------------------------------------------------                  
    def closedialog(self):

        GEN = generalClass(self)
        res = GEN.makeDialog_question('Exit this program ?')
        if res == -9:
            return
        else:
            home = expanduser("~")
            size = self.window.get_size()
            GEN.pickleDump(home + '/.OpenFOAM/windowSize', size)
            gtk.main_quit() 
    #---------------------------------------------------------------------------------------------  
    def newcase(self):
    
        GEN = generalClass(self)
        returnedname = GEN.newcase()
        if returnedname != 'None':
            if glob.glob(returnedname + '/*') == []:        
                self.caseDir = returnedname
                self.window.set_title(self.ver + ', ' + self.caseDir)                
                self.resetNewCase()

                cmd = 'cd ' + self.caseDir + '\n'
                self.terminal.feed_child(cmd, len(cmd))                                    

                self.renderer.RemoveAllViewProps()
                for ii in self.bdbox.get_children():
                    self.bdbox.remove(ii) 
                self.selectedPatch = None
                self.VTK_All = VTKStuff(self.caseDir)                
                self.window.show_all()
            else:
                GEN.makeDialog('Error!!! ' + self.caseDir + ' is already exist. Define new name')
                return
                
        if glob.glob(self.caseDir + '/Running'):
            os.system('rm ' + self.caseDir + '/Running')                 
    #-------------------------------------------------------------------------------------------------    
    def readcase(self):
    
        GEN = generalClass(self)
        returnedname = GEN.readcase()
        if returnedname != 'None':
            self.caseDir = returnedname
            self.checkCase()            
            self.notebook.set_current_page(1)
            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd, len(cmd))
            self.window.set_title(self.ver + ', ' + self.caseDir)            

            for ii in self.freevbox.get_children():
                self.freevbox.remove(ii)        
            self.meshbox = self.meshPart()
            self.freevbox.pack_start(self.meshbox, True, True, 0)
            self.window.show_all()
            
            self.notebook.set_current_page(0)
            
        if glob.glob(self.caseDir + '/Running'):
            os.system('rm ' + self.caseDir + '/Running')
            
        #self.displayMesh()
        
    #------------------------------------------------------------------------------------------           
    def saveAs(self):
    
        clonename = self.saveas()
        if clonename != 'None':
            home = expanduser("~") 
            if self.caseDir == home + '/.OpenFOAM/Baram_temporary':
                os.system('rm -rf ' + self.caseDir)
            elif self.caseDir[:-1] == home + '/.OpenFOAM/Baram_temporary':
                os.system('rm -rf ' + self.caseDir)
                
            self.caseDir = clonename
            self.window.set_title(self.ver + ', ' + self.caseDir)
            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd, len(cmd))
            self.window.show_all()
           
        if glob.glob(self.caseDir + '/Running'):
            os.system('rm ' + self.caseDir + '/Running')            
    #------------------------------------------------------------------------------------------
    def cloneCase(self):
    
        clonename = self.clone()
        if clonename != 'None':
            home = expanduser("~") 
            if self.caseDir == home + '/.OpenFOAM/Baram_temporary':
                os.system('rm -rf ' + self.caseDir)
            elif self.caseDir[:-1] == home + '/.OpenFOAM/Baram_temporary':
                os.system('rm -rf ' + self.caseDir)
        
            self.caseDir = clonename
            self.window.set_title(self.ver + ', ' + self.caseDir)
            cmd = 'cd ' + self.caseDir + '\n'
            self.terminal.feed_child(cmd,len(cmd))
            self.window.show_all()
            
        if glob.glob(self.caseDir + '/Running'):
            os.system('rm ' + self.caseDir + '/Running')
    #-------------------------------------------------------------------------------------
    def saveas(self):
    
        dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, 
					gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            clonename = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            clonename = 'None'
        dialog.destroy()
        if clonename != 'None':
            os.system('cp -r ' + self.caseDir + '/* ' + clonename + '/')
        
        if os.path.isfile(self.caseDir + '/Running'):
            os.system('rm ' + self.caseDir + '/Running')
        return clonename
    #-------------------------------------------------------------------------------------
    def clone(self):
    
        dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,
                    gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            clonename = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            clonename = 'None'
        dialog.destroy()
        if clonename != 'None':
            os.system('cp -r ' + self.caseDir + '/0 ' + clonename + '/')
            os.system('cp -r ' + self.caseDir + '/constant ' + clonename + '/')
            os.system('cp -r ' + self.caseDir + '/system ' + clonename + '/')
        return clonename
    #---------------------------------------------------------------------------------------------    
    def checkCase(self):
        
        GEN = generalClass(self)
        if not os.path.isfile(self.caseDir + '/system/controlDict'):
            GEN.makeDialog('Error!!! This case is not properly saved')
            return  
                    
        b1 = glob.glob(self.caseDir + '/system/settings')
        b2 = glob.glob(self.caseDir + '/logfiles')
        
        if b1 == []:
            os.system('mkdir -p ' + self.caseDir + '/system/settings')
        if b2 == []:
            os.system('mkdir -p ' + self.caseDir + '/logfiles')
    #----------------------------------------------------------------------------------------------------
    def resetview(self, viewposition, target, up):
    
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(viewposition[0], viewposition[1], viewposition[2])
        camera.SetFocalPoint(target[0], target[1], target[2])
        camera.SetViewUp(up[0],up[1],up[2])

        self.renderer.SetActiveCamera(camera)
        self.renderer.ResetCamera()
        self.gvtk.Initialize()
    #----------------------------------------------------------------------------------------------------
    def resetSize(self):
    
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
    # ------------------------------------------------------------------------------------------------------
    # mesh part
    # ------------------------------------------------------------------------------------------------------
    def meshPart(self):
    
        self.displayMesh()

        self.meshbox = gtk.VBox()        
        self.vpan = gtk.VPaned()
        self.meshbox.pack_start(self.vpan, True, True, 0)
        
        self.treebox = gtk.VBox(False, 0)
        self.treebox.set_size_request(400, 100)
        self.valuebox = gtk.VBox(False, 0)
        self.valuebox.set_size_request(400, 10)
        
        self.vpan.pack1(self.treebox, False, True)
        self.vpan.pack2(self.valuebox,False, True)
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        self.treebox.pack_start(frame, False, False, 0)
        label = gtk.Label()
        label.set_markup('<b>  Mesh  </b>')
        label.set_alignment(0, 0.5)
        label.set_size_request(-1, 45)
        ebox = gtk.EventBox()
        ebox.add(label)
        frame.add(ebox)        
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.treebox.add(swin)
        self.vbox = gtk.VBox()
        swin.add_with_viewport(self.vbox)
                
        self.ccombo = gtk.combo_box_entry_new_text()
        self.ccombo.set_size_request(160, 28)
        utils = ['OpenFOAM', 'fluentMeshToFoam', 'fluent3DMeshToFoam', 'StarCCM+ ccm', 'Gmsh msh', 'Ideas unv']
        for ii in utils:
            self.ccombo.append_text(ii)
        self.ccombo.set_active(0)

        self.selmeshB = gtk.Button('Select')
        self.selmeshB.set_size_request(100, 28)
        self.selmeshB.connect('clicked', self.selectmesh)
        hbox = gtk.HBox(False, 5)
        self.vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Load mesh'), False, False, 10)
        hbox.pack_end(self.selmeshB, False, False, 5)
        hbox.pack_end(self.ccombo, False, False, 0)
        #-----------------------------------------------------------------------------------------------
        plusB = gtk.Button('✔')
        plusB.set_size_request(24, 24)
        plusB.connect('clicked', self.selall)
        plusB.set_tooltip_text('Select All')
        
        minusB = gtk.Button('✖')
        minusB.set_size_request(24, 24)
        minusB.connect('clicked', self.deselall)
        minusB.set_tooltip_text('Select None')
        
        hbox = gtk.HBox(False, 5)
        self.vbox.pack_start(hbox, False, False, 10)
        hbox.pack_start(gtk.Label('Display Patch'), False, False, 10)
        hbox.pack_end(minusB, False, False, 5)
        hbox.pack_end(plusB, False, False, 0)
        #--------------------------------------------------------------------------------
        self.scwin = gtk.ScrolledWindow()
        self.scwin.set_border_width(0)
        self.scwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.vbox.pack_start(self.scwin, True, True, 0)

        vbox = gtk.VBox(False, 0)
        self.bdbox = gtk.HBox(False, 0)
        vbox.pack_start(self.bdbox, True, True, 0)
        self.scwin.add_with_viewport(vbox)
        #--------------------------------------------------------------------------------
        self.checkMeshB = gtk.Button('Check Mesh')
        self.meshInfoB = gtk.Button('Mesh Information')
        self.crbaffleB = gtk.Button('Create Baffle')
        self.refineLayerB = gtk.Button('Refine Layer')
        self.transformB = gtk.Button('Transform Mesh')
        
        self.checkMeshB.set_size_request(100, 28)
        self.meshInfoB.set_size_request(100, 28)
        self.crbaffleB.set_size_request(100, 28)
        self.refineLayerB.set_size_request(100, 28)
        self.transformB.set_size_request(100, 28)
        
        self.checkMeshB.connect('clicked', self.checkMesh)
        self.meshInfoB.connect('clicked', self.meshInfo)
        self.crbaffleB.connect('clicked', self.createBaffle)
        self.refineLayerB.connect('clicked', self.refineWallLayer)
        self.transformB.connect('clicked', self.transformMesh)
        
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.meshInfoB, True, True, 0)
        hbox.pack_start(self.checkMeshB,True,True,0)
        
        hbox = gtk.HBox(False, 0)
        self.valuebox.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.transformB, True, True, 0)
        hbox.pack_start(self.refineLayerB, True, True, 0)
        hbox.pack_start(self.crbaffleB, True, True, 0)
        
        self.initWin()
               
        return self.meshbox
    #------------------------------------------------------------------------------------------------------------------
    def selall(self,widget):
    
        self.treestore.clear()
        for i in range(len(self.bcNameList)):
            self.treestore.append(None, [self.pixbuf_main, self.bcNameList[i], True])
            self.View_Object1(True, self.bcNameList[i])
            self.displayPatchDict[self.bcNameList[i]] = True
    #------------------------------------------------------------------------------------------------------------------
    def deselall(self,widget):
    
        self.treestore.clear()
        for i in range(len(self.bcNameList)):
            self.treestore.append(None, [self.pixbuf_main, self.bcNameList[i], False])
            self.View_Object1(False, self.bcNameList[i])
            self.displayPatchDict[self.bcNameList[i]] = False
    #------------------------------------------------------------------------------------------------------------------
    def initWin(self):
    
        self.VTK_All = VTKStuff(self.caseDir)
        if not self.bcNameList == False :
            self.renderer.RemoveAllViewProps()
            if glob.glob(self.caseDir + '/VTK'):
                self.vtkActors, self.vtkFeatureActors, self.domainRange = \
                    self.VTK_All.unsgeometryVTK_feature(self.bcNameList, self.renderer,self.discombo.child.get_text())
            self.renderer.ResetCamera()
            self.viewbc()                
    #------------------------------------------------------------------------------------------------------------------
    def selectmesh(self, widget):
    
        GEN = generalClass(self)
        MESH = meshManipulationClass(self)
        util = self.ccombo.child.get_text()
        
        if util == 'OpenFOAM':
            meshfile = MESH.readMesh()
            aa = meshfile.split('/')
            if aa[-1] != 'polyMesh':
                GEN.makeDialog('Error!!! Select "polyMesh" folder')
                return
        else:
            meshfile = MESH.importMeshutil(util)       
                   
        if meshfile == 'None':
            return

        if os.path.isdir(self.caseDir + '/constant'):
            os.system('pyFoamClearCase.py ' + self.caseDir)
        
        runfile = self.caseDir + '/loadMesh'
        finishfile = self.caseDir + '/loadMeshFinished'        
        if os.path.isfile(runfile):
            os.system('rm ' + runfile)
        if os.path.isfile(finishfile):
            os.system('rm ' + finishfile)
        
        if glob.glob(self.caseDir + '/0/*'):
            os.system('rm -r ' + self.caseDir + '/0/*')
        if glob.glob(self.caseDir + '/constant/polyMesh'):
            os.system('rm -r ' + self.caseDir + '/constant/polyMesh')
        if glob.glob(self.caseDir + '/VTK'):
            os.system('rm -r ' + self.caseDir + '/VTK')
        if glob.glob(self.caseDir + '/constant') == []:
            os.system('mkdir ' + self.caseDir + '/constant')
                    
        self.notebook.set_current_page(1) 
        
        f = open(runfile, 'w')                       
        if util == 'OpenFOAM':        
            f.write('cp -r ' + meshfile + ' ' + self.caseDir + '/constant/polyMesh \n')
        else:
            if util == 'fluentMeshToFoam' or util == 'fluent3DMeshToFoam':            
                if util == 'fluentMeshToFoam':
                    f.write('fluentMeshToFoam -writeSets -writeZones ' + meshfile + '\n')
                else:
                    f.write('fluent3DMeshToFoam ' + meshfile + '\n')
            elif util=='StarCCM+ ccm':
                f.write('ccm26ToFoam ' + meshfile + '\n')
            elif util=='Gmsh msh':
                f.write('gmshToFoam ' + meshfile + '\n')
            elif util=='Ideas unv':
                f.write('ideasUnvToFoam ' + meshfile + '\n')
        f.write('foamToVTK -constant -noInternal  -noFaceZones -case ' + self.caseDir + '\n')
        f.write('touch ' + finishfile)
        f.close()
        
        time.sleep(0.1)        

        os.system('chmod +x ' + runfile)
        
        cmd = './loadMesh \n'
        self.terminal.feed_child(cmd, len(cmd))
        
        self.lock = threading.Lock()
        
        t1 = threading.Thread(name = 'update', target = self.getGeometry)
        t1.daemon = True
        t1.start()
    #---------------------------------------------------------------------------------------------------------                    
    def getGeometry(self):
    
        with self.lock:
        
            GEN=generalClass(self)

            runfile = self.caseDir + '/loadMesh'
            finishfile = self.caseDir + '/loadMeshFinished'
            
            while(not os.path.isfile(finishfile)):
                pass

            time.sleep(0.5)
                        
            if os.path.isfile(runfile):
                os.system('rm ' + runfile)
            if os.path.isfile(finishfile):
                os.system('rm ' + finishfile)

            self.displayPatchDict = {}
            self.bcNameList, bctypeList = GEN.getBCName()
            for ii in self.bcNameList:
                self.displayPatchDict[ii] = True

            filesToDel=[self.caseDir + '/system/settings/cellZoneSetup',### 
                        self.caseDir + '/system/cellZoneConditions*',
                        self.caseDir + '/system/settings/BCDict:*',
                        self.caseDir + '/system/settings/boundaryTypes',
                        self.caseDir + '/system/settings/boundaryConditions',
                        self.caseDir + '/system/settings/AMIConditions',
                        self.caseDir + '/system/settings/boundaryValues']
                        
            for ii in filesToDel:
                files = glob.glob(ii)
                if files:
                    for jj in files:
                        os.system('rm '+ii)

            self.selectedPatch = None                  
            self.notebook.set_current_page(0)

            self.initWin()             
    #---------------------------------------------------------------------------------------------------------                    
    def viewbc(self):
    
        if os.path.isfile(self.caseDir+'/constant/polyMesh/boundary'):

            for ii in self.bdbox.get_children():
                self.bdbox.remove(ii)

            vbox=gtk.VBox(False,0)
            self.bdbox.pack_start(vbox,True,True,0)
            
            self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, bool)
            
            for ii in self.bcNameList:
                self.treestore.append(None, [self.pixbuf_main, ii, True])
                
            self.treeview = gtk.TreeView(self.treestore)
            self.treeview.connect('cursor-changed', self.selected)
            self.treeview.set_grid_lines(False)
            
            self.tvcolumn0 = gtk.TreeViewColumn('Boundary Name')
            self.tvcolumn1 = gtk.TreeViewColumn('OnOff')            
            self.tvcolumn1.set_alignment(0.5)
            
            self.treeview.append_column(self.tvcolumn0)
            self.treeview.append_column(self.tvcolumn1)
            
            self.renbuf = gtk.CellRendererPixbuf()
            self.ren0 = gtk.CellRendererText()           
                       
            self.toggleren = gtk.CellRendererToggle()
            self.toggleren.set_property('activatable', True)

            self.tvcolumn0.pack_start(self.renbuf, False)
            self.tvcolumn0.pack_start(self.ren0, False)
            self.tvcolumn1.pack_end(self.toggleren, True)
            
            self.tvcolumn0.set_attributes(self.renbuf, pixbuf=0)
            self.tvcolumn0.set_attributes(self.ren0, text=1)
            self.tvcolumn1.add_attribute(self.toggleren, 'active', 2)            
            self.tvcolumn0.set_resizable(True)
            
            self.toggleren.connect('toggled', self.toggleMesh, self.treestore)            
            self.treeview.expand_all()
            
            vbox.add(self.treeview)            
            self.bdbox.show_all()
    #-----------------------------------------        
    def toggleMesh(self,widget,path,model):
    
        model[path][2] = not model[path][2]
        patch = model[path][1]        
        self.View_Object1(model[path][2], patch)
        self.displayPatchDict[patch] = model[path][2]              
    #---------------------------------------------------------------------------------------------------------        
    def selected(self,widget):
    
        self.selection = self.treeview.get_selection()
        tree_model, tree_iter = self.selection.get_selected()
        path = tree_model.get_path(tree_iter)            
        
        self.oldpatch = self.selectedPatch
        self.selectedPatch = self.bcNameList[path[0]]        
        
        self.highlightColor()
    #-----------------------------------------------------------------------------
    def highlightColor(self):
    
        if os.path.isdir(self.caseDir + '/VTK'):            
            if self.oldpatch:
                oldind = self.bcNameList.index(self.oldpatch)
            if self.selectedPatch:
                newind=self.bcNameList.index(self.selectedPatch)                
            
            if self.displayMode == 'SurfaceEdge' or self.displayMode == 'Surface' or self.displayMode == 'Wireframe':
                for i in range(self.renderer.GetActors().GetNumberOfItems()):
                    self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetColor(1,1,1)          
                self.vtkActors[newind].GetProperty().SetColor(0,0,1)                
            elif self.displayMode == 'Feature':
                for ii in self.vtkActors:
                    self.renderer.RemoveActor(ii)
                if self.displayPatchDict[self.selectedPatch] == True:
                    self.renderer.AddActor(self.vtkActors[newind])
                    self.vtkActors[newind].GetProperty().SetColor(0,0,1)
                    self.vtkActors[newind].GetProperty().EdgeVisibilityOff()
                    self.vtkActors[newind].GetProperty().SetRepresentation(2)
        self.gvtk.Initialize()   
    #-----------------------------------------
    def View_Object1(self, trueOrNot, patch):
    
        ind = self.bcNameList.index(patch)        
        if os.path.isdir(self.caseDir+'/VTK'):
            if trueOrNot:
                if self.discombo.child.get_text() == 'Feature':
                    self.renderer.AddActor(self.vtkFeatureActors[ind])
                else:
                    self.renderer.AddActor(self.vtkActors[ind])
            else:
                if self.discombo.child.get_text() == 'Feature':
                    self.renderer.RemoveActor(self.vtkFeatureActors[ind]) 
                else:
                    self.renderer.RemoveActor(self.vtkActors[ind]) 
        self.gvtk.Initialize()
    #---------------------------------------------------------------------------------------------------------            
    def changeDisplayMode(self,widget):
    
        self.displayMode = self.discombo.child.get_text()
                
        panel1 = ['CfMesh', 'Mesh Manipulation', 'Flow Conditions', 'Boundary Conditions',
                  'Numerical Conditions', 'Monitoring', 'Run Conditions', 'Extract Data']
        
        if self.nowPanel in panel1:        
            self.renderer.RemoveAllViewProps()
            if self.displayMode == 'SurfaceEdge' or self.displayMode == 'Surface' or self.displayMode == 'Wireframe':
                for j in range(len(self.bcNameList)):
                    if self.displayPatchDict[self.bcNameList[j]] == True:
                        self.renderer.AddActor(self.vtkActors[j])
            elif self.displayMode == 'Feature':
                for j in range(len(self.bcNameList)):
                    if self.displayPatchDict[self.bcNameList[j]] == True:
                        self.renderer.AddActor(self.vtkFeatureActors[j])
                        if self.backgroudColor=='white':
                            self.vtkFeatureActors[j].GetProperty().SetColor(0,0,0)
                        else:
                            self.vtkFeatureActors[j].GetProperty().SetColor(1,1,1)            
                
        num = self.renderer.GetActors().GetNumberOfItems()
        
        if self.displayMode == 'Surface':
            for i in range(num):
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().EdgeVisibilityOff()
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentation(2)
        elif self.displayMode == 'SurfaceEdge':
            for i in range(num):
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().EdgeVisibilityOn()
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentation(2)
        elif self.displayMode == 'Wireframe':
            for i in range(num):
                self.renderer.GetActors().GetItemAsObject(i).GetProperty().SetRepresentationToWireframe()

        if self.nowPanel == 'Cell Zone Conditions':
            if self.displayMode == 'SurfaceEdge':
                for j in range(len(self.bcNameList)):
                    self.vtkFeatureActors[j].GetProperty().EdgeVisibilityOff()
                    if self.backgroudColor=='white':
                        self.vtkFeatureActors[j].GetProperty().SetColor(0,0,0)
                    else:
                        self.vtkFeatureActors[j].GetProperty().SetColor(1,1,1)
        
        self.gvtk.Initialize()
    # -------------------------------------------------------------------------
    def meshInfo(self,widget):
    
        GEN = generalClass(self)
        filename = self.caseDir + '/constant/polyMesh/owner'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                ff = f.readlines()
            
            splited = None
            
            for ii in ff:
                striped = ii.strip()
                if striped[:4] == 'note':
                    splited = striped.split()
                    point = splited[1][1:]
                    cell = splited[2]
                    face = splited[3]
                    
            if splited == None:
                os.system('renumberMesh -overwrite -case ' + self.caseDir + '> /dev/null 2>&1')
                
                with open(filename, 'r') as f:
                    ff = f.readlines()
                
                for ii in ff:
                    striped = ii.strip()
                    if striped[:4] == 'note':
                        splited = striped.split()
                        point = splited[1][1:]
                        cell = splited[2]
                        face = splited[3]                
            
            nPoint = point.split(':')[1]
            nCell = cell.split(':')[1]
            nFace = face.split(':')[1]
            
            xmin = '%0.6f'%self.domainRange[0]
            xmax = '%0.6f'%self.domainRange[1]
            ymin = '%0.6f'%self.domainRange[2]
            ymax = '%0.6f'%self.domainRange[3]
            zmin = '%0.6f'%self.domainRange[4]
            zmax = '%0.6f'%self.domainRange[5]
            GEN.makeDialog_info('Mesh information \n\n' \
                + 'Number of cells : ' + nCell + '\n\n' \
                + 'Number of faces : ' + nFace + '\n\n' \
                + 'Number of points : ' + nPoint + '\n\n' \
                + 'Domain Range \n' \
                + '    x : '+xmin + ' ~ ' + xmax + '\n' \
                + '    y : '+ymin + ' ~ ' + ymax + '\n' \
                + '    z : '+zmin + ' ~ ' + zmax + '\n'  )
                
        else:
            GEN.makeDialog('Error!!! There is not mesh') 
    #---------------------------------------------------------------------------------------------------------            
    def createBaffle(self,widget):

        def closethis(widget):
            window.destroy()
    
        def makeBaffle(widget):
            mode = scombo.get_active()
            if mode == 0: 
                selectedSet = []
                tf = []
                for i in range(len(sets)):
                    if setName[i].get_active() == True:
                        selectedSet.append(sets[i])		
                WFILE.topoSetDict(selectedSet)
                WFILE.createBafflesDict(selectedSet)
                
                os.system('topoSet -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.topoSet')
                cmd = 'cat  ' + self.caseDir + '/logfiles/log.setsToZones\n'
                self.terminal.feed_child(cmd,len(cmd))
        
                os.system('createBaffles -case ' + self.caseDir + ' -overwrite > ' + self.caseDir + '/logfiles/log.createBaffles')
                cmd = 'cat ' + self.caseDir + '/logfiles/log.createBaffles\n'
                self.terminal.feed_child(cmd,len(cmd))

                os.system('foamToVTK -noInternal -noFaceZones -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.foamToVTK')
                cmd = 'cat ' + self.caseDir + '/logfiles/log.foamToVTK\n'
                self.terminal.feed_child(cmd,len(cmd))
                
                os.system('rm -r ' + self.caseDir + '/constant/polyMesh/sets') # sets file is no longer valid after createBaffles
            else:
                selectedZone = []
                tff = []
                for i in range(len(zones)):
                    if zoneName[i].get_active() == True:
                        selectedZone.append(zones[i])		
                WFILE.createBafflesDict(selectedZone)

                os.system('createBaffles -case ' + self.caseDir + ' -overwrite > ' + self.caseDir + '/logfiles/log.createBaffles')
                cmd = 'cat ' + self.caseDir + '/logfiles/log.createBaffles\n'
                self.terminal.feed_child(cmd,len(cmd))

                os.system('foamToVTK -noInternal -noFaceZones -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.foamToVTK')
                cmd = 'cat ' + self.caseDir + '/logfiles/log.foamToVTK\n'
                self.terminal.feed_child(cmd,len(cmd))

            self.bcNameList, bcTypeList = GEN.getBCName()
            self.displayPatchDict = {}
            for ii in self.bcNameList:
                self.displayPatchDict[ii] = True
            
            dic={}
            dic1={}
            for i in range(len(selectedSet)):
                dic['type'] = 'thermoCoupledWall'
                dic['couplePatch'] = selectedSet[i] + '_slave'
                dic1['type'] = 'thermoCoupledWall'
                dic1['couplePatch'] = selectedSet[i] + '_master'
                self.AMIDict[selectedSet[i] + '_master'] = dic
                self.AMIDict[selectedSet[i] + '_slave'] = dic1
            GEN.pickleDump(self.caseDir + '/system/settings/AMIConditions', self.AMIDict)
            
            if os.path.isfile(self.caseDir + '/system/settings/boundaryTypes'):
                os.system('rm '+self.caseDir + '/system/settings/boundaryTypes')
        
            self.initWin()
            window.destroy()
            self.meshbox.show_all()                
            
        def chscombo(widget, sets, zones, hbox1, hbox11, setName, zoneName):
            sss = scombo.get_active()
            if sss == 1:
                for i in range(len(sets)):
                    itembox.remove(hbox1[i])
                for i in range(len(zones)):
                    itembox.pack_start(hbox11[i], False, False, 2)
                scombo.set_active(1)
                window.show_all()
            else: 
                for i in range(len(zones)):
                    itembox.remove(hbox11[i])
                for i in range(len(sets)):
                    itembox.pack_start(hbox1[i], False, False, 2)
                scombo.set_active(0)
                window.show_all()

        GEN = generalClass(self)
        WFILE = writeFileClass(self.caseDir)
        sets = GEN.getSets()
        zones = GEN.getfaceZones()
        sets.sort()
        zones.sort()
        
        self.AMIDict = GEN.pickleLoad(self.caseDir + '/system/settings/AMIConditions')
        if self.AMIDict == None:
            self.AMIDict = {}

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('create baffle')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.window)
        
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)
        scombo = gtk.combo_box_entry_new_text()
        scombo.set_size_request(200, 28)
        scombo.append_text('use faceSet')
        scombo.append_text('use faceZone')
        scombo.set_active(0)
        hbox0 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(scombo, False, False, 5)
        swin = gtk.ScrolledWindow()
        swin.set_border_width(5)
        swin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        mainbox.pack_start(swin, True, True, 5)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)      
        swin.set_size_request(300,500)
        
        setName = []
        hbox1 = []                
        for i in range(len(sets)):
            hbox1.append(gtk.HBox(False, 5))
            itembox.pack_start(hbox1[i], False, False, 2)                
            setName.append(gtk.CheckButton(sets[i], use_underline = False))
            setName[i].set_size_request(180, 28)
            hbox1[i].pack_start(setName[i], False, False, 0)
        zoneName = []
        hbox11 = []
        for i in range(len(zones)):
            hbox11.append(gtk.HBox(False, 5))
            zoneName.append(gtk.CheckButton(zones[i], use_underline = False))
            zoneName[i].set_size_request(180, 28)
            hbox11[i].pack_start(zoneName[i], False, False, 0)
        scombo.connect('changed', chscombo, sets, zones, hbox1, hbox11, setName, zoneName)
        hbox2 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox2, False, False, 5)
        app = gtk.Button('Apply')
        app.set_size_request(100, 28)
        cll = gtk.Button('Cancel')
        cll.set_size_request(100, 28)
        app.connect('clicked', makeBaffle)
        cll.connect('clicked', closethis)
        hbox2.pack_end(cll, False, False, 5)
        hbox2.pack_end(app, False, False, 5)  
        window.show_all()    
    #---------------------------------------------------------------------------------------------------------            
    def transformMesh(self,widget):
    
        def transform(wiget):
            if combo.child.get_text() == 'Scale':
                xscale = scaleEntrys[0].get_text()
                yscale = scaleEntrys[1].get_text()
                zscale = scaleEntrys[2].get_text()
                os.system("transformPoints -case " + self.caseDir + " -scale '(" + xscale + ' ' + yscale + ' ' + zscale + ")'")
                os.system('foamToVTK -constant -noInternal -noFaceZones -case ' + self.caseDir) 
            elif combo.child.get_text() == 'Translate':
                xtrans = transEntrys[0].get_text()
                ytrans = transEntrys[1].get_text()
                ztrans = transEntrys[2].get_text()
                os.system("transformPoints -case " + self.caseDir + " -translate '(" + xtrans + ' ' + ytrans + ' ' + ztrans + ")'")
                os.system('foamToVTK -constant -noInternal -noFaceZones -case ' + self.caseDir) 
            elif combo.child.get_text() == 'Rotate':
                xrot = rotateEntrys[0].get_text()
                yrot = rotateEntrys[1].get_text()
                zrot = rotateEntrys[2].get_text()
                os.system("transformPoints -case " + self.caseDir + " -rollPitchYaw '(" + xrot + ' ' + yrot + ' ' + zrot + ")'")
                os.system('foamToVTK -constant -noInternal -noFaceZones -case ' + self.caseDir)               
            self.initWin()
            win.destroy()                   
        
        def chTransType(widget):
            for ii in selbox.get_children():
                selbox.remove(ii)
            if combo.child.get_text() == 'Scale':
                selbox.pack_start(boxs[0], False, False, 5)
            elif combo.child.get_text() == 'Translate':
                selbox.pack_start(boxs[1], False, False, 5)
            elif combo.child.get_text() == 'Rotate':
                selbox.pack_start(boxs[2], False, False, 5)
            win.show_all()                 
        
        MESH = meshManipulationClass(self)
        win, app, combo, scaleEntrys, transEntrys, rotateEntrys, selbox, boxs = MESH.transformMeshWindow()
        app.connect('clicked', transform)
        combo.connect('changed', chTransType)        
        win.show_all() 
    #---------------------------------------------------------------------------------------------------------                            
    def checkMesh(self, widget):
    
        GEN = generalClass(self)    
        az = self.caseDir + '/constant/polyMesh/boundary'
        with open(az, 'r') as filea:
            lines = filea.readlines()
        line1 = []  
        for i in range(16,len(lines)):
            a = (lines[i]).strip()
            if a == '{':
                line1.append(i)
        for i in line1:
            bb = (lines[i-1]).strip()
            b = bb[0]
            if GEN.isNumber(b):
                GEN.makeDialoge('Warning!!! Some patch name begin with number\n It might have some problem') 
            
        self.notebook.set_current_page(1)
        cmd = 'checkMesh -case ' + self.caseDir +'\n'
        self.terminal.feed_child(cmd,len(cmd))       
    #---------------------------------------------------------------------------------------------------------                            
    def refineWallLayer(self, widget):
    
        def doRefineWallLayer(wiget):
            edgeFraction = fracEntry.get_text()        
            selected = []
            for i in range(len(setName)):
                if setName[i].get_active() == 1:
                    selected.append(setName[i].get_label())                    
            string = ''
            for ii in selected:
                string = string + ' ' + ii                
            os.system('refineWallLayer -overwrite -case ' + self.caseDir + " '(" + string + ")' " + edgeFraction)
            os.system('foamToVTK -constant -noInternal -noFaceZones -case ' + self.caseDir)
            win.destroy()            
            self.initWin()        
        
        MESH = meshManipulationClass(self)
        win, app, fracEntry, setName = MESH.refineWallLayerWindow()
        app.connect('clicked', doRefineWallLayer)        
        win.show_all()
    #---------------------------------------------------------------------------------------------------------
    def displayMesh(self):
    
        self.displayPatchDict = {}
        self.displayMode = self.discombo.child.get_text()
        if glob.glob(self.caseDir + '/constant/polyMesh/boundary'):
            GEN = generalClass(self)
            self.bcNameList, bcTypeList = GEN.getBCName()
            for ii in self.bcNameList:
                self.displayPatchDict[ii] = True
            self.initWin()
        else:
            self.bcNameList = []
            self.vtkActors = []
            self.vtkFeatureActors = []
            #self.vtkActors = None
            #self.vtkFeatureActors = None
        self.selectedPatch = None        
    #--------------------------------------------------------------------------------------
    def chbg(self,widget):
    
        color = self.bgCombo.child.get_text()
        if color == 'white':
            self.backgroudColor = 'white'
            self.rr = 1
            self.gg = 1
            self.bb = 1
        elif color == 'black':
            self.backgroudColor = 'black'
            self.rr = 0
            self.gg = 0
            self.bb = 0
        elif color == 'paraview':
            self.backgroudColor = 'paraview'
            self.rr = 0.32
            self.gg = 0.34
            self.bb = 0.43
        self.renderer.SetBackground(self.rr, self.gg, self.bb)
        
        self.gvtk.Initialize()
        
        if self.displayMode == 'Feature':
            self.changeDisplayMode(None)
            
        self.window.show_all()
    #--------------------------------------------------------------------------------------
    def resetNewCase(self):
    
        os.system('rm -rf ' + self.caseDir)
        os.system('createCase -case ' + self.caseDir + ' simpleNFoam > /dev/null 2>&1')
        os.system('mkdir ' + self.caseDir + '/0')
        os.system('mkdir ' + self.caseDir + '/constant')
        os.system('mkdir ' + self.caseDir + '/logfiles')
        os.system('mkdir ' + self.caseDir + '/system/settings')
        os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/system/fvS* ' + self.caseDir + '/system/')
        os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/system/numericConditions ' + self.caseDir + '/system/settings/')                
        os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/constant/transportProperties ' + self.caseDir + '/constant/')
        os.system('cp ' + self.installpath + '/DictFile/5.0/simpleNFoam/constant/turbulenceProperties ' + self.caseDir + '/constant/')    
    #--------------------------------------------------------------------------------------------
    def leftButtonPressEvent(self, obj, event):   
    
        if self.displayMode == 'Feature':
            return
     
        clickPos = self.gvtk.GetEventPosition()

        self.cellPicker.Pick(clickPos[0], clickPos[1], 0, self.renderer)        
        NewPickedActor = self.cellPicker.GetActor()

        if NewPickedActor:
            self.selectedActor = NewPickedActor
            
            actorType = NewPickedActor.GetMapper().GetInput().GetCellType(0)        
            #if actorType == 9:

            for i in range(len(self.vtkActors)):
                if self.selectedActor == self.vtkActors[i]:
                    self.vtkActors[i].GetProperty().SetColor(0,0,1)
                    if self.nowPanel == 'Mesh Manipulation':
                        path = (i,)
                        self.treeview.set_cursor(path)
                    elif self.nowPanel == 'Boundary Conditions':
                        path = (1,i,)
                        for ii in self.freevbox.get_children():
                            self.freevbox.remove(ii)
                        self.FREEBOUNDARY = freepanelBoundaryConditionClass(self)
                        self.FREEBOUNDARY.boundaryCondition(path)

                        self.notebook.set_current_page(0)
                        if self.nowPanel in self.displayPanel:
                            self.discombo.append_text('Feature')
                                        
                else:
                    self.vtkActors[i].GetProperty().SetColor(1,1,1)  

        return
        
                
