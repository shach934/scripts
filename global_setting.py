root.configure(background = 'gray99')

root.option_add("*Font", "courier 12")

mygreen = "#d2ffd2"
myred = "Dodgerblue2"

style = ttk.Style()

big_button_size = [20, 2]
small_buttion_size = [15, 1]

label_size = [15, 3]
entry_width = 30
combo_size = [entry_width - 1, 3]

label_justify = {"anchor": "w", "justify":"left", "padx":30}
switch_pool = ["True", "False"]

combo_size = [entry_width - 1, 3]

style.theme_create( "myTab", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 15, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": mygreen },
            "map":       {"background": [("selected", myred)],
                        "expand": [("selected", [1, 1, 1, 0])] } } } )

style = ttk.Style(root)
style.theme_use("myTab")
style.configure('myTab', tabposition='wn')  # horizontal  tapposition = 'nw'
