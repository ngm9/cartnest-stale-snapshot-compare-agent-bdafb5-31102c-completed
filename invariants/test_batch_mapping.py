from __future__ import annotations

from agent.tools import get_product_details_batch


def test_batch_returns_one_result_per_sku_in_order():
    skus = ["BIN-3001", "DRW-5150", "SHELF-7742"]
    results = get_product_details_batch(skus)
    assert len(results) == len(skus), "every requested SKU must produce exactly one result"
    returned_skus = [r.get("sku") for r in results]
    assert returned_skus == skus, "results must stay aligned to requested SKUs"


def test_batch_preserves_status_per_sku():
    skus = ["BIN-3001", "DRW-5150", "SHELF-7742"]
    by_sku = {r["sku"]: r for r in get_product_details_batch(skus)}
    assert by_sku["BIN-3001"]["status"] == "fresh"
    assert by_sku["DRW-5150"]["status"] == "missing"
    assert by_sku["SHELF-7742"]["status"] == "stale"
