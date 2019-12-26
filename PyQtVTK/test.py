
boundary = {"disc":"solid", "air":"fluid", "shield":"solid"}

print(set(boundary.keys()))
print(set(boundary.values()))
print(set(boundary.keys()) == set(boundary.values()))