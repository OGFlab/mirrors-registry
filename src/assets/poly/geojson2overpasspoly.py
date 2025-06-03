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
# 而且最后一行坐标后面不要有多余的空格，否则就认为还有点

# <?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
#     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
# <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
# <head>
#   <meta http-equiv="content-type" content="text/html; charset=utf-8" lang="en"/>
#   <title>OSM3S Response</title>
# </head>
# <body>

# <p>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</p>
# <p><strong style="color:#FF0000">Error</strong>: line 8: static error: For the attribute &quot;bounds&quot; of the element &quot;polygon-query&quot; an even number of float values must be provided. </p>

# </body>
# </html>