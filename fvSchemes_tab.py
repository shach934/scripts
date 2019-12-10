fvSchemes_tab = tk.Frame(tab_control)                
tab_control.add(fvSchemes_tab, text = f'{"fvSchemes": ^50s}')  

fvSchemes_tab_grid = [0, 0, 6, 4]

ddtSchemes = tk.StringVar()
ddtSchemes_pool=["steadyState", "Euler", "localEuler", "backward", "CrankNicolson"]
ddtSchemes_opt = {"justify":"left", "textvariable":ddtSchemes}
ddtSchemes_Combo = make_Combo(fvSchemes_tab, "ddtSchemes: ", label_size, fvSchemes_tab_grid, ddtSchemes_pool, combo_size, label_justify, ddtSchemes_opt)
ddtSchemes.set(ddtSchemes_Combo.get())

gradScheme = tk.StringVar()
gradScheme_pool = ["Gauss linear", "leastSquares", "cellLimited Gauss linear 1", "cellLimited Gauss linear 0.33", "cellLimited Gauss linear 0.5"]
gradScheme_opt = {"justify":"left", "textvariable":gradScheme}
gradScheme_Combo = make_Combo(fvSchemes_tab, "gradScheme: ", label_size, fvSchemes_tab_grid, gradScheme_pool, combo_size, label_justify, gradScheme_opt)
gradScheme.set(gradScheme_Combo.get())

laplacianSchemes = tk.StringVar()
laplacianSchemes_pool = ["Gauss linear corrected", "Gauss linear uncorrected", "Gauss linear limited 1", "Gauss linear limited 0.33", "Gauss linear limited 0.5", "Gauss linear orthogonal"]
laplacianSchemes_opt = {"justify":"left", "textvariable":laplacianSchemes}
laplacianSchemes_Combo = make_Combo(fvSchemes_tab, "laplacianSchemes: ", label_size, fvSchemes_tab_grid, laplacianSchemes_pool, combo_size, label_justify, laplacianSchemes_opt)
laplacianSchemes.set(laplacianSchemes_Combo.get())

snGradSchemes = tk.StringVar()
snGradSchemes_pool = ["corrected", "limited 1","limited 0.5", "orthogonal","uncorrected"]
snGradSchemes_opt = {"justify":"left", "textvariable":snGradSchemes}
snGradSchemes_Combo = make_Combo(fvSchemes_tab, "snGradSchemes: ", label_size, fvSchemes_tab_grid, snGradSchemes_pool, combo_size, label_justify, snGradSchemes_opt)
snGradSchemes.set(snGradSchemes_Combo.get())

fluid_group = tk.LabelFrame(fvSchemes_tab, text="fluid divSchemes", padx=5, pady=5)
fluid_group.grid(row = fvSchemes_tab_grid[0], column = fvSchemes_tab_grid[1], columnspan = fvSchemes_tab_grid[3])

div_phi_U = tk.StringVar()
div_phi_U_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss linearUpwind grad(U)", "bounded Gauss linearUpwindV grad(U)","Gauss limitedLinearV 1", "Gauss LUST grad(U)",  "Gauss limitedLinear 1", "Gauss linear"]
div_phi_U_opt = {"justify":"left", "textvariable":div_phi_U}
div_phi_U_Combo = make_Combo(fluid_group, "div_phi_U: ", label_size, fvSchemes_tab_grid, div_phi_U_pool, combo_size, label_justify, div_phi_U_opt)
div_phi_U.set(div_phi_U_Combo.get())

div_phi_k = tk.StringVar()
div_phi_k_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_phi_k_opt = {"justify":"left", "textvariable":div_phi_k}
div_phi_k_Combo = make_Combo(fluid_group, "div_phi_k: ", label_size, fvSchemes_tab_grid, div_phi_k_pool, combo_size, label_justify, div_phi_k_opt)
div_phi_k.set(div_phi_k_Combo.get())

div_phi_epsilon = tk.StringVar()
div_phi_epsilon_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_phi_epsilon_opt = {"justify":"left", "textvariable":div_phi_epsilon}
div_phi_epsilon_Combo = make_Combo(fluid_group, "div_phi_epsilon: ", label_size, fvSchemes_tab_grid, div_phi_epsilon_pool, combo_size, label_justify, div_phi_epsilon_opt)
div_phi_epsilon.set(div_phi_epsilon_Combo.get())

div_phi_h = tk.StringVar()
div_phi_h_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_phi_h_opt = {"justify":"left", "textvariable":div_phi_h}
div_phi_h_Combo = make_Combo(fluid_group, "div_phi_h: ", label_size, fvSchemes_tab_grid, div_phi_h_pool, combo_size, label_justify, div_phi_h_opt)
div_phi_h.set(div_phi_h_Combo.get())

div_phi_K = tk.StringVar()
div_phi_K_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_phi_K_opt = {"justify":"left", "textvariable":div_phi_K}
div_phi_K_Combo = make_Combo(fluid_group, "div_phi_K: ", label_size, fvSchemes_tab_grid, div_phi_K_pool, combo_size, label_justify, div_phi_K_opt)
div_phi_K.set(div_phi_K_Combo.get())

div_phi_nuTilda = tk.StringVar()
div_phi_nuTilda_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_phi_nuTilda_opt = {"justify":"left", "textvariable":div_phi_nuTilda}
div_phi_nuTilda_Combo = make_Combo(fluid_group, "div_phi_nuTilda: ", label_size, fvSchemes_tab_grid, div_phi_nuTilda_pool, combo_size, label_justify, div_phi_nuTilda_opt)
div_phi_nuTilda.set(div_phi_nuTilda_Combo.get())

div_Ji_Ii_h = tk.StringVar()
div_Ji_Ii_h_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
div_Ji_Ii_h_opt = {"justify":"left", "textvariable":div_Ji_Ii_h}
div_Ji_Ii_h_Combo = make_Combo(fluid_group, "div_Ji_Ii_h: ", label_size, fvSchemes_tab_grid, div_Ji_Ii_h_pool, combo_size, label_justify, div_Ji_Ii_h_opt)
div_Ji_Ii_h.set(div_Ji_Ii_h_Combo.get())

radiation = False
if not radiation:
    div_Ji_Ii_h_Combo.config(state = "readonly")
 
divrho_nuEff_dev2TgradU = tk.StringVar()
divrho_nuEff_dev2TgradU_pool = ["Gauss upwind", "bounded Gauss upwind", "Gauss limitedLinear 1", "Gauss limitedLinear 0.1","Gauss limitedLinear 0.2", "bounded Gauss linearUpwind limited", "bounded Gauss limitedLinear 1",  "Gauss linear"]
divrho_nuEff_dev2TgradU_opt = {"justify":"left", "textvariable":divrho_nuEff_dev2TgradU}
divrho_nuEff_dev2TgradU_Combo = make_Combo(fluid_group, "divrho_nuEff_dev2TgradU: ", label_size, fvSchemes_tab_grid, divrho_nuEff_dev2TgradU_pool, combo_size, label_justify, divrho_nuEff_dev2TgradU_opt)
divrho_nuEff_dev2TgradU.set(divrho_nuEff_dev2TgradU_Combo.get())