from time import localtime, strftime

# OpenFOAM files, FoamFile info, for scalar field also UNIT.
# FoamFile: "class" and "object" type
# UNIT: SI [kg(weight), m(meter), s(second), K(kelvin), mol(mole), A(ampere), cd(candela)]
# fileName : [class, object, unit]

#**********************************Write out file ingredients****************************************************#
FoamFile_Dict = {
# files in constant folder
    "regionProperties":             ["dictionary",                      "regionProperties"],                \
    "thermophysicalProperties":     ["dictionary",                      "thermophysicalProperties"],        \
    "radiationProperties":          ["dictionary",                      "radiationProperties"],             \
    "boundary":                     ["polyBoundaryMesh",                "boundary"],                        \
    "dynamicMeshDict":              ["dictionary",                      "dynamicMeshDict"],                 \
    "turbulenceProperties":         ["dictionary",                      "turbulenceProperties"],            \
    "transportProperties":          ["dictionary",                      "transportProperties"],             \
    "MRFProperties":                ["dictionary",                      "MRFProperties"],                   \
    "boundaryRadiationProperties":  ["dictionary",                      "boundaryRadiationProperties"],     \
# files in 0 folder, except g in constant
    "nut":                          ["volScalarField",                  "IDefault",  "[0 2 -1 0 0 0 0]"],   \
    "k":                            ["volScalarField",                  "k",         "[0 2 -2 0 0 0 0]"],   \
    "IDefault":                     ["volScalarField",                  "IDefault",  "[1 0 -3 0 0 0 0]"],   \
    "epsilon":                      ["volScalarField",                  "epsilon",   "[0 2 -3 0 0 0 0]"],   \
    "alphat":                       ["volScalarField",                  "alphat",    "[1 -1 -1 0 0 0 0]"],  \
    "U":                            ["volScalarField",                  "U",         "[0 1 -1 0 0 0 0]"],   \
    "T":                            ["volScalarField",                  "T",         "[0 0 0 1 0 0 0]"],    \
    "p_rgh":                        ["volScalarField",                  "p_rgh",     "[1 -1 -2 0 0 0 0]"],  \
    "p":                            ["volScalarField",                  "p",         "[1 -1 -2 0 0 0 0]"],  \
    "g":                            ["uniformDimensionedVectorField",   "g",         "[0 1 -2 0 0 0 0]"],   \
# files in system folder
    "fvOptions":                    ["dictionary",                      "fvOptions"],                       \
    "fvSchemes":                    ["dictionary",                      "fvSchemes"],                       \
    "fvSolution":                   ["dictionary",                      "fvSolution"],                      \
    "decomposeParDict":             ["dictionary",                      "decomposeParDict"],                \
    "controlDic":                   ["dictionary",                      "controlDict"]                      \
}

OpenFOAM_declaimer = r"""  
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v1906                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |
|    \\/     M anipulation  | Time:     """ + strftime("%Y-%m-%d %H:%M:%S", localtime()) + \
r"""                   |
\*---------------------------------------------------------------------------*/
"""

split_line = r"// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"


requiredFields = {"laminar": ["p", "U"],
                 "RAS.kEpsilon":["k", "p", "U", "epsilon"]}

wallDist = "method meshWave"
interpolationSchemes = "default linear"