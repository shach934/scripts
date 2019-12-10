label_size = [15, 3]
entry_width = 30
combo_size = [entry_width - 1, 3]

N_regions = 3

boundary_tab = tk.Frame(tab_control)                
tab_control.add(boundary_tab, text = f'{"Boundary": ^50s}')  

boundary_pool = ["wall", "mappedWall", "patch", "cyclicAMI"]
relax_grid = [0, 0, 3, 10]

for region_i in range(N_regions):
    relaxationFactors = tk.LabelFrame(boundary_tab, text = "region" + str(region_i), padx = 5, pady = 5)
    relaxationFactors.grid(row = region_i, column = 0)


num_bc = 10

col_name = ["Name", "Type", "sampleRegion", "samplePatch", "sampleMethod"]

for i in range(len(col_name)):
    col_name_label = tk.Label(boundary_tab, text = col_name[i], width = 12)
    col_name_label.grid(row = 0, column = i)

boundary_name_col = tk.Label(boundary_tab, text = "Name")
boundary_type_col = tk.Label(boundary_tab, text = "Type")


for i in range(num_bc):
    boundary_name_label = tk.Label(boundary_tab, text = "Boundary" + str(i))
    boundary_name_label.grid(row = i + 1, column = 0)