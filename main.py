import argparse
import logging
import shutil
import sys
from datetime import date
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


def _copy_files_to_subfolders(source_dir: Path, category_dirs: dict[str, Path]) -> dict[str, int]:
    """
    Copy all files from the source folder into the appropriate category folders.

    Args:
        source_dir: Folder where the source files are located.
        category_dirs: Mapping of category name -> destination folder path.

    Returns:
        Dict with category -> file count
    """
    counts = {cat: 0 for cat in category_dirs}

    for file in source_dir.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            category = _get_category(ext)
            dest = category_dirs[category] / file.name

            try:
                shutil.copy2(file, dest)
                logging.info(f"Copied {file} -> {dest}")
                counts[category] += 1
            except Exception as e:
                logging.error(f"Failed to copy {file}: {e}")

    return counts


def _clean_txt_files(dir: Path) -> list[Path]:
    """
    Clean all .txt files inside the destination directory:
    - remove empty lines
    - strip leading/trailing spaces

    Args:
        dir: Folder where .txt files are located.

    Returns:
        List of cleaned .txt file paths.
    """
    cleaned = []

    for txt_file in dir.rglob("*.txt"):
        try:
            with txt_file.open("r", encoding="utf-8") as f:
                cleaned_lines = [
                    line.strip()
                    for line in f
                    if line.strip()  # skip empty lines
                ]

            with txt_file.open("w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_lines))

            logging.info(f"Cleaned {txt_file}")
            cleaned.append(txt_file.relative_to(dir))

        except Exception as e:
            logging.error(f"Failed to clean {txt_file}: {e}")

    return cleaned


def _generate_report(dest_dir: Path,
                     files_per_category: dict[str, int],
                     cleaned_txt_files: list[Path] | None) -> None:
    """
    Generate the final report file in the destination folder.

    Args:
        dest_dir: Folder where the report will be created.
        files_per_category: Counts of files per category.
        cleaned_txt_files: List of cleaned .txt files (or None if cleaning disabled).

    Returns:
        None
    """
    today = date.today().isoformat()
    report_path = dest_dir / f"report_{today}.txt"

    try:
        with report_path.open("w", encoding="utf-8") as f:
            f.write("=== File Organizer Report ===\n\n")
            f.write(f"Total files processed: {sum(files_per_category.values())}\n\n")

            f.write("Files per category:\n")
            for cat, count in files_per_category.items():
                f.write(f"- {cat}: {count}\n")

            f.write("\n")

            if cleaned_txt_files is not None:
                f.write("Cleaned .txt files:\n")
                for path in cleaned_txt_files:
                    f.write(f"- {path}\n")

        logging.info(f"Report generated: {report_path}")

    except Exception as e:
        logging.error(f"Failed to generate report: {e}")


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
    parser.add_argument('--clean',
                        action='store_true',
                        help='Clean .txt files')

    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    logging.info(f"Source: {source_dir}")

    dest_dir = Path(args.destination).resolve()
    logging.info(f"Destination: {dest_dir}")

    logging.info(f"Clean .txt files: {args.clean}")

    _check_dir_exists(source_dir)
    _prepare_destination_dir(dest_dir)

    subfolders = _create_category_folders(dest_dir)
    files_per_category = _copy_files_to_subfolders(source_dir, subfolders)

    cleaned_txt_files = None
    if args.clean:
        cleaned_txt_files = _clean_txt_files(dest_dir)

    _generate_report(dest_dir, files_per_category, cleaned_txt_files)


if __name__ == "__main__":
    main()
