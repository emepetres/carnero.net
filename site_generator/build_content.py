from pathlib import Path
import yaml
from site_generator.atom_feed import AtomFeed
from site_generator.content import Content


def build_content(bundle_path: Path, content_path: Path, folder: Path, master_config: dict) -> None:
    """Builds html files from markdown content and writes them to disk.

    Args:
        bundle_path (Path): base path to write html files
        content_path (Path): base path to read markdown files
        master_config (dict): master configuration
    """
    # create bundle path if it doesn't exist
    (bundle_path / folder).mkdir(parents=True, exist_ok=True)

    # get config
    website_tile = master_config["title"] if "title" in master_config else None
    base_url = f"{master_config["protocol"]}://{master_config["domain"]}"
    config_path = content_path / folder / "config.yaml"
    if config_path.exists():
        config = yaml.safe_load(open(config_path))
    else:
        config = master_config

    # configure Content class
    Content.uri = str(folder)
    Content.website_title = website_tile
    Content.master_title = config["title"] if "title" in config else None
    Content.templates = config["templates"]

    is_blog = "feed_file" in config

    if is_blog:
        feed = AtomFeed(base_url, folder, config)

    contents = _read_markdown_content(content_path, folder)
    contents = sorted(contents, key=lambda x: x.pub_date, reverse=True)

    summaries = []
    not_listable: list[Content] = []
    for content in contents:

        if content.listable:

            if is_blog:
                # add post to feed
                feed.add_entry(content)

            # create html page
            content.write_to_html(bundle_path)
            content.write_properties()

            summaries.append(
                {
                    "title": content.title,
                    "summary_content": content.sections[0]["content"] if content.sections else "",
                    "pub_date": content.pub_date,
                    "uri": content.uri,
                }
            )
        else:
            not_listable.append(content)

    for page in not_listable:
        page.write_to_html(bundle_path, summaries=summaries)
        page.write_properties()

    if is_blog:
        feed.write_feed_to_disk(bundle_path)


def _read_markdown_content(content_path: Path, folder: Path) -> list[Content]:
    contents: list[Content] = []

    # loop through files inside content_path
    for file in (content_path / folder).glob("*.md"):
        # discard draft files that start with "_"
        if file.name.startswith("_"):
            continue

        content = Content.read_from_markdown(file)
        contents.append(content)

    return contents
