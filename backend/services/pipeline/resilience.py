"""
Pipeline Resilience & Auto-Retry Module
----------------------------------------
Provides exponential backoff retry wrappers and asset sanity validators
to ensure zero-crash pipeline execution.
"""
from __future__ import annotations

import asyncio
import logging
import functools
from pathlib import Path

logger = logging.getLogger(__name__)


def with_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions=(Exception,)):
    """Decorator that retries an async function with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    logger.warning(f"Attempt {attempt}/{max_retries} for '{func.__name__}' failed: {exc}")
                    if attempt < max_retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            logger.error(f"All {max_retries} attempts failed for '{func.__name__}'. Last error: {last_exception}")
            raise last_exception
        return wrapper
    return decorator


def validate_audio_file(file_path: str) -> bool:
    """Verifies an audio file exists, is non-empty, and has a size > 1KB."""
    if not file_path:
        return False
    path = Path(file_path)
    return path.exists() and path.is_file() and path.stat().st_size > 1024


def validate_media_file(file_path: str) -> bool:
    """Verifies a video or image media file exists and has size > 2KB."""
    if not file_path:
        return False
    path = Path(file_path)
    return path.exists() and path.is_file() and path.stat().st_size > 2048
