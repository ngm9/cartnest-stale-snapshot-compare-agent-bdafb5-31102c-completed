from __future__ import annotations

import sys

from agent.config import test_mode_enabled
from agent.tools import TOOL_SCHEMAS


def _selfcheck() -> int:
    assert TOOL_SCHEMAS, "tool schemas must be defined"
    names = {t["function"]["name"] for t in TOOL_SCHEMAS}
    assert "get_product_details" in names, "get_product_details tool must exist"
    print(f"selfcheck ok (test_mode={test_mode_enabled()})")
    return 0


def main(argv: list[str]) -> int:
    if "--selfcheck" in argv:
        return _selfcheck()
    print("usage: python -m agent --selfcheck")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
