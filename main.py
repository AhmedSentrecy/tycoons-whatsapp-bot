from flask import Flask, request, jsonify
import requests
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

CHATBASE_API_KEY = os.environ.get("CHATBASE_API_KEY")
CHATBASE_BOT_ID = os.environ.get("CHATBASE_BOT_ID")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
GOOGLE_SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

@app.route("/", methods=["GET"])
def health():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        entry = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_message = entry["text"]["body"]
        phone_number = entry["from"]

        chatbase_response = requests.post(
            "https://www.chatbase.co/api/v1/chat",
            headers={
                "Authorization": f"Bearer " + CHATBASE_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"content": user_message, "role": "user"}],
                "chatbot_id": CHATBASE_BOT_ID,
                "stream": False
            }
        ).json()

        bot_reply = chatbase_response["messages"][0]["content"]

        requests.post(
            f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
            headers={
                "Authorization": f"Bearer " + WHATSAPP_TOKEN,
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": bot_reply}
            }
        )

        sheet.append_row([
            datetime.datetime.now().isoformat(),
            phone_number,
            user_message,
            bot_reply
        ])

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test_bot():
    user_message = "Hello, how can I buy a property?"
    phone_number = "201234567890"

    chatbase_response = requests.post(
        "https://www.chatbase.co/api/v1/chat",
        headers={
            "Authorization": f"Bearer " + CHATBASE_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "messages": [{"content": user_message, "role": "user"}],
            "chatbot_id": CHATBASE_BOT_ID,
            "stream": False
        }
    ).json()

    bot_reply = chatbase_response["messages"][0]["content"]

    sheet.append_row([
        datetime.datetime.now().isoformat(),
        phone_number,
        user_message,
        bot_reply
    ])

    return jsonify({
        "user_message": user_message,
        "bot_reply": bot_reply
    })

app.run(host="0.0.0.0", port=8080)

