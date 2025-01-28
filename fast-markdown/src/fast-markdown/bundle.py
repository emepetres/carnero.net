from pathlib import Path
import click
import shutil
import yaml

import fast-markdown.settings as settings
from fast-markdown.build_content import build_content


@click.command()
@click.argument("bundle_path", type=click.Path(), default="_site")
@click.argument("data_path", type=click.Path(exists=True))
def bundle_site(bundle_path: Path, data_path: Path):
    # clean bundle path
    bundle_path = Path(bundle_path)
    if bundle_path.exists():
        shutil.rmtree(bundle_path, ignore_errors=True)

    data_path = Path(data_path)

    # get master config
    config_path = data_path / settings.CONFIG_FILE
    master_config = yaml.safe_load(open(config_path))

    # get list of folders under content path
    content_path = data_path / settings.CONTENT_FOLDER
    content_folders = [
        f.relative_to(content_path) for f in content_path.iterdir() if f.is_dir()
    ]
    content_folders.insert(0, "")  # add root content folder

    # build html files
    for _folder in content_folders:
        build_content(bundle_path, data_path, _folder, master_config)

    # add static files
    static_path = data_path / settings.STATIC_FOLDER
    shutil.copytree(str(static_path), str(bundle_path), dirs_exist_ok=True)


if __name__ == "__main__":
    bundle_site()
