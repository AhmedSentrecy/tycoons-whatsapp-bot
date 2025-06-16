from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# بيانات Chatbase الخاصة بك
CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"
CHATBASE_API_URL = "https://www.chatbase.co/api/v1/chat"

@app.route("/", methods=["GET"])
def health():
    return "✅ Webhook is running!"

@app.route("/test", methods=["GET"])
def test():
    user_message = "Hello from test endpoint"
    
    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "chatbotId": CHATBASE_BOT_ID,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(CHATBASE_API_URL, headers=headers, json=payload)
        bot_reply = response.json().get("text", "❌ Chatbase did not return a valid reply")
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    print("📩 Webhook received!")
    data = request.get_json()

    user_message = ""
    # حاول استخراج الرسالة بأي شكل
    if isinstance(data, dict):
        user_message = data.get("input_flow_data") or data.get("message") or ""

    if not user_message:
        return jsonify({"error": "❌ No valid user input found"}), 400

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "chatbotId": CHATBASE_BOT_ID,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(CHATBASE_API_URL, headers=headers, json=payload)
        bot_reply = response.json().get("text", "❌ Chatbase did not return a valid reply")
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

if __name__ == "__main__":
    # لازم نحدد port 10000 ل Render
    app.run(host="0.0.0.0", port=10000)
