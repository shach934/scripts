import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re
from Global import *


class Patch(object):
    def __init__(self, name=None, region=None, type="", startFace=0, nFaces=0):
        self.name = name
        self.region = region
        self.type = type
        self.startFace = startFace
        self.nFaces = nFaces


class MappedWall(Patch):
    def __init__(self, name = None, region=None, type="mappedWall", startFace=0, nFaces=0, sampleMode=None,
                 samplePatch=None, sampleRegion=None):
        super(MappedWall, self).__init__(name, region, type, startFace, nFaces)
        self.sampleMode = sampleMode
        self.samplePatch = samplePatch
        self.sampleRegion = sampleRegion


class CyclicAMI(Patch):
    def __init__(self, name=None, region=None, type="cyclicAMI", startFace=0, nFaces=0, Tolerance=0.0,
                 neighbourPatch=None, transform=None):
        super(CyclicAMI, self).__init__(name, region, type, startFace, nFaces)
        self.Tolerance = Tolerance
        self.neighbourPatch = neighbourPatch
        self.transform = transform


class MRF_zone(object):
    def __init__(self, name, cellZone, active, nonRotatingPatches, origin, axis, omega):
        self.name = name
        self.cellZone = cellZone
        self.active = active
        self.nonRotatingPatches = nonRotatingPatches
        self.origin = origin
        self.axis = axis
        self.omega = omega


class Turbulence_model(object):
    def __init__(self, turbulence):
        self.turbulence = turbulence


class Physical_property(object):
    def __init__(self, mu):
        self.mu = mu


class radiation_model(object):
    def __init__(self):
        self.radiation_model = radiation_model


class FoamCase(object):

    def __init__(self, in_path, out_path):
        self.input_path = in_path
        self.out_path = out_path

    def __init__(self):
        self.solver = solver_info

    def _read_case(self):
        self.solver_info = read_controlDict()

    def _write_case(self):
        with open(self.out_path, "rw"):
            pass


def read_text(path):
    # strip off the OpenFOAM head part
    try:
        with open(path, "r") as fid:
            text = fid.read()
        text = text[text.find("}") + 1:]
    except IOError as e:
        return [""]
    return text


def read_controlDict():
    global status, solver_info

    default_solver_info = ["chtMultiRegionSimpleFoam", "latestTime", "1000", "1", "50", "yes", "no", "1"]

    try:
        with open(foam_path.get() + "/system/controlDict", 'r') as fid:
            text = fid.read()
            for i, field in enumerate(solver_field):
                info = re.findall(field + r"(.*)?;", text)
                info = [i for i in info if len(i)]
                if info:
                    solver_info[field] = info[0].strip()
                else:
                    solver_info[field] = "None"
    except IOError:
        status.set("No solver info, set to Default config!\n")
        for i, field in enumerate(solver_field):
            info = re.findall(field + r"(.*);", text)
            if info[0]:
                solver_info[i] = default_solver_info[i]


def read_regions():
    # region info can have three different situation:
    # multiRegion:  fluid + solid  or  solid + solid
    # singleRegion: fluid   No sub folder system
    # singleRegion: solid   still sub system 
    global status, region_info

    initial_folder = foam_path.get() + "/0/"
    constant_folder = foam_path.get() + "/constant/"
    system_folder = foam_path.get() + "/system/"

    if os.path.exists(constant_folder + "regionProperties"):
        with open(constant_folder + "regionProperties", 'r') as fid:
            text = fid.read()
        fluid_regions = re.findall(r"fluid.*\((.*)?\)", text)[0].split()
        solid_regions = re.findall(r"solid.*\((.*)?\)", text)[0].split()

        regions = fluid_regions + solid_regions
        regions = [name for name in regions if len(name)]  # maybe there is no fluid or solid region at all.
        regions.sort()

        regions2 = [name for name in os.listdir(constant_folder) if os.path.isdir(constant_folder + "/" + name)]
        regions2.sort()

        regions3 = [name for name in os.listdir(initial_folder) if os.path.isdir(initial_folder + "/" + name)]
        regions3.sort()

        regions4 = [name for name in os.listdir(system_folder) if os.path.isdir(system_folder + "/" + name)]
        regions4.sort()

        if regions != regions2 or regions != regions3 or regions != regions4:
            status.set("The multiRegion folder structure is NOT correct! Check again! \n")
        else:
            region_info = {}
            for region in solid_regions:
                if len(region):
                    region_info[region] = "solid"
            for region in fluid_regions:
                if len(region):
                    region_info[region] = "fluid"

    else:
        status.set("No regionProperties dict! Treat it as single phase case\n")
        region_info["default"] = "fluid"
        return 0


