#!/usr/bin/env python
#-*-coding:utf8-*-

from common.fromAll_snappy  import *

installPath = os.path.dirname(os.path.abspath(__file__))

class startWindow:
    def __init__(self):
        if glob.glob(home + '/.OpenFOAM') == []:
            os.system('mkdir ' + home + '/.OpenFOAM')

        if self.getPs() == 2:
            if glob.glob(home + '/.OpenFOAM/Baram_snappy_temporary') != []:
                os.system('rm -rf ' + home + '/.OpenFOAM/Baram_snappy_temporary*')
        if glob.glob(home + '/.OpenFOAM/Baram_snappy_temporary') == []:
            os.system('mkdir ' + home + '/.OpenFOAM/Baram_snappy_temporary')
            self.caseDir = home + '/.OpenFOAM/Baram_snappy_temporary'
        else:
            num = len(glob.glob(home + '/.OpenFOAM/Baram_snappy_temporary*'))
            os.system('mkdir ' + home + '/.OpenFOAM/Baram_snappy_temporary' + str(num))
            self.caseDir = home + '/.OpenFOAM/Baram_snappy_temporary' + str(num)
        # ---------
        self.newSim()
        
    def newSim(self):   
        MAIN = mainWindowSnappy(self.caseDir, installPath)
        MAIN.mainWindowGUI()

    def getPs(self):
        path_Ps = home + '/.OpenFOAM/psc'
        os.system('ps -C snappy > ' + path_Ps)
        f = open(path_Ps, 'r')
        ff = f.readlines()
        f.close()
        os.system('rm ' + path_Ps)
        return len(ff)

    def main(self):
        gtk.main()

if __name__=='__main__':
    win=startWindow()
    win.main()

