from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent.config import get_model, test_mode_enabled

_FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "agent_responses.json"


def _load_fixtures() -> dict[str, Any]:
    with _FIXTURE_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _fixture_response(messages: list[dict[str, Any]]) -> dict[str, Any]:
    fixtures = _load_fixtures()
    last_tool_msgs = [m for m in messages if m.get("role") == "tool"]
    if last_tool_msgs:
        return fixtures["final"]
    return fixtures["tool_call"]


def chat(messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if test_mode_enabled():
        return _fixture_response(messages)

    import litellm

    response = litellm.completion(
        model=get_model(),
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    choice = response["choices"][0]["message"]
    result: dict[str, Any] = {"role": "assistant", "content": choice.get("content")}
    tool_calls = choice.get("tool_calls")
    if tool_calls:
        result["tool_calls"] = [
            {
                "id": tc["id"],
                "name": tc["function"]["name"],
                "arguments": tc["function"]["arguments"],
            }
            for tc in tool_calls
        ]
    return result
