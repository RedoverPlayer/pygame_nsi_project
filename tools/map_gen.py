import json

with open("maps1.json", "w") as f:
    f.write(json.dumps([["terrain" for _ in range(60)] for _ in range(60)], indent=4))