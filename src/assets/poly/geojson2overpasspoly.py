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
