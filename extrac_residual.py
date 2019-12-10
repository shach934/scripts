import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import re

file_path = "C:/Shaohui/OpenFoam/scripts/log"

with open(file_path, 'r') as fid:
    text = fid.read()

# check how many time steps
step_num = re.compile(r'\nTime = (\d*)\n')
steps = step_num.findall(text)
Time_steps = [m for m in steps]

# extract all the time steps
single_step = re.finditer(r"\nTime = ", text)
indices = [m.start() for m in single_step]
block = text[indices[0]:indices[1]]

# extract the regions name
regions = re.compile(r"region (.*)\n")
region_names = regions.findall(block)

# region and time step number
N_regions = len(region_names)
N_steps = len(indices) - 1

# extract the solved field for each region
region_fields = {}
regions = block.split("region")
regions = regions[1:]

for i in range(N_regions):
    region = regions[i]
    solved = re.compile(r"Solving for (.*), I")
    field = solved.findall(region)
    
    count = {}
    for f in field:
        if f in count:
            count[f] = count[f] + 1
        else:
            count[f] = 1
    
    field = []
    for item in count:
        if count[item] > 1:
            field.extend([item + str(i) for i in range(count[item])])
        else:
            field.append(item)
    field_full = []
    for f in field:
        field_full.extend([f + "_init", f + "_final"])

    if region.find("Min/max T:") is not -1:
        Thermo = True
        field_full.extend(["T_Min", "T_Max"])
    else:
        Thermo = False

    region_fields[region_names[i]] = field_full

dfs = {}
for region_name in region_names:
    dfs[region_name] = pd.DataFrame(0.0, index=np.arange(N_steps), columns = region_fields[region_name])

resi = re.compile(r"residual = (-?\ *\d+\.?\d*(?:[Ee]\ *-?\ *\d+)?),")
extreme_T = re.compile(r"Min/max T:(-?\d*\.?\d*) (-?\d*\.?\d*)\n")

for step in range(N_steps - 1):
    block = text[indices[step]:indices[step + 1]]

    regions = block.split("region")
    regions = regions[1:]

    for r in range(N_regions):
        step_resi = [float(num) for num in resi.findall(regions[r])]

        if Thermo:
            Ts = extreme_T.findall(regions[r])
            Tmin_max = [float(num) for t in Ts for num in t]
            step_resi.extend(Tmin_max)

        if len(dfs[region_names[r]].iloc[step, :]) is not len(step_resi):
            continue
        dfs[region_names[r]].iloc[step, :] = np.array(step_resi)

for region_name in region_names:
    dfs[region_name] = dfs[region_name][(dfs[region_name].T != 0).any()]

plotFrom = 0

fig1 = plt.figure(1, figsize = (25, 15))
fig2 = plt.figure(2, figsize = (25, 15))

for i, region_name in enumerate(region_names):

    resi_cols = dfs[region_name].columns[0:-2:2]
    ax1 = fig1.add_subplot("22"+str(i +1 ))
    dfs[region_name][resi_cols][plotFrom:].plot(kind = "line",logx=False, logy=True, legend = 1, ax = ax1)
    ax1.title.set_text(region_name)

    T_cols = dfs[region_name].columns[-2:]
    ax2 = fig2.add_subplot("22"+str(i +1 ))
    ax2.title.set_text(region_name)
    dfs[region_name][T_cols][plotFrom:].plot(kind = "line",logx=False, logy=True, legend = 1, ax = ax2)

plt.show()