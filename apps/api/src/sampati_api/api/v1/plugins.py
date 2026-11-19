# SPDX-License-Identifier: Apache-2.0
"""Plugins API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement plugins routes for MVP

@router.get("")
async def list_plugins():
    """List plugins."""
    return {"message": "plugins endpoint - implementation in progress"}
