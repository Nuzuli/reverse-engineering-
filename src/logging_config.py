"""Optional structured (JSON) logging for the command-line interface."""

import json
import logging
import os
import sys
from typing import IO, Any, Dict, Optional

LOG_LEVEL_ENV = "LOG_LEVEL"
DEFAULT_LEVEL = logging.WARNING
_HANDLER_MARK = "_analyzer_json_handler"


class JsonFormatter(logging.Formatter):
    """Format each log record as a single JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def resolve_level(value: Optional[str]) -> int:
    """Turn a LOG_LEVEL value such as ``debug`` into a logging level."""
    if not value:
        return DEFAULT_LEVEL
    level = logging.getLevelName(value.strip().upper())
    return level if isinstance(level, int) else DEFAULT_LEVEL


def configure_logging(
    level: Optional[int] = None, stream: Optional[IO[str]] = None
) -> logging.Handler:
    """Send JSON log lines to ``stream`` (default stderr) and return the handler.

    The level defaults to ``$LOG_LEVEL`` (or WARNING). Calling this again
    replaces the handler installed earlier instead of adding a second one.
    """
    if level is None:
        level = resolve_level(os.environ.get(LOG_LEVEL_ENV))
    root = logging.getLogger()
    for existing in list(root.handlers):
        if getattr(existing, _HANDLER_MARK, False):
            root.removeHandler(existing)
    handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
    handler.setFormatter(JsonFormatter())
    setattr(handler, _HANDLER_MARK, True)
    root.addHandler(handler)
    root.setLevel(level)
    return handler