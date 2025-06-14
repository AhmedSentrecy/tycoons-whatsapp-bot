from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/", methods=["GET"])
def home():
    return "✅ Webhook is live and running"

@app.route("/test", methods=["GET"])
def test():
    response = requests.post(
        "https://www.chatbase.co/api/v1/chat",
        headers={"Authorization": f"Bearer {CHATBASE_API_KEY}"},
        json={
            "chatbot_id": CHATBASE_BOT_ID,
            "message": "Hello from test endpoint",
            "stream": False
        }
    )
    reply = response.json()["messages"][0]["content"] if response.ok else "❌ Chatbase did not reply"
    return jsonify({"user_message": "Hello from test endpoint", "bot_reply": reply})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("user_message", "")
    phone_number = data.get("phone_number", "")

    chatbase_response = requests.post(
        "https://www.chatbase.co/api/v1/chat",
        headers={"Authorization": f"Bearer {CHATBASE_API_KEY}"},
        json={
            "chatbot_id": CHATBASE_BOT_ID,
            "message": user_message,
            "stream": False
        }
    )

    if chatbase_response.ok:
        bot_reply = chatbase_response.json()["messages"][0]["content"]
    else:
        bot_reply = "❌ Sorry, Chatbase did not respond."

    return jsonify({
        "phone_number": phone_number,
        "user_message": user_message,
        "bot_reply": bot_reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
