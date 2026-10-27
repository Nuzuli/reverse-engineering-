#!/usr/bin/env python3
"""Inspect basic file properties for reverse engineering."""

import argparse
import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, Union

from src.report import format_json, format_report

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Raised when a file cannot be analyzed."""


class FileNotFoundAnalysisError(AnalysisError):
    """Raised when the path does not exist."""


class NotARegularFileError(AnalysisError):
    """Raised when the path exists but is not a regular file."""


class FileReadError(AnalysisError):
    """Raised when a regular file cannot be read."""


def analyze_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Return basic information about a regular file."""
    file_path = Path(file_path)
    logger.info("analyze_start path=%s", file_path)

    if not file_path.exists():
        logger.debug("analyze_rejected path=%s reason=file_not_found", file_path)
        raise FileNotFoundAnalysisError(f"File not found: {file_path}")

    if not file_path.is_file():
        logger.debug("analyze_rejected path=%s reason=not_a_regular_file", file_path)
        raise NotARegularFileError(f"Not a regular file: {file_path}")

    sha256 = hashlib.sha256()

    try:
        with file_path.open("rb") as file:
            header = file.read(16)
            sha256.update(header)

            for chunk in iter(lambda: file.read(8192), b""):
                sha256.update(chunk)
    except OSError as error:
        logger.debug("analyze_failed path=%s error=%s", file_path, error)
        raise FileReadError(
            f"Unable to read file: {file_path}"
        ) from error

    size = file_path.stat().st_size
    logger.info("analyze_done name=%s size_bytes=%d", file_path.name, size)

    return {
        "name": file_path.name,
        "size_bytes": size,
        "sha256": sha256.hexdigest(),
        "header_hex": header.hex(" "),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect basic properties of a file."
    )
    parser.add_argument("file", help="Path to the file to analyze")
    parser.add_argument(
        "--json", action="store_true", help="Print the result as JSON"
    )
    args = parser.parse_args()

    try:
        result = analyze_file(Path(args.file))
    except AnalysisError as error:
        parser.error(str(error))

    print(format_json(result) if args.json else format_report(result))


if __name__ == "__main__":
    main()