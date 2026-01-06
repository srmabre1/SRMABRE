import os
from flask import Flask, render_template, request
from twilio.rest import Client
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- CONFIGURATION ---
MY_NAME = "Mautasim" 
TWILIO_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_MSG_SERVICE_SID = os.getenv('TWILIO_MSG_SERVICE_SID')

client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    to_number = request.form['phone']
    user_message = request.form['message']
    date_str = request.form['time'] 

    # This adds your name to every message automatically
    final_message = f"{user_message}\n\n— Sent by {MY_NAME}"

    # Convert time to ISO format (Required by Twilio)
    send_at = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc).isoformat()

    try:
        message = client.messages.create(
            messaging_service_sid=TWILIO_MSG_SERVICE_SID,
            body=final_message,
            send_at=send_at,
            schedule_type='fixed',
            to=to_number
        )
        return f"<h2>Success, Mautasim!</h2><p>Message scheduled ID: {message.sid}</p><a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h2>Error</h2><p>{str(e)}</p><a href='/'>Try Again</a>"

if __name__ == "__main__":
    app.run(debug=True)
