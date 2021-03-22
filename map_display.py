import json

with open("map1.json", "r") as f:
    map = json.loads(f.read())

for y in map:
    for x in y:
        if len(x) == 0:
            print(" ", end="")
        else:
            print(x[0], end="")
    print("")