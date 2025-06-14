from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 مفاتيح Chatbase
CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

# ✅ دالة للحصول على الرد من Chatbase
def get_chatbase_reply(user_message):
    url = "https://www.chatbase.co/api/v1/chat"
    payload = {
        "messages": [{"content": user_message, "role": "user"}],
        "chatbotId": CHATBASE_BOT_ID,
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("📦 Chatbase Response:")
        print(data)

        return data.get("messages", [{"content": "❌ Chatbase did not return a valid reply"}])[0].get("content")
    except Exception as e:
        print("❌ Error:", e)
        return "❌ Error reaching Chatbase"

# 🔁 Webhook endpoint (POST)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("user_message", "")
    bot_reply = get_chatbase_reply(user_message)
    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

# 🔍 Endpoint للتجربة من المتصفح
@app.route("/test", methods=["GET"])
def test():
    user_message = "Hello from test endpoint"
    bot_reply = get_chatbase_reply(user_message)
    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

# ✅ Health check
@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"
