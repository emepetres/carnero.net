from pathlib import Path
from datetime import datetime, UTC
import yaml
import click
from feedgen.feed import FeedGenerator
from multilang import MultilangExtension, MultilangEntryExtension


@click.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.option(
    "--atomfile", help="File name of RSS XML file to create.", type=click.Path(), default="atom.xml"
)

# read yaml file from click argument
def create_feed(data_path, atomfile):
    """
    Create an RSS XML file from a yaml file containing blog entry metadata.

    data_path: (String) path to yaml file with blog post entry metadata
    atomfile: (String) path to RSS XML file to write to disk
    """

    posts_path = Path(data_path).parent.absolute()
    data = yaml.safe_load(open(data_path))

    feed = FeedGenerator()
    feed.register_extension("multilang", MultilangExtension, MultilangEntryExtension)


    feed.id(data["id"])
    feed.title(data["title"])
    feed.author(
        {"name": data["author"]["name"], "email": data["author"]["email"]}
    )
    feed.logo(data["logo"])
    feed.link(href=data["link"], rel="self")
    feed.language(data["language"])
    feed.description(data["description"])

    for post in data["posts"]:
        # set post entry pub date if it doesn't exist
        if "pub_date" not in post:
            post["pub_date"] = datetime.now(UTC).isoformat()
        post_pub_date = post["pub_date"]

        # post_date = datetime.strptime(post["date"], '%Y-%m-%d  %H:%M').
        post_file = post["file"]
        post_lang = post["lang"]

        # read first line of post_file
        with open(posts_path / post_file, "r") as f:
            first_line = f.readline()
            post_title = first_line.replace("#", "").strip()

        post_url = f"{data['link']}/{post_file.replace('.md', '.html')}"

        entry = feed.add_entry(order="append")
        entry.id(post_url)
        entry.title(post_title)
        entry.multilang.language(post_lang)
        entry.published(post_pub_date)
        entry.updated(post_pub_date)
        entry.author(
            {"name": data["author"]["name"], "email": data["author"]["email"]}
        )
        entry.link({"href": post_url, "title": post_title, "hreflang": post_lang})

    feed.atom_file(atomfile, pretty=True) # Write the ATOM feed to a file

    yaml.dump(data, open(data_path, "w"), sort_keys=False) # Write the updated yaml file to disk


if __name__ == "__main__":
    create_feed()