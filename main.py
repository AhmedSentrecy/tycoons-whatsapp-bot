from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# متغيرات Chatbase
CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"
CHATBASE_API_URL = "https://www.chatbase.co/api/v1/chat"

@app.route("/", methods=["GET"])
def home():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("message", "")

    # إعداد البيانات لطلب Chatbase
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "chatbotId": CHATBASE_BOT_ID
    }

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(CHATBASE_API_URL, json=payload, headers=headers)
        response_data = response.json()
        bot_reply = response_data.get("text", "❌ Chatbase did not reply")
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
