from pathlib import Path
from datetime import datetime, UTC
import yaml
import click
from markdown import markdown
from parse_post import parse_post
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

# read yaml file from click argument
def build_blog(data_path, landing_template, entry_template, blog_path):
    """
    Create an RSS XML file from a yaml file containing blog entry metadata.

    data_path: (String) path to yaml file with blog post entry metadata
    atomfile: (String) path to RSS XML file to write to disk
    """

    posts_path = Path(data_path).parent.absolute()
    data = yaml.safe_load(open(data_path))

    # blog_title = data["title"]
    # blog_author = data["author"]["name"]
    # blog_email = data["author"]["email"]
    # blog_logo = data["logo"]
    # blog_link = data["link"]
    # blog_description = data["description"]

    blog_path = Path(blog_path).absolute()
    if blog_path.exists():
        shutil.rmtree(blog_path, ignore_errors=True)
    blog_path.mkdir()


    # read landing template
    with open(posts_path / Path(landing_template)) as f:
        landing_template = f.read()

    for post in data["posts"]:
        # set post entry pub date if it doesn't exist
        if "pub_date" not in post:
            post["pub_date"] = datetime.now(UTC).isoformat()
        post_pub_date = post["pub_date"]
        post_file = post["file"]
        post_lang = post["lang"]
        post_url = f"{data['link']}/{post_file.replace('.md', '.html')}"

        title, summary_title, summary_content, sections = parse_post(posts_path / Path(post_file))

        # read entry template
        with open(posts_path / Path(entry_template)) as f:
            entry_html = f.read()

        entry_html = entry_html.replace("{% title %}", title)

        entry_html = entry_html.replace("{% summary %}", f'<section>\n{markdown(f"## {summary_title}\n{summary_content}")}\n</section>')

        sections_html = ""
        for section in sections:
            sections_html += f'<section>\n{markdown(section)}\n</section>'
        entry_html = entry_html.replace("{% sections %}", sections_html)

        with open(blog_path / Path(post_file.replace(".md", ".html")), "w") as f:
            f.write(entry_html)


    yaml.dump(data, open(data_path, "w"), sort_keys=False) # Write the updated yaml file to disk

if __name__ == "__main__":
    build_blog()