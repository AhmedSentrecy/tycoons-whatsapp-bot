from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "user_message": "test message",
        "bot_reply": "test reply"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("user_message", "")
    
    # رد تجريبي ثابت — هنا لاحقًا نربطه بـ Chatbase
    bot_reply = f"رد تلقائي على: {user_message}"

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

# أهم حاجة علشان يشتغل على Render:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
