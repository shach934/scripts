#-*-coding:utf8-*-

import gtk
import pickle
import os
import math
import sys
import glob
import time

from generalSub import *
from VTKStuffClass import *
from writeFileSub import *

class meshManipulationClass:

    def __init__(self, mainself):

        self.caseDir = mainself.caseDir
        self.mainwindow = mainself.window
        
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.renderer = mainself.renderer
        
        self.GEN = generalClass(mainself)
        self.VTK_All = VTKStuff(mainself.caseDir)        
    #---------------------------------------------------------------------------------------------------------
    def cpMesh(self, name, util):
    
        self.notebook.set_current_page(1)
        cmd = 'cp -r ' + name + ' ' + self.caseDir + '/constant/polyMesh & \n' \
              + 'echo $! > ' + self.caseDir + '/system/settings/importPID' + '\n' \
              + 'fg 1' + '\n'

        self.terminal.feed_child(cmd, len(cmd))
    #---------------------------------------------------------------------------------------------------------
    def readMesh(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            stmesh = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            stmesh = 'None'
        dialog.destroy()
        
        return stmesh        
    #-------------------------------------------------------------------------------------------------      
    def importMeshutil(self, util):
                          
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       

        if util == 'fluentMeshToFoam' or util == 'fluent3DMeshToFoam':
            filter = gtk.FileFilter()
            filter.set_name("Fluent")
            patterns = ['*.msh', '*.Msh', '*.MSH', '*.cas', '*.CAS', '*.Cas']
            for ii in patterns:
                filter.add_pattern(ii)
            dialog.add_filter(filter)
        elif util == 'StarCCM+ ccm':
            filter = gtk.FileFilter()
            filter.set_name("StarCCM+")        
            filter.add_pattern("*.ccm")
            filter.add_pattern("*.CCM")
            filter.add_pattern("*.Ccm")
            dialog.add_filter(filter)
        elif util == 'Gmsh msh':
            filter = gtk.FileFilter()
            filter.set_name("Gmsh")        
            filter.add_pattern("*.msh")
            filter.add_pattern("*.MSH")
            filter.add_pattern("*.Msh")    
            dialog.add_filter(filter) 
        elif util == 'Ideas unv':        
            filter = gtk.FileFilter()
            filter.set_name("ideasUnv")        
            filter.add_pattern("*.UNV")
            filter.add_pattern("*.unv")
            filter.add_pattern("*.Unv")        
            dialog.add_filter(filter) 
            
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            if util == 'fluentMeshToFoam' or util == 'fluent3DMeshToFoam':
                if filename[-3:].lower() != 'msh' and filename[-3:].lower() != 'cas':
                    self.GEN.makeDialog('Error!!! Selected file is not fluent mesh.')
                    filename = 'None'
            elif util == 'StarCCM+ ccm':
                if filename[-3:].lower() != 'ccm':
                    self.GEN.makeDialog('Error!!! Selected file is not ccm file')
                    filename = 'None'
            elif util == 'Gmsh msh':
                if filename[-3:].lower() != 'msh':
                    self.GEN.makeDialog('Error!!! Selected file is not ccm file')
                    filename = 'None'
            elif util == 'Ideas unv':
                if filename[-3:].lower() != 'unv':
                    self.GEN.makeDialog('Error!!! Selected file is not ccm file')
                    filename = 'None'                    
        elif response == gtk.RESPONSE_CANCEL:
            filename = 'None'
        dialog.destroy()
               
        return filename
    #-------------------------------------------------------------------------------------------------      
    def convertm(self, name, util): # not used
        
        logDir = self.caseDir + '/system/settings'
        
        if name != 'None':
            self.notebook.set_current_page(1)
            os.system('pyFoamClearCase.py ' + self.caseDir)
            if len(glob.glob(self.caseDir + '/0/*')) !=0 :
                os.system('rm -r ' + self.caseDir + '/0/*')
            if glob.glob(self.caseDir + '/constant/polyMesh'):
                os.system('rm -r ' + self.caseDir + '/constant/polyMesh')
            if glob.glob(self.caseDir + '/system/settings/boundaryConditions'):
                os.system('rm -r ' + self.caseDir + '/system/settings/boundaryConditions')
            if glob.glob(self.caseDir + '/VTK'):
                os.system('rm -r ' + self.caseDir + '/VTK')
            
            if util == 'fluentMeshToFoam' or util == 'fluent3DMeshToFoam':            
                if util == 'fluentMeshToFoam':
                    cmd = 'fluentMeshToFoam -writeSets -writeZones -case ' + self.caseDir + ' ' + name + ' & \n' \
                          + 'echo $! > ' + logDir + '/importPID' + '\n' \
                          + 'fg 1' + '\n'
                else:
                    cmd = 'fluent3DMeshToFoam -case ' + self.caseDir + ' ' + name + ' & \n' \
                          + 'echo $! > ' + logDir + '/importPID' + '\n' \
                          + 'fg 1' + '\n'
            elif util=='StarCCM+ ccm':
                cmd = 'ccm26ToFoam -case ' + self.caseDir + ' ' + name + ' & \n' \
                      + 'echo $! > ' + logDir + '/importPID' + '\n' \
                      + 'fg 1' + '\n'
            elif util=='Gmsh msh':
                cmd = 'gmshToFoam -case ' + self.caseDir + ' ' + name + ' & \n' \
                      + 'echo $! > ' + logDir + '/importPID' + '\n' \
                      + 'fg 1' + '\n'
            elif util=='Ideas unv':
                cmd = 'ideasUnvToFoam -case ' + self.caseDir + ' ' + name + ' & \n' \
                      + 'echo $! > ' + logDir + '/importPID' + '\n' \
                      + 'fg 1' + '\n'

            self.terminal.feed_child(cmd, len(cmd))
    #-------------------------------------------------------------------------------------------------      
    def convertToVTK(self): # not used
    
        logDir = self.caseDir + '/system/settings'
    
        importPIDFile = open(logDir + '/importPID', 'r')
        importPID = int(importPIDFile.read())
        
        while(self.GEN.isRunning(importPID)):
            pass
    
        cmd = 'foamToVTK -constant -noInternal  -noFaceZones -case ' + self.caseDir + \
              ' & \n' + 'echo $! > ' + logDir + '/foamToVTKPID' + '\n' \
              + 'fg 1' + '\n'
              
        self.terminal.feed_child(cmd, len(cmd))           
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def createBaffleWindow(self):
        
        sets = self.GEN.getSets()
        sets.sort()        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('create baffle')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)
        
        hbox0 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(gtk.Label('faceSets'), False, False, 5)
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(5)
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        swin.set_size_request(300, 500)
        mainbox.pack_start(swin, True, True, 5)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)        
        
        setName = []
        hbox1 = []                
        for i in range(len(sets)):
            hbox1.append(gtk.HBox(False, 5))
            itembox.pack_start(hbox1[i], False, False, 2)                
            setName.append(gtk.CheckButton(sets[i], use_underline = False))
            setName[i].set_size_request(180, 28)
            hbox1[i].pack_start(setName[i], False, False, 0)
        hbox2 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox2, False, False, 5)
        app = gtk.Button('Apply')
        app.set_size_request(100, 28)
        cll = gtk.Button('Cancel')
        cll.set_size_request(100, 28)
        cll.connect('clicked', self.closeBaffle, window)
        hbox2.pack_end(cll, False, False, 5)
        hbox2.pack_end(app, False, False, 5)
        return window, app, setName
        
    def closeBaffle(self, wiget, window):
        window.destroy()        
    #---------------------------------------------------------------------------------------------------------            
    def transformMeshWindow(self):

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Transform mesh')
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
        combo = gtk.combo_box_entry_new_text()
        combo.set_size_request(150, 28)
        typelist = ['Scale', 'Translate', 'Rotate']
        for ii in typelist:
            combo.append_text(ii)
        combo.set_active(0)
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Transform type'), False, False, 5)
        hbox.pack_end(combo, False, False, 5)

        selbox = gtk.VBox(False, 5)
        vbox.pack_start(selbox, False, False, 5)

        scalebox = gtk.VBox(False, 5)
        selbox.pack_start(scalebox, False, False, 5)
        hbox = gtk.HBox(False, 5)
        scalebox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Scale factors for x, y, z'), False, False, 5)
        scalex = gtk.Entry()
        scaley = gtk.Entry()
        scalez = gtk.Entry()
        scalex.set_size_request(80, 28)
        scaley.set_size_request(80, 28)
        scalez.set_size_request(80, 28)
        scalex.set_text('0.001')
        scaley.set_text('0.001')
        scalez.set_text('0.001')
        hbox = gtk.HBox(False, 5)
        scalebox.pack_start(hbox, False, False, 5)
        hbox.pack_end(scalez, False, False, 5)
        hbox.pack_end(scaley,False,False,0)
        hbox.pack_end(scalex, False, False, 5)

        translatebox = gtk.VBox(False, 5)
        hbox = gtk.HBox(False, 5)
        translatebox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Translate factors for x, y, z [m]'), False, False, 5)
        transx = gtk.Entry()
        transy = gtk.Entry()
        transz = gtk.Entry()
        transx.set_size_request(80, 28)
        transy.set_size_request(80, 28)
        transz.set_size_request(80, 28)
        transx.set_text('1')
        transy.set_text('0')
        transz.set_text('0')
        hbox = gtk.HBox(False, 5)
        translatebox.pack_start(hbox, False, False, 5)
        hbox.pack_end(transz, False, False, 5)
        hbox.pack_end(transy,False,False,0)
        hbox.pack_end(transx, False, False, 5)

        rotatebox = gtk.VBox(False, 5)
        hbox = gtk.HBox(False, 5)
        rotatebox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Rotate Angle for x, y, z [deg]'), False, False, 5)        
        rotatex = gtk.Entry()
        rotatey = gtk.Entry()
        rotatez = gtk.Entry()
        rotatex.set_size_request(80, 28)
        rotatey.set_size_request(80, 28)
        rotatez.set_size_request(80, 28)
        rotatex.set_text('90')
        rotatey.set_text('0')
        rotatez.set_text('0')
        hbox = gtk.HBox(False, 5)
        rotatebox.pack_start(hbox, False, False, 5)
        hbox.pack_end(rotatez, False, False, 5)
        hbox.pack_end(rotatey,False,False,0)
        hbox.pack_end(rotatex, False, False, 5)

        appB = gtk.Button('Apply')
        clsB = gtk.Button('Close')
        clsB.connect('clicked', self.closeTransform,window)
        appB.set_size_request(100, 28)
        clsB.set_size_request(100, 28)
        bubox = gtk.HBox(False, 5)
        mainbox.pack_start(bubox, False, False, 5)
        bubox.pack_end(clsB, False, False, 5)
        bubox.pack_end(appB, False, False, 5)
        
        scaleEntrys = [scalex, scaley, scalez]
        transEntrys = [transx, transy, transz]
        rotateEntrys = [rotatex, rotatey, rotatez]
        boxs = [ scalebox, translatebox, rotatebox]
        
        return window, appB, combo, scaleEntrys, transEntrys, rotateEntrys, selbox, boxs

    def closeTransform(self, wiget, window):
        window.destroy()  
    #---------------------------------------------------------------------------------------------------------                            
    def checkMesh(self, widget):

        az = self.caseDir + '/constant/polyMesh/boundary'
        with open(az, 'r') as filea:
            lines=filea.readlines()
        line1 = []  
        for i in range(16, len(lines)):
            a = (lines[i]).strip()
            if a == '{':
                line1.append(i)
        for i in line1:
            bb = (lines[i-1]).strip()
            b = bb[0]
            if self.GEN.isNumber(b):
                self.GEN.makeDialoge('Warning!!! Some patch name begin with number\n It might have some problem')  
                
        os.system('checkMesh -case ' + self.caseDir + ' > ' + self.caseDir + '/logfiles/log.checkMesh')
        cmd = 'cat  '+ self.caseDir + '/logfiles/log.checkMesh\n'
        self.terminal.feed_child(cmd,len(cmd))
        self.notebook.set_current_page(1)                     
    #---------------------------------------------------------------------------------------------------------                            
    def refineWallLayerWindow(self):

        bcs, types = self.GEN.getBCName()
        bcs.sort()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('refineWallLayer')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox=gtk.VBox(False, 5)
        window.add(mainbox)
            
        fracEntry = gtk.Entry()
        fracEntry.set_size_request(100, 28)
        fracEntry.set_text('0.5')
        hbox0 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(gtk.Label('Edge fraction [0~1]'), False, False, 5)
        hbox0.pack_start(fracEntry, False, False, 5)
            
        hbox0=gtk.HBox(False, 5)
        mainbox.pack_start(hbox0, False, False, 0)
        hbox0.pack_start(gtk.Label('Select patches to refine'), False, False, 5)
            
        swin = gtk.ScrolledWindow()
        swin.set_border_width(5)
        swin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        swin.set_size_request(300, 500)
        mainbox.pack_start(swin, True, True, 5)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)        
        setName = []
        hbox1 = []                
        for i in range(len(bcs)):
            hbox1.append(gtk.HBox(False, 5))
            itembox.pack_start(hbox1[i], False, False, 2)                
            setName.append(gtk.CheckButton(bcs[i], use_underline = False))
            setName[i].set_size_request(180, 28)
            hbox1[i].pack_start(setName[i], False, False, 0)

        hbox2 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox2, False, False, 5)
        app = gtk.Button('Apply')
        app.set_size_request(100, 28)
        cll = gtk.Button('Cancel')
        cll.set_size_request(100, 28)
        cll.connect('clicked', self.closeRefine,window)
        hbox2.pack_end(cll, False, False, 5)
        hbox2.pack_end(app, False, False, 5)  
        
        return window, app, fracEntry, setName
        
    def closeRefine(self, wiget, window):
        window.destroy()

    #---------------------------------------------------------------------------------------------------------
    def cyclicAMIWindow(self, patch, newtype):
    
        bcNameList, polyPatchTypeList = self.GEN.getBCName()
        nametype = {}
        for i in range(len(bcNameList)):
            nametype[bcNameList[i]] = polyPatchTypeList[i]

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Select Interface')
        window.set_border_width(5)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        mainbox=gtk.VBox(False, 5)
        window.add(mainbox)

        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Select coupled patch'), False, False, 15)            
        
        swin = gtk.ScrolledWindow()
        swin.set_border_width(5)
        swin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        mainbox.pack_start(swin, True, True, 5)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)
        scheight = len(bcNameList) * 38
        if scheight > 750:
            scheight = 750        
        swin.set_size_request(300, scheight)

        setName = []
        for i in range(len(bcNameList)):
            hbox1 = gtk.HBox(False, 5)
            itembox.pack_start(hbox1, False, False, 2)                
            setName.append(gtk.CheckButton(bcNameList[i], use_underline = False))
            setName[i].set_size_request(180, 28)
            if nametype[bcNameList[i]] != 'cyclicAMI' and bcNameList[i] != patch:
                hbox1.pack_start(setName[i], False, False, 0)

        if newtype == 'rotationalPeriodic':        
            r1Entry = gtk.Entry()
            r2Entry = gtk.Entry()
            r3Entry = gtk.Entry()
            r1Entry.set_size_request(60, 28)
            r2Entry.set_size_request(60, 28)
            r3Entry.set_size_request(60, 28)
            r1Entry.set_text('0')
            r2Entry.set_text('0')
            r3Entry.set_text('0')
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('rotationCenter'), False, False, 5)
            hbox.pack_end(r3Entry, False, False, 5)
            hbox.pack_end(r2Entry, False, False, 5)
            hbox.pack_end(r1Entry, False, False, 5)

            label2 = gtk.Label('rotationAxis')
            axisCombo = gtk.combo_box_entry_new_text()
            axisCombo.set_size_request(120, 28)
            axisCombo.append_text('x')
            axisCombo.append_text('y')
            axisCombo.append_text('z')
            axisCombo.set_active(2)
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(label2, False, False, 5)
            hbox.pack_end(axisCombo, False, False, 5)

        elif newtype == 'translationalPeriodic':
            c1Entry = gtk.Entry()
            c2Entry = gtk.Entry()
            c3Entry = gtk.Entry()
            c1Entry.set_size_request(60, 28)
            c2Entry.set_size_request(60, 28)
            c3Entry.set_size_request(60, 28)
            c1Entry.set_text('0')
            c2Entry.set_text('0')
            c3Entry.set_text('0')
            hbox = gtk.HBox(False, 5)
            mainbox.pack_start(hbox, False, False, 5)
            hbox.pack_start(gtk.Label('Separation vector, 1st to 2nd'), False, False, 5)
            hbox.pack_end(c3Entry, False, False, 5)
            hbox.pack_start(c2Entry,False,False,0)
            hbox.pack_end(c1Entry, False, False, 5)
        
        hbox2 = gtk.HBox(False, 5)
        mainbox.pack_start(hbox2, False, False, 5)
        app = gtk.Button('Apply')
        app.set_size_request(100, 28)
        cll = gtk.Button('Close')
        cll.set_size_request(100, 28)
        cll.connect('clicked', self.closeAMIWindow,window)
        hbox2.pack_end(cll, False, False, 5)
        hbox2.pack_end(app, False, False, 5)
        
        return  
            
    def closeAMIWindow(self, wiget, window):
        window.destroy()      



        
        
        
        
