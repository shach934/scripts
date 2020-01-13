#-*-coding:utf8-*-

from common.fromAll     import *

class menuClass:

    def destroy(self,widget):
        self.Win.destroy()

    def __init__(self, mainself):
    
        self.caseDir = mainself.caseDir
        self.solver = mainself.solver
        self.mainwindow = mainself.window
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal

        self.renderer = mainself.renderer
        self.VTK_All = VTKStuff(mainself.caseDir)
        self.GEN = generalClass(mainself)        
    #--------------------------------------------------------------------------------------
    def newcase(self):
    
        dialog = gtk.FileChooserDialog("New..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            caseDir = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            caseDir = 'None'
        dialog.destroy()
        return caseDir
    #-------------------------------------------------------------------------------------------------
    def readcase(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            caseDir = dialog.get_filename()
            if glob.glob(caseDir+'/system/controlDict') == []:
                self.makeDialog('Error! This folder is not proper OpenFOAM case.\n There is not system/controlDict')
                caseDir = 'None'
        elif response == gtk.RESPONSE_CANCEL:
            caseDir = 'None'
        dialog.destroy()          
        return caseDir        
    #-------------------------------------------------------------------------------------
    def saveas(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
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
        return clonename
    #-------------------------------------------------------------------------------------
    def clone(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            clonename = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            clonename = 'None'
        dialog.destroy()
        if clonename != 'None':
            os.system('cp -r ' + self.caseDir + '/0 ' + clonename+'/')
            os.system('cp -r ' + self.caseDir + '/constant ' + clonename+'/')
            os.system('cp -r ' + self.caseDir + '/system ' + clonename+'/')
            os.system('cp ' + self.caseDir + '/FOAM_SETTINGS ' + clonename+'/')
        return clonename
    #-----------------------------------------------------------------------------------------------------
    def reconstructPar(self):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            f = open(self.caseDir + '/system/settings/reconstruct','w')
            if latestCB.get_active() == True:
                f.write('reconstructNPar -case ' + self.caseDir + ' -latestTime \n')
            else:
                if allCB.get_active() == True:
                    f.write('reconstructNPar -case ' + self.caseDir + '\n')
                else:
                    times = []
                    for ii in CBs:
                        if ii.get_active() == 1:
                            times.append(ii.get_label())
                    
                    f.write('reconstructNPar -case ' + self.caseDir + ' -time ')
                    for i in range(len(times) - 1):
                        f.write(times[i] + ',')
                    f.write(times[-1] + '\n')                
            f.write('rm -r ' + self.caseDir + '/processor* \n')
            f.close()
            
            os.system('chmod +x ' + self.caseDir + '/system/settings/reconstruct')            
            self.notebook.set_current_page(1)
            
            cmd = self.caseDir + '/system/settings/reconstruct\n'
            self.terminal.feed_child(cmd,len(cmd))            
            mwin.destroy()

        def chlast(widget):
            onOff = widget.get_active()
            if onOff == 1:
                for ii in CBs:
                    ii.set_sensitive(0)
                allCB.set_sensitive(0)
            else:
                for ii in CBs:
                    ii.set_sensitive(1)
                allCB.set_sensitive(1)

        def chall(widget):
            onOff = widget.get_active()
            if onOff == 1:
                for ii in CBs:
                    ii.set_sensitive(0)
                latestCB.set_sensitive(0)
            else:
                for ii in CBs:
                    ii.set_sensitive(1)
                latestCB.set_sensitive(1)
                        
        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('reconstructPar')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        swin = gtk.ScrolledWindow()
        swin.set_border_width(0)
        swin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        box1.pack_start(swin)
        itembox = gtk.VBox(False, 0)
        swin.add_with_viewport(itembox)
        swin.set_size_request(250, 500)

        latestCB = gtk.CheckButton('SourceTime is latestTime')
        latestCB.set_active(1)
        latestCB.connect('toggled', chlast)
        hbox = gtk.HBox(False, 5)
        itembox.pack_start(hbox, False, False, 5)
        hbox.pack_start(latestCB, False, False, 5)
            
        allCB = gtk.CheckButton('SourceTime is All')
        allCB.set_active(0)
        allCB.set_sensitive(0)
        allCB.connect('toggled',chall)
        hbox = gtk.HBox(False, 5)
        itembox.pack_start(hbox, False, False, 5)
        hbox.pack_start(allCB, False, False, 5)

        separator = gtk.HSeparator()
        separator.set_size_request(10, 5)
        itembox.pack_start(separator, False, True, 5)
        
        hbox = gtk.HBox(False, 5)
        itembox.pack_start(hbox, False, False, 5)
        hbox.pack_start(gtk.Label('Select times'), False, False, 10)
        
        if glob.glob(self.caseDir + '/processor*') != []:
            bb = os.listdir(self.caseDir + '/processor0/')
            res = []
            for ii in bb:
                if self.GEN.isNumber(ii) == True and ii != '0':
                    res.append(ii)
            intres = []
            for ii in res:
                intres.append(float(ii))
            intres.sort()
            results = []
            for jj in intres:
                results.append(str(jj))
                    
            CBs = []        
            for i in range(len(results)):
                CBs.append(gtk.CheckButton(results[i]))
                hbox = gtk.HBox(False, 5)
                itembox.pack_start(hbox, False, False, 5)
                hbox.pack_start(CBs[i], False, False, 30)
                CBs[i].set_sensitive(0)        
        else:
            self.GEN.makeDialog('There in no decomposed data')
            return
        
        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('reconstruct')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)

        mwin.show_all()
    #-----------------------------------------------------------------------------------------------------
    def readSetting(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            caseDir = dialog.get_filename()
            if glob.glob(caseDir+'/system/controlDict') == []:
                self.makeDialog('Error! This folder is not proper OpenFOAM case.\n There is not system/controlDict')
                caseDir = None
        elif response == gtk.RESPONSE_CANCEL:
            caseDir = None
        dialog.destroy()          

        if caseDir != None:
            os.system('cp ' + caseDir + '/system/settings/* ' + self.caseDir + '/system/settings/')
    #------------------------------------------------------------------------------------------
    def setFields(self, gvtk, renderer, dic):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            minx = minxEntry.get_text()
            miny = minyEntry.get_text()
            minz = minzEntry.get_text()
            maxx = maxxEntry.get_text()
            maxy = maxyEntry.get_text()
            maxz = maxzEntry.get_text()
            setFieldsRangeMin = '(' + minx + ' ' + miny + ' ' + minz + ')'
            setFieldsRangeMax = '(' + maxx + ' ' + maxy + ' ' + maxz+')'
            scalar = scCombo.child.get_text()
            dvalue = dvEntry.get_text()
            value = vEntry.get_text()	
            
            dic={}
            dic['minx'] = minx
            dic['miny'] = miny
            dic['minz'] = minz
            dic['maxx'] = maxx
            dic['maxy'] = maxy
            dic['maxz'] = maxz
            dic['scalar'] = scalar
            dic['default'] = dvalue
            dic['value'] = value;
            self.GEN.pickleDump(self.caseDir + '/system/settings/setFieldsSetup', dic)
            
            self.setFieldsDict(setFieldsRangeMin, setFieldsRangeMax, scalar, dvalue, value)
            
            bb = glob.glob(self.caseDir + '/0/U')
            pp = glob.glob(self.caseDir + '/processor*')
            if bb == []:
                self.makeDialog('Error!!! setFields should be done after initialize')
            else:
                if pp == []:
                    cmd = 'setFields -case ' + self.caseDir + '\n'
                else:    
                    cmd = 'mpirun -np ' + str(len(pp)) + ' setFields -case ' + self.caseDir + '\n'                   
                self.notebook.set_current_page(1)
                self.terminal.feed_child(cmd,len(cmd))        
            mwin.destroy()

        def setSavedValue():
            if os.path.isfile(self.caseDir + '/system/settings/setFieldsSetup'):
                dic = self.GEN.pickleLoad(self.caseDir + '/system/settings/setFieldsSetup')                
                minxEntry.set_text(dic['minx'])
                minyEntry.set_text(dic['miny'])
                minzEntry.set_text(dic['minz'])
                maxxEntry.set_text(dic['maxx'])
                maxyEntry.set_text(dic['maxy'])
                maxzEntry.set_text(dic['maxz'])
                scCombo.child.set_text(dic['scalar'])
                dvEntry.set_text(dic['default'])
                vEntry.set_text(dic['value'])
                
        def showregion(widget): 
            minx = minxEntry.get_text()
            miny = minyEntry.get_text()
            minz = minzEntry.get_text()
            maxx = maxxEntry.get_text()
            maxy = maxyEntry.get_text()
            maxz = maxzEntry.get_text() 
            
            self.notebook.set_current_page(0)            
            viewposition = [1,1,1]
            patchName, patchType = self.GEN.getBCName()
            VTK = VTKStuff(self.caseDir)
            actor, actors = VTK.showSetFieldRegion(minx, miny, minz, maxx, maxy, maxz, viewposition, patchName)
            renderer.RemoveAllViewProps()
            renderer.AddActor(actor)
            for ii in actors:
                renderer.AddActor(ii)            
            gvtk.Initialize()

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('setFields')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        minxEntry = gtk.Entry()
        minyEntry = gtk.Entry()
        minzEntry = gtk.Entry()
        minxEntry.set_text('0')
        minyEntry.set_text('0')
        minzEntry.set_text('0')
        minxEntry.set_size_request(60, 28)
        minyEntry.set_size_request(60, 28)
        minzEntry.set_size_request(60, 28)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)                
        hbox1.pack_start(gtk.Label('Min. x,y,z '), False, False, 5)
        hbox1.pack_end(minzEntry, False, False, 5)
        hbox1.pack_end(minyEntry, False, False, 5)
        hbox1.pack_end(minxEntry, False, False, 5)	

        maxxEntry = gtk.Entry()
        maxyEntry = gtk.Entry()
        maxzEntry = gtk.Entry()
        maxxEntry.set_text('0')
        maxyEntry.set_text('0')
        maxzEntry.set_text('0')
        maxxEntry.set_size_request(60, 28)
        maxyEntry.set_size_request(60, 28)
        maxzEntry.set_size_request(60, 28)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)                
        hbox2.pack_start(gtk.Label('Max. x,y,z '), False, False, 5)
        hbox2.pack_end(maxzEntry, False, False, 5)
        hbox2.pack_end(maxyEntry, False, False, 5)
        hbox2.pack_end(maxxEntry, False, False, 5)
            
        showB = gtk.Button('Display region')
        showB.set_size_request(160, 28)
        showB.connect('clicked', showregion)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)                
        hbox2.pack_end(showB, False, False, 5)            

        scCombo = gtk.combo_box_entry_new_text()
        scCombo.set_size_request(100, 28)
        
        scalars = []
        allitems = os.listdir(self.caseDir + '/0')
        for ii in allitems:
            if not os.path.isdir('./' + ii):
                scalars.append(ii)

        for ii in scalars:
            scCombo.append_text(ii)
        scCombo.set_active(0)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(gtk.Label('Select scalar'), False, False, 5)
        hbox3.pack_end(scCombo, False, False, 5)	

        dvEntry = gtk.Entry()
        dvEntry.set_size_request(100, 28)
        dvEntry.set_text('0')
        hbox4 = gtk.HBox(False, 5)
        box1.pack_start(hbox4, False, False, 5)
        hbox4.pack_start(gtk.Label('default value'), False, False, 5)
        hbox4.pack_end(dvEntry, False, False, 5)
	    
        vEntry = gtk.Entry()
        vEntry.set_size_request(100, 28)
        vEntry.set_text('0')
        hbox5 = gtk.HBox(False, 5)
        box1.pack_start(hbox5, False, False, 5)
        hbox5.pack_start(gtk.Label('fix value'), False, False, 5)
        hbox5.pack_end(vEntry, False, False, 5)

        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('setFields')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, True, True, 5)
        box2.pack_end(appB, True, True, 5)
        
        setSavedValue()
        mwin.show_all()
    #-----------------------------------------------------------------------------------------------------
    def setFieldsDict(self, setFieldsRangeMin, setFieldsRangeMax, scalar, defualtValue, value):
        f = open(self.caseDir + '/system/setFieldsDict','w')
        f.write("/*--------------------------------*- C++ -*----------------------------------*\ \n")
        f.write('| =========                 |                                                 |\n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        f.write('|  \\    /   O peration     | Version:  2.3.0                                 |\n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n')
        f.write('|    \\/     M anipulation  |                                                 |\n')
        f.write('\*---------------------------------------------------------------------------*/\n')
        f.write('FoamFile\n')
        f.write('{\n')
        f.write('    version     2.0;\n')
        f.write('    format      ascii;\n')
        f.write('    class       dictionary;\n')
        f.write('    object      setFieldsDict;\n')
        f.write('}\n')

        f.write('defaultFieldValues\n')
        f.write('(\n')
        f.write('    volScalarFieldValue ' + scalar + ' ' + defualtValue + ' \n')
        f.write(');\n')
        f.write('regions\n')
        f.write('(\n')
        f.write('    boxToCell\n')
        f.write('    {\n')
        f.write('        box ' + setFieldsRangeMin + ' ' + setFieldsRangeMax + ';\n')
        f.write('        fieldValues\n')
        f.write('        (\n')
        f.write('            volScalarFieldValue ' + scalar + ' ' + value + '\n')
        f.write('        );\n')
        f.write('    }\n')
        f.write('    boxToFace\n')
        f.write('    {\n')
        f.write('        box ' + setFieldsRangeMin + ' ' + setFieldsRangeMax + ';\n')
        f.write('        fieldValues\n')
        f.write('        (\n')
        f.write('            volScalarFieldValue ' + scalar + ' ' + value + '\n')
        f.write('        );\n')
        f.write('    }\n')         
        f.write(');\n')
        f.close()
    # -----------------------------------------------------------------------------------------------------
    def yPlusRAS(self):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            time = timeEntry.get_text()
            stime = stimeEntry.get_text()
            etime = etimeEntry.get_text()
            nozero = nozeroCB.get_active()

            if parCheckB.get_active() == False:
                par = ''
                par1 = ''
            else:
                par = 'mpirun -np ' + str(len(parlist)) + ' '
                par1 = ' -parallel'
                
            if glob.glob(self.caseDir + '/system/settings/simulationConditions'):
                dic = self.GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')
                RASModel = dic['Turbulence model']
            else:
                RASModel = 'kEpsilon'

            if RASModel == 'laminar':
                self.makeDialog('Error!!! This is laminar')
                mwin.destroy()
                return
            else:
                f = open(self.caseDir + '/system/settings/yplusras', 'w')
                if nozero == 0:
                    if selmethod == 'All':
                        f.write(par + self.solver + ' -postProcess -func yPlus -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'latestTime':
                        f.write(par + self.solver + ' -postProcess -func yPlus -latestTime -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'Time':
                        f.write(par + self.solver + ' -postProcess -func yPlus -time ' + time + ' -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'Time Range':
                        f.write(par + self.solver + ' -postProcess -func yPlus -time ' + stime + ':' + etime + ' -case ' + self.caseDir + par1 +'\n')
                else:
                    if selmethod == 'All':
                        f.write(par + self.solver + ' -postProcess -func yPlus -noZero -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'latestTime':
                        f.write(par + self.solver + ' -postProcess -func yPlus -noZero -latestTime -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'Time':
                        f.write(par + self.solver + ' -postProcess -func yPlus -noZero -time ' + time + ' -case ' + self.caseDir + par1 +'\n')
                    elif selmethod == 'Time Range':
                        f.write(par + self.solver + ' -postProcess -func yPlus -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + par1 +'\n')
                f.close()

                os.system('chmod +x ' + self.caseDir + '/system/settings/yplusras')
                self.notebook.set_current_page(1)
                cmd = self.caseDir + '/system/settings/yplusras\n'
                self.terminal.feed_child(cmd, len(cmd))
                mwin.destroy()

        def toggled(widget):
            selmethod = widget.child.get_text()
            if selmethod == 'All':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'latestTime':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time':
                timeEntry.set_sensitive(1)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time Range':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(1)
                etimeEntry.set_sensitive(1)

        selmethod = 'All'

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('yPlusRAS')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)
        
        parCheckB = gtk.CheckButton('Decomposed case')
        hbox = gtk.HBox()
        hbox.pack_start(parCheckB, False, False, 5)
        mainbox.pack_start(hbox, False, False, 5)
        
        parlist = glob.glob(self.caseDir + '/processor*')
        if len(parlist) == 0:
            parCheckB.set_active(0)
        else:
            parCheckB.set_active(1)        

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.set_label('    Select time to create y+    ')
        frame.set_label_align(0.1, 0.5)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        but0 = gtk.RadioButton(None,'All')
        but0.connect('toggled', toggled)
        hbox0 = gtk.HBox(False, 5)
        box1.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(but0, False, False, 5)

        but1 = gtk.RadioButton(but0, 'latestTime')
        but1.connect('toggled', toggled)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)
        hbox1.pack_start(but1, False, False, 5)

        but2 = gtk.RadioButton(but0, 'Time')
        but2.set_size_request(120, 28)
        but2.connect('toggled', toggled)
        timeEntry = gtk.Entry()
        timeEntry.set_size_request(60, 28)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)
        hbox2.pack_start(but2, False, False, 5)
        hbox2.pack_start(timeEntry, False, False, 5)

        but3 = gtk.RadioButton(but0, 'Time Range')
        but3.set_size_request(120, 28)
        but3.connect('toggled', toggled)
        stimeEntry = gtk.Entry()
        stimeEntry.set_size_request(60, 28)
        etimeEntry = gtk.Entry()
        etimeEntry.set_size_request(60, 28)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(but3, False, False, 5)
        hbox3.pack_start(stimeEntry, False, False, 5)
        hbox3.pack_start(gtk.Label('~'), False, False, 5)
        hbox3.pack_start(etimeEntry, False, False, 5)

        nozeroCB = gtk.CheckButton('noZero Option')
        hbox4 = gtk.HBox(False, 5)
        box1.pack_start(hbox4, False, False, 5)
        hbox4.pack_start(nozeroCB, False, False, 5)

        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('Apply')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)

        mwin.show_all()
    # -----------------------------------------------------------------------------------------------------
    def QCriterion(self):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            time = timeEntry.get_text()
            stime = stimeEntry.get_text()
            etime = etimeEntry.get_text()
            nozero = nozeroCB.get_active()

            f = open(self.caseDir + '/system/settings/QCriterion', 'w')
            if parCheckB.get_active() == False:
                if nozero == 0:
                    if selmethod == 'All':
                        f.write('postProcess -func Q -case ' + self.caseDir + '\n')
                    elif selmethod == 'latestTime':
                        f.write('postProcess -func Q -latestTime -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time':
                        f.write('postProcess -func Q -time ' + time + ' -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time Range':
                        f.write('postProcess -func Q -time ' + stime + ':' + etime + ' -case ' + self.caseDir + '\n')
                else:
                    if selmethod == 'All':
                        f.write('postProcess -func Q -noZero -case ' + self.caseDir + '\n')
                    elif selmethod == 'latestTime':
                        f.write('postProcess -func Q -noZero -latestTime -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time':
                        f.write('postProcess -func Q -noZero -time ' + time + ' -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time Range':
                        f.write('postProcess -func Q -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + '\n')
            else:
                if nozero == 0:
                    if selmethod == 'All':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'latestTime':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -latestTime -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -time ' + time + ' -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time Range':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -time ' + stime + ':' + etime + ' -case ' + self.caseDir + ' -parallel\n')
                else:
                    if selmethod == 'All':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -noZero -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'latestTime':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -noZero -latestTime -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -noZero -time ' + time + ' -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time Range':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func Q -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + ' -parallel\n')
            f.close()

            os.system('chmod +x ' + self.caseDir + '/system/settings/QCriterion')
            self.notebook.set_current_page(1)

            cmd = self.caseDir + '/system/settings/QCriterion\n'
            self.terminal.feed_child(cmd, len(cmd))
            mwin.destroy()

        def toggled(widget):
            selmethod = widget.child.get_text()
            if selmethod == 'All':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'latestTime':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time':
                timeEntry.set_sensitive(1)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time Range':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(1)
                etimeEntry.set_sensitive(1)

        selmethod = 'All'

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('Q-criterion')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        parCheckB = gtk.CheckButton('Decomposed case')
        hbox = gtk.HBox()
        hbox.pack_start(parCheckB, False, False, 5)
        mainbox.pack_start(hbox, False, False, 5)
        
        parlist = glob.glob(self.caseDir + '/processor*')
        if len(parlist) == 0:
            parCheckB.set_active(0)
        else:
            parCheckB.set_active(1)    
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.set_label('    Select time to create Q    ')
        frame.set_label_align(0.1, 0.5)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        but0 = gtk.RadioButton(None, 'All')
        but0.connect('toggled', toggled)
        hbox0 = gtk.HBox(False, 5)
        box1.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(but0, False, False, 5)

        but1 = gtk.RadioButton(but0, 'latestTime')
        but1.connect('toggled', toggled)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)
        hbox1.pack_start(but1, False, False, 5)

        but2 = gtk.RadioButton(but0, 'Time')
        but2.set_size_request(120, 28)
        but2.connect('toggled', toggled)
        timeEntry = gtk.Entry()
        timeEntry.set_size_request(60, 28)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)
        hbox2.pack_start(but2, False, False, 5)
        hbox2.pack_start(timeEntry, False, False, 5)

        but3 = gtk.RadioButton(but0, 'Time Range')
        but3.set_size_request(120, 28)
        but3.connect('toggled', toggled)
        stimeEntry = gtk.Entry()
        stimeEntry.set_size_request(60, 28)
        etimeEntry = gtk.Entry()
        etimeEntry.set_size_request(60, 28)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(but3, False, False, 5)
        hbox3.pack_start(stimeEntry, False, False, 5)
        hbox3.pack_start(gtk.Label('~'), False, False, 5)
        hbox3.pack_start(etimeEntry, False, False, 5)

        nozeroCB = gtk.CheckButton('noZero Option')
        hbox4 = gtk.HBox(False, 5)
        box1.pack_start(hbox4, False, False, 5)
        hbox4.pack_start(nozeroCB, False, False, 5)

        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('Apply')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)

        mwin.show_all()
    # -----------------------------------------------------------------------------------------------------
    def vorticity(self):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            time = timeEntry.get_text()
            stime = stimeEntry.get_text()
            etime = etimeEntry.get_text()
            nozero = nozeroCB.get_active()

            f = open(self.caseDir + '/system/settings/vorticity', 'w')
            if parCheckB.get_active()==False:
                if nozero == 0:
                    if selmethod == 'All':
                        f.write('postProcess -func vorticity -case ' + self.caseDir + '\n')
                    elif selmethod == 'latestTime':
                        f.write('postProcess -func vorticity -latestTime -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time':
                        f.write('postProcess -func vorticity -time ' + time + ' -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time Range':
                        f.write('postProcess -func vorticity -time ' + stime + ':' + etime + ' -case ' + self.caseDir + '\n')
                else:
                    if selmethod == 'All':
                        f.write('postProcess -func vorticity -noZero -case ' + self.caseDir + '\n')
                    elif selmethod == 'latestTime':
                        f.write('postProcess -func vorticity -noZero -latestTime -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time':
                        f.write('postProcess -func vorticity -noZero -time ' + time + ' -case ' + self.caseDir + '\n')
                    elif selmethod == 'Time Range':
                        f.write('postProcess -func vorticity -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + '\n')
            else:
                if nozero == 0:
                    if selmethod == 'All':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'latestTime':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -latestTime -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -time ' + time + ' -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time Range':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -time ' + stime + ':' + etime + ' -case ' + self.caseDir + ' -parallel\n')
                else:
                    if selmethod == 'All':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -noZero -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'latestTime':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -noZero -latestTime -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -noZero -time ' + time + ' -case ' + self.caseDir + ' -parallel\n')
                    elif selmethod == 'Time Range':
                        f.write('mpirun -np '+str(len(parlist))+' postProcess -func vorticity -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + ' -parallel\n')
            f.close()

            os.system('chmod +x ' + self.caseDir + '/system/settings/vorticity')
            self.notebook.set_current_page(1)

            cmd = self.caseDir + '/system/settings/vorticity\n'
            self.terminal.feed_child(cmd, len(cmd))
            mwin.destroy()

        def toggled(widget):
            selmethod = widget.child.get_text()
            if selmethod == 'All':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'latestTime':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time':
                timeEntry.set_sensitive(1)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time Range':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(1)
                etimeEntry.set_sensitive(1)

        selmethod = 'All'

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('vorticity')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        parCheckB = gtk.CheckButton('Decomposed case')
        hbox = gtk.HBox()
        hbox.pack_start(parCheckB, False, False, 5)
        mainbox.pack_start(hbox, False, False, 5)
        
        parlist = glob.glob(self.caseDir + '/processor*')
        if len(parlist) == 0:
            parCheckB.set_active(0)
        else:
            parCheckB.set_active(1) 
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.set_label('    Select time to create vorticity    ')
        frame.set_label_align(0.1, 0.5)
        mainbox.pack_start(frame,True,True,5)

        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        but0 = gtk.RadioButton(None, 'All')
        but0.connect('toggled', toggled)
        hbox0 = gtk.HBox(False, 5)
        box1.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(but0, False, False, 5)

        but1 = gtk.RadioButton(but0, 'latestTime')
        but1.connect('toggled', toggled)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)
        hbox1.pack_start(but1, False, False, 5)

        but2 = gtk.RadioButton(but0, 'Time')
        but2.set_size_request(120, 28)
        but2.connect('toggled', toggled)
        timeEntry = gtk.Entry()
        timeEntry.set_size_request(60, 28)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)
        hbox2.pack_start(but2, False, False, 5)
        hbox2.pack_start(timeEntry, False, False, 5)

        but3 = gtk.RadioButton(but0, 'Time Range')
        but3.set_size_request(120, 28)
        but3.connect('toggled', toggled)
        stimeEntry = gtk.Entry()
        stimeEntry.set_size_request(60, 28)
        etimeEntry = gtk.Entry()
        etimeEntry.set_size_request(60, 28)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(but3, False, False, 5)
        hbox3.pack_start(stimeEntry, False, False, 5)
        hbox3.pack_start(gtk.Label('~'), False, False, 5)
        hbox3.pack_start(etimeEntry, False, False, 5)

        nozeroCB = gtk.CheckButton('noZero Option')
        hbox4 = gtk.HBox(False, 5)
        box1.pack_start(hbox4, False, False, 5)
        hbox4.pack_start(nozeroCB, False, False, 5)

        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('Apply')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)

        mwin.show_all()
    # -----------------------------------------------------------------------------------------------------
    def MachNo(self):

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            time = timeEntry.get_text()
            stime = stimeEntry.get_text()
            etime = etimeEntry.get_text()
            nozero = nozeroCB.get_active()

            pp = glob.glob(self.caseDir + '/processor*')
            if pp == []:
                par = ''
                par1 = ''
            else:
                par = 'mpirun -np ' + str(len(pp)) + ' '
                par1 = ' -parallel'
                
            f = open(self.caseDir + '/system/settings/MachNo', 'w')
            if nozero == 0:
                if selmethod == 'All':
                    f.write(par + self.solver+' -postProcess -func MachNo -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'latestTime':
                    f.write(par + self.solver+' postProcess -func MachNo -latestTime -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'Time':
                    f.write(par + self.solver+' postProcess -func MachNo -time ' + time + ' -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'Time Range':
                    f.write(par + self.solver+' postProcess -func MachNo -time ' + stime + ':' + etime + ' -case ' + self.caseDir + par1 +'\n')
            else:
                if selmethod == 'All':
                    f.write(par + self.solver+' postProcess -func MachNo -noZero -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'latestTime':
                    f.write(par + self.solver+' postProcess -func MachNo -noZero -latestTime -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'Time':
                    f.write(par + self.solver+' postProcess -func MachNo -noZero -time ' + time + ' -case ' + self.caseDir + par1 +'\n')
                elif selmethod == 'Time Range':
                    f.write(par + self.solver+' postProcess -func MachNo -noZero -time ' + stime + ':' + etime + ' -case ' + self.caseDir + par1 +'\n')
            f.close()

            os.system('chmod +x ' + self.caseDir + '/system/settings/MachNo')
            self.notebook.set_current_page(1)

            cmd = self.caseDir + '/system/settings/MachNo\n'
            self.terminal.feed_child(cmd, len(cmd))
            mwin.destroy()

        def toggled(widget):
            selmethod = widget.child.get_text()
            if selmethod == 'All':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'latestTime':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time':
                timeEntry.set_sensitive(1)
                stimeEntry.set_sensitive(0)
                etimeEntry.set_sensitive(0)
            elif selmethod == 'Time Range':
                timeEntry.set_sensitive(0)
                stimeEntry.set_sensitive(1)
                etimeEntry.set_sensitive(1)

        selmethod = 'All'

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('Mach No.')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.set_label('    Select time to create Mach No.    ')
        frame.set_label_align(0.1, 0.5)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)

        but0 = gtk.RadioButton(None, 'All')
        but0.connect('toggled', toggled)
        hbox0 = gtk.HBox(False, 5)
        box1.pack_start(hbox0, False, False, 5)
        hbox0.pack_start(but0, False, False, 5)

        but1 = gtk.RadioButton(but0, 'latestTime')
        but1.connect('toggled', toggled)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)
        hbox1.pack_start(but1, False, False, 5)

        but2 = gtk.RadioButton(but0, 'Time')
        but2.set_size_request(120, 28)
        but2.connect('toggled', toggled)
        timeEntry = gtk.Entry()
        timeEntry.set_size_request(60, 28)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)
        hbox2.pack_start(but2, False, False, 5)
        hbox2.pack_start(timeEntry, False, False, 5)

        but3 = gtk.RadioButton(but0, 'Time Range')
        but3.set_size_request(120, 28)
        but3.connect('toggled', toggled)
        stimeEntry = gtk.Entry()
        stimeEntry.set_size_request(60, 28)
        etimeEntry = gtk.Entry()
        etimeEntry.set_size_request(60, 28)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(but3, False, False, 5)
        hbox3.pack_start(stimeEntry, False, False, 5)
        hbox3.pack_start(gtk.Label('~'), False, False, 5)
        hbox3.pack_start(etimeEntry, False, False, 5)

        nozeroCB = gtk.CheckButton('noZero Option')
        hbox4 = gtk.HBox(False, 5)
        box1.pack_start(hbox4, False, False, 5)
        hbox4.pack_start(nozeroCB, False, False, 5)

        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('Apply')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)

        mwin.show_all()
    # -----------------------------------------------------------------------------------------------------
    def mapFields(self):
        
        self.sourceCase = 'None'

        def source(widget):
            dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                self.sourceCase = dialog.get_filename()
            elif response == gtk.RESPONSE_CANCEL:
                self.sourceCase = 'None'
            dialog.destroy()

        def closethis(widget):
            mwin.destroy()

        def applythis(widget):
            if latestCB.get_active() == True:
                sourceTime = 'latestTime'
            else:
                sourceTime = stimeEntry.get_text()
            
            self.notebook.set_current_page(1)
            
            pp = glob.glob(self.caseDir + '/processor*')
            if pp == []:            
                cmd = 'mapFields -consistent -case ' + self.caseDir + ' -sourceTime ' + sourceTime + ' ' + self.sourceCase + '\n'
            else:    
                cmd = 'mpirun -np ' + str(len(pp)) + ' mapFields -consistent -case ' + self.caseDir + ' -sourceTime ' + sourceTime + ' ' + self.sourceCase + '\n'
            self.terminal.feed_child(cmd,len(cmd))
                
            mwin.destroy()

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(10)
        mwin.set_title('mapFields')
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox = gtk.VBox(False, 0)
        mwin.add(mainbox)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(frame, True, True, 5)
        box1 = gtk.VBox(False, 5)
        frame.add(box1)
        sourceB = gtk.Button(' Select source case ')
        sourceB.connect('clicked', source)
        hbox1 = gtk.HBox(False, 5)
        box1.pack_start(hbox1, False, False, 5)
        hbox1.pack_start(sourceB, False, False, 5)
        latestCB = gtk.CheckButton('SourceTime is latestTime')
        latestCB.set_active(1)
        hbox2 = gtk.HBox(False, 5)
        box1.pack_start(hbox2, False, False, 5)
        hbox2.pack_start(latestCB, False, False, 5)
        stimeEntry = gtk.Entry()
        stimeEntry.set_size_request(100, 28)
        hbox3 = gtk.HBox(False, 5)
        box1.pack_start(hbox3, False, False, 5)
        hbox3.pack_start(gtk.Label('sourceTime'), False, False, 5)
        hbox3.pack_end(stimeEntry, False, False, 5)
        box2 = gtk.HBox(False, 5)
        mainbox.pack_start(box2, False, False, 5)
        appB = gtk.Button('mapFields')
        closeB = gtk.Button('Close')
        appB.set_size_request(100, 28)
        closeB.set_size_request(100, 28)
        appB.connect('clicked', applythis)
        closeB.connect('clicked', closethis)
        box2.pack_end(closeB, False, False, 5)
        box2.pack_end(appB, False, False, 5)
        mwin.show_all()	
        
    # -----------------------------------------------------------------------------------------------------
    def about(self,mainwindow,installPath):

        def closethis(widget):
            win.destroy()

        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title('Baram-v5')
        win.set_border_width(5)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_modal(True)
        win.set_transient_for(mainwindow)

        smainbox = gtk.VBox(False, 0)
        win.add(smainbox)

        logobox = gtk.HBox(False, 5)
        smainbox.pack_start(logobox, False, False, 5)        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        logobox.pack_start(frame, True, True, 5) 
        logo = gtk.Image()
        logo.set_from_file(installPath + "/pic/splash.png")
        frame.add(logo)
         
        stailbox = gtk.HBox(False, 5)
        smainbox.pack_start(stailbox, False, False, 5)        
        label = gtk.Label('Baram version 5.1. Based on OpenFOAM v5')
        
        home = gtk.LinkButton("http://www.nextfoam.co.kr", label = "www.nextfoam.co.kr")
        stailbox.pack_end(home, False, False, 5)
        
        stailbox.pack_end(label, False, False, 5)
        
        hbox = gtk.HBox(False, 5)
        close = gtk.Button('Close')
        close.set_size_request(150, 28)
        close.connect('clicked', closethis)
        hbox.pack_end(close, False, False, 5)
        smainbox.pack_start(hbox, False, False, 5)        
        win.show_all()

        
        
        
            
                
