# This file is intended to bundle all generated packages and publish them to a static hosting service.
import json
import os
import shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from jinja2 import Template

from method.const import HOSTING, NOT_PROFILE_NAME


def get_local_timezone():
    from tzlocal import get_localzone

    try:
        return ZoneInfo(str(get_localzone()))
    except Exception:
        return ZoneInfo("UTC")


# get profile list
ignore_filename_list = NOT_PROFILE_NAME

profiles = [
    "https_"
    + json.load(open("../assets/profile/" + profile, "r", encoding="utf-8"))
    .get("id")
    .replace(".jinja2", "")
    + "_index.html"
    # ↓ 需要在这里排除一下profile文件夹里面的index和readme
    # 今天没时间了下次一定
    for profile in list(
        filter(
            bool,
            [
                profile if profile not in ignore_filename_list else ""
                for profile in os.listdir("../assets/profile/")
            ],
        )
    )
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
    gen_time=datetime.now(get_local_timezone()).isoformat(),
)
# print(index_html)

# write index html
if os.path.exists("../../dist/") == False:
    os.mkdir("../../dist/")
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

# gitkeep
if os.path.exists("../../dist/.gitkeep") != True:
    with open("../../dist/.gitkeep","w") as f:
        f.write("")