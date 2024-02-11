from pathlib import Path
from markdown import markdown

def create_html_post(
    template_path: Path,
    metadata: dict,
    title: str,
    summary_title: str,
    summary_content: str,
    sections: list[str],
    publish_date: str,
    output_path: Path,
):
    # read entry template
    with open(template_path) as f:
        entry_html = f.read()

    master_title = metadata["title"]
    # TODO Author, fecha, categories

    # replace title
    entry_html = entry_html.replace("{% master-title %}", master_title)
    entry_html = entry_html.replace("{% title %}", title)
    entry_html = entry_html.replace("{% pubdate %}", publish_date)

    # replace summary
    entry_html = entry_html.replace("{% summary %}", f'<section>\n{markdown(f"## {summary_title}\n{summary_content}")}\n</section>')

    # replace sections
    sections_html = ""
    for section in sections:
        sections_html += f'<section>\n{markdown(section)}\n</section>'
    entry_html = entry_html.replace("{% sections %}", sections_html)

    with open(output_path, "w") as f:
        f.write(entry_html)