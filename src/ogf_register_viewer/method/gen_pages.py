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
        "../assets/template/" + template_file_name, "r", encoding="utf-8"
    )
    template_str = template_file.read()
    template_file.close()

    template = Template(template_str)
    rendered_html = template.render(
        elements_completed=elements_completed_sorted,
        elements_uncompleted=elements_uncompleted_sorted,
        elements_completed_count=len(elements_completed_sorted),
        elements_full_count=len(elements_completed_sorted)
        + len(elements_uncompleted_sorted),
        page_title=optional_data["page_title"],
    )
    html_file_name = (
        "https_" + template_file_name.replace(".html", "") + "_index.html"
    )
    html_file_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "dist", html_file_name
    )
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    webbrowser.open("file://" + os.path.realpath(html_file_path))
