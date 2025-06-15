from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHATBASE_API_KEY = "3d722142-3344-4490-a741-72b9c614c19a"
CHATBASE_BOT_ID = "KfOP1E1pvrQBRpn9tWcAE"

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "Hello from test endpoint",
        "bot_reply": "✅ test reply"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📥 Received webhook payload:", data)

        user_message = data.get("input_flow_data")
        if not user_message:
            print("❌ input_flow_data not found.")
            return jsonify({"error": "Missing input_flow_data"}), 400

        # Build payload for Chatbase
        chatbase_payload = {
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

        response = requests.post("https://www.chatbase.co/api/v1/chat", json=chatbase_payload, headers=headers)
        print("📤 Sent to Chatbase:", chatbase_payload)
        print("📬 Chatbase response:", response.status_code, response.text)

        if response.status_code == 200:
            reply = response.json().get("text", "⚠️ Chatbase returned no text.")
        else:
            reply = "❌ Chatbase did not return a valid reply"

        return jsonify({
            "user_message": user_message,
            "bot_reply": reply
        })

    except Exception as e:
        print("💥 Error in /webhook:", str(e))
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
