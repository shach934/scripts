import os
import tkinter as tk
from tkinter import messagebox, ttk

from tkinter import filedialog

root = tk.Tk()

#**********************************************************************************************************#
exec(open("global_setting.py").read())

exec(open("tk_wraper.py").read())

#**********************************************************************************************************#
exec(open("head_buttons.py").read())

#**********************************************************************************************************#
exec(open("solver_tab.py").read())

#**********************************************************************************************************#
exec(open("fvSchemes_tab.py").read())

#**********************************************************************************************************#
exec(open("fvSolution_tab.py").read())

#**********************************************************************************************************#
exec(open("boundary_tab.py").read())

#**********************************************************************************************************#
initial_Condition_tab = tk.Frame(tab_control)                
tab_control.add(initial_Condition_tab, text = f'{"Initial Condition": ^50s}')  

#**********************************************************************************************************#
radiation_tab = tk.Frame(tab_control)                
tab_control.add(radiation_tab, text = f'{"Radiation": ^50s}')   

radiation_on = tk.BooleanVar() 
radiation_on_check = tk.Checkbutton(radiation_tab, text = "Radiation", variable = radiation_on)
radiation_on_check.grid(row = 0, column = 0, sticky = "W")

#**********************************************************************************************************#
motion_tab = tk.Frame(tab_control)                
tab_control.add(motion_tab, text = f'{"Motion": ^50s}')   

MRF_on = tk.BooleanVar()
MRF_on_check = tk.Checkbutton(motion_tab, text = "MRF", variable = MRF_on)
MRF_on_check.grid(row = 0, column = 0, sticky = "W")

dynamicMesh_on = tk.BooleanVar()
dynamicMesh_on_check = tk.Checkbutton(motion_tab, text = "dynamicMesh", variable = dynamicMesh_on)
dynamicMesh_on_check.grid(row = 0, column = 1, sticky = "W")

#**********************************************************************************************************#
tab_control.grid(row = 2, column = 0, columnspan = 10) 

status = ttk.Label(root, text = foam_path.get(), relief = "sunken", anchor = "w")
status.grid(row = 100, column = 0, columnspan = 15, sticky = "WE")

root.mainloop()
