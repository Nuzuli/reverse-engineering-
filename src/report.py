"""Format analysis results as a plain-text report."""

from typing import Any, Mapping

REQUIRED_KEYS = ("name", "size_bytes", "sha256", "header_hex")


def format_report(result: Mapping[str, Any]) -> str:
    """Render an analysis result as a readable report.

    Raises ValueError when the result is missing required keys.
    """
    missing = [key for key in REQUIRED_KEYS if key not in result]
    if missing:
        raise ValueError(f"Result is missing keys: {', '.join(missing)}")

    header = result["header_hex"] or "(empty file)"
    lines = [
        "=== File Analysis Report ===",
        f"File name : {result['name']}",
        f"Size      : {result['size_bytes']} bytes",
        f"SHA-256   : {result['sha256']}",
        f"Header    : {header}",
    ]
    return "\n".join(lines)