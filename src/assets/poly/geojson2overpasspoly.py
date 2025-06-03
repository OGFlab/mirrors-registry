import json

source=input()

with open(source,"r",encoding="utf-8") as f:
    raw=json.loads(f.read())

# print(len(raw["features"][0]["geometry"]["coordinates"]))

print([f"{round(i[1],6)} {round(i[0],6)}" for i in raw["features"][0]["geometry"]["coordinates"]])
