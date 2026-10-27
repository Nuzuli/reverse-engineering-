"""Format analysis results as text or JSON."""

import json
from typing import Any, Mapping

REQUIRED_KEYS = ("name", "size_bytes", "sha256", "header_hex")


def _require_keys(result: Mapping[str, Any]) -> None:
    missing = [key for key in REQUIRED_KEYS if key not in result]
    if missing:
        raise ValueError(f"Result is missing keys: {', '.join(missing)}")


def format_report(result: Mapping[str, Any]) -> str:
    """Render an analysis result as a readable report.

    Raises ValueError when the result is missing required keys.
    """
    _require_keys(result)

    header = result["header_hex"] or "(empty file)"
    lines = [
        "=== File Analysis Report ===",
        f"File name : {result['name']}",
        f"Size      : {result['size_bytes']} bytes",
        f"SHA-256   : {result['sha256']}",
        f"Header    : {header}",
    ]
    return "\n".join(lines)


def format_json(result: Mapping[str, Any]) -> str:
    """Render an analysis result as pretty-printed JSON.

    Raises ValueError when the result is missing required keys.
    """
    _require_keys(result)
    return json.dumps({key: result[key] for key in REQUIRED_KEYS}, indent=2)