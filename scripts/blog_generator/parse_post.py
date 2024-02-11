from pathlib import Path


def _is_h1(line):
    return line.startswith("# ")

def _is_h2(line):
    return line.startswith("## ")

def parse_post(post_path: Path) -> tuple[str, str, str, list[str]]:
    with open(post_path) as f:
        mddata = f.readlines()

    title = None
    sections = []
    current_section = ""
    for line in mddata:
        if _is_h1(line):
            if title:
                raise ValueError("More than one h1 found")
            title = line.replace("#", "").strip()
            continue
        elif _is_h2(line):
            if current_section:
                sections.append(current_section)
            current_section = line
            continue

        if title and current_section:
            current_section += line
    if current_section:
        sections.append(current_section)

    # get first section as summary
    summary = sections[0]
    sections = sections[1:]

    # separate summary into title and content
    non_empty_lines = [line for line in summary.split("\n") if line.strip()]
    summary_title = non_empty_lines[0].replace("##", "").strip()
    summary_content = "\n".join(non_empty_lines[1:])

    return title, summary_title, summary_content, sections
