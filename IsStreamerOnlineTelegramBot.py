import os
import requests
import json
import threading

# Define constants
TWITCH_CLIENT_ID = "your_twitch_client_id"
TWITCH_CLIENT_SECRET = "your_twitch_client_secret"
TWITCH_USER_LOGIN = "your_twitch_user_login"
TELEGRAM_BOT_TOKEN = "telegram_bot_token"
TELEGRAM_CHAT_ID = "telegram_chat_id"
STATE_FILE_PATH = "isOnlineFile.txt"
CHECK_INTERVAL = 10

# Twitch OAuth token
def get_twitch_token():
    try:
        response = requests.post(
            f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&grant_type=client_credentials"
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"Error getting Twitch OAuth token: {str(e)}")
        return None

# Check if the Twitch stream is online and send a notification if it just went live
def check_stream():
    try:
        # Get the Twitch OAuth token
        token = get_twitch_token()
        if not token:
            return
        
        # Make the API request to check the stream status
        headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {token}"}
        response = requests.get(f"https://api.twitch.tv/helix/streams?user_login={TWITCH_USER_LOGIN}", headers=headers)
        response.raise_for_status()
        stream_data = response.json()
        
        # Determine if the stream is online or offline
        if "data" in stream_data and stream_data["data"]:
            # Stream is online
            stream_title = stream_data["data"][0]["title"]
            stream_url = f"https://www.twitch.tv/{TWITCH_USER_LOGIN}"
            message = f"{TWITCH_USER_LOGIN} just started streaming:\n\n{stream_title}\n\n{stream_url}"

            # Check if the streamer's state has changed
            if (os.path.exists(STATE_FILE_PATH) == False):
            	f = open(STATE_FILE_PATH, "w")
            	f.close()
            with open(STATE_FILE_PATH, "r") as f:
                current_state = f.read().strip()
            if current_state != "online":
                # If the streamer was offline the last time we checked, send a notification and update the state
                response = send_telegram_message(message)
                if response and response.get("ok"):
                    print("Sent notification to Telegram.")
                else:
                    print(f"Error sending notification to Telegram: {response}")
                with open(STATE_FILE_PATH, "w") as f:
                    f.write("online")
        else:
            # Stream is offline
            with open(STATE_FILE_PATH, "r") as f:
                current_state = f.read().strip()
            if current_state != "offline":
                with open(STATE_FILE_PATH, "w") as f:
                    f.write("offline")
    except Exception as e:
        print(f"Error checking Twitch stream: {str(e)}")

# Send a message to Telegram
def send_telegram_message(message):
    try:
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending message to Telegram: {str(e)}")
        return None

# Main loop
def main():
    check_stream()
    threading.Timer(CHECK_INTERVAL, main).start()

if __name__ == "__main__":
    main()

