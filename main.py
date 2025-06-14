from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# health check route
@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "test message",
        "bot_reply": "test reply"
    })

# webhook endpoint
CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    user_message = data.get("user_message", "")
    phone_number = data.get("phone_number", "unknown")

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "chatbot_id": CHATBASE_BOT_ID,
        "stream": False
    }

    response = requests.post("https://www.chatbase.co/api/v1/chat", headers=headers, json=payload)
    
    try:
        bot_reply = response.json().get("messages", [{}])[0].get("content", "معذرة، لم أفهم الرسالة.")
    except:
        bot_reply = "حدث خطأ أثناء التواصل مع Chatbase."

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
