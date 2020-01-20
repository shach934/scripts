import os
status = os.system("bash -ilc -i ls > log & ")
print(status)