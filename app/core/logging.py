"""Logging setup.

Called once from app/main.py. Modules get their own logger with:

    import logging
    logger = logging.getLogger(__name__)

Set EMBED_LOG_LEVEL=debug to see per-request details while debugging.
"""

import logging

from app.core.config import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    )
