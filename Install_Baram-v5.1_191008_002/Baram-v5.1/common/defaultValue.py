#-*-coding:utf8-*-

class defaultValueClass:

    def __init__(self,mainself):pass
               
    def defaultDict(self):
    
        # simulation condition
        simDict={}
        keys=['Time advance','Energy','solver',
              'Turbulence model','Prt','ReyStar','deltaRey',
              'density_method','density','transport_method','viscosity','conductivity','As','Ts','Cp','molecular weight',
              'Gravity',
              'radiationModel','solverFrequency','absorptivity','emissivity','E','wallEmissivity','nPhi','nTheta','convergence','maxIter','cacheDiv']
        values=['Steady','Off','simpleNFoam',
                'kEpsilon','0.85','60','10',
                'Constant','1.225','Constant','1e-5','0.0245','1.67212e-6','170.672','1004','28',
                'None',
                'none','1','0.5','0.5','0',{},'3','5','1e-3','10','false']
        for i in range(len(keys)):simDict[keys[i]]=values[i]

        # initial condition
        initialDict={}
        keys=['X-velocity','Y-velocity','Z-velocity','Pressure [Pa]','Temperature [K]','velocityScale [m/s]','turbulentIntensity','viscosityRatio','nuTilda']       
        values=['0','0','0','0','300','1','0.001','10','1e-6']
        
        for i in range(len(keys)):initialDict[keys[i]]=values[i]
        
        # run condition
        runDict={}
        keys=['startFrom','startTime','stopAt','endTime','deltaT','writeInterval','writeControl','purgeWrite','writeFormat',
              'writePrecision','writeCompression','timeFormat','timePrecision','runTimeModifiable','adjustTimeStep','maxCo','nCores','machineType','plotResidual',
              'hostfile']
        values=['latestTime','0','endTime','1000','1','500','adjustableRunTime','0','binary',
                '6','no','general','6','yes','no','1','1','SMP','no',
                'None']
        for i in range(len(keys)):runDict[keys[i]]=values[i]
       
        # numerical
        numeDict={}
        keys=['discretize_time','discretize_momentum','discretize_energy','discretize_turbulence',
              'nOuterCorrectors',
              'relax_pressure','relax_momentum','relax_energy','relax_turbulence',
              'conv_pressure','conv_momentum','conv_energy','conv_turbulence','conv_pressure_relative','conv_momentum_relative','conv_energy_relative','conv_turbulence_relative',
              'Use Ref. Pressure','refPoint-x','refPoint-y','refPoint-z','refValue']
        values=['firstOrder','secondOrder','secondOrder','firstOrder',
                '10',
                '0.3','0.7','0.9','0.7',
                '0.001','0.001','0.001','0.001','0.05','0.05','0.05','0.05',
                False,'0','0','0','0']
                
        for i in range(len(keys)):numeDict[keys[i]]=values[i]            
       
        # display patch        
        patchDict={}        
        keys=['scalar','time','colormap','displayContour','displayVector','colorBy','scaleFactor','patches','Overlay']        
        values=['p','0','blue to red',False,False,'Scalar','0.1',[],False] 

        for i in range(len(keys)):patchDict[keys[i]]=values[i]

        # display cutPlane        
        cutDict={}        
        keys=['scalar', 'time', 'colormap', 'displayContour', 'displayVector', 'colorBy', 'scaleFactor', 'Overlay', 'dataType']        
        values=['p', '0', 'blue to red', False, False, 'Scalar', '0.001', False, 'point value'] 

        for i in range(len(keys)):cutDict[keys[i]]=values[i]

        # display isoSurface        
        isoDict={}        
        keys=['scalar', 'time', 'colormap', 'displayContour', 'Overlay', 'isoField', 'dataType']
        values=['coordsX', '0', 'blue to red', False, False, 'coordsX', 'point value']

        for i in range(len(keys)):isoDict[keys[i]]=values[i]
        
        # display clip        
        clipDict={}        
        keys=['scalar', 'time', 'colormap', 'clipBy', 'value']
        values=['coordsX', '0', 'blue to red', 'coordsX', 0]

        for i in range(len(keys)):clipDict[keys[i]]=values[i]
                   
        # display pathline        
        streamDict={}        
        keys=['scalar', 'time', 'colormap', 'Overlay', 'showSeed', 'integrator', 'direction', 'maxLength',
              'shape', 'lineWidth', 'tubeRadius', 'ribbonWidth', 'ribbonAngle']
        values=['Umag', '0', 'blue to red', False, True, 'RungeKutta45', 'both', '5',
                'line', '3', '0.003', '0.003', '0']

        for i in range(len(keys)):streamDict[keys[i]]=values[i]
        
        return [simDict,initialDict,runDict,numeDict,patchDict,cutDict,isoDict,clipDict,streamDict]


