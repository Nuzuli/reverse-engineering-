#!/usr/bin/env python3
"""
Analyze basic file properties for reverse engineering.

This script does not execute the file being analyzed.
"""

import argparse
import hashlib
from pathlib import Path


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def analyze_file(file_path):
    """Return basic information about a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Not a regular file: {file_path}")

    with file_path.open("rb") as file:
        header = file.read(16)

    return {
        "name": file_path.name,
        "size_bytes": file_path.stat().st_size,
        "sha256": calculate_sha256(file_path),
        "header_hex": header.hex(" "),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Inspect basic properties of a file safely."
    )
    parser.add_argument("file", help="Path to the file to analyze")
    args = parser.parse_args()

    try:
        result = analyze_file(Path(args.file))
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("=== File Analysis Report ===")
    print(f"File name : {result['name']}")
    print(f"Size      : {result['size_bytes']} bytes")
    print(f"SHA-256   : {result['sha256']}")
    print(f"Header    : {result['header_hex'] or '(empty file)'}")


if __name__ == "__main__":
    main()