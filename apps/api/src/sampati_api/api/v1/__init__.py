# SPDX-License-Identifier: Apache-2.0
"""API v1 routes."""

from fastapi import APIRouter

from . import auth, organisations, frameworks, controls, evidence, evidence_requests, plugins, tasks, audit

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(organisations.router, prefix="/organisations", tags=["organisations"])
router.include_router(frameworks.router, prefix="/frameworks", tags=["frameworks"])
router.include_router(controls.router, prefix="/controls", tags=["controls"])
router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
router.include_router(evidence_requests.router, prefix="/evidence-requests", tags=["evidence-requests"])
router.include_router(plugins.router, prefix="/plugins", tags=["plugins"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(audit.router, prefix="/audit", tags=["audit"])
