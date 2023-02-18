# Twitch Stream Notification Bot
Python script that uses Twitch API and Telegram API to send a notification when a streamer comes online.

# Getting Started

To use this script, you will need to set up a few things first:

## Twitch API

1. Go to the [Twitch Developer Dashboard](https://dev.twitch.tv/console/apps) and create a new application.
2. Take note of the Client ID and Client Secret values for your application.
3. Add https://localhost to the OAuth Redirect URLs section.
4. Edit the _userStream_ variable in the *.py file to match the username of the streamer you want to track.

## Telegram Bot

1. Create a new bot on Telegram by talking to the [BotFather](https://telegram.me/BotFather).
2. Take note of the bot token that BotFather gives you.
3. Add your bot to a Telegram chat, and take note of the chat ID, using Telegram API request (e.g https://api.telegram.org/bot[HERE_IS_BOT_TOKEN]/getUpdates). 

## OAuth Tokens

To authenticate the script with the Twitch API and Telegram Bot API, you will need to fill in OAuth tokens.
1. Replace `YOUR_TWITCH_CLIENT_ID` and `YOUR_TWITCH_CLIENT_SECRET` in the script with your Twitch application's Client ID and Client Secret.
2. Replace `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in the script with your Telegram bot token and chat ID.
3. And the last thing you should do is fill in `TWITCH_USER_LOGIN` with Twitch Username that you want to track.

## Running the Bot

1. Start your VPS or VM with Python on board.
1. Open a terminal and navigate to the directory where *.py is saved.
2. Run command `python *.py`.
3. The bot will check the stream status every 10 seconds, and send a Telegram message when the streamer goes online.
