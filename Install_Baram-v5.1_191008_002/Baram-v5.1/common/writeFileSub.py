#-*-coding:utf8-*-

import math
import os
import glob
import sys

from generalSub import *

class writeFileClass:

    def __init__(self, caseDir):
    
        self.caseDir = caseDir
    # -------------------------------------------------------------------------------------

    def foamComment(self):
    
        fc = []
        fc.append("/*--------------------------------*- C++ -*----------------------------------*\ \n")
        fc.append("| =========                 |                                                 |\n")
        fc.append("| \\      /  F ield          | OpenFOAM: The Open Source CFD Toolbox           |\n")
        fc.append("|  \\    /   O peration      | Version:  4.x                                   |\n")
        fc.append("|   \\  /    A nd            | Web:      www.OpenFOAM.org                      |\n")
        fc.append("|    \\/     M anipulation   |                                                 |\n")
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
        # ------------------------------------------------------------------------------

    def header(self, location, obj):
    
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
            
        fcom = self.foamComment()
        head = self.header('constant','turbulenceProperties')
        hhh = fcom + head
        f = open(self.caseDir + '/constant/turbulenceProperties', 'w')
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
    
        fcom = self.foamComment()
        head = self.header('constant','turbulenceProperties')
        hhh = fcom + head
        f = open(self.caseDir + '/constant/turbulenceProperties', 'w')
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
        f = open(self.caseDir + '/constant/g', 'w')
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
        f = open(self.caseDir + '/constant/operatingConditions', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('Op      Op [1 -1 -2 0 0 0 0]    ' + op + ';\n')
        f.close()
    #------------------------------------------------------------------------------
    def equationSwitches(self, energy):
    
        fcom = self.foamComment()
        head = self.header('system','equationSwitches')
        hhh = fcom + head
        f = open(self.caseDir + '/system/equationSwitches', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('flow      on;\n')
        if energy=='false':
            f.write('energy      off;\n')
        else:
            f.write('energy      on;\n')                
        f.close()
    #------------------------------------------------------------------------------        
    def transportProperties(self, simDict):
    
        mu = simDict['viscosity']
        rho = simDict['density']
        nu = float(mu) / float(rho)
                    
        fcom = self.foamComment()
        head = self.header('constant','transportProperties')
        hhh = fcom + head
        f = open(self.caseDir + '/constant/transportProperties', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('transportModel    Newtonian;\n')
        f.write('nu    [ 0 2 -1 0 0 0 0 ] ' + str(nu) + ';\n')        
        f.close()
    #------------------------------------------------------------------------------
    def thermophysicalProperties(self, simDict):   
        
        hf = '0'
        sf = '0'

        if simDict['density_method'] == 'Constant':
            equationOfState = 'rhoConst'
        elif simDict['density_method'] == 'Perfect gas':
            equationOfState = 'perfectGas'
            
        if simDict['transport_method'] == 'Constant':
            transport='const'
        elif simDict['transport_method'] == 'Sutherland':
            transport='sutherland'
        thermo = 'hConst'
        mw = simDict['molecular weight']
        mu = simDict['viscosity']
        As = simDict['As']
        Ts = simDict['Ts']
        cp = simDict['Cp']
        kk = simDict['conductivity']
        pr = float(cp) * float(mu) / float(kk)

        fcom = self.foamComment()
        head = self.header('constant','thermophysicalProperties')
        hhh = fcom + head
        f = open(self.caseDir + '/constant/thermophysicalProperties', 'w')
        for aaa in hhh:f.write(aaa)           
        f.write('thermoType\n')
        f.write('{\n')
        f.write('    type             heRhoThermo;\n')
        f.write('    mixture          pureMixture;\n')
        f.write('    transport        ' + transport + ';\n')
        f.write('    thermo           ' + thermo + ';\n')
        f.write('    equationOfState  ' + equationOfState + ';\n')
        f.write('    specie           specie;\n')
        f.write('    energy           sensibleEnthalpy;\n')
        f.write('}\n')

        f.write('mixture\n')
        f.write('{\n')
        f.write('    specie\n')
        f.write('    {\n')
        f.write('        nMoles    1;\n')
        f.write('        molWeight ' + mw + ';\n')
        f.write('    }\n')

        f.write('    transport\n')
        f.write('    {\n')
        if simDict['Turbulence model']=='inviscid':
            f.write('        mu    0;\n')
            f.write('        Pr    ' + str(pr) + ';\n')
        else:
            if transport=='const':
                f.write('        mu    ' + mu + ';\n')                
                f.write('        Pr    ' + str(pr) + ';\n')
            elif transport=='sutherland':
                f.write('        As    ' + As + ';\n')
                f.write('        Ts    ' + Ts + ';\n')                       
        f.write('    }\n')

        f.write('    thermodynamics\n')
        f.write('    {\n')
        f.write('        Cp    ' + cp + ';\n')
        f.write('        Hf    ' + hf + ';\n')                       
        f.write('    }\n')

        if simDict['density_method']=='Constant':
            f.write('    equationOfState\n')
            f.write('    {\n')
            f.write('        rho    '+simDict['density'] + ';\n')
            f.write('    }\n')
        f.write('}\n')
        f.close()                                                  
    #-------------------------------------------------------------------------------------        
    def porousFile(self, dic):
    
        cellzones = dic['cellZones']
        zonetypes = dic['types']
        zonedicts = dic['dict']
        porousZones = []
        porousDicts = []
        for i in range(len(cellzones)):
            if zonetypes[i] == 'Porous':
                porousZones.append(cellzones[i])
                porousDicts.append(zonedicts[i]) 
                
        for i in range(len(porousZones)):
        
            porouszone = porousZones[i]
            poroustype = porousDicts[i]['porousType']
            if poroustype == 'Darcy':
                poroustype = 'DarcyForchheimer'
            dx = porousDicts[i]['dx']
            dy = porousDicts[i]['dy']
            dz = porousDicts[i]['dz']
            fx = porousDicts[i]['fx']
            fy = porousDicts[i]['fy']
            fz = porousDicts[i]['fz']
            e1x = porousDicts[i]['e1x']
            e1y = porousDicts[i]['e1y']
            e1z = porousDicts[i]['e1z']
            e2x = porousDicts[i]['e2x']
            e2y = porousDicts[i]['e2y']
            e2z = porousDicts[i]['e2z']
            c0 = porousDicts[i]['c0']
            c1 = porousDicts[i]['c1']
        
            f = open(self.caseDir + '/system/cellZoneConditions_Porous_' + porouszone, 'w')

            f.write('porous_' + porouszone + '\n')
            f.write('{\n')
            f.write('    type            explicitPorositySource;\n')
            f.write('    active          true;\n')
            f.write('\n')
            f.write('    explicitPorositySourceCoeffs\n')
            f.write('    {\n')
            f.write('        selectionMode   cellZone;\n')
            f.write('        cellZone        ' + porouszone + ';\n')
            f.write('        type            ' + poroustype + ';\n')
            f.write('        active          yes;\n')
            f.write('\n')
            if poroustype=='DarcyForchheimer':
                f.write('        DarcyForchheimerCoeffs\n')
                f.write('        {\n')
                f.write('            d       d [0 -2 0 0 0 0 0] (' + dx + ' ' + dy + ' ' + dz + ');\n')
                f.write('            f       f [0 -1 0 0 0 0 0] (' + fx + ' ' + fy + ' ' + fz + ');\n')
                f.write('\n')
                f.write('            coordinateSystem\n')
                f.write('            {\n')
                f.write('                type    cartesian;\n')
                f.write('                origin  (0 0 0);\n')
                f.write('                coordinateRotation\n')
                f.write('                {\n')
                f.write('                    type    axesRotation;\n')
                f.write('                    e1  (' + e1x + ' ' + e1y + ' ' + e1z + ');\n')
                f.write('                    e2  (' + e2x + ' ' + e2y + ' ' + e2z + ');\n')
                f.write('                }\n')
                f.write('            }\n')
                f.write('        }\n')
            else:
                f.write('        powerLawCoeffs\n')
                f.write('        {\n')
                f.write('            C0      ' + c0 + ';\n')
                f.write('            C1      ' + c1 + ';\n')
                """
                f.write('\n')
                f.write('            coordinateSystem\n')
                f.write('            {\n')
                f.write('                type    cartesian;\n')
                f.write('                origin  (0 0 0);\n')
                f.write('                coordinateRotation\n')
                f.write('                {\n')
                f.write('                    type    axesRotation;\n')
                f.write('                    e1  (' + e1x + ' ' + e1y + ' ' + e1z + ');\n')
                f.write('                    e2  (' + e2x + ' ' + e2y + ' ' + e2z + ');\n')
                f.write('                }\n')
                f.write('            }\n')
                """
                f.write('        }\n')
            f.write('    }\n')
            f.write('}\n')
            f.close()
    #-------------------------------------------------------------------------------------
    def heatsourceFile(self, dic):

        cellzones = dic['cellZones']
        #zonetypes = dic['types']
        zonedicts = dic['dict']
        heatsourceZones = []
        heatsourceDicts = []
        for i in range(len(cellzones)):
            if zonedicts[i]['sourceType'] != 'None':
                heatsourceZones.append(cellzones[i])
                heatsourceDicts.append(zonedicts[i]) 
                
        for i in range(len(heatsourceZones)):
        
            heatsourcezone = heatsourceZones[i]
            sourcetype = heatsourceDicts[i]['sourceType']
            value = heatsourceDicts[i]['sourceValue']
            
            f = open(self.caseDir + '/system/cellZoneConditions_heatsource_' + heatsourcezone, 'w')
            
            if sourcetype == 'fixed.T':
                f.write('fixedT_' + heatsourcezone + '\n')
                f.write('{\n')
                f.write('    type            fixedTemperatureConstraint;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + heatsourcezone + ';\n')
                f.write('\n')
                f.write('    fixedTemperatureConstraintCoeffs\n')
                f.write('    {\n')
                f.write('        mode           uniform;\n')
                f.write('        temperature    ' + value + ';\n')
                f.write('    }\n')
                f.write('}\n')
            else:
                f.write('energySource_'+heatsourcezone+'\n')
                f.write('{\n')
                f.write('    type            scalarSemiImplicitSource;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + heatsourcezone + ';\n')
                f.write('\n')
                f.write('    volumeMode     ' + sourcetype + ';\n')
                f.write('    injectionRateSuSp\n')
                f.write('    {\n')
                f.write('        h    (' + value + ' 0);\n')
                f.write('    }\n')
                f.write('}\n')

            f.close()
    #------------------------------------------------------------------------------
    def fvOptions(self):
    
        po = glob.glob(self.caseDir + '/system/cellZoneConditions_Porous_*')
        hs = glob.glob(self.caseDir + '/system/cellZoneConditions_heatsource_*')       
        
        fcom = self.foamComment()
        head = self.header('system','fvOptions')
        hhh = fcom + head
        f = open(self.caseDir + '/system/fvOptions', 'w')
        for aaa in hhh:f.write(aaa)
        if len(po)!=0:
            for ii in po:f.write('#include "' + ii.split('/')[-1] + '"\n')
        if len(hs)!=0:
            for ii in hs:f.write('#include "' + ii.split('/')[-1] + '"\n')
        f.close() 
    #-------------------------------------------------------------------------------------
    def fixedUFile(self, dic):
    
        cellZone = dic['cellZoneName']
        ux = dic['fixedUx']
        uy = dic['fixedUy']
        uz = dic['fixedUz']        
        
        f = open(self.caseDir + '/system/cellZoneConditions:' + cellZone + ':Fixed.U', 'w')
        f.write('fixedU_' + cellZone + '\n')
        f.write('{\n')	
        f.write('    type            pressureGradientExplicitSource;\n')
        f.write('    active          yes;\n')
        f.write('    selectionMode   cellZone;\n')
        f.write('    cellZone        ' + cellZone + ';\n')
        f.write('\n')
        f.write('    pressureGradientExplicitSourceCoeffs\n')
        f.write('    {\n')
        f.write('        fieldNames    (U);\n')
        f.write('        Ubar          ('+ux+' '+uy+' '+uz+');\n')
        f.write('        gradPini      gradPini [0 2 -2 0 0] 0;\n')
        f.write('    }\n')
        f.write('}\n')
        
        if dic['energySourceOnOff']=='true':
            if dic['eSourceMethod']=='fixed.T':
                f.write('fixedT_' + cellZone + '\n')
                f.write('{\n')
                f.write('    type            fixedTemperatureConstraint;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + cellZone + ';\n')
                f.write('\n')
                f.write('    fixedTemperatureConstraintCoeffs\n')
                f.write('    {\n')
                f.write('        mode           uniform;\n')
                f.write('        temperature    ' + dic['eSource'] + ';\n')
                f.write('    }\n')
                f.write('}\n')
            else:
                f.write('energySource_' + cellZone + '\n')
                f.write('{\n')
                f.write('    type            scalarSemiImplicitSource;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + cellZone + ';\n')
                f.write('\n')
                f.write('    scalarSemiImplicitSourceCoeffs\n')
                f.write('    {\n')
                f.write('        volumeMode     ' + dic['eSourceMethod'] + ';\n')
                f.write('        injectionRateSuSp\n')
                f.write('        {\n')
                f.write('            h    (' + dic['eSource'] + ' 0);\n')
                f.write('        }\n')
                f.write('    }\n')
                f.write('}\n')        
        f.close()  
    #-------------------------------------------------------------------------------------
    def noneFile(self, dic):
    
        cellZone = dic['cellZoneName']        
       
        if dic['energySourceOnOff'] == 'true':
            f = open(self.caseDir + '/system/cellZoneConditions:' + cellZone + ':None', 'w')
            if dic['eSourceMethod'] == 'fixed.T':
                f.write('fixedT_' + cellZone + '\n')
                f.write('{\n')
                f.write('    type            fixedTemperatureConstraint;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + cellZone + ';\n')
                f.write('\n')
                f.write('    fixedTemperatureConstraintCoeffs\n')
                f.write('    {\n')
                f.write('        mode           uniform;\n')
                f.write('        temperature    ' + dic['eSource'] + ';\n')
                f.write('    }\n')
                f.write('}\n')
            else:
                f.write('energySource_' + cellZone + '\n')
                f.write('{\n')
                f.write('    type            scalarSemiImplicitSource;\n')
                f.write('    active          yes;\n')
                f.write('    selectionMode   cellZone;\n')
                f.write('    cellZone        ' + cellZone + ';\n')
                f.write('\n')
                f.write('    scalarSemiImplicitSourceCoeffs\n')
                f.write('    {\n')
                f.write('        volumeMode     ' + dic['eSourceMethod'] + ';\n')
                f.write('        injectionRateSuSp\n')
                f.write('        {\n')
                f.write('            h    (' + dic['eSource'] + ' 0);\n')
                f.write('        }\n')
                f.write('    }\n')
                f.write('}\n')        
            f.close()                                
    #------------------------------------------------------------------------------
    def topoSetDict(self, sets):
    
        fcom = self.foamComment()
        head = self.header('system','topoSetDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/topoSetDict', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('actions\n')
        f.write('(\n')
        for ss in sets:
            f.write('    {\n')
            f.write('        name    ' + ss + ';\n')
            f.write('        type    faceZoneSet;\n')
            f.write('        action  new;\n')
            f.write('        source  setToFaceZone;\n')
            f.write('        sourceInfo\n')
            f.write('        {\n')
            f.write('            faceSet ' + ss + ';\n')
            f.write('        }\n')
            f.write('    }\n')
        f.write(');\n')
        f.close()
    #------------------------------------------------------------------------------
    def createBafflesDict(self, sets):
    
        fcom = self.foamComment()
        head = self.header('system','createBafflesDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/createBafflesDict', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('internalFacesOnly true;\n')
        f.write('baffles\n')
        f.write('{\n')
        for ss in sets:                  
            f.write('    ' + ss + '\n')
            f.write('    {\n')
            f.write('        type        faceZone;\n')
            f.write('        zoneName    ' + ss + ';\n')
            f.write('        patchPairs\n')
            f.write('        {\n')
            f.write('            type	mappedWall;\n')
            f.write('            sampleMode	nearestPatchFace;\n')
            f.write('	     }\n')
            f.write('    }\n')
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------
    def createInteriorDict(self, sets):
    
        fcom = self.foamComment()
        head = self.header('system','createBafflesDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/createBafflesDict', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('internalFacesOnly true;\n')
        f.write('baffles\n')
        f.write('{\n')
        for ss in sets:                  
            f.write('    ' + ss + '\n')
            f.write('    {\n')
            f.write('        type        faceZone;\n')
            f.write('        zoneName    ' + ss + ';\n')
            f.write('        patchPairs\n')
            f.write('        {\n')
            f.write('            type        cyclic;\n')
            f.write('	     }\n')
            f.write('    }\n')
        f.write('}\n')
        f.close()                   
    #------------------------------------------------------------------------------
    def changeDictionaryDictNoCyclicAMI(self, patch, newtype):
    
        fcom = self.foamComment()
        head = self.header('system','changeDictionaryDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/changeDictionaryDict', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('\n')
        f.write('boundary\n')
        f.write('{\n')
        if newtype!='cyclicAMI':
            f.write('    ' + patch + '\n')
            f.write('    {\n')
            f.write('        type    ' + newtype + ';\n')
            f.write('    }\n')			
        f.write('}\n')
        f.close() 
    #------------------------------------------------------------------------------
    def changeDictionaryDictInterface(self, selectedFaces, weight, weightValue):
            
        fcom = self.foamComment()
        head = self.header('system','changeDictionaryDictInterface')
        hhh = fcom + head
        f = open(self.caseDir + '/system/changeDictionaryDictInterface', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('\n')
        f.write('boundary\n')
        f.write('{\n')
        f.write('    ' + selectedFaces[0] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        inGroups          1(cyclicAMI);\n')
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         noOrdering;\n')
        f.write('        neighbourPatch    ' + selectedFaces[1] + ';\n')
        if weight == True:
            f.write('        lowWeightCorrection    ' + weightValue + ';\n')
        f.write('    }\n')
        f.write('    '+selectedFaces[1] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        inGroups          1(cyclicAMI);\n')        
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         noOrdering;\n')
        f.write('        neighbourPatch    ' + selectedFaces[0] + ';\n')
        if weight == True:
            f.write('        lowWeightCorrection    ' + weightValue + ';\n')
        f.write('    }\n')			
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------
    def changeDictionaryDictRotCyclic(self, sets, cc1, cc2, cc3, axis):          
        
        if axis == 'x':raxis = '(1 0 0)'
        elif axis == 'y':raxis = '(0 1 0)'
        elif axis == 'z':raxis = '(0 0 1)'

        fcom = self.foamComment()
        head = self.header('system','changeDictionaryDictRotCyclic')
        hhh = fcom + head
        f = open(self.caseDir + '/system/changeDictionaryDictRotCyclic', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('\n')     
        f.write('boundary\n')
        f.write('{\n')
        f.write('    '+sets[0] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         rotational;\n')
        f.write('        neighbourPatch    ' + sets[1] + ';\n')
        f.write('        rotationAxis      ' + raxis + ';\n')
        f.write('        rotationCentre    (' + cc1 + ' ' + cc2 + ' ' + cc3 + ');\n')
        f.write('    }\n')
        f.write('    '+sets[1] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         rotational;\n')
        f.write('        neighbourPatch    ' + sets[0] + ';\n')
        f.write('        rotationAxis      ' + raxis + ';\n')
        f.write('        rotationCentre    (' + cc1 + ' ' + cc2 + ' ' + cc3 + ');\n')
        f.write('    }\n')
        f.write('}\n')
        f.close()                      
    #------------------------------------------------------------------------------
    def changeDictionaryDictTranslateCyclic(self, sets, cc1, cc2, cc3):         

        vector1 = '(' + cc1+' ' + cc2 + ' ' + cc3 + ')'
        xx = -1 * float(cc1)
        yy = -1 * float(cc2)
        zz = -1 * float(cc3)
        vector2 = '(' + str(xx) + ' ' + str(yy) + ' ' + str(zz) + ')'
	
        fcom = self.foamComment()
        head = self.header('system','changeDictionaryDictTranslateCyclic')
        hhh = fcom + head
        f = open(self.caseDir + '/system/changeDictionaryDictTranslateCyclic', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('\n')          
        f.write('boundary\n')
        f.write('{\n')
        f.write('    ' + sets[0] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         translational;\n')
        f.write('        neighbourPatch    ' + sets[1] + ';\n')
        f.write('        separationVector  ' + vector1 + ';\n')
        f.write('    }\n')
        f.write('    '+sets[1] + '\n')
        f.write('    {\n')
        f.write('        type              cyclicAMI;\n')
        f.write('        matchTolerance    0.0001;\n')
        f.write('        transform         translational;\n')
        f.write('        neighbourPatch    ' + sets[0] + ';\n')
        f.write('        separationVector  ' + vector2 + ';\n')
        f.write('    }\n')
        f.write('}\n')
        f.close()          
    #------------------------------------------------------------------------------
    def pointProbeFile(self, dic, name):
       
        f = open(self.caseDir + '/system/pointProbe_'+name, 'w')
        f.write('#includeEtc "caseDicts/postProcessing/probes/probes.cfg";\n')
        f.write('fields    (' + dic['Field_point'] + ');\n')
        f.write('probeLocations\n')   
        f.write('(\n')
        f.write('    (' + dic['x-coord'] + ' ' + dic['y-coord'] + ' ' + dic['z-coord'] + ') \n')
        f.write(');\n')
        f.close()
    #------------------------------------------------------------------------------
    def surfaceProbeFile(self, dic, name):
        
        f = open(self.caseDir + '/system/surfaceProbe_'+name, 'w')       
        if dic['Mode']=='Average':
            f.write('name            ' + dic['Patch'] + ';\n')
            f.write('fields          (' + dic['Field_surface'] + ');\n')
            f.write('operation       areaAverage;\n')
            f.write('#includeEtc "caseDicts/postProcessing/surfaceFieldValue/patch.cfg";\n')
        elif dic['Mode']=='Integrate':
            f.write('name            ' + dic['Patch'] + ';\n')
            f.write('fields          (' + dic['Field_surface'] + ');\n')
            f.write('operation       areaIntegrate;\n')
            f.write('#includeEtc "caseDicts/postProcessing/surfaceFieldValue/patch.cfg";\n')    
        elif dic['Mode']=='Flowrate':
            f.write('name            ' + dic['Patch'] + ';\n')
            f.write('#includeEtc "caseDicts/postProcessing/flowRate/flowRatePatch.cfg";\n')
        f.close()          
    #------------------------------------------------------------------------------
    def writeFilePointProbe(self, nn, xx, yy, zz, inter, fields, trueFalse):
    
        f = open(self.caseDir + '/system/probeFunction_'+nn, 'w')
        f.write('    probes_' + nn + '\n')
        f.write('    {\n')
        f.write('        functionObjectLibs ( "libsampling.so" );\n')
        f.write('        type            probes;\n')
        f.write('        name            probes;\n')
        f.write('        writeControl   timeStep;\n')
        f.write('        writeInterval  ' + inter + ';\n')
        f.write('\n')
        f.write('        fields\n')
        f.write('        (\n')
        for i in range(len(fields)):
            if trueFalse[i] == True:
                f.write('            ' + fields[i] + '\n')
        f.write('        );\n')
        f.write('\n')
        f.write('        probeLocations\n')
        f.write('        (\n')
        f.write('            (' + xx + ' ' + yy + ' ' + zz + ') \n')
        f.write('        );\n')
        f.write('    }\n') 
        f.close()
    #------------------------------------------------------------------------------
    def writeFileSurfaceProbe(self, fields, dic):

        fcom = self.foamComment()
        head = self.header('system','surfaceAverageDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/surfaceProbeFunction', 'w')
        for aaa in hhh:f.write(aaa)
            
        selectedSet = dic['selected']
        fields = dic['fields']

        for i in range(len(selectedSet)):
            f.write('surfaceAverage_' + selectedSet[i] + '\n')
            f.write('{\n')
            f.write('    name    ' + selectedSet[i] + ';\n')
            f.write('    fields  (')
            for jj in fields:
                f.write(jj + ' ')
            f.write(');\n')
            f.write('    operation areaAverage;\n')
            f.write('    #includeEtc "caseDicts/postProcessing/surfaceRegion/patch.cfg";\n')
            f.write('    log         true;\n')
            f.write('}\n')
 
        f.close()
    #------------------------------------------------------------------------------
    def writeFlowRate(self, selectedSet):
    
        for ii in selectedSet:
            f = open(self.caseDir + '/system/flowRatePatch_'+ii, 'w')

            fcom = self.foamComment()
            for jj in fcom:
                f.write(jj)
                    
            f.write('name   ' + ii + ';\n')
            f.write('#includeEtc "caseDicts/postProcessing/flowRate/flowRatePatch.cfg"\n')
            f.close()
        
    #------------------------------------------------------------------------------
    def forceFile(self, dic, name, simDict):

        if simDict['Energy'] == 'Off':
            rho = 'rhoInf'
        else:
            rho = 'rho'
                
        f = open(self.caseDir + '/system/forces_'+name, 'w')
        f.write('forces_' + name + '\n')
        f.write('{\n')
        f.write('    type               forces;\n')
        f.write('    functionObjectLibs ( "libforces.so" );\n')
        f.write('    writeControl   	timeStep;\n')
        f.write('    timeInterval   	1;\n')
        f.write('    log                yes;\n')
        f.write('    patches \n')
        f.write('    ( \n')
        for ii in dic['Patches_force']:
            f.write('        ' + ii + ' \n')
        f.write('    ); \n')
        f.write('    pName       p;\n')
        f.write('    UName       U;\n')
        f.write('    rho         '+rho+';\n')
        f.write('    log         true;\n')
        f.write('    rhoInf      ' + dic['Reference Density [kg/m³]'] + ';\n')
        f.write('    liftDir     (' + dic['liftDir_x'] + ' ' + dic['liftDir_y'] + ' ' + dic['liftDir_z'] + ');\n')
        f.write('    dragDir     (' + dic['dragDir_x'] + ' ' + dic['dragDir_y'] + ' ' + dic['dragDir_z'] + ');\n')
        f.write('    CofR        (' + dic['CofR_x'] + ' ' + dic['CofR_y'] + ' ' + dic['CofR_z'] + ');\n')
        f.write('    pitchAxis   (' + dic['pitchAxis_x'] + ' ' + dic['pitchAxis_y'] + ' ' + dic['pitchAxis_z'] + ');\n')
        f.write('    magUInf     ' + dic['Reference Velocity [m/s]'] + ';\n')
        f.write('    lRef        ' + dic['Reference Length [m]'] + ';\n')    
        f.write('    Aref        ' + dic['Reference Area [m²]'] + ';\n')   
        f.write('}\n')
        f.close()
            
        f = open(self.caseDir + '/system/forceCoeffs_' + name, 'w')
        f.write('forceCoeffs_' + name + '\n')
        f.write('{\n')
        f.write('    type               forceCoeffs;\n')
        f.write('    functionObjectLibs ( "libforces.so" );\n')
        f.write('    writeControl   	timeStep;\n')
        f.write('    timeInterval   	1;\n')
        f.write('    log                yes;\n')
        f.write('    patches \n')
        f.write('    ( \n')
        for ii in dic['Patches_force']:f.write('        ' + ii + ' \n')
        f.write('    ); \n')
        f.write('    pName       p;\n')
        f.write('    UName       U;\n')
        f.write('    rho         '+rho+';\n')
        f.write('    log         true;\n')
        f.write('    rhoInf      ' + dic['Reference Density [kg/m³]'] + ';\n')
        f.write('    liftDir     (' + dic['liftDir_x'] + ' ' + dic['liftDir_y'] + ' ' + dic['liftDir_z'] + ');\n')
        f.write('    dragDir     (' + dic['dragDir_x'] + ' ' + dic['dragDir_y'] + ' ' + dic['dragDir_z'] + ');\n')
        f.write('    CofR        (' + dic['CofR_x'] + ' ' + dic['CofR_y'] + ' ' + dic['CofR_z'] + ');\n')
        f.write('    pitchAxis   (' + dic['pitchAxis_x'] + ' ' + dic['pitchAxis_y'] + ' ' + dic['pitchAxis_z'] + ');\n')
        f.write('    magUInf     ' + dic['Reference Velocity [m/s]'] + ';\n')
        f.write('    lRef        ' + dic['Reference Length [m]'] + ';\n')    
        f.write('    Aref        ' + dic['Reference Area [m²]'] + ';\n')      
        f.write('}\n')
        f.close()   
    #------------------------------------------------------------------------------
    def force(self, dic, simDict):        
    
        if simDict['Energy'] == 'Off':
            rhoname = 'rhoInf'
        else:
            rhoname = 'rho'
        
        f = open(self.caseDir + '/system/execFlowFunctionDict', 'w')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version    2.0; \n')
        f.write('    format     ascii; \n')
        f.write('    class      dictionary; \n')
        f.write('    object     execFlowFunctionDict; \n')
        f.write('} \n')
        f.write(' \n')
        f.write('functions \n')
        f.write('{ \n')
        f.write('    forces \n')
        f.write('    { \n')
        f.write('	     type               forces; \n')
        f.write('	     functionObjectLibs ( "libforces.so" ); \n')
        f.write('	     writeControl       timeStep; \n')
        f.write('	     writeInterval      1; \n')
        f.write('	     patches \n')
        f.write('	     ( \n')
        for ii in dic['Patches']:f.write('	     ' + ii + ' \n')
        f.write('	     ); \n')
        f.write('        rho        ' + rhoname + '; \n')
        f.write('	     UName      U; \n')
        f.write('	     pName      p; \n')
        f.write('	     log        true; \n')
        f.write('	     rhoInf     ' + dic['Reference Density [kg/m³]'] + '; \n')
        f.write('	     CofR       (' + dic['CofR_x'] + ' ' + dic['CofR_y'] + ' ' + dic['CofR_z'] + '); \n')
        f.write('    } \n')
        f.write(' \n')
        f.write('} \n')
        f.close()
        
        f = open(self.caseDir + '/system/execFlowFunctionDictCoeff', 'w')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version    2.0; \n')
        f.write('    format     ascii; \n')
        f.write('    class      dictionary; \n')
        f.write('    object     execFlowFunctionsDict; \n')
        f.write('} \n')
        f.write(' \n')
        f.write('functions \n')
        f.write('{ \n')
        f.write('forcesCoeffs \n')
        f.write('    { \n')
        f.write('        type               forceCoeffs; \n')
        f.write('        functionObjectLibs ( "libforces.so" ); \n')
        f.write('        writeControl       timeStep; \n')
        f.write('        writeInterval      1; \n')
        f.write('        patches \n')
        f.write('        ( \n')
        for ii in dic['Patches']:f.write('            ' + ii + ' \n')        
        f.write('        ); \n')
        f.write('        rho        ' + rhoname + '; \n')
        f.write('        log         true; \n')
        f.write('        rhoInf      ' + dic['Reference Density [kg/m³]'] + '; \n')
        f.write('	     CofR       (' + dic['CofR_x'] + ' ' + dic['CofR_y'] + ' ' + dic['CofR_z'] + '); \n')
        f.write('	     liftDir       (' + dic['liftDir_x'] + ' ' + dic['liftDir_y'] + ' ' + dic['liftDir_z'] + '); \n')
        f.write('	     dragDir       (' + dic['dragDir_x'] + ' ' + dic['dragDir_y'] + ' ' + dic['dragDir_z'] + '); \n')
        f.write('	     pitchAxis       (' + dic['pitchAxis_x'] + ' ' + dic['pitchAxis_y'] + ' ' + dic['pitchAxis_z'] + '); \n')
        f.write('        magUInf     ' + dic['Reference Velocity [m/s]'] + '; \n')
        f.write('        lRef        ' + dic['Reference Length [m]'] + '; \n')
        f.write('        Aref        ' + dic['Reference Area [m²]'] + '; \n')
        f.write('    } \n')
        f.write('} \n')
        f.close() 
    #------------------------------------------------------------------------------
    def decomposeParDict(self, ncore):
    
        fcom = self.foamComment()
        head = self.header('system','decomposeParDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/decomposeParDict', 'w')
        for aaa in hhh:f.write(aaa)
        f.write('numberOfSubdomains     ' + ncore + ';\n')
        f.write('method                 scotch;\n')
        f.close()
    #------------------------------------------------------------------------------
    def controlDictFile(self, dic, solver):
    
        f1 = glob.glob(self.caseDir + '/system/forces_*')
        f2 = glob.glob(self.caseDir + '/system/forceCoeffs_*')
        f3 = glob.glob(self.caseDir + '/system/pointProbe_*')
        f4 = glob.glob(self.caseDir + '/system/surfaceProbe_*')

        fcom = self.foamComment()
        head = self.header('system','controlDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/controlDict', 'w')
        for aaa in hhh:f.write(aaa)

        f.write('application        ' + solver + ';\n\n')
        f.write('startFrom          ' + dic['startFrom'] + ';\n\n')
        f.write('startTime          ' + dic['startTime'] + ';\n\n')
        f.write('stopAt             ' + dic['stopAt'] + ';\n\n')
        f.write('endTime            ' + dic['endTime'] + ';\n\n')
        f.write('deltaT             ' + dic['deltaT'] + ';\n\n')
        f.write('writeControl       ' + dic['writeControl'] + ';\n\n')
        f.write('writeInterval      ' + dic['writeInterval'] + ';\n\n')
        f.write('purgeWrite         ' + dic['purgeWrite'] + ';\n\n')
        f.write('writeFormat        ' + dic['writeFormat'] + ';\n\n')
        f.write('writePrecision     ' + dic['writePrecision'] + ';\n\n')  
        f.write('writeCompression   ' + dic['writeCompression'] + ';\n\n')
        f.write('timeFormat         ' + dic['timeFormat'] + ';\n\n')
        f.write('timePrecision      ' + dic['timePrecision'] + ';\n\n')
        f.write('runTimeModifiable  true;\n\n')
        f.write('adjustTimeStep     ' + dic['adjustTimeStep'] + ';\n\n')
        f.write('maxCo              ' + dic['maxCo'] + ';\n\n')                        
        
        f.write('functions\n')
        f.write('{\n')
        
        for ii in f1:
            aa = ii.split('/')
            f.write('    #include        "'+aa[-1] + '"\n')
        for ii in f2:
            aa = ii.split('/')
            f.write('    #include        "'+aa[-1] + '"\n')        
        for ii in f3:
            aa = ii.split('/')
            f.write('    #includeFunc    "'+aa[-1] + '"\n')
        for ii in f4:
            aa = ii.split('/')
            f.write('    #includeFunc    "'+aa[-1] + '"\n')
        f.write('}\n')
        f.close()                
    #------------------------------------------------------------------------------        
    def MRFProperties(self, dic):
    
        cellzones = dic['cellZones']
        zonetypes = dic['types']
        zonedicts = dic['dict']
        MRFZones = []
        MRFDicts = []
        for i in range(len(cellzones)):
            if zonetypes[i] == 'MRF':
                MRFZones.append(cellzones[i])
                MRFDicts.append(zonedicts[i])                                

        if len(MRFZones) != 0:
    
            fcom = self.foamComment()
            head = self.header('constant','MRFProperties')
            hhh = fcom + head
            f = open(self.caseDir + '/constant/MRFProperties', 'w')
            for aaa in hhh:f.write(aaa) 
            
            for i in range(len(MRFZones)):
                cellZone=MRFZones[i]
                nonRotPatch=MRFDicts[i]['StaticPatch']
                orix = MRFDicts[i]['orix']
                oriy = MRFDicts[i]['oriy']
                oriz = MRFDicts[i]['oriz']
                axisx = MRFDicts[i]['axisx']
                axisy = MRFDicts[i]['axisy']
                axisz = MRFDicts[i]['axisz']
                axis = '(' + axisx + ' ' + axisy + ' ' + axisz + ')'     
                rpm = MRFDicts[i]['RPM']              
                omega = float(rpm) * 2 * 3.141592 / 60	    

                f.write('MRFCellZone_' + cellZone + '\n')
                f.write('{\n')
                f.write('    cellZone        ' + cellZone + ';\n')
                f.write('    active          yes;\n')
                f.write('    nonRotatingPatches    (')
                for jj in nonRotPatch:f.write(' '+jj+' ')
                f.write(' );\n')
                f.write('    origin     (' + orix + ' ' + oriy + ' ' + oriz + ');\n')
                f.write('    axis       ' + axis + ';\n')
                f.write('    omega      ' + str(omega) + ';\n')
                f.write('}\n')
                f.write('\n')
            f.close()
    #------------------------------------------------------------------------------        
    def initialConditions(self, iniDict, solver, turbulence):

        f = open(self.caseDir + '/system/initialConditions', 'w')
        
        fcom = self.foamComment()
        head = self.header('system','initialConditions')
        hhh = fcom + head
        for ii in hhh:f.write(ii) 
        
        f.write('region0\n')
        f.write('{\n')
        f.write('    flow\n')
        f.write('    {\n')
        f.write('        p               uniform '+iniDict['Pressure'] + ';\n')
        f.write('        U               uniform ( '+iniDict['X-velocity'] + ' '+iniDict['Y-velocity'] + ' '+iniDict['Z-velocity'] + ' );\n')
        if solver=='buoyantSimpleNFoam' or solver=='buoyantPimpleNFoam':
            f.write('        T               uniform '+iniDict['Temperature'] + ';\n')        
        f.write('    }\n')
        f.write('    turbulence\n')
        f.write('    {\n')
        if turbulence=='kOmegaSST':
            f.write('        k               uniform 0.1;\n')
            f.write('        omega           uniform 0.1;\n')
        elif turbulence=='kEpsilon' or turbulence=='realizableKE' or turbulence=='RNGkEpsilon':
            f.write('        k               uniform 0.1;\n')
            f.write('        epsilon         uniform 0.1;\n')
        f.write('    }\n')
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------        
    def boundaryConditions(self, boundaryTypeDict, bcDictList, solver):
        
        GEN = generalClass(self)
        bcName, polyType = GEN.getBCName()
        
        bctype=[]
        for i in range(len(bcName)):
            bctype.append(boundaryTypeDict[bcName[i]])
               
        f = open(self.caseDir + '/system/boundaryConditions', 'w')
        
        fcom = self.foamComment()
        head = self.header('system','boundaryConditions')
        hhh = fcom + head
        for ii in hhh:f.write(ii) 
        
        f.write('region0\n')
        f.write('{\n')
        
        for i in range(len(bcName)):
            f.write('    '+bcName[i] + '\n')
            f.write('    {\n')
            string = self.detailBC(bcName[i],bctype[i],bcDictList,solver)
            f.write(string)
            f.write('    }\n')            
                   
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------        
    def radiationProperties(self, dic):
        
        fcom = self.foamComment()
        head = self.header('constant','radiationProperties')
        hhh = fcom + head        
        if dic['radiationModel'] != 'none':
            f = open(self.caseDir + '/constant/radiationProperties', 'w')
            for aaa in hhh:f.write(aaa)
            f.write('radiation         on;\n')
            f.write('radiationModel    ' + dic['radiationModel'] + ';\n')
            f.write('solverFreq        ' + dic['solverFrequency'] + ';\n\n')
            
            if dic['radiationModel']=='fvDOM':
                f.write('fvDOMCoeffs\n')
                f.write('{\n')
                f.write('    nPhi        ' + dic['nPhi'] + ';\n')
                f.write('    nTheta      ' + dic['nTheta'] + ';\n')
                f.write('    convergence ' + dic['convergence'] + ';\n')
                f.write('    maxIter     ' + dic['maxIter'] + ';\n')
                f.write('    cacheDiv    ' + dic['cacheDiv'] + ';\n')
                f.write('}\n\n')
            
            f.write('absorptionEmissionModel        constantAbsorptionEmission;\n')
            f.write('constantAbsorptionEmissionCoeffs\n')
            f.write('{\n')
            f.write('    absorptivity    absorptivity    [ m^-1 ]         ' + dic['absorptivity'] + ';\n')
            f.write('    emissivity      emissivity      [ m^-1 ]         ' + dic['emissivity'] + ';\n')
            f.write('    E               E               [ kg m^-1 s^-3 ] ' + dic['E'] + ';\n')
            f.write('}\n\n')
                                 
            f.write('scatterModel      none;\n')                      
            f.write('sootModel         none;\n')
            f.close()
    #------------------------------------------------------------------------------
    def radiationBCFile(self, dic):
    
        valuedic = dic['wallEmissivity']
    
        if dic['radiationModel'] == 'P1':

            fcom = self.foamComment()
            head=self.BCheader('volScalarField','G')
            hhh = fcom + head
            GEN = generalClass(self)
            bcname, bctype = GEN.getBCName()

            f = open(self.caseDir + '/0/G', 'w')
            for aaa in hhh:f.write(aaa)
            
            f.write('dimensions      [1 0 -3 0 0 0 0];\n')
            f.write('internalField   uniform 0;\n')
            f.write('boundaryField\n')
            f.write('{\n')
            for j in range(len(bcname)):
                f.write('    ' + bcname[j] + '\n')
                f.write('    {\n')
                if bctype[j] == 'wall' or bctype[j] == 'mappedWall':
                    f.write('        type               MarshakRadiation;\n')                
                    f.write('        emissivityMode     lookup;\n')
                    f.write('        emissivity         uniform ' + valuedic[bcname[j]] + ';\n')
                    f.write('        value              uniform 0;\n')
                elif bctype[j] == 'patch':
                    f.write('        type               MarshakRadiation;\n')                
                    f.write('        emissivityMode     lookup;\n')
                    f.write('        emissivity         uniform 0.0;\n')
                    f.write('        value              uniform 0;\n')                
                elif bctype[j]=='symmetry':f.write('        type    symmetry;\n')
                elif bctype[j]=='symmetryPlane':f.write('        type    symmetryPlane;\n')
                elif bctype[j]=='empty':f.write('        type    empty;\n')
                elif bctype[j]=='cyclic':f.write('        type    cyclic;\n')
                elif bctype[j]=='cyclicAMI':f.write('        type    cyclicAMI;\n')
                elif bctype[j]=='wedge':f.write('        type    wedge;\n')
                f.write('    }\n')
            f.write('}\n')
            f.close()        
        
        elif dic['radiationModel'] == 'fvDOM':

            fcom = self.foamComment()
            head=self.BCheader('volScalarField','IDefault')
            hhh = fcom + head
            GEN = generalClass(self)
            bcname, bctype = GEN.getBCName()
            f = open(self.caseDir + '/0/IDefault', 'w')
            for aaa in hhh:f.write(aaa)
            
            f.write('dimensions      [1 0 -3 0 0 0 0];\n')
            f.write('internalField   uniform 0;\n')
            f.write('boundaryField\n')
            f.write('{\n')
            for j in range(len(bcname)):
                f.write('    ' + bcname[j] + '\n')
                f.write('    {\n')
                if bctype[j] == 'wall' or bctype[j] == 'mappedWall':
                    f.write('        type               greyDiffusiveRadiation;\n')                
                    f.write('        emissivityMode     lookup;\n')
                    f.write('        emissivity         uniform ' + valuedic[bcname[j]] + ';\n')
                    f.write('        value              uniform 0;\n')
                elif bctype[j] == 'patch':
                    f.write('        type               greyDiffusiveRadiation;\n')                
                    f.write('        emissivityMode     lookup;\n')
                    f.write('        emissivity         uniform 1.0;\n')
                    f.write('        value              uniform 0;\n')                
                elif bctype[j]=='symmetry':f.write('        type    symmetry;\n')
                elif bctype[j]=='symmetryPlane':f.write('        type    symmetryPlane;\n')
                elif bctype[j]=='empty':f.write('        type    empty;\n')
                elif bctype[j]=='cyclic':f.write('        type    cyclic;\n')
                elif bctype[j]=='cyclicAMI':f.write('        type    cyclicAMI;\n')
                elif bctype[j]=='wedge':f.write('        type    wedge;\n')
                f.write('    }\n')
            f.write('}\n')
            f.close()
    #------------------------------------------------------------------------------
    def modifyFvSolutionForRad(self, dic):
    
        radmodel = dic['radiationModel']
        
        with open(self.caseDir + '/system/fvSolution', 'r') as f:
            ff = f.readlines()
        
        endSolver = 76        
        
        for i in range(len(ff)):
            a1 = ff[i].strip()
            a2 = a1.split()
            if a2:
                if a2[0] == 'residualControl':
                    endRes = i + 8
                if a2[0] == 'equations':
                    endRelax = i + 7
            
        if radmodel == 'P1':
            ff.insert(endSolver,'    G\n')
            ff.insert(endSolver+1,'    {\n')
            ff.insert(endSolver+2,'        solver          PCG;\n')
            ff.insert(endSolver+3,'        preconditioner  DIC;\n')
            ff.insert(endSolver+4,'        tolerance       1e-5;\n')
            ff.insert(endSolver+5,'        relTol          0.1;\n')
            ff.insert(endSolver+6,'        maxIter         5;\n')
            ff.insert(endSolver+7,'        minIter         1;\n')
            ff.insert(endSolver+8,'    }\n')
            
            ff.insert(endRes+8,'        G               1e-3;\n')            
            ff.insert(endRelax+9,'        G               0.7;\n')        
        
        elif radmodel == 'fvDOM':
            ff.insert(endSolver,'    Ii\n')
            ff.insert(endSolver+1,'    {\n')
            ff.insert(endSolver+2,'        solver          GAMG;\n')
            ff.insert(endSolver+3,'        smoother        symGaussSeidel;\n')
            ff.insert(endSolver+4,'        tolerance       1e-4;\n')
            ff.insert(endSolver+5,'        relTol          0;\n')
            ff.insert(endSolver+6,'        maxIter         5;\n')
            ff.insert(endSolver+7,'        minIter         1;\n')
            ff.insert(endSolver+8,'    }\n')
            
            ff.insert(endRes+8,'        "ILambda.*"     1e-3;\n')
            ff.insert(endRelax+9,'        "ILambda.*"    0.7;\n')
        
        f = open(self.caseDir + '/system/fvSolution', 'w')
        for ii in ff:
            f.write(ii)
        f.close()
                         
