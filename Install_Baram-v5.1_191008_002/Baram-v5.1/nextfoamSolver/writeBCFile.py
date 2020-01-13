#-*-coding:utf8-*-

from common.fromAll     import *

class writeBCFileClass:

    def __init__(self,mainself):
        
        self.caseDir = mainself.caseDir
        self.GEN = generalClass(mainself)
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
    # -------------------------------------------------------------------------------------
    def BCheader(self,classtype, obj):
    
        he = []
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
    def boundaryConditions(self, simDict, iniDict, bcTypeDict, bcValueDict, AMIDict):
        
        fcom = self.foamComment()
        head = self.header('system/settings', 'boundaryConditions')
        hhh = fcom + head
        f=open(self.caseDir + '/system/settings/boundaryConditions','w')
        for aaa in hhh:f.write(aaa)
        
        bcNameList, polyTypeList = self.GEN.getBCName()

        amis = AMIDict.keys()
        coupleDic = {}
        couplelist = []
        couples = []
        coupleGroup = []
        for ii in amis:
            couplelist.append(AMIDict[ii]['couplePatch'])
        for ii in amis:
            coupleDic[ii] = amis[couplelist.index(ii)]
            couples.append([ii, amis[couplelist.index(ii)]])            
        
        for ii in couples:
            ii.sort()                
        for ii in couples:
            if coupleGroup.count(ii) < 1:
                coupleGroup.append(ii)
                
        bcNameListWOAMI = []
        for ii in bcNameList:
            if ii in amis:
                pass
            else:
                bcNameListWOAMI.append(ii)
    
        f.write('region0\n')
        f.write('{\n')
        
        for i in range(len(bcNameListWOAMI)):
            valueDict = bcValueDict[bcNameListWOAMI[i]]
            f.write('    ' + bcNameListWOAMI[i] + '\n')
            f.write('    {\n')
            
            if polyTypeList[bcNameList.index(bcNameListWOAMI[i])] == 'empty' or polyTypeList[bcNameList.index(bcNameListWOAMI[i])] == 'wedge':
                f.write('        type            ' + polyTypeList[bcNameList.index(bcNameListWOAMI[i])] + ';\n')
            else:    
                if bcTypeDict[bcNameListWOAMI[i]] == 'heatFluxWall' or bcTypeDict[bcNameListWOAMI[i]] == 'convectionWall':
                    f.write('        type            externalHeatTransferWall;\n')
                else:
                    f.write('        type            ' + bcTypeDict[bcNameListWOAMI[i]] + ';\n')

                if bcTypeDict[bcNameListWOAMI[i]] == 'velocityInlet':
                    f.write('        U               uniform (' + valueDict['velocity_x'] + ' ' + valueDict['velocity_y'] + ' ' + valueDict['velocity_z'] + ');\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T              uniform ' + valueDict['temperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')
                
                elif bcTypeDict[bcNameListWOAMI[i]] == 'surfaceNormalVelocityInlet':
                    f.write('        Umag            uniform ' + valueDict['Umag'] + ';\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T              uniform ' + valueDict['temperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')
                
                elif bcTypeDict[bcNameListWOAMI[i]] == 'massFlowRateInlet':
                    f.write('        massFlowRate    uniform ' + valueDict['massFlowRate'] + ';\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T0              uniform ' + valueDict['temperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')
                
                elif bcTypeDict[bcNameListWOAMI[i]] == 'volumeFlowRateInlet':
                    f.write('        volumetricFlowRate  uniform ' + valueDict['volumeFlowRate'] + ';\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T              uniform ' + valueDict['temperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')
                        
                elif bcTypeDict[bcNameListWOAMI[i]] == 'pressureInlet':
                    f.write('        p0              uniform ' + valueDict['volumeFlowRate'] + ';\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T0              uniform ' + valueDict['totalTemperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')
                        
                elif bcTypeDict[bcNameListWOAMI[i]] == 'pressureOutlet':
                    f.write('        p0              uniform ' + valueDict['totalPressure'] + ';\n')
                    if simDict['Energy'] == 'On':
                        f.write('        T0              uniform ' + valueDict['totalTemperature'] + ';\n')                
                    f.write('        turbIntensity   uniform ' + valueDict['turbulentIntensity'] + ';\n')
                    f.write('        viscosityRatio  uniform ' + valueDict['viscosityRatio'] + ';\n')

                elif bcTypeDict[bcNameListWOAMI[i]] == 'pressureOutletExt':
                    f.write('        p0              uniform ' + valueDict['totalPressure'] + ';\n')
                    
                elif bcTypeDict[bcNameListWOAMI[i]] == 'adiabaticWall':
                    if valueDict['velocityMode'] == 'noSlip':
                        f.write('        velocityMode    noSlip;\n')
                        f.write('        U               uniform (0 0 0);\n')                        
                    elif valueDict['velocityMode'] == 'slip':
                        f.write('        velocityMode    slip;\n')
                        f.write('        U               uniform (' + valueDict['movingVelocity_x'] + ' ' + valueDict['movingVelocity_y'] + ' ' + valueDict['movingVelocity_z'] + ');\n')
                    elif valueDict['velocityMode'] == 'rotating':
                        f.write('        velocityMode    rotating;\n')
                        f.write('        origin          (' + valueDict['rotatingOrigin_x'] + ' ' + valueDict['rotatingOrigin_y'] + ' ' + valueDict['rotatingOrigin_z'] + ');\n')
                        f.write('        axis            (' + valueDict['rotatingAxis_x'] + ' ' + valueDict['rotatingAxis_y'] + ' ' + valueDict['rotatingAxis_z'] + ');\n')
                        omega = float(valueDict['RPM']) * 2 * 3.141592 / 60
                        f.write('        omega           ' + str(omega) + ';\n') 
                    elif valueDict['velocityMode'] == 'translating':
                        f.write('        velocityMode    translating;\n')
                        f.write('        U               uniform (' + valueDict['movingVelocity_x'] + ' ' + valueDict['movingVelocity_y'] + ' ' + valueDict['movingVelocity_z'] + ');\n')

                elif bcTypeDict[bcNameListWOAMI[i]] == 'isoThermalWall':
                    f.write('        U               uniform (0 0 0);\n')
                    f.write('        T               uniform ' + valueDict['temperature'] + ';\n')
                        
                elif bcTypeDict[bcNameListWOAMI[i]] == 'thermoCoupledWall':
                    f.write('        U               uniform (0 0 0);\n')

                elif bcTypeDict[bcNameListWOAMI[i]] == 'heatFluxWall':
                    f.write('        U               uniform (0 0 0);\n')
                    f.write('        q               uniform ' + valueDict['heatFlux'] + ';\n')
                    f.write('        mode            flux;\n')
                    
                elif bcTypeDict[bcNameListWOAMI[i]] == 'convectionWall':
                    f.write('        U               uniform (0 0 0);\n')
                    f.write('        h               uniform ' + valueDict['h'] + ';\n')
                    f.write('        Ta              uniform ' + valueDict['Ta'] + ';\n')
                    f.write('        mode            coefficient;\n')
            f.write('    }\n')
           
        for ii in coupleGroup:
            f.write('    ' + ii[0] + '\n')
            f.write('    {\n')
            f.write('        type            ' + bcTypeDict[ii[0]] + ';\n')            
            f.write('        coupleGroup     ' + ii[0] + '_' + ii[1] + ';\n')            
            if bcTypeDict[ii[0]] == 'rotationalPeriodic':
                if AMIDict[ii[0]]['rotationAxis'] == 'x':axis = '(1 0 0)'
                elif AMIDict[ii[0]]['rotationAxis'] == 'y':axis = '(0 1 0)'
                elif AMIDict[ii[0]]['rotationAxis'] == 'z':axis = '(0 0 1)'
                f.write('        rotationAxis    ' + axis + ';\n')
                f.write('        rotationCentre  (' + AMIDict[ii[0]]['rotationCentre_x'] + ' ' + AMIDict[ii[0]]['rotationCentre_y'] + ' ' + AMIDict[ii[0]]['rotationCentre_z'] + ');\n')
            elif bcTypeDict[ii[0]] == 'translationalPeriodic':
                f.write('        separationVector  (' + AMIDict[ii[0]]['separationVector_x'] + ' ' + AMIDict[ii[0]]['separationVector_y'] + ' ' + AMIDict[ii[0]]['separationVector_z'] + ');\n')
            f.write('    }\n')
            
            f.write('    ' + ii[1] + '\n')
            f.write('    {\n')
            f.write('        type            ' + bcTypeDict[ii[1]] + ';\n')            
            f.write('        coupleGroup     ' + ii[0] + '_' + ii[1] + ';\n')            
            if bcTypeDict[ii[1]] == 'rotationalPeriodic':
                if AMIDict[ii[1]]['rotationAxis'] == 'x':axis = '(1 0 0)'
                elif AMIDict[ii[1]]['rotationAxis'] == 'y':axis = '(0 1 0)'
                elif AMIDict[ii[1]]['rotationAxis'] == 'z':axis = '(0 0 1)'
                f.write('        rotationAxis    ' + axis + ';\n')
                f.write('        rotationCentre  (' + AMIDict[ii[1]]['rotationCentre_x'] + ' ' + AMIDict[ii[1]]['rotationCentre_y'] + ' ' + AMIDict[ii[1]]['rotationCentre_z'] + ');\n')
            elif bcTypeDict[ii[1]] == 'translationalPeriodic':
                f.write('        separationVector  (' + AMIDict[ii[1]]['separationVector_x'] + ' ' + AMIDict[ii[1]]['separationVector_y'] + ' ' + AMIDict[ii[1]]['separationVector_z'] + ');\n')
            f.write('    }\n')           
            
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------
    def initialConditions(self, iniDict, simDict):
    
        fcom = self.foamComment()
        head = self.header('system/settings', 'initialConditions')
        hhh = fcom + head
        f = open(self.caseDir + '/system/settings/initialConditions','w')
        for aaa in hhh:f.write(aaa)
        
        f.write('region0\n')
        f.write('{\n')
        f.write('    flow\n')
        f.write('    {\n')
        f.write('        p            uniform ' + iniDict['Pressure [Pa]'] + ';\n')
        f.write('        U            uniform (' + iniDict['X-velocity'] + ' ' + iniDict['Y-velocity'] + ' ' + iniDict['Z-velocity'] + ');\n')
        if simDict['Energy'] == 'On':
            f.write('        T            uniform ' + iniDict['Temperature [K]'] + ';\n')
        f.write('    }\n')

        f.write('    turbulence\n')
        f.write('    {\n')
        f.write('        velocityScale   uniform ' + iniDict['velocityScale [m/s]'] + ';\n')
        f.write('        turbIntensity   uniform ' + iniDict['turbulentIntensity'] + ';\n')
        f.write('        viscosityRatio  uniform ' + iniDict['viscosityRatio'] + ';\n')
        f.write('    }\n')              
        f.write('}\n')
        f.close()
    #------------------------------------------------------------------------------
    def numericConditions(self, numeDict, simDict):
    
        fcom = self.foamComment()
        head = self.header('system/settings', 'numericConditions')
        hhh = fcom + head
        f = open(self.caseDir + '/system/settings/numericConditions','w')
        for aaa in hhh:f.write(aaa)
        
        f.write('discretization\n')
        f.write('{\n')
        if simDict['Time advance'] == 'Transient':
            f.write('    time           ' + numeDict['discretize_time'] + ';\n')
        f.write('    momentum       ' + numeDict['discretize_momentum'] + ';\n')
        f.write('    turbulence     ' + numeDict['discretize_turbulence'] + ';\n')
        if simDict['Energy'] == 'On':
            f.write('    energy         ' + numeDict['discretize_energy'] + ';\n')        
        f.write('}\n')
        
        f.write('relaxationFactors\n')
        f.write('{\n')
        f.write('    pressure       ' + numeDict['relax_pressure'] + ';\n')
        f.write('    momentum       ' + numeDict['relax_momentum'] + ';\n')
        f.write('    turbulence     ' + numeDict['relax_turbulence'] + ';\n')
        if simDict['Energy'] == 'On':
            f.write('    energy         ' + numeDict['relax_energy'] + ';\n')      
        f.write('}\n')
        
        f.write('convergenceCriteria\n')
        f.write('{\n')
        if simDict['Time advance'] == 'Steady':
            f.write('    pressure       ' + numeDict['conv_pressure'] + ';\n')
            f.write('    momentum       ' + numeDict['conv_momentum'] + ';\n')
            f.write('    turbulence     ' + numeDict['conv_turbulence'] + ';\n')
            if simDict['Energy'] == 'On':
                f.write('    energy         ' + numeDict['conv_energy'] + ';\n')      
        else:
            f.write('    pressure       (' + numeDict['conv_pressure_relative'] + ' ' + numeDict['conv_pressure'] + ');\n')
            f.write('    momentum       (' + numeDict['conv_momentum_relative'] + ' ' + numeDict['conv_momentum'] + ');\n')
            f.write('    turbulence     (' + numeDict['conv_turbulence_relative'] + ' ' + numeDict['conv_turbulence'] + ');\n')
            if simDict['Energy'] == 'On':
                f.write('    energy         (' + numeDict['conv_energy_relative'] + ' ' + numeDict['conv_energy'] + ');\n')
        f.write('}\n')
       
        if simDict['Time advance'] == 'Transient':
            f.write('maxItrPerTimeStep    ' + numeDict['nOuterCorrectors'] + ';\n')
        
        f.close()
        
        
        
        
         
               
