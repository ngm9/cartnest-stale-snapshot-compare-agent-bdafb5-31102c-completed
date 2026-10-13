from __future__ import annotations

import json
import logging
import re
from typing import Any

from agent.config import get_model
from agent.llm_client import chat
from agent.tools import TOOL_SCHEMAS, get_product_details

logger = logging.getLogger("cartnest.compare")

SYSTEM_PROMPT = (
    "You are CartNest's product comparison assistant. "
    "Use the get_product_details tool to look up price and availability for each SKU "
    "the shopper mentions. Only state prices and availability that the tool returns. "
    "If a tool result indicates data is not fresh or is unavailable, say so plainly "
    "and do not present it as a confirmed current fact. "
    "Keep each product's numbers attributed to its own SKU."
)

_SKU_PATTERN = re.compile(r"[A-Z]{2,5}-\d{3,5}")


def extract_skus(message: str) -> list[str]:
    seen: list[str] = []
    for match in _SKU_PATTERN.findall(message.upper()):
        if match not in seen:
            seen.append(match)
    return seen


def _dispatch_tool_call(name: str, arguments: str) -> dict[str, Any]:
    args = json.loads(arguments) if isinstance(arguments, str) else arguments
    if name == "get_product_details":
        return get_product_details(args["sku"])
    raise ValueError(f"Unknown tool: {name}")


def run_comparison(user_message: str) -> dict[str, Any]:
    skus = extract_skus(user_message)
    tool_results: dict[str, Any] = {}
    for sku in skus:
        tool_results[sku] = get_product_details(sku)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": f"call_{i}",
                    "type": "function",
                    "function": {
                        "name": "get_product_details",
                        "arguments": json.dumps({"sku": sku}),
                    },
                }
                for i, sku in enumerate(skus)
            ],
        },
    ]
    for i, sku in enumerate(skus):
        messages.append(
            {
                "role": "tool",
                "tool_call_id": f"call_{i}",
                "name": "get_product_details",
                "content": json.dumps(tool_results[sku]),
            }
        )

    model_reply = chat(messages, tools=TOOL_SCHEMAS)
    logger.info("comparison synthesized for skus=%s model=%s", skus, get_model())

    return {
        "skus": skus,
        "tool_results": tool_results,
        "summary": model_reply.get("content"),
    }
