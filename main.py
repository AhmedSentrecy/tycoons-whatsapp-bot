from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/")
def health():
    return "Webhook is running"

@app.route("/test")
def test():
    user_message = "Hello from test endpoint"
    bot_reply = get_chatbase_reply(user_message)
    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("user_message", "Hi")
    bot_reply = get_chatbase_reply(user_message)
    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

def get_chatbase_reply(user_message):
    url = f"https://www.chatbase.co/api/v1/chat"
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

        print("Chatbase raw response:", data)  # لمتابعة التصحيح
        if "messages" in data and data["messages"]:
            return data["messages"][0]["content"]
        else:
            return "❌ Chatbase did not return a valid reply"

    except Exception as e:
        print("Error:", e)
        return "❌ Error reaching Chatbase"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
