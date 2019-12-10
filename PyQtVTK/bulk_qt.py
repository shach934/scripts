from functions import *

# 模块化就好好的模块化，不能胡子眉毛一把抓，要好好的分块，然后整合到一起去！ 
# 读→→显示→→调整→→写出
# 读：每个tab需要的内容分别读出
# 显示：每个模块分别显示
# 调整：每个变量记录需要的选项
# 写出：每个变量，格式写出

# **********************************************************************************************************#
N_button = 0

browse_button = tk.Button(root, text="OpenFOAM Case", width=button_size[0], height=button_size[1], command=fetch_path)

browse_button.grid(row=0, column=N_button)
N_button += 1

next_button = tk.Button(root, text='Load', width=button_size[0], height=button_size[1], command=load_case)
next_button.grid(row=0, column=N_button)
N_button += 1

write_button = tk.Button(root, text='Write', width=button_size[0], height=button_size[1])
write_button.grid(row=0, column=N_button)
N_button += 1

openDir_button = tk.Button(root, text='Open Directory', width=button_size[0],
                           height=button_size[1])  # , command = lambda event: open_path(event, path))
openDir_button.grid(row=0, column=N_button)
N_button += 1

exit_button = tk.Button(root, text='Quit', width=button_size[0], height=button_size[1], command=root.destroy)
exit_button.grid(row=0, column=N_button)
N_button += 1

tab_control = ttk.Notebook(root, style='lefttab.TNotebook')

# **********************************************************************************************************#

# regions read from the folders. 

# read the regions properties.

# **********************************************************************************************************#
solver_tab = tk.Frame(tab_control)
tab_control.add(solver_tab, text=f'{"Solver": ^30s}')

# solve_info: [solver, startFrom, endTime, deltaT, writeInterval, runTimeModifiable, adjustTimeStep, maxCo]

solver, startFrom, endTime, deltaT, writeInterval, runTimeModifiable, adjustTimeStep, maxCo = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

solver_tab_grid = [0, 0, 4, 4]

solver_pool = ["chtMultiRegionSimpleFoam", "interFoam", "chtMultiRegionFoam"]
combo_opt = {"justify": "left", "textvariable": solver}
solver_Combo = make_Combo(solver_tab, "application: ", label_size, solver_tab_grid, solver_pool, combo_size,
                          label_justify, combo_opt)
solver.set(solver_Combo.get())

