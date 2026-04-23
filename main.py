import argparse
import logging
import shutil
import sys
from pathlib import Path


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


if __name__ == "__main__":
    main()
