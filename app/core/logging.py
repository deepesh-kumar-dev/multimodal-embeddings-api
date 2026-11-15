"""Logging setup.

Called once from ``app/main.py``. Every other module gets its own logger::

    import logging

    logger: logging.Logger = logging.getLogger(__name__)

Set ``EMBED_LOG_LEVEL=debug`` to see per-request details while debugging.
"""

import logging
from typing import Final

from app.core.config import settings

LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
"""Format of every log line: time, level, logger name (module path), message."""


def setup_logging() -> None:
    """Configure the root logger from ``settings.log_level``.

    Safe to call more than once: ``logging.basicConfig`` does nothing if the root
    logger already has handlers.
    """
    logging.basicConfig(level=settings.log_level.upper(), format=LOG_FORMAT)
