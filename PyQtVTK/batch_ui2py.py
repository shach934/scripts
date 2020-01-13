ui_files = ["createBox", "createSphere", "createCone", "createCyliner"]

for ui_file in ui_files:
    exec("pyuic5 -x " + ui_file + ".ui -o " + ui_file + ".py")
