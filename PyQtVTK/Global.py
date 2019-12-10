from time import localtime, strftime
from tkinter import ttk
import tkinter as tk
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
#*************************************read fields of each tab***********************************************#

solver_field = ["application", "startFrom", "endTime", "deltaT", "writeInterval", "runTimeModifiable", "adjustTimeStep", "maxCo"]


#***************************************apparence config*********************************************#
icon_path = r'c:\Shaohui\OpenFoam\scripts\OpenFOAM_icon.ico'

root = tk.Tk()
root.iconbitmap(icon_path)
root.title("OpenFOAM")
# root.geometry('250x150+300+300')
root.configure(background = 'gray99')
root.option_add("*Times New Rome", "courier 24")

style = ttk.Style(root)

mygreen = "#d2ffd2"
myred = "Dodgerblue2"

style.theme_create( "myTab", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 15, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], 
                          "font" : ('URW Gothic L', '12', 'bold'), 
                          "background": mygreen },
            "map":       {"background": [("selected", myred)],
                        "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("myTab")
style.configure('myTab', tabposition='wn')  # horizontal  tapposition = 'nw'

button_size = [20, 2]
small_buttion_size = [15, 1]
label_size = [25, 3]
entry_width = 30
combo_size = [entry_width - 1, 3]

label_justify = {"anchor": "w", "justify":"left", "padx":30}
switch_pool = ["True", "False"]

#*****************************************Global vairables to store foam config****************************#
# cannot defined before the Tk() root object is initiated
foam_path = tk.StringVar()
status = tk.StringVar()


"""
turbulence_info: region: [simulationType-"laminar"], region: [simulationType: "RAS", RASModel:"kEpsilon", turbulance- "on", ...]
region_info: if not a multiRegion case: default: fluid, else: region_info["region1"] = "fluid" or "solid"
decomposeParDict:  global: [number of domains, decompose method], region1:[number of domains, decompose method]....
boundary_info: 
"""

solver_info, region_info, region_info, boundary_info, fvSchemes_info, fvSolution_info, fvOptions_info, radiation_info, MRF_info, dyMesh_info, decomp_info, iniCond_info, turbulence_info = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}


#**********************************************************************************************************#
wallDist = "method meshWave"
interpolationSchemes = "default linear"