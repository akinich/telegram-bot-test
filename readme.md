# Telegram Bot on Streamlit Cloud

A simple Telegram bot that runs on Streamlit Cloud with a monitoring dashboard.

## Features

- ✅ Runs 24/7 on Streamlit Cloud (as long as the app is active)
- 📊 Real-time monitoring dashboard
- 💬 Echo messages and respond to commands
- 🤖 Simple command handling (/start, /help, /time)

## Setup Instructions

### 1. Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the **API token** you receive (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Deploy to Streamlit Cloud

1. Push this code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set the main file path to `telegram_bot.py`

### 3. Add Your Bot Token as a Secret

1. In the Streamlit Cloud deployment settings, click on "Advanced settings"
2. In the "Secrets" section, add:
   ```toml
   BOT_TOKEN = "your_bot_token_here"
   ```
3. Replace `your_bot_token_here` with your actual bot token from BotFather

### 4. Deploy!

Click "Deploy" and wait for your app to start. Once it's running, your bot will be active!

## Testing Your Bot

1. Open Telegram
2. Search for your bot by username (the one you created with BotFather)
3. Send `/start` to begin
4. Try these commands:
   - `/start` - Welcome message
   - `/help` - Show available commands
   - `/time` - Get current server time
   - Send any text - The bot will echo it back

## How It Works

The bot uses **polling** to check for new messages every 2 seconds. When a message arrives:
1. The bot processes the message
2. Sends an appropriate response
3. Updates the dashboard with activity logs

## Customizing Your Bot

Edit the `process_message()` function in `telegram_bot.py` to add your own commands and responses:

```python
def process_message(message):
    chat_id = message['chat']['id']
    text = message.get('text', '')
    
    if text == '/mycommand':
        response = "Your custom response!"
        send_message(chat_id, response)
```

## Important Notes

- **Streamlit Cloud Free Tier**: Apps may sleep after inactivity. For 24/7 uptime, consider upgrading or using a different hosting solution
- **Rate Limits**: This bot is suitable for personal use. For high-traffic bots, consider using webhooks instead of polling
- **Security**: Never commit your bot token to GitHub. Always use Streamlit secrets!

## Troubleshooting

**Bot not responding?**
- Check that your BOT_TOKEN is correctly set in Streamlit secrets
- Verify the token with BotFather
- Check the dashboard for error messages

**App keeps restarting?**
- This is normal for Streamlit Cloud free tier
- The bot will resume once the app restarts

**Need help?**
- Check Streamlit Cloud logs for errors
- Verify your bot token is valid
- Make sure you've started a conversation with your bot in Telegram

## Next Steps

- Add database integration to store messages
- Implement more complex command handling
- Add inline keyboard buttons
- Integrate with external APIs
- Add user authentication

Enjoy your Telegram bot! 🚀
