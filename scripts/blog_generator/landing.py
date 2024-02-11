from pathlib import Path

def create_html_landing(
    template_path: Path,
    metadata: dict,
    posts_summaries: list[dict],
    output_path: Path,
):
    # read entry template
    with open(template_path) as f:
        landing_html = f.read()

    master_title = metadata["title"]
    # # author = metadata["author"]["name"]
    # # email = metadata["author"]["email"]
    # # logo = metadata["logo"]
    # # link = metadata["link"]
    # # description = metadata["description"]

    # replace title
    landing_html = landing_html.replace("{% master-title %}", master_title)

    # replace list of posts
    posts_html = ""
    for post in posts_summaries:
        posts_html += f'''
            <section>
                <h2><a href="{post["uri"]}">{post["title"]}</a></h2>
                <p>{post["summary_content"]}</p>
                <aside>{post["pub_date"]}</aside>
            </section>
            '''
    landing_html = landing_html.replace("{% list %}", posts_html)

    with open(output_path, "w") as f:
        f.write(landing_html)