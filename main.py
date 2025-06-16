from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
        "chatbotId": CHATBASE_BOT_ID
    }
    response = requests.post("https://www.chatbase.co/api/v1/chat", headers=headers, json=payload)
    reply = response.json().get("text", "❌ Chatbase did not return a valid reply")
    return jsonify({"user_message": user_message, "bot_reply": reply})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("input_flow_data", "")

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": user_message}],
        "chatbotId": CHATBASE_BOT_ID
    }

    response = requests.post("https://www.chatbase.co/api/v1/chat", headers=headers, json=payload)
    reply = response.json().get("text", "❌ Chatbase did not reply")

    # رجّع الرد على هيئة JSON
    return jsonify({"bot_reply": reply})
    
# مهم جدًا علشان Render يشتغل على port 10000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
