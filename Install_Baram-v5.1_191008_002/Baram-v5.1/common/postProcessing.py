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
from defaultValue import *
from writeFileSub import *

class postProcessingClass:

    def __init__(self, mainself):

        self.caseDir = mainself.caseDir
        self.gvtk = mainself.gvtk
        self.notebook = mainself.notebook
        self.terminal = mainself.terminal
        self.installpath = mainself.installpath
        self.mainwindow = mainself.mainwindow
        self.mainself = mainself              
        
        self.renderer = mainself.renderer
        self.VTK_All = VTKStuff(mainself.caseDir)
        self.GEN = generalClass(mainself)
        self.DEFAULT = defaultValueClass(mainself)        
                
        self.simDict = self.GEN.pickleLoad(self.caseDir + '/system/settings/simulationConditions')        
        if self.simDict == None:
            dicts = self.DEFAULT.defaultDict()
            self.simDict = dicts[0]
        self.solver = self.simDict['solver']
    #--------------------------------------------------------------------------------------
    def showPatch(self, dic, reader, displayMode):
    
        scalar = dic['scalar']
        time = dic['time']
        colormap = dic['colormap']
        displayContour = dic['displayContour']
        displayVector = dic['displayVector']
        colorBy = dic['colorBy']
        scaleFactor = dic['scaleFactor']
        patches = dic['patches']
        Overlay = dic['Overlay']       
               
        if colorBy == 'Scalar':
            vectorScalar = scalar
        elif colorBy == 'U':
            vectorScalar = 'U'
        
        onOff = []
        bcname, bctype = self.GEN.getBCName()
        for ii in bcname:
            if ii in patches:
                onOff.append(1)
            else:
                onOff.append(0)
        
        viewposition = [1, 1, 1]
        
        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:
            caseType = 1

        if caseType == 0:
            path = self.caseDir + '/processor0/' + time
        else:
            path = self.caseDir + '/' + time
        
        fields = os.listdir(path)
        if scalar in fields:
            pass
        else:
            self.GEN.makeDialog('Error!! There is not the field "' + scalar + '"')
            return
           
        if not 1 in onOff:
            return
       
        if Overlay == False:
            self.renderer.RemoveAllViewProps()
        colormapDict = self.colormapData()
        cactor, vactor, scalar_bar, compositeFilter, glyph = self.VTK_All.patchField(reader,
            bcname, onOff, scalar, time, displayMode, vectorScalar, scaleFactor, colormap, colormapDict)

        self.notebook.set_current_page(0)

        return cactor, vactor, scalar_bar, compositeFilter, glyph        
    #--------------------------------------------------------------------------------------
    def showCut(self, dic, planeList, reader, displayMode):
    
        domainrange = self.GEN.getDomainRange()
        
        domainMin = domainrange[0]
        domainMax = domainrange[1]
        xmin = domainMin[0]
        xmax = domainMax[0]
        ymin = domainMin[1]
        ymax = domainMax[1]
        zmin = domainMin[2]
        zmax = domainMax[2]
        
        scalar = dic['scalar']
        time = dic['time']
        colormap = dic['colormap']        
        displayContour = dic['displayContour']
        displayVector = dic['displayVector']
        colorBy = dic['colorBy']
        scaleFactor = dic['scaleFactor']
        Overlay = dic['Overlay']

        if colorBy == 'Scalar':
            vectorScalar = scalar
        elif colorBy == 'U':
            vectorScalar = 'Umag'        

        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:
            caseType = 1

        if caseType == 0:
            path = self.caseDir + '/processor0/' + time
        else:
            path = self.caseDir + '/' + time
        
        fields = os.listdir(path)
        if scalar in fields:
            pass
        else:
            if scalar != 'mesh':
                self.GEN.makeDialog('Error!! There is not the field "' + scalar + '"')
                return

        viewposition = [1, 1, 1]
        if Overlay == False:
            self.renderer.RemoveAllViewProps()
        
        colormapDict = self.colormapData()
        self.notebook.set_current_page(0)
        
        allActors = []
        allCutters = []
        allGlyph = []
                                        
        for ii in planeList:
        
            axis=dic[ii]['axis']
            value=dic[ii]['value']

            if axis == 'x':
                if float(value) < float(xmin) or float(value) > float(xmax):
                    self.GEN.makeDialog('Error!!! x range is ' + xmin + ' ~ ' + xmax)
                    return                          
                origin = [value, 0, 0]
                normal = [1, 0, 0]
            elif axis == 'y':
                if float(value) < float(ymin) or float(value) > float(ymax):
                    self.GEN.makeDialog('Error!!! y range is ' + ymin + ' ~ ' + ymax)
                    return      
                origin = [0, value, 0]
                normal = [0, 1, 0]
            elif axis == 'z':
                if float(value) < float(zmin) or float(value) > float(zmax):
                    self.GEN.makeDialog('Error!!! z range is ' + zmin + ' ~ ' + zmax)
                    return      
                origin = [0, 0, value]
                normal = [0, 0, 1]

            if scalar == 'mesh':
                cactor, cutter = self.VTK_All.cutPlaneMesh(reader, 
                    normal, origin, scalar, time, displayMode)
                allActors.append([cactor])
                allCutters.append(cutter)
                allGlyph.append(None)
            else:
                cactor, vactor, scalar_bar, cutter, glyph = self.VTK_All.cutPlane(reader,
                    normal, origin, scalar, time, displayMode, vectorScalar, scaleFactor, colormap, colormapDict)
                allActors.append([cactor, vactor, scalar_bar])
                allCutters.append(cutter)
                allGlyph.append(glyph)
                
        return allActors, allCutters, allGlyph
    #--------------------------------------------------------------------------------------
    def showIso(self, dic, isoSurfaceList, multiSurfaceList, actors, reader, displayMode):
        
        scalar = dic['scalar']
        time = dic['time']
        colormap = dic['colormap']        
        displayContour = dic['displayContour']
        Overlay = dic['Overlay']

        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:
            caseType = 1

        if caseType == 0:
            path = self.caseDir + '/processor0/' + time
        else:
            path = self.caseDir + '/' + time
        
        viewposition = [1, 1, 1]
        if Overlay == False:
            self.renderer.RemoveAllViewProps()
        
        colormapDict = self.colormapData()
        self.notebook.set_current_page(0)        
       
        allActors = []
        allIsos = []
        
        isoField = dic['isoField']                        
        
        for ii in isoSurfaceList:                   
            value = dic[ii]['value']
            cactor, scalar_bar, iso = self.VTK_All.isoSurface(reader,
                isoField, float(value), scalar, time, displayMode, colormap, colormapDict)
            allActors.append([cactor, scalar_bar])
            allIsos.append(iso)
            
        for ii in multiSurfaceList:                   
            start = dic[ii]['from']
            end = dic[ii]['to']
            steps = dic[ii]['steps']
            cactor, scalar_bar, iso = self.VTK_All.multiIsoSurface(reader, isoField,
                float(start), float(end), int(steps), scalar, time, displayMode, colormap, colormapDict)
            allActors.append([cactor,scalar_bar])
            allIsos.append(iso)
                
        return allActors, allIsos
    #--------------------------------------------------------------------------------------
    def showClip(self, dic, reader, displayMode):
        
        scalar = dic['scalar']
        time = dic['time']
        colormap = dic['colormap']        
        value = dic['value']

        if glob.glob(self.caseDir + '/processor*'):
            caseType = 0
        else:
            caseType = 1

        if caseType == 0:
            path = self.caseDir + '/processor0/' + time
        else:
            path = self.caseDir + '/' + time

        dataSets = []
        num = self.renderer.GetActors().GetNumberOfItems()
        vtkFeatureActors = self.mainself.vtkFeatureActors 
        for i in range(num):
            aa = self.renderer.GetActors().GetItemAsObject(i)
            if aa not in vtkFeatureActors:
                dataSets.append(aa.GetMapper().GetInputAsDataSet())

        colormapDict = self.colormapData()
        self.notebook.set_current_page(0)        

        clipBy = dic['clipBy']                        
        
        cactor, scalar_bar, clipper = self.VTK_All.clip(reader, clipBy, float(value), scalar,
                                      time, displayMode, colormap, colormapDict, dataSets)
        
        allActors = [cactor, scalar_bar]
                
        return allActors, clipper
    #--------------------------------------------------------------------------------------
    def showStream(self, dic, seedList, reader):

        if dic['Overlay'] == False:
            self.renderer.RemoveAllViewProps()
        
        colormapDict = self.colormapData()
        self.notebook.set_current_page(0)
        
        allActors = []
                                        
        for ii in seedList:
        
            actor, seedActor, scalar_bar = self.VTK_All.streamTracer(reader, dic, ii)
            allActors.append([actor, seedActor, scalar_bar])
                
        return allActors
    #----------------------------------------------------------------------------------------------------
    def resetSize(self):
    
        camera = self.renderer.GetActiveCamera()
        self.renderer.SetActiveCamera(camera)
        self.renderer.ResetCamera()
        self.gvtk.Initialize()
    #----------------------------------------------------------------------------------------------------
    def colormapData(self):        
    
        cmaps = glob.glob(self.installpath + '/colormaps/*')        
        names = []
        nums = []
        datas = []
        for ii in cmaps:
            with open(ii, 'r') as f:
                ff = f.readlines()            
            names.append(ff[0].strip())            
            nums.append(int(ff[2].strip()))
            vvs = []
            for i in range(len(ff) - 3):
                aa = ff[i + 3].split()
                lis = [float(aa[0]), float(aa[1]), float(aa[2])]
                vvs.append(lis)
            datas.append(vvs)            
        cmapdic = {}
        for i in range(len(names)):
            cmapdic[names[i]] = [nums[i],datas[i]]            
        return cmapdic
    #----------------------------------------------------------------------------------------------
    def plotResidual(self, widget):        
    
        bb = glob.glob(self.caseDir + '/PyFoamRunner.mpirun.logfile')
        if bb:
            aa = 'pyFoamPlotWatcher.py PyFoamRunner.mpirun.logfile &'
        else:
            aa = 'pyFoamPlotWatcher.py PyFoamRunner.' + self.solver + '.logfile &'
        os.chdir(self.caseDir)
        os.system(aa)        
    #--------------------------------------------------
    def plotPoint(self, widget, dic):
            
        names = []
        allNames = dic.keys() 
        for ii in allNames:
            if dic[ii]['type'] == 'point':
                names.append(ii)        
        
        for i in range(len(names)):
            if glob.glob(self.caseDir + '/postProcessing/pointProbe_' + names[i]+'/*')==[]:
                self.GEN.makeDialog('Warning!!! There is not saved data')
                return               
               
            field = dic[names[i]]['Field_point']
                        
            times = []
            for ii in glob.glob(self.caseDir + '/postProcessing/pointProbe_' + names[i] + '/*'):
                bb = ii.split('/')
                times.append(bb[-1])
            times.sort()
            lastTime = times[-1]

            postdir = self.caseDir + '/postProcessing/pointProbe_' + names[i]
            gpstate = "state=system(\"cat " + self.caseDir + "/PyFoamState.TheState\")\n"
            gpreread = "if(state eq \"Running\") pause 1; reread;\n"
                        
            plotcommand = "plot '" + postdir + '/' + lastTime + '/' + field + "' u 1:2 w l title '" + field + "'\n"                    
                
            f = open(self.caseDir + '/system/settings/plotcmd' + field + '_' + names[i], 'w')
            f.write('set terminal x11 1 noraise\n')
            f.write('set xlabel "time"\n')
            f.write("set title 'Point Probe : " + names[i] + "'\n")
            f.write(gpstate)
            f.write(plotcommand)
            f.write(gpreread)
            f.close()
                
            pidfile = self.caseDir+'/system/settings/plotprobecmd' + field + '_' + names[i] + '_pid'                      
            os.system('gnuplot -persist ' + self.caseDir + '/system/settings/plotcmd' + field + '_' + names[i] + ' |echo $! > ' + pidfile + ' &')                                             
            time.sleep(0.5)
    #--------------------------------------------------
    def plotForce(self, widget, dic): 
        
        names = []
        allNames = dic.keys() 
        for ii in allNames:
            if dic[ii]['type'] == 'force':names.append(ii)
            
        for i in range(len(names)):
            if glob.glob(self.caseDir + '/postProcessing/forceCoeffs_' + names[i] + '/*') == []:
                self.GEN.makeDialog('Warning!!! There is not saved data')
                return
                                                   
            times = []
            for ii in glob.glob(self.caseDir + '/postProcessing/forceCoeffs_' + names[i] + '/*'):
                bb = ii.split('/')
                times.append(bb[-1])
            times.sort()
            lastTime = times[-1]

            postdir = self.caseDir + '/postProcessing/forceCoeffs_' + names[i]
            gpstate = "state=system(\"cat " + self.caseDir + "/PyFoamState.TheState\")\n"
            gpreread = "if(state eq \"Running\") pause 1; reread;\n"

            plotcommand = "plot '" + postdir + '/' + lastTime + "/forceCoeffs.dat' u 1:3 w l title 'Cd' \n"                    
                                
            f = open(self.caseDir + '/system/settings/plotcmd_force_' + names[i],'w')
            f.write('set terminal x11 1 noraise\n')
            f.write('set xlabel "time"\n')
            f.write("set title 'Force coeffs'\n")
            f.write(gpstate)
            f.write(plotcommand)
            f.write(gpreread)
            f.close()

            pidfile = self.caseDir + '/system/settings/forcecmd_pid_' + names[i]
            os.system('gnuplot -persist '+ self.caseDir +'/system/settings/plotcmd_force_' + names[i] + ' |echo $! > ' + pidfile + ' &')
            time.sleep(0.5)
    #--------------------------------------------------
    def plotSurface(self, widget, dic):

        names = []
        allNames = dic.keys() 
        for ii in allNames:
            if dic[ii]['type'] == 'surface':names.append(ii)
            
        for i in range(len(names)):
            if glob.glob(self.caseDir +'/postProcessing/surfaceProbe_' + names[i] + '/*') == []:
                self.GEN.makeDialog('Warning!!! There is not saved data')
                return               
           
            field = dic[names[i]]['Field_surface']
                        
            times = []
            for ii in glob.glob(self.caseDir + '/postProcessing/surfaceProbe_' + names[i] + '/*'):
                bb = ii.split('/')
                times.append(bb[-1])
            times.sort()
            lastTime = times[-1]

            postdir = self.caseDir + '/postProcessing/surfaceProbe_' + names[i]
            gpstate = "state=system(\"cat " + self.caseDir + "/PyFoamState.TheState\")\n"
            gpreread = "if(state eq \"Running\") pause 1; reread;\n"
                        
            plotcommand = "plot '" + postdir + '/' + lastTime + "/surfaceFieldValue.dat' u 1:2 w l title '" + field + "'\n"           
                          
            f = open(self.caseDir +'/system/settings/plotcmd' + field + '_' + names[i], 'w')
            f.write('set terminal x11 1 noraise\n')
            f.write('set xlabel "time"\n')
            f.write("set title 'Point Probe : " + names[i] + "'\n")
            f.write(gpstate)
            f.write(plotcommand)
            f.write(gpreread)
            f.close()
                
            pidfile = self.caseDir + '/system/settings/plotprobecmd' + field + '_' + names[i] + '_pid'                      
            os.system('gnuplot -persist ' + self.caseDir + '/system/settings/plotcmd' + field + '_' + names[i] + ' |echo $! > ' + pidfile + ' &')                                             
            time.sleep(0.5)
    #--------------------------------------------------
    def forceReport(self, widget, dic, simDict):
    
        WFILE = writeFileClass(self.caseDir)
        WFILE.force(dic,simDict)
        pp = glob.glob(self.caseDir + '/processor*')
                
        if pp == []:
            os.system(simDict['solver'] + ' -postProcess -case ' + self.caseDir + ' -dict ' \
                      + self.caseDir +'/system/execFlowFunctionDict -latestTime > '+ self.caseDir + '/logfiles/log.force')
            os.system(simDict['solver'] + ' -postProcess -case ' + self.caseDir + ' -dict ' \
                      + self.caseDir +'/system/execFlowFunctionDictCoeff -latestTime > ' + self.caseDir + '/logfiles/log.forceCoeff')            
        else:
            os.system('mpirun -np ' + str(len(pp)) + ' ' + self.solver + ' -postProcess -case ' + self.caseDir \
                      +' -dict ' + self.caseDir + '/system/execFlowFunctionDict -latestTime -parallel > ' + self.caseDir + '/logfiles/log.force')
            os.system('mpirun -np ' + str(len(pp)) + ' ' + self.solver + ' -postProcess -case ' + self.caseDir \
                      +' -dict ' + self.caseDir + '/system/execFlowFunctionDictCoeff -latestTime -parallel > ' + self.caseDir + '/logfiles/log.forceCoeff ')
                        
        forceFile = self.caseDir + '/logfiles/log.force'
        forceCoeffFile = self.caseDir + '/logfiles/log.forceCoeff'
        string = self.extractForceData(forceFile, forceCoeffFile)
        self.viewReport(string, 'Force Report')
    #--------------------------------------------------
    def pointReport(self, widget, dic):
    
        xyz = '(' + dic['x-coord'] + ' ' + dic['y-coord'] + ' ' + dic['z-coord'] + ')'
        f = open(self.caseDir + '/system/pointReport', 'w')
        f.write('FoamFile\n')
        f.write('{\n')
        f.write('    version         2.0;\n')
        f.write('    format          ascii;\n')
        f.write('    class           dictionary;\n')
        f.write('    location        system;\n')
        f.write('    object          probesDict;\n')
        f.write('}\n')
        f.write('#includeEtc "caseDicts/postProcessing/probes/probes.cfg"\n')
        f.write('fields\n')
        f.write('(\n')
        f.write('    ' + dic['Field'] + '\n')
        f.write(');\n')
        f.write('probeLocations\n')
        f.write('(\n')
        f.write('    ' + xyz + '\n')
        f.write(');\n')	    
        f.close()

        aa = glob.glob(self.caseDir + '/processor*')
        if aa == []:
            os.system('postProcess -func pointReport -case ' + self.caseDir)
        else:
            os.system('mpirun -np '+str(len(aa))+' postProcess -func pointReport -case '+ self.caseDir +' -parallel')

        with open(self.caseDir + '/postProcessing/pointReport/0/' + dic['Field'], 'r') as f:
            string = f.read()
        self.viewReport(string, 'Point Probe')

        os.system('rm -r ' + self.caseDir + '/postProcessing/pointReport')
    #--------------------------------------------------
    def surfaceReport(self, widget, dic):

        field = dic['Field']
        mode = dic['Mode']
        patch = dic['Patch']           
        
        f = open(self.caseDir+'/system/surfaceReport', 'w')       
        if mode == 'Average':
            f.write('name            ' + patch + ';\n')
            f.write('fields          (' + field + ');\n')
            f.write('operation       areaAverage;\n')
            f.write('#includeEtc "caseDicts/postProcessing/surfaceFieldValue/patch.cfg";\n')
        elif mode == 'Integrate':
            f.write('name            ' + patch + ';\n')
            f.write('fields          (' + field + ');\n')
            f.write('operation       areaIntegrate;\n')
            f.write('#includeEtc "caseDicts/postProcessing/surfaceFieldValue/patch.cfg";\n')    
        elif mode == 'Flowrate':
            f.write('name            ' + patch + ';\n')
            f.write('#includeEtc "caseDicts/postProcessing/flowRate/flowRatePatch.cfg";\n')
        f.close() 
                
        aa = glob.glob(self.caseDir + '/processor*')
        if aa == []:
            os.system('postProcess -func surfaceReport -case ' + self.caseDir)
        else:
            os.system('mpirun -np ' + str(len(aa)) + ' postProcess -func surfaceReport -parallel -case ' + self.caseDir)
        
        times = os.listdir(self.caseDir + '/postProcessing/surfaceReport/')
        times.sort()
        
        with open(self.caseDir + '/postProcessing/surfaceReport/' + times[-1] + '/surfaceFieldValue.dat', 'r') as f:
            string=f.read()
        self.viewReport(string, 'Surface Value')

        os.system('rm -r ' + self.caseDir + '/postProcessing/surfaceReport')
    #--------------------------------------------------
    def extractForceData(self, force, forceCoeff):
    
        with open(force, 'r') as f:
            ff = f.readlines()
        forceList = ff[-12:-3]
        with open(forceCoeff, 'r') as g:
            gg = g.readlines()
        forceCoeffList = gg[-9:-2]
        string = '###  Force\n\n'
        for ii in forceList:
            string = string + ii + '\n'
        string = string + '###  Force Coefficients\n\n'
        for ii in forceCoeffList:
            string = string + ii + '\n'
        return string        
    #-----------------------------------------------------------------------------------------------------
    def viewReport(self, string, title):

        def closethis(widget):
            mwin.destroy()

        mwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mwin.set_border_width(5)
        mwin.set_title(title)
        mwin.set_position(gtk.WIN_POS_CENTER)
        mwin.set_transient_for(self.mainwindow)
        mainbox=gtk.VBox(False, 0)
        mwin.add(mainbox)
        hbox = gtk.HBox(False, 5)
        hbox.set_size_request(500, 600)
        mainbox.pack_start(hbox, True, True, 0)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        sw.add_with_viewport(textview)
        
        hbox.pack_start(sw, True, True, 5)

        textbuffer.set_text(string)

        buttonbox = gtk.HBox(False, 5)
        mainbox.pack_start(buttonbox, False, False, 5)
        closeB = gtk.Button('close')
        closeB.connect('clicked', closethis)
        closeB.set_size_request(140, 28)
        buttonbox.pack_end(closeB, False, False, 5)
        mwin.show_all()
    #--------------------------------------------------
    def saveForce(self, name, dic): 

        dialog = gtk.FileChooserDialog("Save..", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()                   
        elif response == gtk.RESPONSE_CANCEL:
            filename = 'None'
        dialog.destroy()
               
        if glob.glob(self.caseDir + '/postProcessing/forceCoeffs_' + name + '/*')==[]:
            self.GEN.makeDialog('Warning!!! There is not saved data')
            return                    
                               
        times = []
        for ii in glob.glob(self.caseDir + '/postProcessing/forceCoeffs_' + name + '/*'):
            bb = ii.split('/')
            times.append(bb[-1])
        times.sort()
        lastTime = times[-1]

        target1 = self.caseDir + '/postProcessing/forces_' + name+'/' + lastTime + '/forces.dat'
        target2 = self.caseDir + '/postProcessing/forceCoeffs_' + name+'/' + lastTime + '/forceCoeffs.dat'
        
        dest1 = os.path.dirname(filename) + '/forces_' + os.path.basename(filename)
        dest2 = os.path.dirname(filename) + '/forceCoeffs_' + os.path.basename(filename)
        os.system('cp ' + target1 + ' ' + dest1)
        os.system('cp ' + target2 + ' ' + dest2)
    #--------------------------------------------------
    def savePoint(self, name, dic): 

        dialog = gtk.FileChooserDialog("Save..", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()                   
        elif response == gtk.RESPONSE_CANCEL:
            filename = 'None'
        dialog.destroy()
               
        if glob.glob(self.caseDir + '/postProcessing/pointProbe_' + name + '/*') == []:
            self.GEN.makeDialog('Warning!!! There is not saved data')
            return                   
                               
        field = dic[name]['Field_point']
        
        times = []
        for ii in glob.glob(self.caseDir + '/postProcessing/pointProbe_' + name + '/*'):
            bb = ii.split('/')
            times.append(bb[-1])
        times.sort()
        lastTime = times[-1]

        target = self.caseDir + '/postProcessing/pointProbe_' + name + '/' + lastTime + '/' + field

        os.system('cp ' + target + ' ' + filename)
    #--------------------------------------------------
    def saveSurface(self, name, dic): 

        dialog = gtk.FileChooserDialog("Save..", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()                   
        elif response == gtk.RESPONSE_CANCEL:
            filename = 'None'
        dialog.destroy()
               
        if glob.glob(self.caseDir + '/postProcessing/surfaceProbe_' + name + '/*') == []:
            self.GEN.makeDialog('Warning!!! There is not saved data')
            return                                                 
        
        times = []
        for ii in glob.glob(self.caseDir + '/postProcessing/surfaceProbe_' + name + '/*'):
            bb = ii.split('/')
            times.append(bb[-1])
        times.sort()
        lastTime = times[-1]

        target = self.caseDir + '/postProcessing/surfaceProbe_' + name + '/' + lastTime + '/surfaceFieldValue.dat'

        os.system('cp ' + target + ' ' + filename)
    #--------------------------------------------------
    def saveImage(self): 

        dialog = gtk.FileChooserDialog("Save..", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)       

        filter = gtk.FileFilter()
        filter.set_name("PNG")
        patterns = ['*.PNG', '*.png']
        for ii in patterns:
            filter.add_pattern(ii)
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()                   
        elif response == gtk.RESPONSE_CANCEL:
            filename = None
        dialog.destroy()

        return filename

