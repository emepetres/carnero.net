from pathlib import Path
from feedgen.feed import FeedGenerator
from site_builder.multilang import MultilangExtension, MultilangEntryExtension
from site_builder.feedgen_patch import atom_entry_patched
from site_builder.content import Content


class AtomFeed:
    def __init__(self, base_url: str, folder: Path, metadata: dict):
        self.url = f"{base_url}/{folder}"
        self.path = folder
        self.metadata = metadata
        self.feed = self.create_feed()

    def create_feed(self) -> FeedGenerator:
        feed = FeedGenerator()
        feed.register_extension(
            "multilang", MultilangExtension, MultilangEntryExtension
        )

        feed.id(self.url)
        feed.title(self.metadata["title"])
        feed.author(
            {
                "name": self.metadata["author"]["name"],
                "email": self.metadata["author"]["email"],
            }
        )
        feed.logo(self.metadata["logo"])
        feed.link(href=self.url, rel="self")
        feed.link(
            href=f"{self.url}/{self.metadata['feed_file']}",
            rel="alternate",
        )
        feed.language(self.metadata["language"])
        feed.description(self.metadata["description"])

        return feed

    def add_entry(self, content: Content):
        """Adds a new entry to the feed.

        If there is no pub_date in the metadata, it will be set
          to the current date and time

        Args:
            content: Content post data from markdown file
        """
        entry = self.feed.add_entry(order="append")

        import types

        funcType = types.MethodType
        entry.atom_entry = funcType(atom_entry_patched, entry)

        entry.id(content.uri)
        entry.title(content.title)
        entry.summary(content.sections[0]["content"] if content.sections else "")
        if content.img:
            entry.enclosure(content.img, 0, f"image/{content.img.split('.')[-1]}")
        entry.multilang.language(content.lang)
        entry.published(content.properties["pub_date"])
        entry.updated(content.properties["pub_date"])
        entry.link(
            {
                "href": "/" + content.uri,
                "rel": "alternate",
                "title": content.title,
                "hreflang": content.lang,
            }
        )
        entry.author(
            {
                "name": self.metadata["author"]["name"],
                "email": self.metadata["author"]["email"],
            }
        )

    def write_feed_to_disk(self, bundle_path: Path):
        self.feed.atom_file(
            bundle_path / self.path / self.metadata["feed_file"], pretty=True
        )

    def __str__(self):
        return f"Feed: {self.metadata['title']}"

    def __repr__(self):
        return f"Feed: {self.metadata['title']}"

    def __eq__(self, other):
        return self.metadata == other.metadata

    def __ne__(self, other):
        return self.metadata != other.metadata
