foam_path = tk.StringVar()

browse_button = tk.Button(root, text = "Load OpenFOAM Case", width = big_button_size[0], height = big_button_size[1],  command = lambda: browse_button(root, foam_path))
browse_button.grid(row = 0, column = 1)

output_path = foam_path.get() + "_temp"

"""
next_button = tk.Button(root, text = 'Next', width = big_button_size[0], height = big_button_size[1])
next_button.grid(row = 0, column = 2)
"""

write_button = tk.Button(root, text = 'Write', width = big_button_size[0], height = big_button_size[1])
write_button.grid(row = 0, column = 3)

openDir_button = tk.Button(root, text = 'Open Directory', width = big_button_size[0], height = big_button_size[1]) #, command = lambda event: open_path(event, path))
openDir_button.grid(row = 0, column = 4)

exit_button = tk.Button(root, text = 'Quit', width = big_button_size[0], height = big_button_size[1], command = root.destroy)
exit_button.grid(row = 0, column = 5)

tab_control = ttk.Notebook(root, style='lefttab.TNotebook')