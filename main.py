from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHATBASE_API_KEY = os.environ.get("CHATBASE_API_KEY")
CHATBASE_BOT_ID = os.environ.get("CHATBASE_BOT_ID")

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)  # ← مهم جدًا علشان نعرف إذا جات بيانات من واتششمب ولا لأ

    user_message = data.get("input_flow_data") or "No input"
    print("User said:", user_message)

    return jsonify({"bot_reply": "✅ test reply", "user_message": user_message})

    
    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": user_msg}],
        "chatbotId": CHATBASE_BOT_ID
    }
    resp = requests.post("https://www.chatbase.co/api/v1/chat", json=payload, headers=headers)
    
    if resp.status_code == 200:
        bot_msg = resp.json().get("text", "✅ Chatbase replied but message missing")
    else:
        bot_msg = "❌ Chatbase did not return a valid reply"

    # هنا ترجع للواتساب اللي هو Whatchimp – code response
    return jsonify({"reply": bot_msg})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "Hello from test endpoint",
        "bot_reply": "✅ test reply"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
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
