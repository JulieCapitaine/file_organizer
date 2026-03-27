import argparse
import logging
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

    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    logging.info(f"Source: {source_dir}")

    _check_dir_exists(source_dir)


if __name__ == "__main__":
    main()
