# SPDX-License-Identifier: Apache-2.0
"""Sampati Evidence Ledger CLI - verify, export, and manage ledger."""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone

import click
from rich.console import Console
from rich.table import Table

from sampati_core_domain.models import Organisation
from sampati_api.database import init_db, get_tenant_session
from sampati_ledger.service import EvidenceLedger
from sampati_ledger.models import EvidenceCollector, EvidenceResult

console = Console()


@click.group()
@click.option("--org-id", required=True, help="Organisation ID")
@click.pass_context
def main(ctx: click.Context, org_id: str) -> None:
    """Sampati Evidence Ledger CLI."""
    ctx.ensure_object(dict)
    ctx.obj["org_id"] = org_id


@main.command()
@click.pass_context
def verify(ctx: click.Context) -> None:
    """Verify the integrity of the evidence ledger hash chain."""
    org_id = ctx.obj["org_id"]
    
    async def _verify():
        await init_db()
        async with get_tenant_session(org_id) as session:
            ledger = EvidenceLedger(session)
            is_valid, errors = await ledger.verify_chain(org_id)
            
            if is_valid:
                console.print("[green]✓ Ledger chain is valid[/green]")
            else:
                console.print("[red]✗ Ledger chain verification failed[/red]")
                for error in errors:
                    console.print(f"  [red]• {error}[/red]")
                sys.exit(1)
    
    asyncio.run(_verify())


@main.command()
@click.option("--limit", default=20, help="Number of records to show")
@click.option("--check", help="Filter by check name")
@click.option("--result", type=click.Choice(["pass", "fail", "error", "info"]), help="Filter by result")
@click.pass_context
def list(ctx: click.Context, limit: int, check: str | None, result: str | None) -> None:
    """List evidence records."""
    org_id = ctx.obj["org_id"]
    
    async def _list():
        await init_db()
        async with get_tenant_session(org_id) as session:
            ledger = EvidenceLedger(session)
            records = await ledger.get_records(
                organisation_id=org_id,
                limit=limit,
                check=check,
                result=EvidenceResult(result) if result else None,
            )
            
            table = Table(title=f"Evidence Records (org: {org_id})")
            table.add_column("ID", style="dim")
            table.add_column("Check")
            table.add_column("Subject")
            table.add_column("Result")
            table.add_column("Collected At")
            table.add_column("Valid Until")
            
            for r in records:
                table.add_row(
                    r.id[:8] + "...",
                    r.check,
                    r.subject[:40] + "..." if len(r.subject) > 40 else r.subject,
                    f"[{_result_color(r.result)}]{r.result.value}[/]",
                    r.collected_at.strftime("%Y-%m-%d %H:%M"),
                    r.valid_until.strftime("%Y-%m-%d %H:%M") if r.valid_until else "—",
                )
            
            console.print(table)
    
    asyncio.run(_list())


@main.command()
@click.pass_context
def latest_hash(ctx: click.Context) -> None:
    """Get the latest hash in the chain."""
    org_id = ctx.obj["org_id"]
    
    async def _hash():
        await init_db()
        async with get_tenant_session(org_id) as session:
            ledger = EvidenceLedger(session)
            hash_val = await ledger.get_latest_hash(org_id)
            console.print(f"Latest hash: {hash_val}")
    
    asyncio.run(_hash())


@main.command()
@click.argument("record_id")
@click.pass_context
def show(ctx: click.Context, record_id: str) -> None:
    """Show a single evidence record."""
    org_id = ctx.obj["org_id"]
    
    async def _show():
        await init_db()
        async with get_tenant_session(org_id) as session:
            ledger = EvidenceLedger(session)
            record = await ledger.get_record(record_id, org_id)
            
            if not record:
                console.print(f"[red]Record {record_id} not found[/red]")
                sys.exit(1)
            
            console.print_json(json.dumps({
                "id": record.id,
                "organisation_id": record.organisation_id,
                "source_plugin": record.source_plugin,
                "plugin_version": record.plugin_version,
                "collector": record.collector.value,
                "check": record.check,
                "subject": record.subject,
                "result": record.result.value,
                "collected_at": record.collected_at.isoformat(),
                "valid_until": record.valid_until.isoformat() if record.valid_until else None,
                "data": record.data,
                "hash": record.hash,
                "prev_hash": record.prev_hash,
                "linked_controls": record.linked_controls,
            }, indent=2))
    
    asyncio.run(_show())


def _result_color(result: EvidenceResult) -> str:
    colors = {
        EvidenceResult.PASS: "green",
        EvidenceResult.FAIL: "red",
        EvidenceResult.ERROR: "yellow",
        EvidenceResult.INFO: "blue",
    }
    return colors.get(result, "white")


if __name__ == "__main__":
    main()
