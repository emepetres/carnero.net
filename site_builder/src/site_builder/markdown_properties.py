import yaml


def get_markdown_properties(markdown: str) -> dict[str, str]:
    """Extracts properties from markdown file."""

    # get properties data bewteen ---
    properties_data = ""
    under_properties = False
    for line in markdown.splitlines():
        if line.startswith("---"):
            if under_properties:
                break
            else:
                under_properties = True
                continue
        if under_properties:
            properties_data += line + "\n"

    # parse yaml properties
    properties = yaml.safe_load(properties_data)
    if properties is None:
        properties = {}

    return properties


def set_markdown_properties(markdown: str, properties: dict[str, str]) -> str:
    """Set properties to markdown file."""

    properties_data = f"---\n{yaml.dump(properties, sort_keys=False)}---\n"

    # replace properties data
    new_markdown = ""
    no_properties = False
    properties_delimiters_found = 0
    for line in markdown.splitlines():
        # check if properties are present
        if properties_delimiters_found == 0:
            if line.strip() == "---":
                properties_delimiters_found += 1
                new_markdown += properties_data
                continue
            elif line.strip() != "":
                no_properties = True
                break

        if properties_delimiters_found == 1:
            if line.strip() == "---":
                properties_delimiters_found += 1
            continue

        new_markdown += line + "\n"

    if no_properties:
        new_markdown = properties_data + markdown

    return new_markdown
