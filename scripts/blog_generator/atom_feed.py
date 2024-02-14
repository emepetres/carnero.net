from datetime import datetime, UTC
from feedgen.feed import FeedGenerator
from multilang import MultilangExtension, MultilangEntryExtension
from feedgen_patch import atom_entry_patched


class AtomFeed:
    def __init__(self, metadata, atomfile):
        self.metadata = metadata
        self.atomfile = atomfile
        self.feed = self.create_feed()

    def create_feed(self) -> FeedGenerator:
        feed = FeedGenerator()
        feed.register_extension("multilang", MultilangExtension, MultilangEntryExtension)

        feed.id(self.metadata["id"])
        feed.title(self.metadata["title"])
        feed.author(
            {"name": self.metadata["author"]["name"], "email": self.metadata["author"]["email"]}
        )
        feed.logo(self.metadata["logo"])
        feed.link(href=self.metadata["link"], rel="self")
        feed.link(href=self.metadata["feed"], rel="alternate")
        feed.language(self.metadata["language"])
        feed.description(self.metadata["description"])

        return feed

    def add_entry(self, metadata: dict, title: str, summary: str):
        """Adds a new entry to the feed.

        If there is no pub_date in the metadata, it will be set to the current date and time

        Args:
            metadata (dict): post metadata from yaml file
            title (str): post title
            summary (str): post summary
        """
        # # FeedEntry.atom_entry = atom_entry_patched

        # set post entry pub date if it doesn't exist
        if "pub_date" not in metadata:
            metadata["pub_date"] = datetime.now(UTC).isoformat()

        post_pub_date = metadata["pub_date"]
        post_file = metadata["file"]
        post_lang = metadata["lang"]
        post_url = f"{self.metadata['link']}/{post_file.replace('.md', '.html')}"

        entry = self.feed.add_entry(order="append")

        import types
        funcType = types.MethodType
        entry.atom_entry = funcType(atom_entry_patched, entry)

        entry.id(post_url)
        entry.title(title)
        entry.summary(summary)
        entry.enclosure(metadata["img"], 0, f"image/{metadata['img'].split('.')[-1]}")
        entry.multilang.language(post_lang)
        entry.published(post_pub_date)
        entry.updated(post_pub_date)
        entry.link({"href": post_url, "rel":"alternate", "title": title, "hreflang": post_lang})
        entry.author(
            {"name": self.metadata["author"]["name"], "email": self.metadata["author"]["email"]}
        )

    def write_feed_to_disk(self):
        self.feed.atom_file(self.atomfile, pretty=True) # Write the ATOM feed to a file

    def __str__(self):
        return f"Feed: {self.metadata['title']}"

    def __repr__(self):
        return f"Feed: {self.metadata['title']}"

    def __eq__(self, other):
        return self.metadata == other.metadata

    def __ne__(self, other):
        return self.metadata != other.metadata