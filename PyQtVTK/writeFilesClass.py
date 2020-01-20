#-*-coding:utf8-*-
import math
import os
import sys

class writeFilesClass(object, casePath):
    def __init__(self):
        super().__init__()
        self.casePath = casePath
    #------------------------------------------------------------------------------
   def foamHeader(self):
    
        fc = []
        fc.append("/*--------------------------------*- C++ -*----------------------------------*\ \n")
        fc.append("| =========                 |                                                 |\n")
        fc.append("| \\      /  F ield          | OpenFOAM: The Open Source CFD Toolbox           |\n")
        fc.append("|  \\    /   O peration      | Version:  4.x                                   |\n")
        fc.append("|   \\  /    A nd            | Web:      www.OpenFOAM.org                      |\n")
        fc.append("|    \\/     M anipulation   | Date:     " + strftime('%Y-%m-%d %H:%M:%S', localtime()) + "                              |\n")
        fc.append("\*---------------------------------------------------------------------------*/\n")
        fc.append("\n")
        return fc

    #------------------------------------------------------------------------------
    def BCheader(self, classtype, obj):
    
        he=[]
        he.append("FoamFile\n")
        he.append("{\n")
        he.append("    version     2.0;\n")
        he.append("    format      ascii;\n")
        he.append("    class       "+classtype+";\n")
        he.append('    object      '+obj+';\n')
        he.append("}\n")
        he.append("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
        return he

    #------------------------------------------------------------------------------
    def DictHeader(self, location, obj):
    
        he = []
        he.append('FoamFile\n')
        he.append('{\n')
        he.append('    version     2.0;\n')
        he.append('    format      ascii;\n')
        he.append('    class       dictionary;\n')
        he.append('    location    "' + location + '";\n')
        he.append('    object      ' + obj + ';\n')
        he.append('}\n')
        he.append('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')
        return he

    #------------------------------------------------------------------------------
    def turbulenceProperties(self, dic):
            
        fcom = self.foamHeader()
        head = self.header('constant','turbulenceProperties')
        hhh = fcom + head
        f = open(self.casePath + '/constant/turbulenceProperties', 'w')
        for aaa in hhh:
            f.write(aaa)	
        if dic['Turbulence model'] == 'laminar' or dic['Turbulence model'] == 'inviscid':
            f.write('simulationType        ' + dic['Turbulence model'] + ';\n')
        else:
            f.write('simulationType        NEXT::RAS;\n')
            f.write('RAS\n')
            f.write('{\n')
            f.write('    RASModel        ' + dic['Turbulence model'] + ';\n')
            f.write('    turbulence      on;\n')
            f.write('    printCoeffs     on;\n') 
            f.write('    Prt             ' + dic['Prt'] + ';\n')
            if dic['Turbulence model']=='realizableKEtwoLayer':
                f.write('    ReyStar         ' + dic['ReyStar'] + ';\n')
                f.write('    deltaRey        ' + dic['deltaRey'] + ';\n')            
            f.write('}\n')
        f.close()

    #------------------------------------------------------------------------------
    def modifyTurbulence(self):
    
        fcom = self.foamHeader()
        head = self.header('constant','turbulenceProperties')
        hhh = fcom + head
        f = open(self.casePath + '/constant/turbulenceProperties', 'w')
        for aaa in hhh:
            f.write(aaa)	
        f.write('simulationType        laminar;\n')
        f.close()   

    #------------------------------------------------------------------------------
    def gravity(self, simDict):
    
        if simDict['Gravity'] == '+x':gg='(9.81 0 0)'
        elif simDict['Gravity'] == '+y':gg='(0 9.81 0)'
        elif simDict['Gravity'] == '+z':gg='(0 0 9.81)'
        elif simDict['Gravity'] == '-x':gg='(-9.81 0 0)'
        elif simDict['Gravity'] == '-y':gg='(0 -9.81 0)'
        elif simDict['Gravity'] == '-z':gg='(0 0 -9.81)'
        elif simDict['Gravity'] == 'None':gg='(0 0 0)'
    
        fcom = self.foamComment()
        head = self.header('constant','g')
        hhh = fcom + head
        f = open(self.casePath + '/constant/g', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('dimensions      [0 1 -2 0 0 0 0];\n')
        f.write('value           ' + gg + ';\n')
        f.close() 

    #------------------------------------------------------------------------------
    def operatingConditions(self, op):
    
        fcom = self.foamComment()
        head = self.header('constant','operatingConditions')
        hhh = fcom + head
        f = open(self.casePath + '/constant/operatingConditions', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('Op      Op [1 -1 -2 0 0 0 0]    ' + op + ';\n')
        f.close()

    #------------------------------------------------------------------------------
    def equationSwitches(self, energy):
    
        fcom = self.foamComment()
        head = self.header('system','equationSwitches')
        hhh = fcom + head
        f = open(self.casePath + '/system/equationSwitches', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('flow      on;\n')
        if energy=='false':
            f.write('energy      off;\n')
        else:
            f.write('energy      on;\n')                
        f.close()