entry_opt = {"justify": "left", "textvariable": startFrom}
startT_entry = make_entry(solver_tab, "startFrom: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
startFrom.set(startT_entry.get())

entry_opt = {"justify": "left", "textvariable": endTime}
endT_entry = make_entry(solver_tab, "endTime: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
endTime.set(endT_entry.get())

entry_opt = {"justify": "left", "textvariable": deltaT}
deltaT_entry = make_entry(solver_tab, "deltaT: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
deltaT.set(deltaT_entry.get())

entry_opt = {"justify": "left", "textvariable": writeInterval}
writeInterval_entry = make_entry(solver_tab, "writeInterval: ", label_size, solver_tab_grid, entry_width, label_justify,
                                 entry_opt)
writeInterval.set(writeInterval_entry.get())

runTimeModifiable_opt = {"justify": "left", "textvariable": runTimeModifiable}
runTimeModifiable_Combo = make_Combo(solver_tab, "runTimeModifiable: ", label_size, solver_tab_grid, switch_pool,
                                     combo_size, label_justify, runTimeModifiable_opt)
runTimeModifiable.set(runTimeModifiable_Combo.get())

adjustTimeStep_opt = {"justify": "left", "textvariable": adjustTimeStep}
adjustTimeStep_Combo = make_Combo(solver_tab, "adjustTimeStep: ", label_size, solver_tab_grid, switch_pool, combo_size,
                                  label_justify, adjustTimeStep_opt)
adjustTimeStep.set(adjustTimeStep_Combo.get())

maxCo_opt = {"justify": "left", "state": "readonly", "textvariable": maxCo}
maxCo_entry = make_entry(solver_tab, "maxCo: ", label_size, solver_tab_grid, entry_width, label_justify, maxCo_opt)
maxCo.set(maxCo_entry.get())

decomposeParDict = tk.StringVar()
decomposeParDict_opt = {"justify": "left", "textvariable": decomposeParDict}
decomposeParDict_entry = make_entry(solver_tab, "decomposeParDict: ", label_size, solver_tab_grid, entry_width,
                                    label_justify, decomposeParDict_opt)
decomposeParDict.set(decomposeParDict_entry.get())

# **********************************************************************************************************#
fvSchemes_tab = tk.Frame(tab_control)
tab_control.add(fvSchemes_tab, text=f'{"fvSchemes": ^30s}')

fvSchemes_tab_grid = [0, 0, 6, 4]

ddtSchemes = tk.StringVar()
ddtSchemes_pool = ["steadyState", "Euler", "localEuler", "backward", "CrankNicolson"]
ddtSchemes_opt = {"justify": "left", "textvariable": ddtSchemes}
ddtSchemes_Combo = make_Combo(fvSchemes_tab, "ddtSchemes: ", label_size, fvSchemes_tab_grid, ddtSchemes_pool,
                              combo_size, label_justify, ddtSchemes_opt)
ddtSchemes.set(ddtSchemes_Combo.get())

gradScheme = tk.StringVar()
gradScheme_pool = ["Gauss linear", "leastSquares", "cellLimited Gauss linear 1", "cellLimited Gauss linear 0.33",
                   "cellLimited Gauss linear 0.5"]
gradScheme_opt = {"justify": "left", "textvariable": gradScheme}
gradScheme_Combo = make_Combo(fvSchemes_tab, "gradScheme: ", label_size, fvSchemes_tab_grid, gradScheme_pool,
                              combo_size, label_justify, gradScheme_opt)
gradScheme.set(gradScheme_Combo.get())

laplacianSchemes = tk.StringVar()
laplacianSchemes_pool = ["Gauss linear corrected", "Gauss linear uncorrected", "Gauss linear limited 1",
                         "Gauss linear limited 0.33", "Gauss linear limited 0.5", "Gauss linear orthogonal"]
laplacianSchemes_opt = {"justify": "left", "textvariable": laplacianSchemes}
laplacianSchemes_Combo = make_Combo(fvSchemes_tab, "laplacianSchemes: ", label_size, fvSchemes_tab_grid,
                                    laplacianSchemes_pool, combo_size, label_justify, laplacianSchemes_opt)
laplacianSchemes.set(laplacianSchemes_Combo.get())

snGradSchemes = tk.StringVar()
snGradSchemes_pool = ["corrected", "limited 1", "limited 0.5", "orthogonal", "uncorrected"]
snGradSchemes_opt = {"justify": "left", "textvariable": snGradSchemes}
snGradSchemes_Combo = make_Combo(fvSchemes_tab, "snGradSchemes: ", label_size, fvSchemes_tab_grid, snGradSchemes_pool,
                                 combo_size, label_justify, snGradSchemes_opt)
snGradSchemes.set(snGradSchemes_Combo.get())

fluid_group = tk.LabelFrame(fvSchemes_tab, text="fluid divSchemes", padx=5, pady=5)
fluid_group.grid(row=fvSchemes_tab_grid[0], column=fvSchemes_tab_grid[1], columnspan=fvSchemes_tab_grid[3])

div_phi_U = tk.StringVar()
div_phi_U_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss linearUpwind grad(U)",
                  "bounded Gauss linearUpwindV grad(U)", "Gauss limitedLinearV 1", "Gauss LUST grad(U)",
                  "Gauss limitedLinear 1", "Gauss linear"]
div_phi_U_opt = {"justify": "left", "textvariable": div_phi_U}
div_phi_U_Combo = make_Combo(fluid_group, "div_phi_U: ", label_size, fvSchemes_tab_grid, div_phi_U_pool, combo_size,
                             label_justify, div_phi_U_opt)
div_phi_U.set(div_phi_U_Combo.get())

div_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "bounded Gauss linearUpwind limited",
            "bounded Gauss limitedLinear 1", "Gauss linear"]

div_phi_k = tk.StringVar()
div_phi_k_opt = {"justify": "left", "textvariable": div_phi_k}
div_phi_k_Combo = make_Combo(fluid_group, "div_phi_k: ", label_size, fvSchemes_tab_grid, div_pool, combo_size,
                             label_justify, div_phi_k_opt)
div_phi_k.set(div_phi_k_Combo.get())

div_phi_epsilon = tk.StringVar()
div_phi_epsilon_opt = {"justify": "left", "textvariable": div_phi_epsilon}
div_phi_epsilon_Combo = make_Combo(fluid_group, "div_phi_epsilon: ", label_size, fvSchemes_tab_grid, div_pool,
                                   combo_size, label_justify, div_phi_epsilon_opt)
div_phi_epsilon.set(div_phi_epsilon_Combo.get())

div_phi_h = tk.StringVar()
div_phi_h_opt = {"justify": "left", "textvariable": div_phi_h}
div_phi_h_Combo = make_Combo(fluid_group, "div_phi_h: ", label_size, fvSchemes_tab_grid, div_pool, combo_size,
                             label_justify, div_phi_h_opt)
div_phi_h.set(div_phi_h_Combo.get())

div_phi_K = tk.StringVar()
div_phi_K_opt = {"justify": "left", "textvariable": div_phi_K}
div_phi_K_Combo = make_Combo(fluid_group, "div_phi_K: ", label_size, fvSchemes_tab_grid, div_pool, combo_size,
                             label_justify, div_phi_K_opt)
div_phi_K.set(div_phi_K_Combo.get())

div_phi_nuTilda = tk.StringVar()
div_phi_nuTilda_opt = {"justify": "left", "textvariable": div_phi_nuTilda}
div_phi_nuTilda_Combo = make_Combo(fluid_group, "div_phi_nuTilda: ", label_size, fvSchemes_tab_grid, div_pool,
                                   combo_size, label_justify, div_phi_nuTilda_opt)
div_phi_nuTilda.set(div_phi_nuTilda_Combo.get())

div_Ji_Ii_h = tk.StringVar()
div_Ji_Ii_h_opt = {"justify": "left", "textvariable": div_Ji_Ii_h}
div_Ji_Ii_h_Combo = make_Combo(fluid_group, "div_Ji_Ii_h: ", label_size, fvSchemes_tab_grid, div_pool, combo_size,
                               label_justify, div_Ji_Ii_h_opt)
div_Ji_Ii_h.set(div_Ji_Ii_h_Combo.get())

radiation = False
if not radiation:
    div_Ji_Ii_h_Combo.config(state="readonly")

divrho_nuEff_dev2TgradU = tk.StringVar()
divrho_nuEff_dev2TgradU_opt = {"justify": "left", "textvariable": divrho_nuEff_dev2TgradU}
divrho_nuEff_dev2TgradU_Combo = make_Combo(fluid_group, "divrho_nuEff_dev2TgradU: ", label_size, fvSchemes_tab_grid,
                                           div_pool, combo_size, label_justify, divrho_nuEff_dev2TgradU_opt)
divrho_nuEff_dev2TgradU.set(divrho_nuEff_dev2TgradU_Combo.get())

# **********************************************************************************************************#
fvSolution_tab = tk.Frame(tab_control)
tab_control.add(fvSolution_tab, text=f'{"fvSolution": ^30s}')

label_size = [12, 3]
entry_width = 15
combo_size = [entry_width - 1, 3]

group_grid = [0, 0, 3, 1]
solver_grid = [0, 0, 10, 8]

solver_pool = ["GAMG", "PBiCGStab", "PCG", "PBiCG", "smoothSolver"]
precon_pool = ["GAMG", "DIC", "DILU", "FDIC", "diagonal", "none"]
smooth_pool = ["GaussSeidel", "symGaussSeidel", "DIC", "DILU", "DICGaussSeidel"]

solver_group = tk.LabelFrame(fvSolution_tab, text="Solvers", padx=5, pady=5)
solver_group.grid(row=0, column=0)

solver_rho = tk.StringVar()
solver_rho_opt = {"justify": "left", "textvariable": solver_rho}
solver_rho_Combo = make_Combo(solver_group, "rho: ", label_size, solver_grid, solver_pool, combo_size, label_justify,
                              solver_rho_opt)
solver_rho.set(solver_rho_Combo.get())

precon_rho = tk.StringVar()
precon_rho_opt = {"justify": "left", "textvariable": precon_rho}
precon_rho_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                              label_justify, precon_rho_opt)
precon_rho.set(precon_rho_Combo.get())

