from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("message", "")  # WatchChimp ممكن تبعت "message"

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [{"role": "user", "content": user_message}],
        "bot_id": CHATBASE_BOT_ID
    }

    try:
        response = requests.post("https://www.chatbase.co/api/v1/chat", headers=headers, json=payload)
        response_data = response.json()
        bot_reply = response_data.get("text", "❌ Chatbase did not return a valid reply")
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    # هنا بنرجع المفتاح اللي ممكن WatchChimp يتعرف عليه
    return jsonify({"message": bot_reply})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "Hello from test endpoint",
        "message": "✅ test reply"
    })

if __name__ == "__main__":
    app.run(port=5000)
