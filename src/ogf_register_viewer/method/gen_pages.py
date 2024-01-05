import os
import webbrowser

from jinja2 import Template


def gen_pages(
    elements_completed_sorted,
    elements_uncompleted_sorted,
    template_file_name: str,
    optional_data={},
):
    template_file = open(
        "../assets/" + template_file_name, "r", encoding="utf-8"
    )
    template_str = template_file.read()
    template_file.close()

    template = Template(template_str)
    rendered_html = template.render(
        universities_completed=elements_completed_sorted,
        universities_uncompleted=elements_uncompleted_sorted,
        universities_completed_count=len(elements_completed_sorted),
        universities_full_count=len(elements_completed_sorted)
        + len(elements_uncompleted_sorted),
        page_title=optional_data["page_title"],
    )
    html_file_path = "https_registry.moe.gov.hx_index.html"
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    webbrowser.open("file://" + os.path.realpath(html_file_path))
