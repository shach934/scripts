fvSolution_tab = tk.Frame(tab_control)                
tab_control.add(fvSolution_tab, text = f'{"fvSolution": ^50s}')   

label_size = [12, 3]
entry_width = 15
combo_size = [entry_width - 1, 3]

group_grid = [0, 0, 3, 1]
solver_grid = [0, 0, 10, 8]

solver_pool = ["GAMG", "PBiCGStab", "PCG", "PBiCG","smoothSolver"]
precon_pool = ["GAMG", "DIC", "DILU", "FDIC","diagonal", "none"]
smooth_pool = ["GaussSeidel", "symGaussSeidel", "DIC", "DILU","DICGaussSeidel"]

solver_group = tk.LabelFrame(fvSolution_tab, text="Solvers", padx=5, pady=5)
solver_group.grid(row = 0, column = 0)

solver_rho = tk.StringVar()
solver_rho_opt = {"justify":"left", "textvariable":solver_rho}
solver_rho_Combo = make_Combo(solver_group, "rho: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_rho_opt)
solver_rho.set(solver_rho_Combo.get())

precon_rho = tk.StringVar()
precon_rho_opt = {"justify":"left", "textvariable":precon_rho}
precon_rho_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_rho_opt)
precon_rho.set(precon_rho_Combo.get())

smoo_rho = tk.StringVar()
smoo_rho_opt = {"justify":"left", "textvariable":smoo_rho}
smoo_rho_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_rho_opt)
smoo_rho.set(smoo_rho_Combo.get())

tol_rho = tk.StringVar()
tol_rho.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_rho}
tol_rho_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_rho.set(tol_rho_entry.get())

solver_p_rgh = tk.StringVar()
solver_p_rgh_opt = {"justify":"left", "textvariable":solver_p_rgh}
solver_p_rgh_Combo = make_Combo(solver_group, "p_rgh: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_p_rgh_opt)
solver_p_rgh.set(solver_p_rgh_Combo.get())

precon_p_rgh = tk.StringVar()
precon_p_rgh_opt = {"justify":"left", "textvariable":precon_p_rgh}
precon_p_rgh_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_p_rgh_opt)
precon_p_rgh.set(precon_p_rgh_Combo.get())

smoo_p_rgh = tk.StringVar()
smoo_p_rgh_opt = {"justify":"left", "textvariable":smoo_p_rgh}
smoo_p_rgh_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_p_rgh_opt)
smoo_p_rgh.set(smoo_p_rgh_Combo.get())

tol_p_rgh = tk.StringVar()
tol_p_rgh.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_p_rgh}
tol_p_rgh_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_p_rgh.set(tol_p_rgh_entry.get())

solver_U = tk.StringVar()
solver_U_opt = {"justify":"left", "textvariable":solver_U}
solver_U_Combo = make_Combo(solver_group, "U: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_U_opt)
solver_U.set(solver_U_Combo.get())

precon_U = tk.StringVar()
precon_U_opt = {"justify":"left", "textvariable":precon_U}
precon_U_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_U_opt)
precon_U.set(precon_U_Combo.get())

smoo_U = tk.StringVar()
smoo_U_opt = {"justify":"left", "textvariable":smoo_U}
smoo_U_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_U_opt)
smoo_U.set(smoo_U_Combo.get())

tol_U = tk.StringVar()
tol_U.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_U}
tol_U_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_U.set(tol_U_entry.get())

solver_k= tk.StringVar()
solver_k_opt = {"justify":"left", "textvariable":solver_k}
solver_k_Combo = make_Combo(solver_group, "k: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_k_opt)
solver_k.set(solver_k_Combo.get())

precon_k = tk.StringVar()
precon_k_opt = {"justify":"left", "textvariable":precon_k}
precon_k_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_k_opt)
precon_k.set(precon_k_Combo.get())

smoo_k = tk.StringVar()
smoo_k_opt = {"justify":"left", "textvariable":smoo_k}
smoo_k_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_k_opt)
smoo_k.set(smoo_k_Combo.get())

tol_k = tk.StringVar()
tol_k.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_k}
tol_k_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_k.set(tol_k_entry.get())

