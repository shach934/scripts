from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

class Patch(object):
    def __init__(self, name = None, region = None, type = "", startFace = 0, nFaces = 0):
        self.name = name
        self.region = region
        self.type = type
        self.startFace = startFace
        self.nFaces = nFaces

class MappedWall(Patch):
    def __init__(self, name = None, region = None, type = "mappedWall", startFace = 0, nFaces = 0, sampleMode = None, samplePatch = None, sampleRegion = None):
        super(MappedWall, self).__init__(name, region, type, startFace, nFaces)
        self.sampleMode = sampleMode
        self.samplePatch = samplePatch
        self.sampleRegion = sampleRegion
        
class CyclicAMI(Patch):
    def __init__(self, name = None, region = None, type = "cyclicAMI", startFace = 0, nFaces = 0, Tolerance = 0.0, neighbourPatch = None, transform = None):
        super(CyclicAMI, self).__init__(name, region, type, startFace, nFaces)
        self.Tolerance = Tolerance
        self.neighbourPatch = neighbourPatch
        self.transform = transform

#**********************************************************************************************************#

def browse_button(root, foam_path):
    filename = filedialog.askdirectory()
    foam_path.set(filename)
    foam_path_str = foam_path.get()  
    case_name = foam_path_str.split("/")[-1]
    root.title(case_name + " : " + foam_path_str)

def update_row_col(tab_row_col):
    # tab_row_col = [row, col, row_max, col_max]
    tab_row_col[1] = tab_row_col[1] + 2
    if tab_row_col[1] >= tab_row_col[3]:
        tab_row_col[0] = tab_row_col[0] + 1
        if tab_row_col[0] >= tab_row_col[2]:
            print("outFlow")
            tab_row_col[0] = tab_row_col[0] + 1 
        tab_row_col[1] = 0
    return tab_row_col

def make_entry(parent, caption, label_size = label_size, location = [0, 0], entry_size = entry_width,\
    label_opt = None, entry_opt = None):
    label = tk.Label(parent, text = caption, width = label_size[0], height = label_size[1])
    label.grid(row = location[0], column = location[1])
    if label_opt:
        label.config(label_opt)

    entry = tk.Entry(parent, width = entry_size)
    entry.grid(row = location[0], column = location[1] + 1)

    if entry_opt:   
        entry.config(entry_opt)
    update_row_col(location)

    return entry

def make_Combo(parent, caption, label_size = label_size, location = [0, 0], combo_value = "", combo_size = combo_size,\
    label_opt = None, combo_opt = None):
    label = tk.Label(parent, text = caption, width = label_size[0], height = label_size[1])
    label.grid(row = location[0], column = location[1])
    
    if label_opt:
        label.config(label_opt)

    combo = ttk.Combobox(parent, value = combo_value, width = combo_size[0], height = combo_size[1])
    combo.grid(row = location[0], column = location[1] + 1)

    if combo_opt:
        combo.config(combo_opt)
    combo.current([0])
    update_row_col(location)
    return combo

"""
def open_path(event, path):
    os.startfile(path)
"""