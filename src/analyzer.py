#!/usr/bin/env python3
"""Inspect basic file properties for reverse engineering."""

import argparse
import hashlib
from pathlib import Path
from typing import Any, Dict, Union


class AnalysisError(Exception):
    """Raised when a file cannot be analyzed."""


def analyze_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Return basic information about a regular file."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise AnalysisError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise AnalysisError(f"Not a regular file: {file_path}")

    sha256 = hashlib.sha256()

    try:
        with file_path.open("rb") as file:
            header = file.read(16)
            sha256.update(header)

            for chunk in iter(lambda: file.read(8192), b""):
                sha256.update(chunk)
    except OSError as error:
        raise AnalysisError(
            f"Unable to read file: {file_path}"
        ) from error

    return {
        "name": file_path.name,
        "size_bytes": file_path.stat().st_size,
        "sha256": sha256.hexdigest(),
        "header_hex": header.hex(" "),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect basic properties of a file."
    )
    parser.add_argument("file", help="Path to the file to analyze")
    args = parser.parse_args()

    try:
        result = analyze_file(Path(args.file))
    except AnalysisError as error:
        parser.error(str(error))

    print("=== File Analysis Report ===")
    print(f"File name : {result['name']}")
    print(f"Size      : {result['size_bytes']} bytes")
    print(f"SHA-256   : {result['sha256']}")
    print(f"Header    : {result['header_hex'] or '(empty file)'}")


if __name__ == "__main__":
    main()