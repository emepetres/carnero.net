from fast-markdown.markdown_properties import (
    get_markdown_properties,
    set_markdown_properties,
)


def test_read_simple_properties():
    markdown = """
---
title: "My Title"
pub_date: "2022-01-01"
---
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {
        "title": "My Title",
        "pub_date": "2022-01-01",
    }


def test_ignore_comments():
    markdown = """
---
title: "My Title"
# this is a comment
pub_date: "2022-01-01" # another comment
---
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {
        "title": "My Title",
        "pub_date": "2022-01-01",
    }


def test_read_lists():
    markdown = """
---
title: "My Title"
pub_date: "2022-01-01"
tags:
    - tag1
    - tag2
---
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {
        "title": "My Title",
        "pub_date": "2022-01-01",
        "tags": ["tag1", "tag2"],
    }


def test_read_nested_properties():
    markdown = """
---
title: "My Title"
pub_date: "2022-01-01"
author:
    name: "John Doe"
    email: "john@doe.com"
---
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {
        "title": "My Title",
        "pub_date": "2022-01-01",
        "author": {"name": "John Doe", "email": "john@doe.com"},
    }


def test_read_empty_properties():
    markdown = """
---
---
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {}


def test_read_no_properties():
    markdown = """
# Section 1
Content 1
    """
    properties = get_markdown_properties(markdown)
    assert properties == {}


def test_update_properties():
    markdown = """
---
title: "My Title"
pub_date: "2022-01-01"
---
# Section 1
Content 1
"""
    properties = {
        "title": "New Title",
        "pub_date": "2023-01-01",
    }
    new_markdown = set_markdown_properties(markdown, properties)
    assert (
        new_markdown
        == """
---
title: New Title
pub_date: '2023-01-01'
---
# Section 1
Content 1
"""
    )


def test_add_properties():
    markdown = """
# Section 1
Content 1
    """
    properties = {
        "title": "My Title",
        "pub_date": "2022-01-01",
    }
    new_markdown = set_markdown_properties(markdown, properties)
    test_markdown = """---
title: My Title
pub_date: '2022-01-01'
---

# Section 1
Content 1
    """
    assert new_markdown == test_markdown
