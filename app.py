from uuid import uuid4

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.get("/v2/health")
def health():
    return jsonify(status="healthy")


@app.post("/v2/chat")
def chat():
    payload = request.get_json(silent=True)
    conversation_id = payload.get("conversation_id") if isinstance(payload, dict) else None
    if not isinstance(conversation_id, str) or not conversation_id:
        conversation_id = f"session-{uuid4().hex}"

    return jsonify(
        conversation_id=conversation_id,
        type="execution_complete",
        content="hello world",
    )