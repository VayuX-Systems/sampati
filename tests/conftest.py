# SPDX-License-Identifier: Apache-2.0
"""Pytest configuration for Sampati tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Set test environment variables
os.environ["SAMPATI_ENV"] = "test"
os.environ["SAMPATI_DATABASE_URL"] = "postgresql+asyncpg://sampati:sampati@localhost:5432/sampati_test"
os.environ["SAMPATI_REDIS_URL"] = "redis://localhost:6379/0"
os.environ["SAMPATI_SECRET_KEY"] = "test-secret-key"
os.environ["SAMPATI_BASE_URL"] = "http://localhost:8000"

import pytest_asyncio

# Pytest-asyncio configuration
pytest_asyncio.plugin.auto_mode = True