def read_bc(path):
    global status
    try:
        text = open(path, 'r').read()
    except IOError:
        status.set(path + "no such file exists! \n")
        return 0

    text = text.replace("\n", "")
    text = text.replace("\t", "")

    bcs = re.findall(r".*(\d+)\((.*)\)", text)
    N_bc, bc_text = int(bcs[0][0]), bcs[0][1].split("}")[:-1]
    region = path.split("/")[-2]
    boundaries = []

    for bc in bc_text:

        bc_name = bc.split("{")[0]
        patch_type = re.findall(r"type (\S+);", bc)[0]
        startFace = re.findall(r"startFace (\d+);", bc)[0]
        nFaces = re.findall(r"nFaces (\d+);", bc)[0]

        if patch_type == "mappedWall":
            sampleMode = re.findall(r"sampleMode (\S+);", bc)[0]
            sampleRegion = re.findall(r"sampleRegion (\S+);", bc)[0]
            samplePatch = re.findall(r"samplePatch (\S+);", bc)[0]

        elif patch_type == "cyclicAMI":
            Tolerance = re.findall(r"Tolerance (\S+);", bc)[0]
            neighbourPatch = re.findall(r"neighbourPatch (\S+);", bc)[0]
            transform = re.findall(r"transform (\S+);", bc)[0]

        elif patch_type != "patch" and patch_type != "wall":
            status.set("I don't know the patch type! \nCheck again! \n")

        if patch_type == "wall" or patch_type == "patch":
            boundaries.append(Patch(bc_name, region, patch_type, startFace, nFaces))
        elif patch_type == "mappedWall":
            boundaries.append(
                MappedWall(bc_name, region, patch_type, startFace, nFaces, sampleMode, samplePatch, sampleRegion))
        elif patch_type == "cyclicAMI":
            boundaries.append(
                CyclicAMI(bc_name, region, patch_type, startFace, nFaces, Tolerance, neighbourPatch, transform))
        else:
            status.set("No suitable patch class for this boundary! \n")
    return boundaries


def load_boundary():
    global boundary_info
    constant_folder = foam_path.get() + "/constant/"
    if len(region_info) > 1:
        # loop over each region
        for region in list(region_info.keys()):
            path = constant_folder + region + "/polyMesh/boundary"
            # load the boundary file for this region
            boundary_info[region] = read_bc(path)
    else:
        boundary_info[next(iter(region_info))] = read_bc(constant_folder + "/polyMesh/boundary")


def read_fvSchemes():
    fvSchemes_info = {}


def read_fvSolution():
    fvSolution_info = {}


def read_fvOptions():
    fvOption_info = {}


def read_radiation():
    global radiation_info


def read_MRF():
    global MRF_info

    if len(region_info) == 1 and "default" in region_info:
        MRF_path = foam_path.get() + "/constant/MRFProperties"
    else:
        for region in list(region_info.keys()):
            if region_info[region] == "fluid":
                path = foam_path.get() + "/constant/" + region + "/MRFProperties"
                with open(path, "r") as fid:
                    text = fid.read()
                MRF_names = re.findall(r"(.*)\s\{", text)[1:]


def read_dyMesh():
    global dyMesh_info


def read_decomp():
    global decomp_info
    global_decom = foam_path.get() + "/system/decomposeParDict"
    decomp_info["global"] = []

    with open(global_decom, "r") as fid:
        text = fid.read()

    decomp_info["global"].append(re.findall(r"numberOfSubdomains\s(\d*);", text)[0])
    decomp_info["global"].append(re.findall(r"method\s(.*);", text)[0])

    for region in list(region_info.keys()):
        if region != "default":
            path = foam_path.get() + "/system/" + region + "/decomposeParDict"
            with open(global_decom, "r") as fid:
                text = fid.read()
            decomp_info[region].append(re.findall(r"numberOfSubdomains\s(\d*);", text)[0])
            decomp_info[region].append(re.findall(r"method\s(.*);", text)[0])


def read_iniCond():
    iniCond_info = {}


def read_turbulence():
    # from the region_info dict to find the fluid regions and parse turbulenceProperties. 
    # default fluid region is for the single domain case.

    global status, turbulence_info
    constant_folder = foam_path.get() + "/constant/"

    if len(region_info) >= 1:

        for region in list(region_info.keys()):
            if region_info[region] == "fluid":

                if region == "default":
                    turbulance_path = constant_folder + "/turbulenceProperties"

                elif region != "default":
                    turbulance_path = constant_folder + "/" + region + "/turbulenceProperties"

                if os.path.isfile(turbulance_path):
                    with open(turbulance_path, "r") as fid:
                        text = fid.read()

                    turbulence_info[region] = []
                    turbulence_info[region].append(re.findall(r"simulationType (.*?);", text)[0])

                    if turbulence_info[region][0] == "RAS":  # add other turbulence model!
                        turbulence_info[region].append(re.findall(r"RASModel (.*?);", text)[0])
                        turbulence_info[region].append(re.findall(r"turbulence (.*?);", text)[0])
                        turbulence_info[region].append(re.findall(r"printCoeffs (.*?);", text)[0])
                else:
                    status.set("missing turbulanceProperties file for " + region + " fluid!, check again! \n")


