solver_tab = tk.Frame(tab_control)                
tab_control.add(solver_tab, text = f'{"Solver": ^50s}')        

solver_tab_grid = [0, 0, 4, 4]

solver = tk.StringVar()
solver_pool = ["chtMultiRegionSimpleFoam", "interFoam", "Coming soon!"]
combo_opt = {"justify":"left", "textvariable":solver}
solver_Combo = make_Combo(solver_tab, "Solver: ", label_size, solver_tab_grid, solver_pool, combo_size, label_justify, combo_opt)
solver.set(solver_Combo.get())

decomposeParDict = tk.StringVar()
decomposeParDict.set("12")
decomposeParDict_opt = {"justify":"left", "textvariable":decomposeParDict}
decomposeParDict_entry = make_entry(solver_tab, "decomposeParDict: ", label_size, solver_tab_grid, entry_width, label_justify, decomposeParDict_opt)
decomposeParDict.set(decomposeParDict_entry.get())

startT = tk.StringVar()
startT.set("latestTime")
entry_opt = {"justify":"left", "textvariable":startT}
startT_entry = make_entry(solver_tab, "startTime: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
startT.set(startT_entry.get())

endT = tk.StringVar()
endT.set("1000")
entry_opt = {"justify":"left", "textvariable":endT}
endT_entry = make_entry(solver_tab, "endTime: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
endT.set(endT_entry.get())

writeCon = tk.StringVar()
writeCon.set("adjustableRunTime")
entry_opt = {"justify":"left", "textvariable":writeCon}
writeCon_entry = make_entry(solver_tab, "writeControl: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
writeCon.set(writeCon_entry.get())

writeInter = tk.StringVar()
writeInter.set("50")
entry_opt = {"justify":"left", "textvariable":writeInter}
writeInter_entry = make_entry(solver_tab, "writeInterval: ", label_size, solver_tab_grid, entry_width, label_justify, entry_opt)
writeInter.set(writeInter_entry.get())

runTimeModifiable = tk.StringVar()
runTimeModifiable_opt = {"justify":"left", "textvariable":runTimeModifiable}
runTimeModifiable_Combo = make_Combo(solver_tab, "runTimeModifiable: ", label_size, solver_tab_grid, switch_pool, combo_size, label_justify, runTimeModifiable_opt)
runTimeModifiable.set(runTimeModifiable_Combo.get())

maxCo = tk.StringVar()
maxCo.set("1")
maxCo_opt = {"justify":"left", "state":"readonly", "textvariable":maxCo}
maxCo_entry = make_entry(solver_tab, "maxCo: ", label_size, solver_tab_grid, entry_width, label_justify, maxCo_opt)
maxCo.set(maxCo_entry.get())