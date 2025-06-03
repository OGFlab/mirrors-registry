import json

source = input()

with open(source, "r", encoding="utf-8") as f:
    raw = json.loads(f.read())

# print(len(raw["features"][0]["geometry"]["coordinates"]))

valid_content = (
    '(poly:"\n'
    + "\n".join(
        [
            f"{round(i[1],6)} {round(i[0],6)} "
            for i in raw["features"][0]["geometry"]["coordinates"]
        ]
    )
    + '\n")'
)

print(("=" * 15 + "\n") + valid_content)

with open("output.overpassql_poly", "w", encoding="utf-8") as f:
    f.write(valid_content)

# overpass 接受的poly文件是不需要重复首末的，geojson需要，请务必小心
# 否则 For the attribute &quot;bounds&quot; of the element &quot;polygon-query&quot; an even number of float values must be provided.
# 而且最后一行坐标后面不要有多余的空格，否则就认为还有点