from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from agent.config import freshness_seconds
from agent.db import fetch_snapshot

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": (
                "Read-only lookup of current price and availability for a single "
                "CartNest product SKU from the snapshot cache."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "description": "Product SKU, e.g. BIN-3001.",
                    }
                },
                "required": ["sku"],
            },
        },
    }
]


def _is_fresh(fetched_at: datetime) -> bool:
    # fetched_at comes from a TIMESTAMPTZ column, so it is timezone-aware.
    # Compare against an aware "now" in UTC; a naive now() would either raise
    # or silently miscompute the age depending on the local offset.
    now = datetime.now(timezone.utc)
    if fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=timezone.utc)
    age = (now - fetched_at).total_seconds()
    return age <= freshness_seconds()


def get_product_details(sku: str) -> dict[str, Any]:
    """Look up a single SKU and always return a structured, honest result.

    Every result carries a ``status`` of ``fresh``, ``stale`` or ``missing`` so
    the caller/model can tell trustworthy data apart from aged or absent data
    instead of seeing identical-looking rows (or ``None``).
    """
    row = fetch_snapshot(sku)
    if row is None:
        return {
            "sku": sku,
            "status": "missing",
            "name": None,
            "price_cents": None,
            "currency": None,
            "in_stock": None,
            "fulfillment_center": None,
        }

    fresh = _is_fresh(row["fetched_at"])

    return {
        "sku": row["sku"],
        "status": "fresh" if fresh else "stale",
        "name": row["name"],
        "price_cents": row["price_cents"],
        "currency": row["currency"],
        "in_stock": row["in_stock"],
        "fulfillment_center": row["fulfillment_center"],
    }


def get_product_details_batch(skus: list[str]) -> list[dict[str, Any]]:
    # One result per requested SKU, in request order. Missing/stale lookups
    # still produce a structured result so the SKU-to-result mapping never
    # drifts when a lookup ages out or returns nothing.
    return [get_product_details(sku) for sku in skus]
