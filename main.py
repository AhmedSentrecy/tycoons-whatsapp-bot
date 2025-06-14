from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("user_message", "")
    phone_number = data.get("phone_number", "")

    CHATBASE_API_KEY = os.environ.get("CHATBASE_API_KEY")
    CHATBASE_BOT_ID = os.environ.get("CHATBASE_BOT_ID")

    if not user_message or not phone_number or not CHATBASE_API_KEY or not CHATBASE_BOT_ID:
        return jsonify({"error": "Missing required data"}), 400

    try:
        resp = requests.post(
            "https://www.chatbase.co/api/v1/chat",
            headers={
                "Authorization": f"Bearer {CHATBASE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"role": "user", "content": user_message}],
                "chatbot_id": CHATBASE_BOT_ID,
                "stream": False
            }
        )
        result = resp.json()
        bot_reply = result["messages"][0]["content"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "phone_number": phone_number,
        "user_message": user_message,
        "bot_reply": bot_reply
    })

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "test message",
        "bot_reply": "test reply"
    })
