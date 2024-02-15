# this file meant to bundle all generated package and publish them to static host service
import json
import os

from jinja2 import Template

profiles = [
    "https_"
    + json.load(open("../assets/profile/" + profile, "r", encoding="utf-8"))
    .get("template_file_name")
    .replace(".html", "")
    + "_index.html"
    for profile in os.listdir("../assets/profile/")
]
# print(profiles)

index_template_file = open(
    "../assets/template/" + "_index.html", "r", encoding="utf-8"
)
index_template = index_template_file.read()
index_template_file.close()
index_html = Template(index_template).render(
    hosting_path="ogflab.zeabur.app",
    profiles=profiles,
)
# print(index_html)

with open("../../dist/" + "index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
