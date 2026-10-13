from __future__ import annotations

from flask import Flask, jsonify, request

from agent.orchestrator import run_comparison

app = Flask(__name__)


@app.post("/api/agent/compare")
def compare():
    payload = request.get_json(force=True) or {}
    message = payload.get("message", "")
    if not message:
        return jsonify({"error": "message is required"}), 400
    result = run_comparison(message)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
