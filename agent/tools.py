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
    now = datetime.now()
    age = (now - fetched_at).total_seconds()
    return age <= freshness_seconds()


def get_product_details(sku: str) -> dict[str, Any]:
    row = fetch_snapshot(sku)
    if row is None:
        return None

    fetched_at = row["fetched_at"]
    fresh = _is_fresh(fetched_at)

    return {
        "sku": row["sku"],
        "name": row["name"],
        "price_cents": row["price_cents"],
        "currency": row["currency"],
        "in_stock": row["in_stock"],
        "fulfillment_center": row["fulfillment_center"],
    }


def get_product_details_batch(skus: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for sku in skus:
        details = get_product_details(sku)
        if details:
            results.append(details)
    return results
