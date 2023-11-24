from flask import Flask, request
import tkinter as tk
from twilio.rest import Client
from pyngrok import ngrok

# Twilio credentials
account_sid = 'AC0319e5fd8c0b2361a8a30fdba255403f'
auth_token = '409f9db3f25756aba675ebf8ea87265a'
twilio_phone_number = '+19136530123'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Global variable to store the latest received message
latest_message = ""

# Function to update the latest message and display it on the screen
def update_message(message):
    global latest_message
    latest_message = message
    show_message()

# Function to display the latest message in a Tkinter window
def show_message():
    window = tk.Tk()
    window.title("Twilio Message Notification")

    label_message = tk.Label(window, text=f"Latest Message: {latest_message}")
    label_message.pack(pady=20)

    window.mainloop()

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def receive_sms():
    # Get the incoming message
    message_body = request.values.get('Body', None)
    
    # Update the latest message and display it on the screen
    update_message(message_body)

    # Respond to the Twilio webhook
    return '', 200

if __name__ == '__main__':
    # Set up Ngrok tunnel with authentication token
    ngrok.set_auth_token("2YcFz0DYwt9zfQ81vvU8HRKAByV_6ASTKfqai8XD84RkrmkYz")
    ngrok_url = ngrok.connect(5000)  # Flask default port is 5000
    print(f"Ngrok URL: {ngrok_url}")

    try:
        app.run(port=5000)  # Use the same port your Flask app is running on locally
    finally:
        ngrok.kill()