smoo_rho = tk.StringVar()
smoo_rho_opt = {"justify": "left", "textvariable": smoo_rho}
smoo_rho_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify,
                            smoo_rho_opt)
smoo_rho.set(smoo_rho_Combo.get())

tol_rho = tk.StringVar()
tol_rho.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_rho}
tol_rho_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_rho.set(tol_rho_entry.get())

solver_p_rgh = tk.StringVar()
solver_p_rgh_opt = {"justify": "left", "textvariable": solver_p_rgh}
solver_p_rgh_Combo = make_Combo(solver_group, "p_rgh: ", label_size, solver_grid, solver_pool, combo_size,
                                label_justify, solver_p_rgh_opt)
solver_p_rgh.set(solver_p_rgh_Combo.get())

precon_p_rgh = tk.StringVar()
precon_p_rgh_opt = {"justify": "left", "textvariable": precon_p_rgh}
precon_p_rgh_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                                label_justify, precon_p_rgh_opt)
precon_p_rgh.set(precon_p_rgh_Combo.get())

smoo_p_rgh = tk.StringVar()
smoo_p_rgh_opt = {"justify": "left", "textvariable": smoo_p_rgh}
smoo_p_rgh_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size,
                              label_justify, smoo_p_rgh_opt)
smoo_p_rgh.set(smoo_p_rgh_Combo.get())

