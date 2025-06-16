# app.py
from flask import Flask, request, jsonify
import json, os
from google.oauth2 import service_account
import google.auth.transport.requests
import requests as http

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]
PROJECT_ID = "reelgo-65e5f"

# Load service account credentials from env variable
try:
    service_account_info = json.loads(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
except KeyError:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS_JSON env var not set")

credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)


@app.route("/", methods=["GET"])
def home():
    return "✅ FCM Server is running!"


@app.route("/send-notification", methods=["POST"])
def send_notification():
    data = request.get_json()
    token = data.get("token")
    title = data.get("title")
    body = data.get("body")

    if not all([token, title, body]):
        return jsonify({"error": "token, title, and body are required"}), 400

    # Refresh token
    request_adapter = google.auth.transport.requests.Request()
    credentials.refresh(request_adapter)
    access_token = credentials.token

    # Prepare FCM request
    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    response = http.post(url, headers=headers, data=json.dumps(payload))

    try:
        return jsonify({
            "status": response.status_code,
            "response": response.json()
        }), response.status_code
    except Exception:
        return jsonify({
            "status": response.status_code,
            "response": response.text
        }), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
