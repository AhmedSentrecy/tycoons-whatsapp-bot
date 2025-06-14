from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Chatbase credentials
CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/test", methods=["GET"])
def test():
    user_message = "Hello from test endpoint"
    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": user_message}],
        "chatbot_id": CHATBASE_BOT_ID
    }
    try:
        response = requests.post("https://www.chatbase.co/api/v1/chat", headers=headers, json=payload)
        data = response.json()
        bot_reply = data.get("messages", [{}])[0].get("content", "❌ Chatbase did not return a valid reply")
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"
    return jsonify({"user_message": user_message, "bot_reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
