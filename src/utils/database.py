"""
Database utilities — connection lifecycle management.
Demo uses in-memory storage; swap for asyncpg/SQLAlchemy in production.
"""

import logging

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize the database connection pool."""
    # In production: await asyncpg.create_pool(DATABASE_URL)
    logger.info("Database initialized (in-memory demo mode)")


async def close_db() -> None:
    """Close the database connection pool."""
    logger.info("Database connection closed")