solver_epsilon= tk.StringVar()
solver_epsilon_opt = {"justify":"left", "textvariable":solver_epsilon}
solver_epsilon_Combo = make_Combo(solver_group, "epsilon: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_epsilon_opt)
solver_epsilon.set(solver_epsilon_Combo.get())

precon_epsilon = tk.StringVar()
precon_epsilon_opt = {"justify":"left", "textvariable":precon_epsilon}
precon_epsilon_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_epsilon_opt)
precon_epsilon.set(precon_epsilon_Combo.get())

smoo_epsilon = tk.StringVar()
smoo_epsilon_opt = {"justify":"left", "textvariable":smoo_epsilon}
smoo_epsilon_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_epsilon_opt)
smoo_epsilon.set(smoo_epsilon_Combo.get())

tol_epsilon = tk.StringVar()
tol_epsilon.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_epsilon}
tol_epsilon_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_epsilon.set(tol_epsilon_entry.get())

solver_h= tk.StringVar()
solver_h_opt = {"justify":"left", "textvariable":solver_h}
solver_h_Combo = make_Combo(solver_group, "h: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_h_opt)
solver_h.set(solver_h_Combo.get())

precon_h = tk.StringVar()
precon_h_opt = {"justify":"left", "textvariable":precon_h}
precon_h_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_h_opt)
precon_h.set(precon_h_Combo.get())

smoo_h = tk.StringVar()
smoo_h_opt = {"justify":"left", "textvariable":smoo_h}
smoo_h_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_h_opt)
smoo_h.set(smoo_h_Combo.get())

tol_h = tk.StringVar()
tol_h.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_h}
tol_h_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_h.set(tol_h_entry.get())

solver_Ii= tk.StringVar()
solver_Ii_opt = {"justify":"left", "textvariable":solver_Ii}
solver_Ii_Combo = make_Combo(solver_group, "Ii: ", label_size, solver_grid, solver_pool, combo_size, label_justify, solver_Ii_opt)
solver_Ii.set(solver_Ii_Combo.get())

precon_Ii = tk.StringVar()
precon_Ii_opt = {"justify":"left", "textvariable":precon_Ii}
precon_Ii_Combo = make_Combo(solver_group, "preconditioner: ", label_size, solver_grid, precon_pool, combo_size, label_justify, precon_Ii_opt)
precon_Ii.set(precon_Ii_Combo.get())

smoo_Ii = tk.StringVar()
smoo_Ii_opt = {"justify":"left", "textvariable":smoo_Ii}
smoo_Ii_Combo = make_Combo(solver_group, "smoother: ", label_size, solver_grid, smooth_pool, combo_size, label_justify, smoo_Ii_opt)
smoo_Ii.set(smoo_Ii_Combo.get())

tol_Ii = tk.StringVar()
tol_Ii.set("10e-6")
entry_opt = {"justify":"left", "textvariable":tol_Ii}
tol_Ii_entry = make_entry(solver_group, "tolerance: ", label_size, solver_grid, entry_width, label_justify, entry_opt)
tol_Ii.set(tol_Ii_entry.get())

Simple_group = tk.LabelFrame(fvSolution_tab, text = "simple", padx = 5, pady = 5)
Simple_group.grid(row = 1 , column = 0, columnspan = fvSchemes_tab_grid[3])
Simple_grid = [0, 0, 3, 8]

