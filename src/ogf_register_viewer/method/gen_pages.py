import os
import webbrowser

from jinja2 import Template


def gen_pages(
    universities_completed_sorted,
    universities_uncompleted_sorted,
    optional_data=None,
):
    template_file = open(
        "../css/registry.moe.gov.hx.html", "r", encoding="utf-8"
    )
    template_str = template_file.read()
    template_file.close()

    template = Template(template_str)
    optional_data = {
        "page_title": "MOE of Republic of Huaxia - Universities List"
    }
    rendered_html = template.render(
        universities_completed=universities_completed_sorted,
        universities_uncompleted=universities_uncompleted_sorted,
        universities_completed_count=len(universities_completed_sorted),
        universities_full_count=len(universities_completed_sorted)
        + len(universities_uncompleted_sorted),
        page_title=optional_data["page_title"],
    )
    html_file_path = "https_registry.moe.gov.hx_index.html"
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    webbrowser.open("file://" + os.path.realpath(html_file_path))