tol_p_rgh = tk.StringVar()
tol_p_rgh.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_p_rgh}
tol_p_rgh_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify,
                             entry_opt)
tol_p_rgh.set(tol_p_rgh_entry.get())

solver_U = tk.StringVar()
solver_U_opt = {"justify": "left", "textvariable": solver_U}
solver_U_Combo = make_Combo(solver_group, "U: ", label_size, solver_grid, solver_pool, combo_size, label_justify,
                            solver_U_opt)
solver_U.set(solver_U_Combo.get())

precon_U = tk.StringVar()
precon_U_opt = {"justify": "left", "textvariable": precon_U}
precon_U_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                            label_justify, precon_U_opt)
precon_U.set(precon_U_Combo.get())

smoo_U = tk.StringVar()
smoo_U_opt = {"justify": "left", "textvariable": smoo_U}
smoo_U_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify,
                          smoo_U_opt)
smoo_U.set(smoo_U_Combo.get())

tol_U = tk.StringVar()
tol_U.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_U}
tol_U_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_U.set(tol_U_entry.get())

solver_k = tk.StringVar()
solver_k_opt = {"justify": "left", "textvariable": solver_k}
solver_k_Combo = make_Combo(solver_group, "k: ", label_size, solver_grid, solver_pool, combo_size, label_justify,
                            solver_k_opt)
solver_k.set(solver_k_Combo.get())

precon_k = tk.StringVar()
precon_k_opt = {"justify": "left", "textvariable": precon_k}
precon_k_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                            label_justify, precon_k_opt)
precon_k.set(precon_k_Combo.get())

smoo_k = tk.StringVar()
smoo_k_opt = {"justify": "left", "textvariable": smoo_k}
smoo_k_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify,
                          smoo_k_opt)
smoo_k.set(smoo_k_Combo.get())

tol_k = tk.StringVar()
tol_k.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_k}
tol_k_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_k.set(tol_k_entry.get())

solver_epsilon = tk.StringVar()
solver_epsilon_opt = {"justify": "left", "textvariable": solver_epsilon}
solver_epsilon_Combo = make_Combo(solver_group, "epsilon: ", label_size, solver_grid, solver_pool, combo_size,
                                  label_justify, solver_epsilon_opt)
