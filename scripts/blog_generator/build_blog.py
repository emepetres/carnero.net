from pathlib import Path
import yaml
import click
from feed import Feed
from parse_post import parse_post
from post import create_html_post
from landing import create_html_landing
import shutil


@click.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.option(
    "--landing_template", help="File name of HTML template to create the blog landing page", type=click.Path(), default="templates/landing.html"
)
@click.option(
    "--entry_template", help="File name of HTML template to create blog entries", type=click.Path(), default="templates/entry.html"
)
@click.option(
    "--blog_path", help="Path where blog will be generated", type=click.Path(), default="blog/"
)
@click.option(
    "--atomfile", help="File name of RSS XML file to create.", type=click.Path(), default="atom.xml"
)

# read yaml file from click argument
def build_blog(data_path, landing_template, entry_template, blog_path, atomfile):
    """
    Create an RSS XML file from a yaml file containing blog entry metadata.

    data_path: (String) path to yaml file with blog post entry metadata
    atomfile: (String) path to RSS XML file to write to disk
    """

    posts_path = Path(data_path).parent.absolute()
    metadata = yaml.safe_load(open(data_path))

    feed = Feed(metadata, atomfile)

    # clean blog path
    blog_path = Path(blog_path).absolute()
    if blog_path.exists():
        shutil.rmtree(blog_path, ignore_errors=True)
    blog_path.mkdir()

    posts_summaries = []
    for post_metadata in metadata["posts"]:
        post_file = post_metadata["file"]
        title, summary_title, summary_content, sections = parse_post(posts_path / Path(post_file))

        # add post to feed
        feed.add_entry(post_metadata, title)

        # create html post
        output_path = blog_path / Path(post_file.replace(".md", ".html"))
        create_html_post(
            posts_path / Path(entry_template),
            title,
            summary_title,
            summary_content,
            sections,
            output_path),

        posts_summaries.append(
            {"title": title,
             "summary_content": summary_content,
             "uri": output_path}
        )

    create_html_landing(
        posts_path / Path(landing_template),
        metadata,
        posts_summaries,
        blog_path / Path("index.html")
    )

    feed.write_feed_to_disk()

    # update metadata yaml with new pub dates
    yaml.dump(metadata, open(data_path, "w"), sort_keys=False)

if __name__ == "__main__":
    build_blog()