def diff_mappedWall_AMI():
    global boundary_info, status
    # now pair the boundaries to make sure the mappedWall and cyclicAMI pair properly. 
    # Change the patch name of mappedWall at fluid side to _shadow to avoid confusing.
    # just loop the solid region, slave correspoinding fluid's patches.
    for region in list(region_info.keys()):

        boundary = boundary_info[region]
        for patch in boundary:

            if patch.type == "mappedWall" and patch.name == patch.samplePatch:

                patch2change = patch.samplePatch
                patch.samplePatch = patch.samplePatch + "_shadow"

                candidate_patches = boundary_info[patch.sampleRegion]
                found = False
                for patch in candidate_patches:
                    # check the corresponding slave patch is mappedWall type
                    if patch.name == patch2change and patch.type != "mappedWall":
                        status.set("Check the patch type, it is not a mappedWall!\n")
                        found = True
                    # check the corresponding slave patch is mapped to the master patch.    
                    elif patch.name == patch2change and patch.samplePatch == patch2change:
                        patch.name = patch.name + "_shadow"
                        found = True
                if not found:
                    status.set("Didn't found the mappedWall slave in corresspoding region! Check again!\n")


# **********************************************************************************************************#
def fetch_path():
    global foam_path
    filename = filedialog.askdirectory()
    foam_path.set(filename)
    case_name = filename.split("/")[-1]
    root.title(case_name + " : " + filename)


def load_case():
    global solver_info, region_info, region_info, boundary_info, fvSchemes_info, fvSolution_info, fvOptions_info, radiation_info, MRF_info, dyMesh_info, decomp_info, iniCond_info, turbulence_info

    read_controlDict()
    read_regions()
    load_boundary()
    read_turbulence()
    read_decomp()
    read_fvSchemes()
    read_fvSolution()
    read_fvOptions()
    read_radiation()
    read_MRF()
    read_dyMesh()
    read_iniCond()


def update_row_col(tab_row_col):
    # tab_row_col = [row, col, row_max, col_max]
    tab_row_col[1] = tab_row_col[1] + 2
    if tab_row_col[1] >= tab_row_col[3]:
        tab_row_col[1] = 0
        tab_row_col[0] = tab_row_col[0] + 1
        if tab_row_col[0] >= tab_row_col[2]:
            print("outFlow")
            tab_row_col[0] = tab_row_col[0] + 1
    return tab_row_col


def make_entry(parent, caption, label_size=label_size, location=[0, 0], entry_size=entry_width, \
               label_opt=None, entry_opt=None):
    label = tk.Label(parent, text=caption, width=label_size[0], height=label_size[1])
    label.grid(row=location[0], column=location[1])
    if label_opt:
        label.config(label_opt)

    entry = tk.Entry(parent, width=entry_size)
    entry.grid(row=location[0], column=location[1] + 1)

    if entry_opt:
        entry.config(entry_opt)
    location = update_row_col(location)

    return entry


def make_Combo(parent, caption, label_size=label_size, location=[0, 0], combo_value="", combo_size=combo_size, \
               label_opt=None, combo_opt=None):
    label = tk.Label(parent, text=caption, width=label_size[0], height=label_size[1])
    label.grid(row=location[0], column=location[1])

    if label_opt:
        label.config(label_opt)

    combo = ttk.Combobox(parent, value=combo_value, width=combo_size[0], height=combo_size[1])
    combo.grid(row=location[0], column=location[1] + 1)

    if combo_opt:
        combo.config(combo_opt)
    combo.current([0])
    location = update_row_col(location)
    return combo


"""
# confirm closing!! 
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        
exit_button = Button(window, text='Quit', command=on_closing)
exit_button.pack()
"""
"""
def open_path(event, path):
    os.startfile(path)
"""

if __name__ == "__main__":
    path = r"C:/Shaohui/OpenFoam/car_model_Af/car3_test"
    foam_path = tk.StringVar()
    foam_path.set(path)
    read_controlDict()
    read_regions()
    load_boundary()
    read_turbulence()

    print(turbulence_info)
