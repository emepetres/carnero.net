import pytest
from pathlib import Path
from freezegun import freeze_time
from site_builder.content import Content
from site_builder.markdown_properties import get_markdown_properties


@pytest.fixture(scope="session")
def config():
    config = {
        "templates": {
            "default": "templates/default.html",
            "section": "templates/section.html",
        }
    }
    return config


@pytest.fixture(autouse=True)
def clean_content(config) -> None:
    Content.uri = "/"
    Content.website_title = None
    Content.master_title = None
    Content.data_path = Path(".")
    Content.templates = config["templates"]


@pytest.fixture()
def markdown_file(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = """
---
uri: "sample.html"
lang: "en"
---

# Title

ignored text

## Summary

Summary content

## Section 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 2

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 3

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

"""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


@pytest.fixture()
def published_markdown_file(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = """
---
uri: "sample.html"
lang: "en"
pub_date: "2024-02-14T22:12:07.502647+00:00"
---

# Title

ignored text

## Summary

Summary content

## Section 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 2

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 3

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

"""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


@pytest.fixture()
def template(tmp_path_factory: pytest.TempPathFactory):
    template_data = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>
        {% title %}
        <aside>{% pubdate %}</aside>
      </h1>

      <section>
        <h2>{% summary_title %}</h2>
        <p>{% summary_content %}</p>
      </section>
</body>
</html>
"""
    templates_path = tmp_path_factory.mktemp("templates")
    fn = templates_path / "template.html"
    fn.write_text(template_data)
    return fn


@pytest.fixture()
def markdown_without_properties(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = """
# Title

ignored text

## Summary

Summary content

## Section 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 2

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 3

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

"""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


@pytest.fixture()
def markdown_wrong_properties(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = """
# Title

ignored text

---
some_property: "some_value"
---

## Summary

Summary content

## Section 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 2

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

## Section 3

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget libero nec

"""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


@pytest.fixture()
def markdown_no_content(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = """
# Title
"""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


@pytest.fixture()
def markdown_empty(tmp_path_factory: pytest.TempPathFactory):
    markdown_content = ""
    content_path = tmp_path_factory.mktemp("content")
    fn = content_path / "content.md"
    fn.write_text(markdown_content)
    return fn


def test_read_title(markdown_file: Path):
    content = Content.read_from_markdown(markdown_file)
    assert content.title == "Title"


def test_read_summary(markdown_file: Path):
    content = Content.read_from_markdown(markdown_file)
    assert content.sections[0]["title"] == "Summary"
    assert content.sections[0]["content"] == "Summary content"


def test_read_sections(markdown_file: Path):
    content = Content.read_from_markdown(markdown_file)
    assert len(content.sections) == 4


@freeze_time("2024-02-21")
def test_update_pub_date(markdown_file: Path):
    content = Content.read_from_markdown(markdown_file)
    assert content.pub_date == "2024-02-21"


@freeze_time("2024-02-21")
def test_keep_pub_date(published_markdown_file: Path
):
    content = Content.read_from_markdown(published_markdown_file)
    assert content.pub_date == "2024-02-14"


@freeze_time("2024-02-21")
def test_update_properties(markdown_file: Path):
    content = Content.read_from_markdown(markdown_file)
    content.write_properties()
    with open(markdown_file) as f:
        markdown = f.read()
    properties = get_markdown_properties(markdown)
    assert len(properties) == 3
    assert properties["uri"] == "sample.html"
    assert properties["lang"] == "en"
    assert properties["pub_date"] == "2024-02-21T00:00:00+00:00"


@freeze_time("2024-02-21")
def test_write_html(markdown_file: Path, template: Path
):
    content = Content.read_from_markdown(markdown_file)
    content.template = template
    content.write_to_html(markdown_file.parent)
    html_file = markdown_file.parent / content.uri
    assert html_file.exists()
    with open(html_file) as f:
        html = f.read()
    assert (
        html
        == """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>
        Title
        <aside>2024-02-21</aside>
      </h1>

      <section>
        <h2>Summary</h2>
        <p>Summary content</p>
      </section>
</body>
</html>
"""
    )


def test_support_for_no_properties(markdown_without_properties: Path
):
    content = Content.read_from_markdown(markdown_without_properties)
    assert len(content.sections) == 4


def test_detect_wrong_properties_position(markdown_wrong_properties: Path
):
    with pytest.raises(ValueError):
        Content.read_from_markdown(markdown_wrong_properties)


def test_support_files_only_title(markdown_no_content: Path
):
    content = Content.read_from_markdown(markdown_no_content)
    assert content.title == "Title"
    assert content.sections == []


def test_raise_with_empty_files(markdown_empty: Path
):
    with pytest.raises(ValueError):
        Content.read_from_markdown(markdown_empty)
