# This file is intended to bundle all generated packages and publish them to a static hosting service.
import json
import os
import shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from jinja2 import Template

from method.const import HOSTING

# get profile list
profiles = [
    "https_"
    + json.load(open("../assets/profile/" + profile, "r", encoding="utf-8"))
    .get("template_file_name")
    .replace(".jinja2", "")
    + "_index.html"
    for profile in os.listdir("../assets/profile/")
]
# print(profiles)

# gen index html
index_template_file = open(
    "../assets/template/" + "_index.jinja2", "r", encoding="utf-8"
)
index_template = index_template_file.read()
index_template_file.close()
index_html = Template(index_template).render(
    hosting_path=HOSTING,
    profiles=profiles,
    gen_time=datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
)
# print(index_html)

# write index html
with open("../../dist/" + "index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

# bundle necessary file
assets_css_list = os.listdir("../assets/css/")
assets_js_list = os.listdir("../assets/js/")
assets_script_list = os.listdir("../assets/script/")
if os.path.exists("../../dist/css") != True:
    os.mkdir("../../dist/css")
if os.path.exists("../../dist/js") != True:
    os.mkdir("../../dist/js")
for css in assets_css_list:
    shutil.copy(src="../assets/css/" + css, dst="../../dist/css/" + css)
for js in assets_js_list:
    shutil.copy(src="../assets/js/" + js, dst="../../dist/js/" + js)
for script in assets_script_list:
    shutil.copy(src="../assets/script/" + script, dst="../../dist/" + script)
