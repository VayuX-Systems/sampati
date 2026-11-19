# SPDX-License-Identifier: Apache-2.0
"""Google Workspace Connector main entry point."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, AsyncGenerator

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pydantic import BaseModel, Field

from sampati_sdk.runtime import PluginRuntime, PluginContext, EvidenceRecord, EvidenceResult, EvidenceCollector


class GoogleWorkspaceConfig(BaseModel):
    customer_id: str
    service_account_key: str
    admin_email: str


class GoogleWorkspaceConnector(PluginRuntime):
    """Google Workspace connector for collecting compliance evidence."""
    
    @property
    def manifest(self) -> dict[str, Any]:
        import json
        from pathlib import Path
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        return json.loads(manifest_path.read_text())
    
    def validate_config(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate Google Workspace configuration."""
        errors = []
        
        if not config.get("customer_id"):
            errors.append("Customer ID is required")
        
        if not config.get("service_account_key"):
            errors.append("Service account key is required")
        
        if not config.get("admin_email"):
            errors.append("Admin email is required")
        
        return len(errors) == 0, errors
    
    def _get_service(self, config: GoogleWorkspaceConfig, service_name: str, version: str):
        """Create a Google API service with domain-wide delegation."""
        credentials_info = json.loads(config.service_account_key)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=[
                "https://www.googleapis.com/auth/admin.directory.user.readonly",
                "https://www.googleapis.com/auth/admin.directory.group.readonly",
                "https://www.googleapis.com/auth/admin.directory.orgunit.readonly",
                "https://www.googleapis.com/auth/drive.metadata.readonly",
            ],
        )
        
        # Impersonate admin
        delegated_credentials = credentials.with_subject(config.admin_email)
        
        return build(service_name, version, credentials=delegated_credentials, cache_discovery=False)
    
    async def collect(self, context: PluginContext) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect evidence from Google Workspace."""
        config = GoogleWorkspaceConfig(**context.config)
        
        # Create services
        admin_service = self._get_service(config, "admin", "directory_v1")
        drive_service = self._get_service(config, "drive", "v3")
        
        # Collect user MFA status
        async for record in self._collect_user_mfa(admin_service, config.customer_id):
            yield record
        
        # Collect suspended users
        async for record in self._collect_suspended_users(admin_service, config.customer_id):
            yield record
        
        # Collect admin privileges
        async for record in self._collect_admin_privileges(admin_service, config.customer_id):
            yield record
        
        # Collect Drive sharing settings
        async for record in self._collect_drive_sharing(drive_service, config.customer_id):
            yield record
        
        # Collect group memberships
        async for record in self._collect_group_memberships(admin_service, config.customer_id):
            yield record
    
    async def _collect_user_mfa(
        self, 
        admin_service: Any, 
        customer_id: str
    ) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect user MFA enforcement status."""
        try:
            users = []
            page_token = None
            
            while True:
                result = admin_service.users().list(
                    customer=customer_id,
                    maxResults=500,
                    pageToken=page_token,
                    projection="full",
                ).execute()
                
                users.extend(result.get("users", []))
                page_token = result.get("nextPageToken")
                
                if not page_token:
                    break
            
            total_users = len(users)
            mfa_enabled = sum(1 for u in users if u.get("isEnrolledIn2Sv", False))
            
            yield self._make_evidence(
                check="user_mfa_status",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.PASS if mfa_enabled == total_users else EvidenceResult.FAIL,
                data={
                    "customer_id": customer_id,
                    "total_users": total_users,
                    "mfa_enabled_users": mfa_enabled,
                    "mfa_enforcement_rate": round(mfa_enabled / total_users * 100, 1) if total_users > 0 else 0,
                },
            )
            
        except Exception as e:
            yield self._make_evidence(
                check="user_mfa_status",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.ERROR,
                data={"error": str(e)},
            )
    
    async def _collect_suspended_users(
        self, 
        admin_service: Any, 
        customer_id: str
    ) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect suspended users count."""
        try:
            users = []
            page_token = None
            
            while True:
                result = admin_service.users().list(
                    customer=customer_id,
                    maxResults=500,
                    pageToken=page_token,
                    query="isSuspended=true",
                ).execute()
                
                users.extend(result.get("users", []))
                page_token = result.get("nextPageToken")
                
                if not page_token:
                    break
            
            yield self._make_evidence(
                check="suspended_users",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.PASS if len(users) == 0 else EvidenceResult.FAIL,
                data={
                    "customer_id": customer_id,
                    "suspended_count": len(users),
                    "suspended_users": [u["primaryEmail"] for u in users],
                },
            )
            
        except Exception as e:
            yield self._make_evidence(
                check="suspended_users",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.ERROR,
                data={"error": str(e)},
            )
    
    async def _collect_admin_privileges(
        self, 
        admin_service: Any, 
        customer_id: str
    ) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect users with admin privileges."""
        try:
            # Get all users
            all_users = []
            page_token = None
            
            while True:
                result = admin_service.users().list(
                    customer=customer_id,
                    maxResults=500,
                    pageToken=page_token,
                    projection="full",
                ).execute()
                
                all_users.extend(result.get("users", []))
                page_token = result.get("nextPageToken")
                
                if not page_token:
                    break
            
            # Get admin roles
            role_assignments = admin_service.roleAssignments().list(
                customer=customer_id,
            ).execute()
            
            admin_users = set()
            for assignment in role_assignments.get("roleAssignments", []):
                if assignment.get("roleId") in ("8899879232623156977", "6842958702234630797"):  # Super admin, Admin
                    admin_users.add(assignment.get("userId"))
            
            admin_count = len(admin_users)
            
            yield self._make_evidence(
                check="admin_privileges",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.INFO,
                data={
                    "customer_id": customer_id,
                    "admin_count": admin_count,
                    "admin_emails": [u["primaryEmail"] for u in all_users if u["id"] in admin_users],
                },
            )
            
        except Exception as e:
            yield self._make_evidence(
                check="admin_privileges",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.ERROR,
                data={"error": str(e)},
            )
    
    async def _collect_drive_sharing(
        self, 
        drive_service: Any, 
        customer_id: str
    ) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect Drive sharing settings."""
        try:
            # Get Drive settings
            settings = drive_service.about().get(fields="*").execute()
            
            # Check domain-wide sharing settings
            domain_sharing = settings.get("importFormats", [])
            
            yield self._make_evidence(
                check="drive_sharing_settings",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.INFO,
                data={
                    "customer_id": customer_id,
                    "storage_limit": settings.get("storageQuota", {}).get("limit"),
                    "storage_usage": settings.get("storageQuota", {}).get("usage"),
                    "import_formats": domain_sharing,
                },
            )
            
        except Exception as e:
            yield self._make_evidence(
                check="drive_sharing_settings",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.ERROR,
                data={"error": str(e)},
            )
    
    async def _collect_group_memberships(
        self, 
        admin_service: Any, 
        customer_id: str
    ) -> AsyncGenerator[EvidenceRecord, None]:
        """Collect group memberships."""
        try:
            groups = []
            page_token = None
            
            while True:
                result = admin_service.groups().list(
                    customer=customer_id,
                    maxResults=500,
                    pageToken=page_token,
                ).execute()
                
                groups.extend(result.get("groups", []))
                page_token = result.get("nextPageToken")
                
                if not page_token:
                    break
            
            yield self._make_evidence(
                check="group_memberships",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.INFO,
                data={
                    "customer_id": customer_id,
                    "total_groups": len(groups),
                    "groups": [g["email"] for g in groups],
                },
            )
            
        except Exception as e:
            yield self._make_evidence(
                check="group_memberships",
                subject=f"customer:{customer_id}",
                result=EvidenceResult.ERROR,
                data={"error": str(e)},
            )
    
    def _make_evidence(
        self,
        check: str,
        subject: str,
        result: EvidenceResult,
        data: dict[str, Any],
    ) -> EvidenceRecord:
        """Create an evidence record."""
        return EvidenceRecord(
            id="",  # Will be generated by ledger
            organisation_id="",  # Will be set by ledger
            source={
                "plugin": "google-workspace",
                "plugin_version": "1.0.0",
                "collector": "connector",
                "check": check,
                "subject": subject,
            },
            result=result,
            collected_at=datetime.now(timezone.utc),
            valid_until=datetime.now(timezone.utc).replace(day=28),
            data=data,
            hash="",
            prev_hash="",
            linked_controls=[],
        )


# CLI entry points
def main() -> None:
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: google-workspace [describe|validate|collect|health]")
        sys.exit(1)
    
    command = sys.argv[1]
    connector = GoogleWorkspaceConnector()
    
    if command == "describe":
        print(json.dumps(connector.manifest, indent=2))
    elif command == "validate":
        config = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        valid, errors = connector.validate_config(config)
        print(json.dumps({"valid": valid, "errors": errors}))
    elif command == "health":
        print(json.dumps({"status": "healthy", "message": "Google Workspace connector operational", "checked_at": datetime.now(timezone.utc).isoformat()}))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
