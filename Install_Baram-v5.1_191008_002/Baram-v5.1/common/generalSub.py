#-*-coding:utf8-*-

from common.importAll   import *

class generalClass:

    def delete_event(self,widget,event):
        aa=glob.glob(self.caseDir+'/system/settings/openSubWindow')
        for ii in aa:os.system('rm '+ii)

    def __init__(self, mainself):
    
        self.caseDir = mainself.caseDir
    #--------------------------------------------------------------------------------------
    def newcase(self):
    
        dialog = gtk.FileChooserDialog("New..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.caseDir = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            self.caseDir = 'None'
        dialog.destroy()
        return self.caseDir
    #-------------------------------------------------------------------------------------------------
    def readcase(self):
    
        dialog = gtk.FileChooserDialog("Open..",None, gtk.FILE_CHOOSER_ACTION_OPEN,
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
    #-----------------------------------------------------------------------------------------
    def getCellZones(self):
    
        alphaList=list(ascii_lowercase)
    
        cellZones=[]
        aa=glob.glob(self.caseDir+'/constant/polyMesh/cellZones')
        if len(aa)!=0:
            filea=open(aa[0],'r');lines=filea.readlines();filea.close()
            line1=[]
            for i in range(15,len(lines)):
                a=(lines[i]).strip()
                if a=='{':line1.append(i)            
            for i in line1:
                b=(lines[i-1]).strip()
                if b[0].lower() in alphaList:cellZones.append(b)
        return cellZones
    #-----------------------------------------------------------------------------------------
    def getfaceZones(self):
    
        with open(self.caseDir + '/constant/polyMesh/faceZones', 'r') as filea:
            lines = filea.readlines()
        line1 = []
        faceZones = []
        for i in range(15,len(lines)):
            a = (lines[i]).strip()
            if a == '{':
                line1.append(i)            
        for i in line1:
            b = (lines[i - 1]).strip()
            faceZones.append(b)
        return faceZones
    #---------------------------------------------------------------------------------------
    def getSets(self):
    
        sss = glob.glob(self.caseDir + '/constant/polyMesh/sets/*')
        sets = []
        for jj in sss:
            bb = jj.split('/')
            sets.append(bb[-1])
        return sets
    #-----------------------------------------------------------------------------------------
    def getBCName(self):
        
        aa = self.caseDir + '/constant/polyMesh/boundary'
        if glob.glob(aa) == []:
            return False
        else:
            with open(aa, 'r') as f:
                ff = f.readlines()
            for i in range(len(ff)):
                if ff[i].strip() == '(':
                    startLine = i
                    break
            
            for ii in ff:
	            if ii == '\n':
	                ff.remove(ii)
            line1 = []
            bcdic = {}
            bcname = []
            bctype = []
            f = open(aa, 'r')
            for i in range(startLine,len(ff)):
                a = (ff[i]).strip()
                if a == '{':
                    line1.append(i)            
            for i in line1:
                b = (ff[i - 1]).strip()
                bcname.append(b)
                bb = (ff[i + 1]).split()
                bb1 = (bb[1])[:-1]
                bctype.append(bb1)
                
            for i in range(len(bcname)):
                bcdic[bcname[i]] = bctype[i]
            
            bcname.sort()
            bctype = []
            for ii in bcname:
                bctype.append(bcdic[ii])
                
            return bcname, bctype
    #--------------------------------------------------------------------
    def getBCType(self):
    
        aa = self.caseDir + '/constant/polyMesh/boundary'
        if glob.glob(aa) == []:
            return False
        else:                   
            with open(aa, 'r') as f:
                ff = f.readlines()
            for i in range(len(ff)):
                if ff[i].strip() == '(':
                    startLine = i
                    break                                
            for ii in ff:
                if ii == '\n':
                    ff.remove(ii)
            line1 = []
            bctype = []
            f = open(aa, 'r')
            for i in range(startLine, len(ff)):
                a = (ff[i]).strip()
                if a == '{':
                    line1.append(i)            
            for i in line1:
                bb = (ff[i + 1]).split()
                bb1 = (bb[1])[:-1]
                bctype.append(bb1)
            return bctype
    #-------------------------------------------------------------------------------------
    def getLatestTime(self):
    
        res = glob.glob(self.caseDir + '/[0-9]*')
        resToInt = []
        for i in range(len(res)):
            ss = res[i].split('/')
            sss = ss[-1]
            if sss != '2dplot.lpt' and sss != '0.org' and sss[-4:] != 'foam':
        	resToInt.append(sss)
        resToInt.sort()
        if resToInt != []:
            latestSingle = resToInt[-1]
        else:
            latestSingle = '0'
        
        res1 = glob.glob(self.caseDir + '/processor0/[0-9]*')
        resToInt1 = []
        for i in range(len(res1)):
            ss = res1[i].split('/')
            sss = ss[-1]
            if sss != '2dplot.lpt' and sss != '0.org' and sss[-4:] != 'foam':
        	resToInt1.append(sss)
        resToInt1.sort()
        if resToInt1 != []:
            latesttPar = resToInt1[-1]
        else:
            latesttPar = '0'

        latestTime = [latestSingle,latesttPar]      
        
        return latestTime      
    #-----------------------------------------------------------------------------------------------------
    def getResult(self):
    
        resultSerial = []
        resultParallel = []
        os.system('foamListTimes -case ' + self.caseDir + ' -noZero > ' + self.caseDir + '/system/settings/resultSerial')
        with open(self.caseDir+'/system/settings/resultSerial', 'r') as f:
            ff = f.readlines()
        for ii in ff:
            resultSerial.append(ii[:-1])
        os.system('rm ' + self.caseDir + '/system/settings/resultSerial')

        if glob.glob(self.caseDir+'/processor*'):
            os.system('foamListTimes -case ' + self.caseDir + ' -noZero -processor > ' + self.caseDir + '/system/settings/resultParallel')
            with open(self.caseDir + '/system/settings/resultParallel', 'r') as f:
                ff = f.readlines()
            for ii in ff:
                resultParallel.append(ii[:-1])
            os.system('rm ' + self.caseDir + '/system/settings/resultParallel')

        results = [resultSerial, resultParallel]
        return results
    #-----------------------------------------------------------------------------------------------------
    def clearResult(self, times, mode):
    
        # mode=1 : include parallel / # mode=0 : serial only / # times : list of time folder
        if mode == '0':
            for ii in times:
                os.system('rm -r ' + self.caseDir + '/' + ii)
        else:
            for ii in times:
                os.system('rm -r ' + self.caseDir + '/' + ii)
            procs = glob.glob(self.caseDir + '/processor*')
            for jj in procs:
                for kk in times:
                    os.system('rm -r ' + jj + '/' + kk)
    #-----------------------------------------------------------------------------------------------------
    def clearParallel(self):
    
        if glob.glob(self.caseDir + '/processor*'):
            os.system('rm -r ' + self.caseDir + '/processor*')	
    #-----------------------------------------------------------------------------------------------------
    def isThereInList(self, List, string):
    
        newlist = []
        for ii in List:
            newlist.append(ii)
        newlist.append(string)
        if newlist.count(string) == 1:
            answer = 'false'
        else:
            answer = 'true'
        return answer        
    # -------------------------------------------------------------------------
    def savestop(self):
    
        runPIDFile = self.caseDir + '/system/settings/runPID'
        controlDictFile = self.caseDir + '/system/controlDict'

        if os.path.isfile(runPIDFile):
            runPID = open(runPIDFile, 'r').read()
            
            os.system('kill -STOP ' + runPID)
            os.remove(runPIDFile)

            with open(controlDictFile, 'r') as readfile:
                controlDict = readfile.readlines()

            for word in range(len(controlDict)):
                if controlDict[word][:6] == 'stopAt':
                    controlDict[word] = 'stopAt             writeNow;\n'

            with open(controlDictFile, 'w') as out:
                for word in controlDict:
                    out.write(word)
                out.flush()

            timeinfo = os.stat(controlDictFile)
            atime = timeinfo.st_atime
            mtime = timeinfo.st_mtime
            os.utime(controlDictFile, (atime, mtime + 20))

            os.system('kill -CONT ' + runPID)
    #-----------------------------------------------------------------------------
    def isNumber(self, string):
        
        try:
            float(string)
            return True
        except ValueError:
            return False       
    #-----------------------------------------------------------------------------        
    def getDomainRange(self):
    
        basename = os.path.basename(self.caseDir)
        
        os.system('touch ' + self.caseDir + '/' + basename + '.foam')
        os.system('setSet -case ' + self.caseDir + ' -batch ' + self.caseDir + '/' + basename + '.foam > ' + \
            self.caseDir + '/logfiles/log.setSet')
           
        with open(self.caseDir + '/logfiles/log.setSet', 'r') as f:
            ff = f.readlines()
        for ii in ff:
            if ii != '\n':
                aa = ii.split()
                if aa[0] == 'Time:0':
                    string = ii.strip()
                    
        b = string.split('(')
        
        c = b[1].split(')')
        c1 = c[0].split()
        
        d = b[2].split(')')
        d1 = d[0].split()
        
        domainMin = [c1[0], c1[1], c1[2]]
        domainMax = [d1[0], d1[1], d1[2]]
        
        return [domainMin, domainMax] 
    #-----------------------------------------------------------------------------        
    def getSTLRange(self, stlfile):
    
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlfile)
        reader.Update()           
        
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())
                
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
            
        bound = actor.GetBounds()
        
        domainMin = [bound[0], bound[2], bound[4]]
        domainMax = [bound[1], bound[3], bound[5]]

        return [domainMin, domainMax]        

    #-----------------------------------------------------------------------------        
    def makeDialog(self, text):
    
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, text)
        md.run()
        md.destroy()
    # -------------------------------------------------------------------------
    def makeDialog_info(self, text):
    
        md = gtk.MessageDialog(
            None,
            gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_CLOSE,
            text)
        md.run()
        md.destroy()
    #-----------------------------------------------------------------------------        
    def makeDialog_question(self, text):
    
        md = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO, text)
        response = md.run()
        md.destroy()
        return response
    #-------------------------------------------------------
    def subWindowOpened(self):    
    
        if glob.glob(self.caseDir+'/system/settings/openSubWindow') == []:
            subwin = False
        else:
            subwin = True
        return subwin  
    #--------------------------------------------------------------------------------------  
    def selSTL(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_select_multiple(True)
        filter = gtk.FileFilter()
        filter.set_name("stl files")
        filter.add_mime_type("stl/STL")
        filter.add_mime_type("stl/stl")
        filter.add_pattern("*.STL")
        filter.add_pattern("*.stl")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            stlList = dialog.get_filenames()
        elif response == gtk.RESPONSE_CANCEL:
            stlList = []
        dialog.destroy()
        return stlList
    #--------------------------------------------------------------------------------------  
    def selSTLSingle(self):
    
        dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_select_multiple(False)
        filter = gtk.FileFilter()
        filter.set_name("stl files")
        filter.add_mime_type("stl/STL")
        filter.add_mime_type("stl/stl")
        filter.add_pattern("*.STL")
        filter.add_pattern("*.stl")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            stlList = dialog.get_filenames()
        elif response == gtk.RESPONSE_CANCEL:
            stlList = []
        dialog.destroy()
        return stlList         
    #--------------------------------------------------------------------------------------  
    def mergeSTL(self, stlList):
    
        f = open(self.caseDir + '/mesh.stl', 'w')
        for ii in stlList:
            a1 = ii.split('/')
            name = a1[-1][:-4]
            with open(ii, 'r') as g:
                gg = g.readlines()
            f.write('solid ' + name + '\n')
            for j in range(len(gg) - 2):
                f.write(gg[j + 1])
            f.write('endsolid ' + name + '\n')
        f.close()                   
    #--------------------------------------------------------------------------------------  
    def mergeFarfield(self, stlList):

        f = open(self.caseDir + '/mesh.stl', 'w')
        for ii in stlList:
            with open(ii, 'r') as g:
                gg = g.readlines()
            for lines in gg:
                if lines[-1] == '\n':
                    f.write(lines)
                else:
                    f.write(lines + '\n')
        f.close()
    #---------------------------------------------------------------------------------------------------------
    def findSTLRegion(self, stlfilename):
    
        with open(stlfilename, 'r') as f:
            ff = f.readlines()
        regions = []
        for i in range(len(ff)):
            if (ff[i].strip())[:5] == 'solid' or (ff[i].strip())[:5] == 'SOLID' or (ff[i].strip())[:5] == 'Solid':
                aa = (ff[i].strip())[5:]
                regions.append(aa.strip())
        return regions         
    #-----------------------------------------------------------------------------------------------------------------------
    def checkNumber(self, item, value):
        if self.isNumber(value) == False:
            self.makeDialog('Error!!! value : "' + value + '" of ' + item + ' is not number')
            return False
        else:
            return True
    #-----------------------------------------------------------------------------------------------------
    def checkNumberSnappy(self, string, errorstr):
    
        for i in range(len(string)):
            if self.isNumber(string[i]) == False:
                self.makeDialog('Error!!! ' + errorstr[i] + ' is not number')
    #--------------------------------------------------------------------------------------  
    def getTurbulenceModel(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/simulationConditions')
        if aa:
            with open(aa[0], 'r') as f:
                dic = pickle.load(f)
            turbulenceModel = dic['RASModel']         
        else:
            turbulenceModel = 'kEpsilon'
        return turbulenceModel                
    #--------------------------------------------------------------------------------------  
    def getEnergyType(self):
    
        aa = glob.glob(self.caseDir + '/system/settings/simulationConditions')
        if aa:
            with open(aa[0], 'r') as f:
                dic=pickle.load(f)
            energyType = dic['energy']         
        else:
            energyType = 'true'
        return energyType
    #------------------------------------------------------------------------------
    def getScalars(self):
    
        timelist = self.getResult()
        if timelist[0] == [] and timelist[1] == []:
            time = '0'
            scalarList = os.listdir(self.caseDir + '/0/')   
        else:
            if len(timelist[0]) >= len(timelist[1]):
                time = timelist[0][-1]
                scalarList = os.listdir(self.caseDir + '/' + time + '/')
            else:
                time = timelist[1][-1]
                scalarList = os.listdir(self.caseDir + '/processor0/' + time + '/')
                
        if 'uniform' in scalarList:
            scalarList.remove('uniform')
        if 'U' in scalarList:
            scalarList.remove('U')
        if 'phi' in scalarList:
            scalarList.remove('phi')
        return scalarList
    #-----------------------------------------------------------------------------------------------------
    def pickleDump(self, filename, var):
    
        f = open(filename, 'w')
        pickle.dump(var, f)
        f.close()
    #-----------------------------------------------------------------------------------------------------
    def pickleLoad(self, filename):
    
        aa = glob.glob(filename)
        if aa != []:
            f = open(aa[0], 'r')
            var=pickle.load(f)
            f.close()        
        else:
            var = None
        return var
    #-----------------------------------------------------------------------------------------------------
    def getAMIType(self, patch):
    
        with open(self.caseDir + '/constant/polyMesh/boundary', 'r') as f:
            ff = f.readlines()
        
        bcNameList, bcTypeList = self.getBCName()
        indOfPatch = bcNameList.index(patch)
        
        for i in range(len(ff)):
            aa = ff[i].split()
            if len(aa) != 0:
                if aa[0] == patch:
                    start = i + 1
                    break
        
        for i in range(20):
            aa = ff[start + i + 2].split()
            if len(aa) != 0:
                if aa[0] == '}':
                    end = start + i + 2
                    break            
        
        transform = None
        coupleGroup = None
        neighbourPatch = None
        for i in range(end - start):
            j = start + i
            aa = ff[j].split()
            
            if len(aa) > 1:
                if aa[0] == 'transform':transform = aa[1][:-1]
                elif aa[0] == 'coupleGroup':coupleGroup = aa[1][:-1]
                elif aa[0] == 'neighbourPatch':neighbourPatch = aa[1][:-1]
                elif aa[0] == 'rotationAxis':
                    bb = ff[j].split('(')
                    cc = bb[1].split(')')
                    dd = cc[0].split()                
                    axisX = dd[0]
                    axisY = dd[1]
                    axisZ = dd[2]
                elif aa[0] == 'rotationCentre':
                    bb = ff[j].split('(')
                    cc = bb[1].split(')')
                    dd = cc[0].split() 
                    centerX = dd[0]
                    centerY = dd[1]
                    centerZ = dd[2]
                elif aa[0] == 'separationVector':
                    bb = ff[j].split('(')
                    cc = bb[1].split(')')
                    dd = cc[0].split() 
                    vectorX = dd[0]
                    vectorY = dd[1]
                    vectorZ = dd[2]                

        if transform == None:
            print 'Error!!! ' + patch + ' is not cyclicAMI'            
        
        if neighbourPatch == None:            
            if coupleGroup == None:
                print 'Error!!! ' + patch + ' is not cyclicAMI. There is not neighbourPatch or coupleGroup'
            else:
                aa = coupleGroup.split('_')
                bb = patch.split('_')
                for ii in aa:
                    if ii in bb:
                        aa.remove(ii)
                
                neighbourPatch = aa[0]
                for i in range(len(aa) - 1):
                    neighbourPatch = neighbourPatch + '_' + ii                
                
        if transform == 'rotational':
            return [transform, neighbourPatch, axisX, axisY, axisZ, centerX, centerY, centerZ]
        elif transform == 'translational':
            return [transform, neighbourPatch, vectorX, vectorY, vectorZ]
        elif transform == 'noOrdering' or transform == 'coincidentFullMatch':
            return [transform, neighbourPatch]
        else:
            return [None, None]
    #-----------------------------------------------------------------------------------------------------
    def getMappedWallType(self, patch):
    
        with open(self.caseDir + '/constant/polyMesh/boundary', 'r') as f:
            ff = f.readlines()
        
        aa = patch.split('_')
        if aa[-1] == 'master':
            aa.remove('master')
            mm = aa[0]
            for i in range(len(aa) - 1):
                mm = mm + '_' + aa[i]
            match = mm + '_slave'
        elif aa[-1] == 'slave':
            aa.remove('slave')
            mm = aa[0]
            for i in range(len(aa) - 1):
                mm = mm + '_' + aa[i]
            match = mm + '_master'
            
        return match                                                                
    #-----------------------------------------------------------------------------------------------------
    def isRunning(self, pid):
    
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    #-----------------------------------------------------------------------------------------------------
    def stlSplitRegions(self, filename):
        
        with open(filename, 'r') as f:
            ff = f.readlines()
        regionnames = []
        startlines = []
        for i in range(len(ff)):
            if ff[i][:5] == 'solid':
                a0 = ff[i].strip()
                a1 = a0.split()
                #regionnames.append(a1[1][:-1])
                regionnames.append(a1[1])
                startlines.append(i+1)

        nlines = []
        for k in range(len(regionnames) - 1):
            cc = int(startlines[k+1]) - int(startlines[k])
            nlines.append(cc)
        nlines.append(len(ff) - int(startlines[-1]) + 1)
                                
        for j in range(len(regionnames)):
            g = open(self.caseDir + '/system/settings/' + regionnames[j] + '.stl', 'w')
            for ii in range(nlines[j]):
                jj = startlines[j] -1 + ii
                g.write(ff[jj])
            g.close()
    #-----------------------------------------------------------------------------------------------------
    def renameSTLRegion(self, filename):       
        
        base = os.path.basename(filename)
        aa = base.split('.')
        nameonly = aa[0]
        
        regs = self.findSTLRegion(filename)
        if len(regs) > 1:
            mes = 'Warning! ' + filename + ' has more than 1 regions'
            print mes
            return                  
        
        with open(filename, 'r') as f:
            ff = f.readlines()
            
        for i in range(len(ff)):
            if ff[i].strip()[:5].lower() == 'solid': 
                ff[i] = 'solid  ' + nameonly + '\n'
            elif ff[i].strip()[:8].lower() == 'endsolid': 
                ff[i] = 'endsolid  ' + nameonly
        
        with open(filename, 'w') as f:
            for ii in ff:
                f.write(ii)

                
