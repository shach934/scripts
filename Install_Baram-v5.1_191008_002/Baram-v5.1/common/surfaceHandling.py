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

class surfaceClass:

    def delete_event(self, widget, event):
        print 'window is deleted'
        
    def __init__(self, mainself):
    
        self.caseDir = mainself.caseDir
        self.installpath = mainself.installpath
        self.mainwindow = mainself.window
        self.terminal = mainself.terminal
        self.notebook = mainself.notebook
    #-----------------------------------------------------------------------------------------------------------------
    def surfaceScale(self):

        GEN = generalClass(self)

        def closethis(widget):
            window.destroy()

        def applythis(widget):
            sx = xEntry.get_text()
            sy = yEntry.get_text()
            sz = zEntry.get_text()
        
            f = open(self.caseDir + '/system/settings/scalestl','w')
            f.write('cd ' + self.caseDir + '\n')
            for ii in self.selectedfile:
                bb = ii.split('/')
                nn = bb[-1]
                f.write("surfaceTransformPoints -scale '(" + sx + " " + sy + " " + sz + ")' " + ii + " scaled_" + nn + "\n")
            f.close()
            os.system('chmod +x ' + self.caseDir + '/system/settings/scalestl')
            os.system(self.caseDir + '/system/settings/scalestl')
            
            window.destroy()

        def selectSTL(widget):
            self.selectedfile=GEN.selSTL()
            string = ''
            for ii in self.selectedfile:
                string = string + ii + '\n'           
            self.textbuffer.set_text(string)         
        # ----------------------------------------------------
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Scale surface')
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)
        
        mainvbox = gtk.VBox(False, 5)
        window.add(mainvbox)

        selectB = gtk.Button('Select STL file(s)')
        selectB.set_size_request(180, 28)
        selectB.connect('clicked', selectSTL)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(selectB, False, False, 5)
        
        sw = gtk.ScrolledWindow()
        sw.set_border_width(0)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(400, 100)
        textview = gtk.TextView()
        self.textbuffer = textview.get_buffer()
        sw.add_with_viewport(textview)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(sw, True, True, 5)
        
        xEntry = gtk.Entry()
        yEntry = gtk.Entry()
        zEntry = gtk.Entry()
        xEntry.set_size_request(80, 28)
        yEntry.set_size_request(80, 28)
        zEntry.set_size_request(80, 28)
        xEntry.set_text('0.001')
        yEntry.set_text('0.001')
        zEntry.set_text('0.001')                        
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Scale factor (x,y,z)'), False, False, 5)
        hbox.pack_end(zEntry, False, False, 5)
        hbox.pack_end(yEntry, False, False, 0)
        hbox.pack_end(xEntry, False, False, 5) 
        
        txt = '   - Output file name is "scaled_<selected file name>". \n   - The location of Output file is current working folder   '
        label = gtk.Label(txt)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 10)
        hbox.pack_start(label, False, False, 5)                      
        #------------------------------------------------------------------------------------------
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 2)
                
        buttonbox = gtk.HBox(False, 5)        
        mainvbox.pack_start(buttonbox, False, False, 5)
        
        app = gtk.Button('Apply')
        app.set_size_request(100, 30)
        cll = gtk.Button('Close')
        cll.set_size_request(100, 30)
        app.connect('clicked', applythis)
        cll.connect('clicked', closethis)
        buttonbox.pack_end(cll, False, False, 5)
        buttonbox.pack_end(app, False, False, 5) 
        
        window.show_all() 
    #-----------------------------------------------------------------------------------------------------------------
    def surfaceTranslate(self):

        GEN = generalClass(self)

        def closethis(widget):
            window.destroy()

        def applythis(widget):
            sx = xEntry.get_text()
            sy = yEntry.get_text()
            sz = zEntry.get_text()
        
            f = open(self.caseDir + '/system/settings/translatestl','w')
            f.write('cd ' + self.caseDir + '\n')
            for ii in self.selectedfile1:
                bb=ii.split('/');nn=bb[-1]
                f.write("surfaceTransformPoints -translate '("+sx+" "+sy+" "+sz+")' "+ii+" translated_"+nn+"\n")
            f.close()
            os.system('chmod +x ' + self.caseDir + '/system/settings/translatestl')
            os.system(self.caseDir + '/system/settings/translatestl')
            
            window.destroy()

        def selectSTL(widget):
            self.selectedfile1=GEN.selSTL()
            string=''
            for ii in self.selectedfile1:string=string+ii+'\n'           
            self.textbuffer1.set_text(string)         
        # ----------------------------------------------------
        window=gtk.Window(gtk.WINDOW_TOPLEVEL);window.set_title('Translate surface')
        window.set_border_width(10);window.set_position(gtk.WIN_POS_CENTER);window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)
        
        mainvbox=gtk.VBox(False, 5);window.add(mainvbox)

        selectB=gtk.Button('Select STL file(s)');selectB.set_size_request(180,28);selectB.connect('clicked',selectSTL)
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5);hbox.pack_start(selectB, False, False, 5)
        
        sw=gtk.ScrolledWindow();sw.set_border_width(0);sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(400,100)
        textview = gtk.TextView()
        self.textbuffer1 = textview.get_buffer()
        sw.add_with_viewport(textview)
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5);hbox.pack_end(sw, True, True, 5)
        
        label = gtk.Label('Vector (x,y,z)')
        xEntry=gtk.Entry();xEntry.set_size_request(80,28);xEntry.set_text('0')
        yEntry=gtk.Entry();yEntry.set_size_request(80,28);yEntry.set_text('0')
        zEntry=gtk.Entry();zEntry.set_size_request(80,28);zEntry.set_text('0')                        
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5);hbox.pack_end(zEntry, False, False, 5);hbox.pack_end(yEntry, False, False, 0);hbox.pack_end(xEntry, False, False, 5) 
        
        txt = '   - Output file name is "translated_<selected file name>". \n   - The location of Output file is current working folder   '
        label = gtk.Label(txt)
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 10);hbox.pack_start(label, False, False, 5)                      
        #------------------------------------------------------------------------------------------
        separator = gtk.HSeparator();separator.set_size_request(285,5);mainvbox.pack_start(separator,False,True,2)
                
        buttonbox=gtk.HBox(False, 5)        
        mainvbox.pack_start(buttonbox, False, False, 5)
        
        app=gtk.Button(label='Apply');app.set_size_request(100,30);cll=gtk.Button(label='Close');cll.set_size_request(100,30)
        app.connect('clicked',applythis);cll.connect('clicked',closethis)
        buttonbox.pack_end(cll, False, False, 5);buttonbox.pack_end(app, False, False, 5) 
        
        window.show_all() 
    #-----------------------------------------------------------------------------------------------------------------
    def splitSolids(self):

        GEN = generalClass(self)

        def closethis(widget,data=None):
            window.destroy()

        def applythis(widget,data=None):
        
            with open(self.selfile,'r') as f:
                ff = f.readlines()
            regionnames = []
            startlines = []
            for i in range(len(ff)):
                if ff[i][:5] == 'solid':
                    a1 = ff[i].split(' ')
                    regionnames.append(a1[1][:-1])
                    startlines.append(i+1)

            nlines = []
            for k in range(len(regionnames) - 1):
                cc = int(startlines[k+1]) - int(startlines[k])
                nlines.append(cc)
            nlines.append(len(ff) - int(startlines[-1]) + 1)
                                
            for j in range(len(regionnames)):
                g = open(self.caseDir + '/splited_' + regionnames[j] + '.stl','w')
                for ii in range(nlines[j]):
                    jj = startlines[j] -1 + ii
                    g.write(ff[jj])
                g.close()
            
            window.destroy()

        def selectSTL(widget):
            sflist = GEN.selSTL()
            if len(sflist) == 1:
                self.selfile = sflist[0]
            else:
                GEN.makeDialog('Error!!! Select only 1 file')
                return
                
            sourceEntry.set_text(self.selfile)
                
            with open(self.selfile,'r') as f:
                ff = f.readlines()
            regionnames = []
            for i in range(len(ff)):
                if ff[i][:5] == 'solid':
                    a1 = ff[i].split(' ')
                    regionnames.append(a1[1][:-1])

            string = ''
            for ii in regionnames:
                string = string + ii + '\n'
            self.textbuffer2.set_text(string)            
        # ----------------------------------------------------
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Split regions to separate file')
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)
        
        mainvbox = gtk.VBox(False, 5)
        window.add(mainvbox)

        selectB = gtk.Button('Select STL file')
        selectB.set_size_request(180, 28)
        selectB.connect('clicked', selectSTL)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(selectB, False, False, 5)
        
        sourceEntry = gtk.Entry()
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Source file'), False, False, 5)
        hbox.pack_end(sourceEntry, True, True, 5)
        
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Regions'), False, False, 5)
        
        sw = gtk.ScrolledWindow()
        sw.set_border_width(0)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(400, 100)
        textview = gtk.TextView()
        self.textbuffer2 = textview.get_buffer()
        sw.add_with_viewport(textview)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(sw, True, True, 5)
                   
        txt = '   - Output file name is "splited_<region name>". \n   - The location of Output file is current working folder   '
        label = gtk.Label(txt)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 10)
        hbox.pack_start(label, False, False, 5)                      
        #------------------------------------------------------------------------------------------
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 2)
                
        buttonbox = gtk.HBox(False, 5)        
        mainvbox.pack_start(buttonbox, False, False, 5)
        
        app = gtk.Button('Apply')
        app.set_size_request(100, 30)
        cll = gtk.Button('Close')
        cll.set_size_request(100, 30)
        app.connect('clicked', applythis)
        cll.connect('clicked', closethis)
        buttonbox.pack_end(cll, False, False, 5)
        buttonbox.pack_end(app, False, False, 5) 
        
        window.show_all()   
    #-----------------------------------------------------------------------------------------------------------------
    def mergeSTLs(self):

        GEN = generalClass(self)

        def closethis(widget):
            window.destroy()

        def applythis(widget):        
            g = open(self.caseDir + '/mergedSTLfile.stl', 'w')
            for ii in self.selectedfile3:
                with open(ii, 'r') as f:
                    ff = f.readlines()
                for jj in ff:
                    g.write(jj)
            g.close()
            
            window.destroy()

        def selectSTL(widget):
            self.selectedfile3 = GEN.selSTL()
            string = ''
            for ii in self.selectedfile3:
                string = string + ii + '\n'           
            self.textbuffer3.set_text(string)         
        # ----------------------------------------------------
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Merge STL files')
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)
        
        mainvbox = gtk.VBox(False, 5)
        window.add(mainvbox)

        selectB = gtk.Button('Select STL files')
        selectB.set_size_request(180,28)
        selectB.connect('clicked',selectSTL)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(selectB, False, False, 5)
        
        sw = gtk.ScrolledWindow()
        sw.set_border_width(0)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(400, 100)
        textview = gtk.TextView()
        self.textbuffer3 = textview.get_buffer()
        sw.add_with_viewport(textview)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_end(sw, True, True, 5)           
       
        txt = '   - Output file name is "mergedSTLfile.stl". \n   - The location of Output file is current working folder   '
        label = gtk.Label(txt)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 10)
        hbox.pack_start(label, False, False, 5)                      
        #------------------------------------------------------------------------------------------
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator,False,True, 2)
                
        buttonbox = gtk.HBox(False, 5)        
        mainvbox.pack_start(buttonbox, False, False, 5)
        
        app = gtk.Button('Apply')
        app.set_size_request(100, 30)
        cll = gtk.Button('Close')
        cll.set_size_request(100, 30)
        app.connect('clicked', applythis)
        cll.connect('clicked', closethis)
        buttonbox.pack_end(cll, False, False, 5)
        buttonbox.pack_end(app, False, False, 5) 
        
        window.show_all() 
    #-----------------------------------------------------------------------------------------------------------------
    def surfaceAutoPatch(self):

        GEN = generalClass(self)

        def closethis(widget):
            window.destroy()

        def applythis(widget):
        
            angle = angleEntry.get_text()
            outfile = outEntry.get_text()

            cmd = 'surfaceAutoPatch ' + self.selfile1 + ' ' + self.caseDir + '/' + outfile + ' ' + angle + '\n'
            self.terminal.feed_child(cmd,len(cmd))                        
            self.notebook.set_current_page(1)          
            window.destroy()
            
        def selectSTL(widget):
            aa = GEN.selSTLSingle()
            self.selfile1 = aa[0]            
            sourceEntry.set_text(self.selfile1)
            bb = self.selfile1.split('/')
            selname = bb[-1]
            outEntry.set_text('autoPatched_' + selname)
        # ----------------------------------------------------
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('surfaceAutoPatch')
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)
        
        mainvbox = gtk.VBox(False, 5)
        window.add(mainvbox)

        selectB = gtk.Button('Select STL file')
        selectB.set_size_request(180, 28)
        selectB.connect('clicked', selectSTL)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(selectB, False, False, 5)
        
        sourceEntry=gtk.Entry()
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Source file'), False, False, 5);hbox.pack_end(sourceEntry, True, True, 5)
        
        angleEntry=gtk.Entry();angleEntry.set_size_request(100,28);angleEntry.set_text('160')
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5);hbox.pack_start(gtk.Label('includedAngle'), False, False, 5);hbox.pack_end(angleEntry, False, False, 5)
        
        outEntry=gtk.Entry();outEntry.set_size_request(250,28)#;outEntry.set_text('160')
        hbox = gtk.HBox(False, 5);mainvbox.pack_start(hbox, False, False, 5);hbox.pack_start(gtk.Label('Output file name'), False, False, 5);hbox.pack_end(outEntry, False, False, 5)
                   
        txt = '   - Output file location is current working folder  '
        label = gtk.Label(txt)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 10)
        hbox.pack_start(label, False, False, 5)                      
        #------------------------------------------------------------------------------------------
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 2)
                
        buttonbox = gtk.HBox(False, 5)        
        mainvbox.pack_start(buttonbox, False, False, 5)
        
        app = gtk.Button('Apply')
        app.set_size_request(100, 30)
        cll = gtk.Button('Close')
        cll.set_size_request(100, 30)
        app.connect('clicked', applythis)
        cll.connect('clicked', closethis)
        buttonbox.pack_end(cll, False, False, 5)
        buttonbox.pack_end(app, False, False, 5) 
        
        window.show_all()
    # -----------------------------------------------------------------------------------------------------------------
    def createCylinder(self):

        GEN = generalClass(self)

        def closethis(widget):
            window.destroy()

        def applythis(widget):

            radius = radiusEntry.get_text()
            height = heightEntry.get_text()
            axis = axisCombo.child.get_text()
            xcenter = xEntry.get_text()
            ycenter = yEntry.get_text()
            zcenter = zEntry.get_text()
            name = nameEntry.get_text()

            sourcename = self.installpath + '/common/unitcylinder.stl'
            targetname = self.caseDir + '/' + name

            xscale = float(radius) * 2
            os.system("surfaceTransformPoints -scale '(" + str(xscale) + " " + str(
                xscale) + " " + height + ")' " + sourcename + " scale.stl")

            if axis == 'x':
                os.system("surfaceTransformPoints -yawPitchRoll '(0 90 0)' scale.stl rot.stl")
            elif axis == 'y':
                os.system("surfaceTransformPoints -yawPitchRoll '(0 0 90)' scale.stl rot.stl")
            else:
                os.system("cp scale.stl rot.stl")

            os.system(
                "surfaceTransformPoints -translate '(" + xcenter + " " + ycenter + " " + zcenter + ")' rot.stl " + targetname)

            window.destroy()
        # ----------------------------------------------------
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Create cylinder STL file')
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_transient_for(self.mainwindow)
        window.connect("delete_event", self.delete_event)

        mainvbox = gtk.VBox(False, 5)
        window.add(mainvbox)

        label = gtk.Label('Radius')
        radiusEntry = gtk.Entry()
        radiusEntry.set_text('0.5')
        radiusEntry.set_size_request(100, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(radiusEntry, False, False, 5)

        label = gtk.Label('Height')
        heightEntry = gtk.Entry()
        heightEntry.set_text('1')
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        heightEntry.set_size_request(100, 28)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(heightEntry, False, False, 5)

        label = gtk.Label('Axis')
        axisCombo = gtk.combo_box_entry_new_text()
        axisCombo.set_size_request(100, 28)
        axisCombo.append_text('x')
        axisCombo.append_text('y')
        axisCombo.append_text('z')
        axisCombo.set_active(2)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(axisCombo, False, False, 5)

        label = gtk.Label('Center      ')
        xEntry = gtk.Entry()
        yEntry = gtk.Entry()
        zEntry = gtk.Entry()
        xEntry.set_text('0')
        yEntry.set_text('0')
        zEntry.set_text('0')
        xEntry.set_size_request(80, 28)
        yEntry.set_size_request(80, 28)
        zEntry.set_size_request(80, 28)
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(zEntry, False, False, 5)
        hbox.pack_end(yEntry, False, False, 0)
        hbox.pack_end(xEntry, False, False, 5)

        label = gtk.Label('fileName')
        nameEntry = gtk.Entry()
        nameEntry.set_text('cylinder.stl')
        hbox = gtk.HBox(False, 5)
        mainvbox.pack_start(hbox, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_end(nameEntry, True, True, 5)
        # ------------------------------------------------------------------------------------------
        separator = gtk.HSeparator()
        separator.set_size_request(285, 5)
        mainvbox.pack_start(separator, False, True, 2)

        buttonbox = gtk.HBox(False, 5)
        mainvbox.pack_start(buttonbox, False, False, 5)

        app = gtk.Button(label='Apply')
        app.set_size_request(100, 30)
        cll = gtk.Button(label='Close')
        cll.set_size_request(100, 30)
        app.connect('clicked', applythis)
        cll.connect('clicked', closethis)
        buttonbox.pack_end(cll, False, False, 5)
        buttonbox.pack_end(app, False, False, 5)

        window.show_all()



