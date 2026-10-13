from __future__ import annotations

from agent.orchestrator import run_comparison


def test_comparison_keeps_all_requested_skus():
    result = run_comparison("compare BIN-3001, DRW-5150 and SHELF-7742")
    assert set(result["skus"]) == {"BIN-3001", "DRW-5150", "SHELF-7742"}
    tool_results = result["tool_results"]
    for sku in ["BIN-3001", "DRW-5150", "SHELF-7742"]:
        assert sku in tool_results, f"{sku} missing from tool_results"
        assert isinstance(tool_results[sku], dict)
        assert tool_results[sku].get("status") in {"fresh", "stale", "missing"}


def test_missing_sku_not_dropped_from_tool_results():
    result = run_comparison("compare BIN-3001 and DRW-5150")
    assert result["tool_results"]["DRW-5150"].get("status") == "missing"
