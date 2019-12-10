"""
The procedure to generate a chtMultiRegionSimpleFoam case. 
Main function: 
 * pair the mappedWall patches. 
 * put the boundaries to initial folders.
 * proper initial condition for each region and patch.
 * set the thermophysicalProperties, radiationProperties, gravity....
"""

""" 
The start point is the ANSA out put OpenFOAM folder. 
rules when mesh the geometry in ANSA 

 1, different Mid for solids, fluids regions, solver set to chtMultiRegionSimpleFoam to enable multiRegion folder structure.
 2, mappedWall for the interface.
 3, _wall for wall, inlet, outlet
 4, turbulence model 
 
"""

import numpy as np
import re
import os

foam_folder = r"C:/Shaohui/OpenFoam/car_model_Af/car3_test"

case_name = foam_folder.split("/")[-1]

initial_folder = foam_folder + "/0/"
constant_folder = foam_folder + "/constant/"
system_folder = foam_folder + "/system/"


with open(foam_folder + "/system/controlDict", 'r') as fid:
    text = fid.read()

# solver, end time and save interval. 
solver = re.findall(r"application (.*);", text)[0]
endT = int(re.findall(r"endTime.*?(\d+)\.?;", text)[0])
write_interval = int(re.findall(r"writeInterval.*?(\d+)\.?;", text)[0])

# regions read from the folders. 
regions = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
regions.sort()

# check if this is a multiRegion case, and load the regions' name if so. 
if os.path.exists(constant_folder + "regionProperties"):
	with open(constant_folder + "regionProperties", 'r') as fid:
		text = fid.read()
else:
    print("This is a pure fluid problem!\nCheck the solver again!")

fluid_regions = re.findall(r"fluid.*\((.*)?\)", text)[0].split()
solid_regions = re.findall(r"solid.*\((.*)?\)", text)[0].split()

regions2 = fluid_regions + solid_regions
regions2.sort()

# read in boundary patches of each region.
if regions != regions2:
	print("The multiRegion folder structure is NOT correct! Check again! \n")
	sys.exit()

# read in boundary patches of each region.

for region in regions:

	# loop over each region 
	path = constant_folder + region + "/boundary"
	
	# load the boundary file for this region
	with open(path, 'r') as fid:
		text = fid.read()
		
	file_head = re.findall(r"(.*)\d+.*\(.*\)", text)
	
	text = text.replace("\n", "")
	text = text.replace("\t", "")
	
	file_head = re.findall(r"FoamFile.*?\{(.*?)\}", text)
	file_head = file_head[0].replace(";", ";\n\t", 4)   # here the replace number is hard coded, as the OpenFOAM file head has 5 input in total, if something wrong, change it here. 
	file_head = file_head.replace(" ", "\t\t")
	file_head = "FoamFile\n{\n\t" + file_head + "\n}\n"
	
	bcs = re.findall(r".*(\d+)\((.*)\)", text)
	N_bc, bc_text = int(bcs[0][0]), bcs[0][1].split("}")
	bc_text = bc_text[:N_bc] 
	
	boundaries = {}
	
	for bc in bc_text:
	
		bc_name = bc.split("{")[0]
		
		patch_type= re.findall(r"type (\S+);", bc)	
		startFace = re.findall(r"startFaces (\d+);", bc)
		nFaces 	  = re.findall(r"nFaces (\d+);", bc)

		if patch_type == "mappedWall":
		      
			sampleMode = re.findall(r"sampleMode ([A-Za-z0-9]+);", bc)
			sampleRegion = re.findall(r"sampleRegion ([A-Za-z0-9]+);", bc)
			samplePatch = re.findall(r"samplePatch ([A-Za-z0-9]+);", bc)
			
		elif patch_type == "patch" or patch_type == "wall":
			print("End! ")


OF_structure, boundary =["0", "constant", "system"], {}

for folder in OF_structure:
    for region in solid_regions:
        os.makedirs(case_directory + "/" + folder + "/" + region)
    for region in fluid_regions:
        os.makedirs(case_directory + "/" + folder + "/" + region)


for region in solid_regions:
    if win:
        subprocess.call(r'powershell cp -r ' \
            + mesh_directory + "/constant/" + region + "/polyMesh "\
            + case_directory + "/constant/" + region + "/ " )
    else:
        subprocess.call(r"cp -rf " \
            + mesh_directory + r"/constant/" + region + r"/polyMesh " \
            + case_directory + r"/constant/" + region + r"/ ")

    # extract all the boundary surfaces and their type
    with open(case_directory + r"/constant/" + region + "/polyMesh/boundary") as fid:
        text = fid.read()
    boundary[region] = [re.findall(r"\t(.*)\n\t\{", text), re.findall(r"type\ *\t*(.*);", text)]

for region in fluid_regions:
    if win:
        subprocess.call(r'powershell cp -r ' \
            + mesh_directory + "/constant/" + region + "/polyMesh "\
            + case_directory + "/constant/" + region + "/ " )
			
    # extract all the boundary surfaces and their type
    with open(case_directory + r"/constant/" + region + "/polyMesh/boundary") as fid:
        text = fid.read()
    boundary[region] = [re.findall(r"\t(.*)\n\t\{", text), re.findall(r"type\ *\t*(.*);", text)]


turb_model = re.findall(r"turbulence model:\ *\t*\ *(.*)\n", config)[0].split("/")

MRF_count = int(re.findall(r"MRF:\ *\t*\ *(.*)\ *\n", config)[0])

for m in range(MRF_count):
    MRF_region = re.findall(r"MRF_region:(.*)", config)[0]
    MRF_cellzone = re.findall(r"MRF_cellZone:(.*)", config)[0]
    MRF_origin = re.findall(r"MRF_origin:(.*)", config)[0]
    MRF_axis = re.findall(r"MRF_axis:(.*)", config)[0]
    MRF_omega = re.findall(r"MRF_omega:(.*)", config)[0]