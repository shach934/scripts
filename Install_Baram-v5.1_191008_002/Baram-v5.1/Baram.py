#!/usr/bin/env python
#-*-coding:utf8-*-

from common.fromAll     import *

installPath = os.path.dirname(os.path.abspath(__file__))

class startWindow:
    def __init__(self):

        if glob.glob(home+'/.OpenFOAM') == []:
            os.system('mkdir '+home+'/.OpenFOAM')

        if self.getPs() == 2:
            if glob.glob(home + '/.OpenFOAM/Baram_temporary') != []:
                os.system('rm -rf ' + home + '/.OpenFOAM/Baram_temporary*')

        if glob.glob(home + '/.OpenFOAM/Baram_temporary') == []:
            os.system('mkdir ' + home + '/.OpenFOAM/Baram_temporary')
            self.caseDir = home + '/.OpenFOAM/Baram_temporary'
        else:
            num = len(glob.glob(home + '/.OpenFOAM/Baram_temporary*'))
            os.system('mkdir ' + home + '/.OpenFOAM/Baram_temporary' + str(num))
            self.caseDir = home + '/.OpenFOAM/Baram_temporary' + str(num)
        
        #---------
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title('Baram-v5.1')
        win.set_border_width(5)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_modal(True)

        smainbox = gtk.VBox(False, 0)
        win.add(smainbox)

        logobox = gtk.HBox(False, 5)
        smainbox.pack_start(logobox, False, False, 5)        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        logobox.pack_start(frame,True,True,5) 
        logo = gtk.Image()
        logo.set_from_file(installPath + "/pic/splash.png")
        frame.add(logo)
         
        stailbox = gtk.HBox(False, 5)
        smainbox.pack_start(stailbox, False, False, 15)        
        label = gtk.Label('Baram version 5.1 Based on OpenFOAM v5')
        
        homepage = gtk.LinkButton("http://www.nextfoam.co.kr", label="www.nextfoam.co.kr")
        stailbox.pack_end(homepage, False, False, 5)
        stailbox.pack_end(label, False, False, 5)
        
        hbox = gtk.HBox(False,5)
        close = gtk.Button('Close')
        close.set_size_request(150, 28)
        close.connect('clicked', win.destroy)
        hbox.pack_end(close, False, False, 5)
        smainbox.pack_start(hbox, False, False, 5)
        
        win.show_all()

        solver='simpleNFoam'
        MAIN = mainWindow(self.caseDir, installPath, solver)
        #MAIN.mainWindowGUI()
        
        gobject.timeout_add(200, MAIN.mainWindowGUI)
        gobject.timeout_add(1000, win.destroy)

    def getPs(self):
        path_Ps = home + '/.OpenFOAM/psc'
        os.system('ps -C Baram > ' + path_Ps)
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
