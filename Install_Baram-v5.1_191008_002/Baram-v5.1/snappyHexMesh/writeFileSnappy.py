#-*-coding:utf8-*-

from common.fromAll_snappy  import *

class writeFileClassSnappy:

    def __init__(self,caseDir):
        self.caseDir = caseDir
	
    #-------------------------------------------------------------------------------------
    def foamComment(self):
        fc=[]
        fc.append('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        fc.append('| =========                 |                                                 |\n')
        fc.append('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        fc.append('|  \\    /   O peration     | Version:  2.3.0                                 |\n')
        fc.append('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n')
        fc.append('|    \\/     M anipulation  |                                                 |\n')
        fc.append('\*---------------------------------------------------------------------------*/\n')	
        return fc
    #------------------------------------------------------------------------------
    def header(self, location, obj):
        he=[]
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
    def BCheader(self, classtype, obj):
        he=[]
        he.append('FoamFile\n')
        he.append('{\n')
        he.append('    version     2.0;\n')
        he.append('    format      ascii;\n')
        he.append('    class       ' + classtype + ';\n')
        he.append('    object      ' + obj + ';\n')
        he.append('}\n')
        he.append('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')
        return he
    #------------------------------------------------------------------------------
    def decomposeParDict(self, ncore):
        fcom = self.foamComment()
        head = self.header('system', 'decomposeParDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/decomposeParDict', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('numberOfSubdomains     ' + ncore + ';\n')
        f.write('method                 scotch;\n')
        f.close()
    #------------------------------------------------------------------------------
    def controlDictFile(self, runDict):

        fcom = self.foamComment()
        head = self.header('system', 'controlDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/controlDict', 'w')
        for aaa in hhh:
            f.write(aaa)
        f.write('application        simpleFoam;\n')
        f.write('startFrom          startTime;\n')
        f.write('startTime          ' + runDict['startFrom'] + ';\n')
        f.write('stopAt             endTime;\n')
        f.write('endTime            100;\n')
        f.write('deltaT             1;\n')
        f.write('writeControl       timeStep;\n')
        f.write('writeInterval      100;\n')
        f.write('purgeWrite         0;\n')
        f.write('writeFormat        ' + runDict['writeFormat'] + ';\n')
        f.write('writePrecision     ' + runDict['writePrecision'] + ';\n')  
        f.write('writeCompression   ' + runDict['dataCompression'] + ';\n')
        f.write('timeFormat         general;\n')
        f.write('timePrecision      6;\n')
        f.write('runTimeModifiable  yes;\n')
        f.close()
    #-------------------------------------------------------------------------------------------------
    def makeFeatureFile(self, stlnames, featureAngle):
    
        f = open(self.caseDir + '/system/surfaceFeatureExtractDict', 'w')
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.3.x                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      surfaceFeatureExtractDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

        for i in range(len(stlnames)):
            f.write(stlnames[i] + '.stl\n')
            f.write('{ \n')
            f.write('    extractionMethod    extractFromSurface;\n')
            f.write('    extractFromSurfaceCoeffs \n')
            f.write('    {\n')
            f.write('        includedAngle   ' + featureAngle + ';\n')
            f.write('    }\n')
            f.write('    subsetFeatures\n')
            f.write('    {\n')
            f.write('        nonManifoldEdges    yes;\n')
            f.write('        openEdges           yes;\n')
            f.write('    }\n')
            f.write('    writeObj                yes;\n')
            f.write('}\n')

        f.close()                     
    #-------------------------------------------------------------------------------------------------
    def snappyHexMeshDict(self, inputDictList):

        stlDict = inputDictList[0]
        stlnames = stlDict.keys()
        stlnames.sort()
        featureAngle = inputDictList[1]
        objDict = inputDictList[2]
        blockDict = inputDictList[3]
        castelDict = inputDictList[4]
        snapDict = inputDictList[5]
        layerDict = inputDictList[6]
        advDict = inputDictList[7]
        runDict = inputDictList[8]

        f = open(self.caseDir + '/system/snappyHexMeshDict', 'w')
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.3.x                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      snappyHexMeshDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

        f.write('castellatedMesh ' + runDict['castellate'] + ';\n')
        f.write('snap            ' + runDict['snap'] + ';\n')
        f.write('addLayers       ' + runDict['layer'] + ';\n')

        f.write('geometry \n')
        f.write('{ \n')
                
        for i in range(len(stlnames)):
            f.write('    '+stlnames[i] + '.stl\n')
            f.write('    { \n')
            f.write('        type    triSurfaceMesh;\n')
            f.write('        name    ' + stlnames[i] + ';\n')                                               
            f.write('    } \n')

        objnames=objDict.keys()
        if len(objnames)!=0:
            for i in range(len(objnames)):
                dic=objDict[objnames[i]]
                f.write('    '+objnames[i] + '\n')
                f.write('    {\n')
                f.write('        type    searchableBox;\n')
                f.write('        min     (' + dic['minx'] + ' ' + dic['miny'] + ' ' + dic['minz'] + ');\n')
                f.write('        max     (' + dic['maxx'] + ' ' + dic['maxy'] + ' ' + dic['maxz'] + ');\n')	
                f.write('    }\n')
        f.write('}; \n')
        #---------------------------------------
        f.write('castellatedMeshControls \n')
        f.write('{ \n')
        f.write('    maxLocalCells ' + castelDict['maxLocalCells'] + ';\n')
        f.write('    maxGlobalCells ' + castelDict['maxGlobalCells'] + ';\n')
        f.write('    minRefinementCells ' + castelDict['minRefinementCells'] + ';\n')
        f.write('    nCellsBetweenLevels ' + castelDict['nCellsBetweenLevels'] + ';\n')

        f.write('    features\n')
        f.write('    (\n')
        for i in range(len(stlnames)):
            flevel = castelDict['featurelevel-' + stlnames[i]]
            f.write('        {\n')
            f.write('            file "' + stlnames[i] + '.eMesh";\n')
            f.write('            levels ((0.01 ' + flevel + '));\n')
            f.write('        } \n')
        f.write('    );\n')

        f.write('    refinementSurfaces \n')
        f.write('    { \n')
        for i in range(len(stlnames)):
            f.write('        ' + stlnames[i] + '\n')
            f.write('        {\n')
            f.write('            level (' + castelDict['stllevel-' + stlnames[i]] + ' ' + castelDict['stllevel-' + stlnames[i]] + ');\n')
            if stlDict[stlnames[i]]['type'] == 'wall':
                f.write('            patchInfo\n')
                f.write('            {\n')
                f.write('                type    wall;\n')
                f.write('            }\n')
            elif stlDict[stlnames[i]]['type'] == 'patch':
                f.write('            patchInfo\n')
                f.write('            {\n')
                f.write('                type    patch;\n')
                f.write('            }\n')
            elif stlDict[stlnames[i]]['type'] == 'baffle':
                f.write('            faceZone    '+stlnames[i] + ';\n')
                f.write('            faceType    baffle;\n')
            elif stlDict[stlnames[i]]['type'] == 'cellZone':
                f.write('            cellZone    '+stlnames[i] + ';\n')
                f.write('            faceZone    '+stlnames[i] + ';\n')                
                f.write('            cellZoneInside    inside;\n')
            f.write('        } \n')
        f.write('    }\n')

        f.write('    resolveFeatureAngle ' + castelDict['resolveFeatureAngle'] + ';\n')

        f.write('    refinementRegions\n')
        f.write('    {\n')
        for i in range(len(objnames)):
            dic = objDict[objnames[i]]
            f.write('        ' + objnames[i] + '\n')
            f.write('        {\n')
            f.write('            mode    inside;\n')
            f.write('            levels  ((1E15 ' + castelDict['regionlevel-' + objnames[i]] + '));\n')
            f.write('        }\n')
        for i in range(len(stlnames)):
            dic = stlDict[stlnames[i]]
            if dic['type'] == 'cellZone':
                f.write('        ' + stlnames[i] + '\n')
                f.write('        {\n')
                f.write('            mode    ' + dic['mode'] + ';\n')
                f.write('            levels  ((' + dic['distance'] + ' ' + dic['level'] + '));\n')
                f.write('        }\n')
        f.write('    }\n')
                    
        f.write('    locationInMesh (' + castelDict['locationInMeshx'] + ' ' + castelDict['locationInMeshy'] + ' ' + castelDict['locationInMeshz'] + ');\n')
        f.write('    allowFreeStandingZoneFaces '+castelDict['allowFreeStandingZoneFaces'] + ';\n')
        f.write('}\n')
        f.write('\n')
        #---------------------------------------
        f.write('snapControls\n')
        f.write('{\n')
        f.write('    nSmoothPatch           ' + snapDict['nSmoothPatch'] + ';\n')
        f.write('    tolerance              ' + snapDict['tolerance'] + ';\n')
        f.write('    nSolveIter             ' + snapDict['nSolveIter'] + ';\n')
        f.write('    nRelaxIter             ' + snapDict['nRelaxIter'] + ';\n')
        f.write('    nFeatureSnapIter       ' + snapDict['nFeatureSnapIter'] + ';\n')
        f.write('    implicitFeatureSnap    ' + snapDict['implicitFeatureSnap'] + ';\n')
        f.write('    explicitFeatureSnap    ' + snapDict['explicitFeatureSnap'] + ';\n')
        f.write('    multiRegionFeatureSnap ' + snapDict['multiRegionFeatureSnap'] + ';\n')
        f.write('}\n')
        f.write('\n')
        #---------------------------------------
        f.write('addLayersControls\n')
        f.write('{\n')
        f.write('    relativeSizes ' + layerDict['relativesize'] + ';\n')

        f.write('    expansionRatio            ' + layerDict['expansionRatio'] + ';\n')
        
        if layerDict['thickmethod'] == 'firstLayer':
            f.write('    firstLayerThickness       ' + layerDict['firstthick'] + ';\n')
        elif layerDict['thickmethod'] == 'finalLayer':
            f.write('    finalLayerThickness       ' + layerDict['finalthick'] + ';\n')
        if layerDict['thickmethod'] == 'overall':
            f.write('    overallLayerThickness       ' + layerDict['overallthick'] + ';\n')

        f.write('    minThickness              ' + layerDict['minThickness'] + ';\n')

        f.write('    layers\n')
        f.write('    {\n')

        bname = layerDict['stlnames']
        onoff = layerDict['layerOnOff']

        for i in range(len(bname)):
            if onoff[i] == 1:
                f.write('        ' + bname[i] + '\n')
                f.write('        { \n')
                f.write('            nSurfaceLayers ' + layerDict['nlayers'] + ';\n')
                f.write('        } \n')
        f.write('    }\n')

        f.write('    nGrow                     ' + layerDict['nGrow'] + ';\n')
        f.write('    featureAngle              ' + layerDict['featureAngle'] + ';\n')
        f.write('    nRelaxIter                ' + layerDict['nRelaxIter'] + ';\n')
        f.write('    nSmoothSurfaceNormals     ' + layerDict['nSmoothSurfaceNormals'] + ';\n')
        f.write('    nSmoothNormals            ' + layerDict['nSmoothNormals'] + ';\n')
        f.write('    nSmoothThickness          ' + layerDict['nSmoothThickness'] + ';\n')
        f.write('    maxFaceThicknessRatio     ' + layerDict['maxFaceThicknessRatio'] + ';\n')
        f.write('    maxThicknessToMedialRatio ' + layerDict['maxThicknessToMedialRatio'] + ';\n')
        f.write('    minMedianAxisAngle        ' + layerDict['minMedianAxisAngle'] + ';\n')
        f.write('    nBufferCellsNoExtrude     ' + layerDict['nBufferCellsNoExtrude'] + ';\n')
        f.write('    nLayerIter                ' + layerDict['nLayerIter'] + ';\n')
        f.write('    nRelaxedIter              ' + layerDict['nRelaxedIter'] + ';\n')

        f.write('}\n')
        f.write('\n')
        #---------------------------------------
        f.write('meshQualityControls\n')
        f.write('{\n')
        f.write('    maxNonOrtho           ' + advDict['maxNonOrtho'] + ';\n')
        f.write('    maxBoundarySkewness   ' + advDict['maxBoundarySkewness'] + ';\n')
        f.write('    maxInternalSkewness   ' + advDict['maxInternalSkewness'] + ';\n')
        f.write('    maxConcave            ' + advDict['maxConcave'] + ';\n')
        f.write('    minVol                ' + advDict['minVol'] + ';\n')
        f.write('    minTetQuality         ' + advDict['minTetQuality'] + ';\n')
        f.write('    minArea               ' + advDict['minArea'] + ';\n')
        f.write('    minTwist              ' + advDict['minTwist'] + ';\n')
        f.write('    minDeterminant        ' + advDict['minDeterminant'] + ';\n')
        f.write('    minFaceWeight         ' + advDict['minFaceWeight'] + ';\n')
        f.write('    minVolRatio           ' + advDict['minVolRatio'] + ';\n')
        f.write('    minTriangleTwist      ' + advDict['minTriangleTwist'] + ';\n')
        f.write('\n')

        f.write('    nSmoothScale   ' + advDict['nSmoothScale'] + ';\n')
        f.write('    errorReduction ' + advDict['errorReduction'] + ';\n')
        f.write('    relaxed\n')
        f.write('    {\n')
        f.write('        maxNonOrtho  ' + advDict['maxNonOrtho'] + ';\n')
        f.write('    }\n')
        f.write('}\n')
        f.write('\n')

        f.write('mergeTolerance ' + advDict['mergeTolerance'] + ';\n')

        f.close()
    #-------------------------------------------------------------------------------------------------
    def creatPatchNone(self):
    
        f = open(self.caseDir + '/system/createPatchDict', 'w')
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.3.x                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      createPatchDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')
        f.write('pointSync  false;\n')
        f.write('patches\n')
        f.write('( );\n')
        f.close()
    #-------------------------------------------------------------------------------------------------
    def createPatch(self, oldname, newname, patchtype):
    
        f = open(self.caseDir + '/system/createPatchDict', 'w')
        f.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
        f.write('| =========                 |                                                 | \n')
        f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
        f.write('|  \\    /   O peration     | Version:  2.3.x                                 | \n')
        f.write('|   \\  /    A nd           | Web:      www.OpenFOAM.org                      | \n')
        f.write('|    \\/     M anipulation  |                                                 | \n')
        f.write('\*---------------------------------------------------------------------------*/ \n')
        f.write('FoamFile \n')
        f.write('{ \n')
        f.write('    version     2.0; \n')
        f.write('    format      ascii; \n')
        f.write('    class       dictionary; \n')
        f.write('    object      createPatchDict; \n')
        f.write('} \n')
        f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')
        f.write('pointSync  false;\n')
        f.write('patches\n')
        f.write('(\n')
        
        f.write('    {\n')
        f.write('        name ' + newname + ';\n')
        f.write('        patchInfo\n')
        f.write('        {\n')
        f.write('             type    ' + patchtype + ';\n')
        f.write('        }\n')
        f.write('        constructFrom patches;\n')
        f.write('        patches (' + oldname + ');\n')
        f.write('    }\n')
        f.write(');\n')
        f.close()	        	
    #--------------------------------------------------------------------------------------  
    def basicfvsolution(self):
    
        fcom = self.foamComment()
        head = self.header('system', 'fvSolution')
        hhh = fcom + head
        f = open(self.caseDir + '/system/fvSolution', 'w')
        for aaa in hhh:
            f.write(aaa)
            
        f.write('solvers\n')
        f.write('{\n')
        f.write('    "rho.*"\n')
        f.write('    {\n')
        f.write('        solver          PCG;\n')
        f.write('        preconditioner  DIC;\n')
        f.write('        tolerance       1e-7;\n')
        f.write('        relTol          0;\n')
        f.write('    }\n')
        f.write('    "(p|p_rgh)"\n')
        f.write('    {\n')
       	f.write('        solver                GAMG;\n')
        f.write('        tolerance             1e-7;\n')
        f.write('        relTol                0.1;\n')
        f.write('        minIter               0;\n')
        f.write('        maxIter               50;\n')
        f.write('        smoother              symGaussSeidel;\n')
        f.write('        nPreSweeps            0;\n')
        f.write('        nPostSweeps           2;\n')
        f.write('        cacheAgglomeration    true;\n')
        f.write('        agglomerator          faceAreaPair;\n')
        f.write('        nCellsInCoarsestLevel 10;\n')
        f.write('        mergeLevels           1;\n')
        f.write('    };\n')
        f.write('    "(pFinal|p_rghFinal)"\n')
        f.write('    {\n')
       	f.write('        $p_rgh;\n')
        f.write('        relTol                0;\n')
        f.write('    };\n')
        f.write('    "(U|k|epsilon|omega)"\n')
        f.write('    {\n')
        f.write('        solver          smoothSolver;\n')
        f.write('        smoother        symGaussSeidel;\n')
        f.write('        tolerance       1e-7;\n')
        f.write('        relTol          0.1;\n')
        f.write('    };\n')
        f.write('    "(U|k|epsilon|omega)Final"\n')
        f.write('    {\n')
      	f.write('        $U;\n')
        f.write('        relTol                0;\n')
        f.write('    };\n')
        f.write('    h\n')
        f.write('    {\n')
        f.write('        solver          smoothSolver;\n')
        f.write('        smoother        symGaussSeidel;\n')
        f.write('        tolerance       1e-7;\n')
        f.write('        relTol          0.01;\n')
        f.write('    };\n')
        f.write('    hFinal\n')
        f.write('    {\n')
       	f.write('        $U;\n')
        f.write('        relTol                0;\n')
        f.write('    };\n')
        f.write('}\n')
        f.write('SIMPLE\n')
        f.write('{\n')
        f.write('    nNonOrthogonalCorrectors 0;\n')
        f.write('    pRefCell	0;\n')
        f.write('    pRefValue	0;\n')  
        f.write('    residualControl\n')
        f.write('    {\n')
        f.write('        p      1e-3;\n')
        f.write('        p_rgh  1e-3;\n')        
        f.write('        U      1e-3;\n')
        f.write('        h      1e-3;\n')        
        f.write('        "(k|epsilon|omega)"    1e-3;\n')
        f.write('    }\n')                
        f.write('}\n')
        f.write('PIMPLE\n')
        f.write('{\n')
        f.write('    nNonOrthogonalCorrectors 0;\n')
        f.write('    nOuterCorrectors 1;\n')
        f.write('    nCorrectors 2;\n')
        f.write('    pRefCell	0;\n')
        f.write('    pRefValue	0;\n')        
        f.write('}\n')
        f.write('relaxationFactors\n')
        f.write('{\n')
        f.write('    fields\n')
        f.write('    {\n')
        f.write('        "rho.*"      1.0;\n')
        f.write('        "p.*"        0.3;\n')        
        f.write('    }\n')
        f.write('    equations\n')
        f.write('    {\n')
        f.write('        "(U|k|epsilon|omega).*"    0.7;\n')
        f.write('        "h.*"         1.0;\n')
        f.write('    }\n')
        f.write('}\n')
        f.close()
    #--------------------------------------------------------------------------------------  
    def basicfvschemes(self):
        
        fcom = self.foamComment()
        head = self.header('system', 'fvSchemes')
        hhh = fcom + head
        f = open(self.caseDir + '/system/fvSchemes', 'w')
        for aaa in hhh:
            f.write(aaa)	
            
        f.write('ddtSchemes\n')
        f.write('{\n')
        f.write('    default         steadyState;\n')
        f.write('}\n')
        f.write('gradSchemes\n')
        f.write('{\n')
        f.write('    default         Gauss linear;\n')
        f.write('    limitedGrad     cellLimited Gauss linear 1;\n')
        f.write('}\n')
        f.write('divSchemes\n')
        f.write('{\n')
        f.write('    default	      Gauss linear;\n')
        f.write('    div(phi,U)       bounded Gauss upwind;\n')
        f.write('    div(phi,k)       bounded Gauss upwind;\n')
        f.write('    div(phi,K)       bounded Gauss upwind;\n')
        f.write('    div(phi,epsilon) bounded Gauss upwind;\n')
        f.write('    div(phi,omega)   bounded Gauss upwind;\n')
        f.write('    div(phi,h)       bounded Gauss upwind;\n')
        f.write('}\n')
        f.write('laplacianSchemes\n')
        f.write('{\n')
        f.write('    default         Gauss linear corrected;\n')
        f.write('}\n')
        f.write('interpolationSchemes\n')
        f.write('{\n')
        f.write('    default         linear;\n')
        f.write('}\n')
        f.write('snGradSchemes\n')
        f.write('{\n')
        f.write('    default         corrected;\n')
        f.write('}\n')
        f.write('fluxRequired\n')
        f.write('{\n')
        f.write('    default         no;\n')
        f.write('    p;\n')
        f.write('    p_rgh;\n')
        f.write('    pcorr;\n')
        f.write('}\n')
        f.close()
    #--------------------------------------------------------------------------------------  
    def basiccontroldict(self):
    
        fcom = self.foamComment()
        head = self.header('system', 'controlDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/controlDict', 'w')
        for aaa in hhh:
            f.write(aaa)	
            
        f.write('application     simpleFoam;\n')
        f.write('startFrom       latestTime;\n')
        f.write('startTime       0;\n')
        f.write('stopAt          endTime;\n')
        f.write('endTime         10000;\n')
        f.write('deltaT          1;\n')
        f.write('writeControl    runTime;\n')
        f.write('writeInterval   1000;\n')
        f.write('purgeWrite      10;\n')
        f.write('writeFormat     ascii;//binary;\n')
        f.write('writePrecision  6;\n')
        f.write('writeCompression uncompressed;\n')
        f.write('timeFormat      general;\n')
        f.write('timePrecision   6;\n')
        f.write('runTimeModifiable yes;\n')
        f.write('adjustTimeStep no;\n')
        f.write('maxCo 1.0;\n')
        f.write('maxDeltaT 1.0;\n')
        f.close()
    #--------------------------------------------------------------------------------------  
    def topoSetDict(self, dic):
        fcom = self.foamComment()
        head = self.header('system', 'topoSetDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/topoSetDict', 'w')
        for aaa in hhh:
            f.write(aaa)	
            
        f.write('actions\n')
        f.write('(\n')
        f.write('    {\n')
        f.write('        name       ' + dic['name'] + ';\n')
        f.write('        type       cellSet;\n')
        f.write('        action     new;\n')
        f.write('        source     boxToCell;\n')
        f.write('        sourceInfo\n')
        f.write('        {\n')
        f.write('             box (' + dic['min'][0] + ' ' + dic['min'][1] + ' ' + dic['min'][2] + ') (' + dic['max'][0] + ' ' + dic['max'][1] + ' ' + dic['max'][2] + ');\n')
        f.write('        }\n')
        f.write('    }\n')
        f.write(');\n')
        f.close()
    #--------------------------------------------------------------------------------------  
    def refineMeshDict(self, dic):
    
        fcom = self.foamComment()
        head = self.header('system', 'refineMeshDict')
        hhh = fcom + head
        f = open(self.caseDir + '/system/refineMeshDict', 'w')
        for aaa in hhh:
            f.write(aaa)	
            
        f.write('set    ' + dic['cellset'] + ';\n')
        f.write('coordinateSystem   global;\n')
        f.write('globalCoeffs\n')
        f.write('{\n')
        f.write('    tan1   (1 0 0);\n')
        f.write('    tan2   (0 1 0);\n')
        f.write('}\n')
        f.write('directions\n')
        f.write('(\n')
        f.write('    tan1\n')
        f.write('    tan2\n')
        f.write('    normal\n')
        f.write(');\n') 
        f.write('useHexTopology     ' + dic['useHexTopology'] + ';\n')
        f.write('geometricCut       ' + dic['geometricCut'] + ';\n')
        f.write('writeMesh          ' + dic['writeMesh'] + ';\n')                           
        f.close() 
        
               
