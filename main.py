import argparse
import logging
import shutil
import sys
from pathlib import Path

EXTENSION_CATEGORIES = {
    'images': {'.jpg', '.jpeg', '.png'},
    'docs': {'.pdf', '.doc', '.docx', '.txt', '.md', '.log'},
    'data': {'.csv', '.json', '.xml'},
}


def _check_dir_exists(directory: Path) -> None:
    """
    Checks if the directory exists. If not, logs an error and exits the program.

    Args:
        directory: The path of the directory to check.
    """
    if not directory.is_dir():
        logging.error(f"Source folder '{directory}' does not exist.")
        sys.exit(1)


def _prepare_destination_dir(dest_dir: Path) -> None:
    """
    Delete the destination directory if it exists, then recreates it empty.

    Args:
        dest_dir: The destination directory to prepare.
    """
    if dest_dir.exists():
        try:
            shutil.rmtree(dest_dir)
            logging.info(f"Destination folder {dest_dir} removed.")
        except Exception as e:
            logging.error(f"Failed to remove folder {dest_dir}: {e}")
            sys.exit(1)
    dest_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Destination folder {dest_dir} created.")


def _create_category_folders(dest_dir: Path) -> dict[str, Path]:
    """
    Create subfolders in the destination directory for all categories.

    Args:
        dest_dir: The root destination folder.

    Returns:
        A dict mapping each category name to its corresponding folder path.
    """
    categories = {cat: dest_dir / cat for cat in EXTENSION_CATEGORIES}
    categories["others"] = dest_dir / "others"

    for folder in categories.values():
        folder.mkdir(exist_ok=True)

    return categories


def _get_category(extension: str) -> str:
    """
    Return the category name for a given file extension.

    Args:
        extension: The file extension (e.g. ".txt").

    Returns:
        The matching category name, or 'others' if no category matches.
    """
    ext = extension.lower()
    for category, extensions in EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'others'


def _copy_files_to_subfolders(source_dir: Path, category_dirs: dict[str, Path]) -> None:
    """
    Copy all files from the source folder into the appropriate category folders.

    Args:
        source_dir: Folder where the source files are located.
        category_dirs: Mapping of category name -> destination folder path.
    """
    for file in source_dir.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            category = _get_category(ext)

            dest = category_dirs[category] / file.name

            try:
                shutil.copy2(file, dest)
                logging.info(f"Copied {file} -> {dest}")
            except Exception as e:
                logging.error(f"Failed to copy {file}: {e}")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    parser = argparse.ArgumentParser(description="Organize files, clean .txt files, and generate a complete report.")
    parser.add_argument('--source',
                        type=str,
                        default='inbox/',
                        help='Source folder for files to organize (default: inbox/)')
    parser.add_argument('--destination',
                        type=str,
                        default='output/',
                        help='Destination folder for organized files (default: output/)')

    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    logging.info(f"Source: {source_dir}")

    dest_dir = Path(args.destination).resolve()
    logging.info(f"Destination: {dest_dir}")

    _check_dir_exists(source_dir)
    _prepare_destination_dir(dest_dir)

    subfolders = _create_category_folders(dest_dir)
    _copy_files_to_subfolders(source_dir, subfolders)


if __name__ == "__main__":
    main()