solver_epsilon.set(solver_epsilon_Combo.get())

precon_epsilon = tk.StringVar()
precon_epsilon_opt = {"justify": "left", "textvariable": precon_epsilon}
precon_epsilon_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                                  label_justify, precon_epsilon_opt)
precon_epsilon.set(precon_epsilon_Combo.get())

smoo_epsilon = tk.StringVar()
smoo_epsilon_opt = {"justify": "left", "textvariable": smoo_epsilon}
smoo_epsilon_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size,
                                label_justify, smoo_epsilon_opt)
smoo_epsilon.set(smoo_epsilon_Combo.get())

tol_epsilon = tk.StringVar()
tol_epsilon.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_epsilon}
tol_epsilon_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify,
                               entry_opt)
tol_epsilon.set(tol_epsilon_entry.get())

solver_h = tk.StringVar()
solver_h_opt = {"justify": "left", "textvariable": solver_h}
solver_h_Combo = make_Combo(solver_group, "h: ", label_size, solver_grid, solver_pool, combo_size, label_justify,
                            solver_h_opt)
solver_h.set(solver_h_Combo.get())

precon_h = tk.StringVar()
precon_h_opt = {"justify": "left", "textvariable": precon_h}
precon_h_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                            label_justify, precon_h_opt)
precon_h.set(precon_h_Combo.get())

smoo_h = tk.StringVar()
smoo_h_opt = {"justify": "left", "textvariable": smoo_h}
smoo_h_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify,
                          smoo_h_opt)
smoo_h.set(smoo_h_Combo.get())

tol_h = tk.StringVar()
tol_h.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_h}
tol_h_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_h.set(tol_h_entry.get())

solver_Ii = tk.StringVar()
solver_Ii_opt = {"justify": "left", "textvariable": solver_Ii}
solver_Ii_Combo = make_Combo(solver_group, "Ii: ", label_size, solver_grid, solver_pool, combo_size, label_justify,
                             solver_Ii_opt)
solver_Ii.set(solver_Ii_Combo.get())

precon_Ii = tk.StringVar()
precon_Ii_opt = {"justify": "left", "textvariable": precon_Ii}
precon_Ii_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size,
                             label_justify, precon_Ii_opt)
precon_Ii.set(precon_Ii_Combo.get())

smoo_Ii = tk.StringVar()
smoo_Ii_opt = {"justify": "left", "textvariable": smoo_Ii}
smoo_Ii_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify,
                           smoo_Ii_opt)
smoo_Ii.set(smoo_Ii_Combo.get())

tol_Ii = tk.StringVar()
tol_Ii.set("10e-6")
entry_opt = {"justify": "left", "textvariable": tol_Ii}
tol_Ii_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_Ii.set(tol_Ii_entry.get())

Simple_group = tk.LabelFrame(fvSolution_tab, text="simple", padx=5, pady=5)
Simple_group.grid(row=1, column=0, columnspan=fvSchemes_tab_grid[3])
Simple_grid = [0, 0, 3, 8]

