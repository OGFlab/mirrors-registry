original_query_result="""@type|@id|amenity|name|name:en|short_name|addr:province|operator
relation|348353|university|国立上京大学|National Shangjing University|NSJU||
"""

# It is not recommended to read the text directly, but it is recommended to read the network directly and request

import requests

ogf_overpass_url="https://overpass.ogf.rent-a-planet.com/api/interpreter?data=%5Bout%3Acsv%28%0A%20%20%20%20%3A%3Atype%2C%0A%20%20%20%20%3A%3A%22id%22%2C%0A%20%20%20%20amenity%2C%0A%20%20%20%20name%2C%0A%20%20%20%20%22name%3Aen%22%2C%0A%20%20%20%20%22short_name%22%2C%0A%20%20%20%20%22addr%3Aprovince%22%2C%0A%20%20%20%20operator%3B%0A%20%20%20%20true%3B%20%22%7C%22%0A%29%5D%3B%0A%0Anwr%5Bamenity%3Duniversity%5D%28poly%3A%2218.049257%20149.051512%2017.970897%20148.184966%2017.704213%20147.579344%2016.599348%20147.153623%2016.612509%20147.013547%2015.884737%20146.947629%2015.533086%20146.557614%2015.776398%20145.316159%2015.541025%20145.195310%2014.317620%20145.360102%2014.104618%20145.722651%2013.036675%20145.431513%2012.522396%20145.634760%2012.071558%20146.431269%2012.431218%20146.909174%2011.730236%20147.904814%2010.493219%20148.458246%209.194298%20148.249506%208.982754%20149.468989%208.559299%20149.611811%209.069557%20151.424555%208.798231%20151.721186%209.486992%20152.858275%209.814624%20152.891234%209.899864%20153.231810%2010.082447%20153.429564%209.218695%20154.756163%208.083707%20153.893735%207.844339%20154.064023%207.904192%20154.857787%207.633755%20155.040092%207.609595%20155.113563%207.593260%20155.346679%207.793998%20155.360411%207.928676%20155.489501%208.231879%20155.523833%208.530776%20155.990752%208.799583%20156.069030%208.962403%20156.073149%2010.120307%20157.489008%2011.636101%20159.114985%2012.838587%20159.125971%2013.432372%20156.137690%2015.146375%20155.467524%2016.673036%20155.692744%2017.214270%20153.539423%2015.987740%20152.501215%2016.167202%20151.171870%2016.926765%20149.852141%2017.143416%20149.861754%2017.283777%20149.820555%2017.270663%20149.740904%2017.372922%20149.690093%2017.503939%20149.501952%2017.973509%20149.262999%2018.049257%20149.051512%22%29%3B%0A%0Aout%20meta%20asc%3B"
original_query_result = requests.get(
    url=ogf_overpass_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Referer": "https://registry.moe.gov.hx/index.html",
    },
).content.decode("utf-8")

header = original_query_result.split("\n")[0].split("|")
query_result = original_query_result.replace(str("|".join(header) + "\n"), "")

universities = list(
    filter(
        bool,
        [
            item_dict if item_dict["short_name"] != "" else None
            for item_dict in [
                dict(zip(header, item.split("|")))
                for item in list(filter(bool, query_result.split("\n")))
            ]
        ],
    )
)

from pprint import pprint

universities_sorted = sorted(universities, key=lambda x: x["addr:province"])
pprint(universities_sorted)
pprint(len(universities_sorted))

# 下面的部分感谢 ChatGPT 4 Turbo 和 Google Palm Codey 32K

from jinja2 import Template
import webbrowser
import os


template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>University List</title>
</head>
<body>
   <h1>University List</h1>
   <table>
       <tr>
           <th>Name</th>
           <th>Name (English)</th>
           <th>ID</th>
           <th>Type</th>
           <th>Province</th>
           <th>Operator</th>
           <th>Short Name</th>
       </tr>
   {% for university in universities %}
       <tr>
           <td>{{ university['name'] }}</td>
           <td>{{ university['name:en'] }}</td>
           <td>{{ university['@id'] }}</td>
           <td>{{ university['@type'] }}</td>
           <td>{{ university['addr:province'] }}</td>
           <td>{{ university['operator'] }}</td>
           <td>{{ university['short_name'] }}</td>
       </tr>
   {% endfor %}
   </table>
</body>
</html>
"""

template = Template(template_str)
rendered_html = template.render(universities=universities_sorted)
html_file_path = "https_registry.moe.gov.hx_index.html"
with open(html_file_path, "w", encoding="utf-8") as file:
    file.write(rendered_html)
webbrowser.open("file://" + os.path.realpath(html_file_path))
