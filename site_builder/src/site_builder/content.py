from typing import Self
from pathlib import Path
from markdown import markdown
from datetime import datetime, UTC
import dateutil.parser
from site_builder.markdown_properties import (
    get_markdown_properties,
    set_markdown_properties,
)


class Content:
    # configurable properties
    uri: str = "/"
    website_title: str | None = None
    master_title: str | None = None
    templates: dict = {}

    def __init__(self, file_path: Path):
        self.file_path: Path = file_path
        self.title: str | None = None
        self.sections: list[str] = []
        self.uri: str | None = None
        self.template: Path | None = None
        self.lang: str | None = None
        self.img: str | None = None
        self.pub_date: str | None = None

        self.listable = self.file_path.name != "index.md"

        with open(file_path, encoding="utf8") as f:
            markdown = f.read()
        self.markdown = markdown
        self.properties = get_markdown_properties(markdown)

    def read_from_markdown(file_path: Path) -> Self:
        content = Content(file_path)

        # set template
        if "template" in content.properties:
            content.template = Path(Content.templates[content.properties["template"]])
        else:
            content.template = Path(Content.templates["default"])

        # set uri
        if Content.uri == "" or Content.uri[-1] != "/":
            Content.uri += "/"
        default_uri = Content.uri + file_path.name.replace(".md", ".html")
        content.uri = (
            content.properties["uri"] if "uri" in content.properties else default_uri
        )
        if content.uri[0] == "/":
            content.uri = content.uri[1:]

        # set lang
        content.lang = (
            content.properties["lang"] if "lang" in content.properties else "en"
        )

        # set img
        content.img = content.properties["img"] if "img" in content.properties else None

        # set publication date
        if "pub_date" not in content.properties:
            content.properties["pub_date"] = datetime.now(UTC).isoformat()
        content.pub_date = (
            dateutil.parser.isoparse(content.properties["pub_date"])
            .date()
            .strftime("%Y-%m-%d")
        )

        # set title and sections
        content.title = None
        content.sections = []
        no_properties = False
        properties_delimiters_found = 0
        for line in content.markdown.splitlines():
            # check if properties are present
            if properties_delimiters_found == 0:
                if line.strip() != "---" and line.strip() != "":
                    no_properties = True

            # check if properties are found after content
            if no_properties and line.strip() == "---":
                raise ValueError(
                    f"Properties found after content in file {content.file_path}"
                )

            # ignore properties if present
            if not no_properties and properties_delimiters_found < 2:
                if line.strip() == "---":
                    properties_delimiters_found += 1
                continue

            # look for title. Data before title is ignored
            if Content._is_h1(line):
                if content.title:
                    raise ValueError("More than one h1 found")
                content.title = line.replace("#", "").strip()
                continue
            elif Content._is_h2(line):  # Look for sections
                content.sections.append(
                    {"title": line.replace("##", "").strip(), "content": ""}
                )
                continue
            if content.title and content.sections:
                content.sections[-1]["content"] += line + "\n"

        # clean sections content empty lines
        for section in content.sections:
            section["content"] = section["content"].strip()

        if content.title is None:
            raise ValueError(f"No title found in file '{content.file_path}'")

        return content

    def write_properties(self):
        self.markdown = set_markdown_properties(self.markdown, self.properties)

        with open(self.file_path, "w", encoding="utf8") as f:
            f.write(self.markdown)

    def write_to_html(
        self,
        bundle_path: Path,
        summaries: list[dict] = [],
    ):
        # read entry template
        with open(self.template) as f:
            html = f.read()

        # replace headers
        if Content.website_title is not None:
            html = html.replace("{% website-title %}", Content.website_title)
        if Content.master_title is not None:
            html = html.replace("{% master-title %}", Content.master_title)
        html = html.replace("{% title %}", self.title)
        html = html.replace("{% pubdate %}", self.pub_date)
        html = html.replace("{% uri %}", self.uri)

        # replace summary
        if self.sections:
            html = html.replace("{% summary_title %}", self.sections[0]["title"])
            html = html.replace("{% summary_content %}", self.sections[0]["content"])
        else:
            html = html.replace("{% summary_title %}", "")
            html = html.replace("{% summary_content %}", "")

        sections_html = ""
        # replace first section
        if len(self.sections) > 1:
            section = self.sections[1]
            sections_html += f"<section>\n{markdown(
                section["content"],
                extensions=['attr_list', 'def_list'])}\n</section>"
        # replace rest of the sections
        if len(self.sections) > 2:
            for section in self.sections[2:]:
                sections_html += (
                    f"<section>\n<h2>{section['title']}</h2>\n"
                    f"{markdown(section["content"], extensions=['attr_list', 'def_list'])}\n</section>"
                )
        html = html.replace("{% sections %}", sections_html)

        # replace list of summaries
        if summaries:
            summaries_html = ""
            for summary in summaries:
                summaries_html += f"""
                    <section>
                        <h2><a href="/{summary["uri"]}">{summary["title"]}</a></h2>
                        <p>{summary["summary_content"]}</p>
                        <aside>{summary["pub_date"]}</aside>
                    </section>
                    """
            html = html.replace("{% list %}", summaries_html)

        with open(bundle_path / self.uri, "w", encoding="utf8") as f:
            f.write(html)

    def _is_h1(line):
        return line.startswith("# ")

    def _is_h2(line):
        return line.startswith("## ")

    def __str__(self):
        return f"{self.title}: {self.summary_content}"

    def __repr__(self):
        return self.__str__()