pRefCell = tk.StringVar()
pRefCell.set("0")
entry_opt = {"justify": "left", "textvariable": pRefCell}
pRefCell_entry = make_entry(Simple_group, "pRefCell: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
pRefCell.set(pRefCell.get())

pRefValue = tk.StringVar()
pRefValue.set("101325")
entry_opt = {"justify": "left", "textvariable": pRefValue}
pRefValue_entry = make_entry(Simple_group, "pRefValue: ", label_size, Simple_grid, entry_width, label_justify,
                             entry_opt)
pRefValue.set(pRefValue.get())

rhoMin = tk.StringVar()
rhoMin.set("0.2")
entry_opt = {"justify": "left", "textvariable": rhoMin}
rhoMin_entry = make_entry(Simple_group, "rhoMin: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
rhoMin.set(rhoMin.get())

rhoMax = tk.StringVar()
rhoMax.set("2")
entry_opt = {"justify": "left", "textvariable": rhoMax}
rhoMax_entry = make_entry(Simple_group, "rhoMax: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
rhoMax.set(rhoMax.get())

nNonOrthogonalCorrectors = tk.StringVar()
nNonOrthogonalCorrectors.set("2")
entry_opt = {"justify": "left", "textvariable": nNonOrthogonalCorrectors}
nNonOrthogonalCorrectors_entry = make_entry(Simple_group, "nNonOrthogonalCorrectors: ", label_size, Simple_grid,
                                            entry_width, label_justify, entry_opt)
nNonOrthogonalCorrectors.set(nNonOrthogonalCorrectors.get())

momentumPredictor = tk.StringVar()
momentumPredictor_opt = {"justify": "left", "textvariable": momentumPredictor}
momentumPredictor_Combo = make_Combo(Simple_group, "momentumPredictor: ", label_size, Simple_grid, switch_pool,
                                     combo_size, label_justify, momentumPredictor_opt)
momentumPredictor.set(momentumPredictor_Combo.get())

consistent = tk.StringVar()
consistent_opt = {"justify": "left", "textvariable": consistent}
consistent_Combo = make_Combo(Simple_group, "consistent: ", label_size, Simple_grid, switch_pool, combo_size,
                              label_justify, consistent_opt)
consistent.set(consistent_Combo.get())

residualControl = tk.StringVar()
residualControl_opt = {"justify": "left", "textvariable": residualControl}
residualControl_Combo = make_Combo(Simple_group, "residualControl: ", label_size, Simple_grid, switch_pool, combo_size,
                                   label_justify, residualControl_opt)
residualControl.set(residualControl_Combo.get())

p_resi = tk.StringVar()
p_resi.set("10e-6")
entry_opt = {"justify": "left", "textvariable": p_resi}
p_resi_entry = make_entry(Simple_group, "p_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
p_resi.set(p_resi.get())

U_resi = tk.StringVar()
U_resi.set("10e-6")
entry_opt = {"justify": "left", "textvariable": U_resi}
U_resi_entry = make_entry(Simple_group, "U_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
U_resi.set(U_resi.get())

k_epsilon_resi = tk.StringVar()
k_epsilon_resi.set("10e-6")
entry_opt = {"justify": "left", "textvariable": k_epsilon_resi}
k_epsilon_resi_entry = make_entry(Simple_group, "k_epsilon_resi: ", label_size, Simple_grid, entry_width, label_justify,
                                  entry_opt)
k_epsilon_resi.set(k_epsilon_resi.get())

ILambda_h_resi = tk.StringVar()
ILambda_h_resi.set("10e-6")
entry_opt = {"justify": "left", "textvariable": ILambda_h_resi}
ILambda_h_resi_entry = make_entry(Simple_group, "ILambda_h_resi: ", label_size, Simple_grid, entry_width, label_justify,
                                  entry_opt)
ILambda_h_resi.set(ILambda_h_resi.get())

relaxationFactors = tk.LabelFrame(fvSolution_tab, text="relaxation", padx=5, pady=5)
relaxationFactors.grid(row=2, column=0)
relax_grid = [0, 0, 3, 10]

label_size = [4, 3]
entry_width = 4
combo_size = [entry_width - 1, 3]

rho_relax = tk.StringVar()
rho_relax.set("1")
entry_opt = {"justify": "left", "textvariable": rho_relax}
rho_relax_entry = make_entry(relaxationFactors, "rho: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
rho_relax.set(rho_relax.get())

p_rgh_relax = tk.StringVar()
p_rgh_relax.set("0.3")
entry_opt = {"justify": "left", "textvariable": p_rgh_relax}
p_rgh_relax_entry = make_entry(relaxationFactors, "p_rgh: ", label_size, relax_grid, entry_width, label_justify,
                               entry_opt)
p_rgh_relax.set(p_rgh_relax.get())

h_relax = tk.StringVar()
h_relax.set("0.99")
entry_opt = {"justify": "left", "textvariable": h_relax}
h_relax_entry = make_entry(relaxationFactors, "h: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
h_relax.set(h_relax.get())

U_relax = tk.StringVar()
U_relax.set("0.5")
entry_opt = {"justify": "left", "textvariable": U_relax}
U_relax_entry = make_entry(relaxationFactors, "U: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
U_relax.set(U_relax.get())

qr_Lambda_relax = tk.StringVar()
qr_Lambda_relax.set("0.6")
entry_opt = {"justify": "left", "textvariable": qr_Lambda_relax}
qr_Lambda_relax_entry = make_entry(relaxationFactors, "qr_Lambda: ", label_size, relax_grid, entry_width, label_justify,
                                   entry_opt)
qr_Lambda_relax.set(qr_Lambda_relax.get())

# **********************************************************************************************************#
label_size = [15, 3]
entry_width = 30
combo_size = [entry_width - 1, 3]

boundary_tab_grid = [0, 0, 10, 8]

N_regions = 3

boundary_tab = tk.Frame(tab_control)
tab_control.add(boundary_tab, text=f'{"Boundary": ^30s}')

boundary_pool = ["wall", "mappedWall", "patch", "cyclicAMI"]
relax_grid = [0, 0, 3, 10]

for region_i in range(N_regions):
    relaxationFactors = tk.LabelFrame(boundary_tab, text="region" + str(region_i), padx=5, pady=5)
    relaxationFactors.grid(row=region_i, column=0)

num_bc = 10

col_name = ["Name", "Type", "sampleRegion", "samplePatch", "sampleMethod"]

for i in range(len(col_name)):
    col_name_label = tk.Label(boundary_tab, text=col_name[i], width=12)
    col_name_label.grid(row=0, column=i)

boundary_name_col = tk.Label(boundary_tab, text="Name")
boundary_type_col = tk.Label(boundary_tab, text="Type")

for i in range(num_bc):
    boundary_name_label = tk.Label(boundary_tab, text="Boundary" + str(i))
    boundary_name_label.grid(row=i + 1, column=0)

boundary_split = tk.Button(boundary_tab, text="split mesh", command=diff_mappedWall_AMI)

boundary_split.grid(row=boundary_tab_grid[0] + 12, column=boundary_tab_grid[1], columnspan=2)

# **********************************************************************************************************#
initial_Condition_tab = tk.Frame(tab_control)
tab_control.add(initial_Condition_tab, text=f'{"Initial Condition": ^30s}')

# **********************************************************************************************************#
radiation_tab = tk.Frame(tab_control)
tab_control.add(radiation_tab, text=f'{"Radiation": ^30s}')

radiation_on = tk.BooleanVar()
radiation_on_check = tk.Checkbutton(radiation_tab, text="Radiation", variable=radiation_on)
radiation_on_check.grid(row=0, column=0, sticky="W")

# **********************************************************************************************************#
motion_tab = tk.Frame(tab_control)
tab_control.add(motion_tab, text=f'{"Motion": ^30s}')

MRF_on = tk.BooleanVar()
MRF_on_check = tk.Checkbutton(motion_tab, text="MRF", variable=MRF_on)
MRF_on_check.grid(row=0, column=0, sticky="W")

dynamicMesh_on = tk.BooleanVar()
dynamicMesh_on_check = tk.Checkbutton(motion_tab, text="dynamicMesh", variable=dynamicMesh_on)
dynamicMesh_on_check.grid(row=0, column=1, sticky="W")

# **********************************************************************************************************#
fvOption_tab = tk.Frame(tab_control)
tab_control.add(fvOption_tab, text=f'{"fvOption": ^30s}')
MRF_on = tk.BooleanVar()
MRF_on_check = tk.Checkbutton(fvOption_tab, text="Heat Source", variable=MRF_on)
MRF_on_check.grid(row=0, column=0, sticky="W")

# **********************************************************************************************************#
tab_control.grid(row=2, column=0, columnspan=10)

status = ttk.Label(root, text=status.get(), relief="sunken", anchor="w")
status.grid(row=100, column=0, columnspan=15, sticky="WE")

root.mainloop()
