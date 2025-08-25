import os
import webbrowser

from jinja2 import Template

from method.const import OSS
from method.environment import (
    get_environment_description,
    get_local_time,
    get_local_timezone,
)


def gen_pages(
    elements_completed_sorted,
    elements_uncompleted_sorted,
    template_file_name: str,
    dst_file_name: str,
    optional_data={},
):
    template_file = open(
        "../assets/template/" + template_file_name, "r", encoding="utf-8"
    )
    template_str = template_file.read()
    template_file.close()

    template = Template(template_str)
    if optional_data.get("clustered_data", None) != None:
        clustered_data = optional_data["clustered_data"]
    else:
        clustered_data = ""
    rendered_html = template.render(
        elements_completed=elements_completed_sorted,
        elements_uncompleted=elements_uncompleted_sorted,
        elements_completed_count=len(elements_completed_sorted),
        elements_full_count=len(elements_completed_sorted)
        + len(elements_uncompleted_sorted),
        page_title=optional_data["page_title"],
        oss_path=OSS,
        gen_time=get_local_time(),
        meta_local_timezone=get_local_timezone(),
        meta_build_machine=get_environment_description(),
        clustered_data=clustered_data.replace("\n", "<br/>"),
    )
    html_file_name = "https_" + dst_file_name + "_index.html"
    html_file_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "dist", html_file_name
    )
    if (
        os.path.exists(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "dist")
        )
        == False
    ):
        os.mkdir(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "dist")
        )
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    webbrowser.open("file://" + os.path.realpath(html_file_path))
