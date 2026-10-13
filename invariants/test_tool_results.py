from __future__ import annotations

from agent.tools import get_product_details

FRESH_SKU = "BIN-3001"
STALE_SKU = "SHELF-7742"
MISSING_SKU = "DRW-5150"


def _status(result) -> str:
    assert isinstance(result, dict), f"expected structured dict result, got {type(result)}"
    status = result.get("status")
    assert status is not None, "tool result must carry a status field"
    return status


def test_fresh_sku_is_flagged_fresh():
    result = get_product_details(FRESH_SKU)
    assert _status(result) == "fresh"
    assert result.get("in_stock") is True
    assert result.get("price_cents") == 1499


def test_stale_sku_is_flagged_not_fresh():
    result = get_product_details(STALE_SKU)
    assert _status(result) == "stale"


def test_missing_sku_is_structured_not_none():
    result = get_product_details(MISSING_SKU)
    assert result is not None, "missing SKU must return a structured result, not None"
    assert _status(result) == "missing"
    assert result.get("sku") == MISSING_SKU
