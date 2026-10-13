from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row

from agent.config import get_database_url


def get_connection() -> psycopg.Connection:
    return psycopg.connect(get_database_url(), row_factory=dict_row)


def fetch_snapshot(sku: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT sku, name, price_cents, currency, in_stock,
                       fulfillment_center, fetched_at
                FROM product_snapshots
                WHERE sku = %s
                """,
                (sku,),
            )
            return cur.fetchone()