pRefCell = tk.StringVar()
pRefCell.set("0")
entry_opt = {"justify":"left", "textvariable":pRefCell}
pRefCell_entry = make_entry(Simple_group, "pRefCell: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
pRefCell.set(pRefCell.get())

pRefValue = tk.StringVar()
pRefValue.set("101325")
entry_opt = {"justify":"left", "textvariable":pRefValue}
pRefValue_entry = make_entry(Simple_group, "pRefValue: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
pRefValue.set(pRefValue.get())

rhoMin = tk.StringVar()
rhoMin.set("0.2")
entry_opt = {"justify":"left", "textvariable":rhoMin}
rhoMin_entry = make_entry(Simple_group, "rhoMin: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
rhoMin.set(rhoMin.get())

rhoMax = tk.StringVar()
rhoMax.set("2")
entry_opt = {"justify":"left", "textvariable":rhoMax}
rhoMax_entry = make_entry(Simple_group, "rhoMax: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
rhoMax.set(rhoMax.get())

nNonOrthogonalCorrectors = tk.StringVar()
nNonOrthogonalCorrectors.set("2")
entry_opt = {"justify":"left", "textvariable":nNonOrthogonalCorrectors}
nNonOrthogonalCorrectors_entry = make_entry(Simple_group, "nNonOrthogonalCorrectors: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
nNonOrthogonalCorrectors.set(nNonOrthogonalCorrectors.get())

momentumPredictor = tk.StringVar()
momentumPredictor_opt = {"justify":"left", "textvariable":momentumPredictor}
momentumPredictor_Combo = make_Combo(Simple_group, "momentumPredictor: ", label_size, Simple_grid, switch_pool, combo_size, label_justify, momentumPredictor_opt)
momentumPredictor.set(momentumPredictor_Combo.get())

consistent = tk.StringVar()
consistent_opt = {"justify":"left", "textvariable":consistent}
consistent_Combo = make_Combo(Simple_group, "consistent: ", label_size, Simple_grid, switch_pool, combo_size, label_justify, consistent_opt)
consistent.set(consistent_Combo.get())

residualControl = tk.StringVar()
residualControl_opt = {"justify":"left", "textvariable":residualControl}
residualControl_Combo = make_Combo(Simple_group, "residualControl: ", label_size, Simple_grid, switch_pool, combo_size, label_justify, residualControl_opt)
residualControl.set(residualControl_Combo.get())

p_resi = tk.StringVar()
p_resi.set("10e-6")
entry_opt = {"justify":"left", "textvariable":p_resi}
p_resi_entry = make_entry(Simple_group, "p_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
p_resi.set(p_resi.get())

U_resi = tk.StringVar()
U_resi.set("10e-6")
entry_opt = {"justify":"left", "textvariable":U_resi}
U_resi_entry = make_entry(Simple_group, "U_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
U_resi.set(U_resi.get())

k_epsilon_resi = tk.StringVar()
k_epsilon_resi.set("10e-6")
entry_opt = {"justify":"left", "textvariable":k_epsilon_resi}
k_epsilon_resi_entry = make_entry(Simple_group, "k_epsilon_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
k_epsilon_resi.set(k_epsilon_resi.get())

ILambda_h_resi = tk.StringVar()
ILambda_h_resi.set("10e-6")
entry_opt = {"justify":"left", "textvariable":ILambda_h_resi}
ILambda_h_resi_entry = make_entry(Simple_group, "ILambda_h_resi: ", label_size, Simple_grid, entry_width, label_justify, entry_opt)
ILambda_h_resi.set(ILambda_h_resi.get())

relaxationFactors = tk.LabelFrame(fvSolution_tab, text = "relaxation", padx = 5, pady = 5)
relaxationFactors.grid(row = 2, column = 0)
relax_grid = [0, 0, 3, 10]

label_size = [4, 3]
entry_width = 4
combo_size = [entry_width - 1, 3]

rho_relax = tk.StringVar()
rho_relax.set("1")
entry_opt = {"justify":"left", "textvariable":rho_relax}
rho_relax_entry = make_entry(relaxationFactors, "rho: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
rho_relax.set(rho_relax.get())

p_rgh_relax = tk.StringVar()
p_rgh_relax.set("0.3")
entry_opt = {"justify":"left", "textvariable":p_rgh_relax}
p_rgh_relax_entry = make_entry(relaxationFactors, "p_rgh: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
p_rgh_relax.set(p_rgh_relax.get())

h_relax = tk.StringVar()
h_relax.set("0.99")
entry_opt = {"justify":"left", "textvariable":h_relax}
h_relax_entry = make_entry(relaxationFactors, "h: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
h_relax.set(h_relax.get())

U_relax = tk.StringVar()
U_relax.set("0.5")
entry_opt = {"justify":"left", "textvariable":U_relax}
U_relax_entry = make_entry(relaxationFactors, "U: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
U_relax.set(U_relax.get())

qr_Lambda_relax = tk.StringVar()
qr_Lambda_relax.set("0.6")
entry_opt = {"justify":"left", "textvariable":qr_Lambda_relax}
qr_Lambda_relax_entry = make_entry(relaxationFactors, "qr_Lambda: ", label_size, relax_grid, entry_width, label_justify, entry_opt)
qr_Lambda_relax.set(qr_Lambda_relax.get())