# Telegram Bot - Broadcast Manager

A Telegram bot running on Streamlit Cloud that lets you send messages to specific groups and individuals.

## 🌟 Features

- 📤 **Broadcast Messages** - Send messages to multiple groups/individuals at once
- 📋 **Chat Discovery** - Automatically discover and list all chats that interact with your bot
- 🎯 **Targeted Messaging** - Send to specific groups or individuals using their Chat IDs
- 📊 **Activity Monitor** - Real-time monitoring of bot activity
- ✨ **Formatting Support** - Send messages with Markdown or HTML formatting
- 🧪 **Test Mode** - Test messages before sending to all recipients

## Setup Instructions

### 1. Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the **API token** you receive (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Add Bot to Groups (Optional)

To send messages to groups:
1. Create a group or use an existing one
2. Add your bot to the group
3. Make sure the bot has permission to send messages

### 3. Deploy to Streamlit Cloud

1. Push this code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set the main file path to `telegram_bot_broadcast.py`

### 4. Add Your Bot Token as a Secret

1. In the Streamlit Cloud deployment settings, click on "Advanced settings"
2. In the "Secrets" section, add:
   ```toml
   BOT_TOKEN = "your_bot_token_here"
   ```
3. Replace `your_bot_token_here` with your actual bot token from BotFather

### 5. Deploy and Discover Chats!

1. Click "Deploy" and wait for your app to start
2. Once running, send a message to your bot (or have someone in a group send a message)
3. Go to the "Chat List" tab and click "Discover New Chats"
4. You'll see all chat IDs that you can now send messages to!

## 📖 How to Use

### Getting Chat IDs

**Method 1: Using the Chat List Tab**
1. Have someone send a message to your bot (private message)
2. Or add your bot to a group and have someone send a message
3. Go to "Chat List" tab in the Streamlit app
4. Click "Discover New Chats"
5. All chat IDs will be listed with details

**Method 2: Manual Discovery**
- **For individual users**: When they message your bot, their chat ID appears in Activity Monitor
- **For groups**: Group chat IDs are negative numbers (e.g., `-1001234567890`)
- **For channels**: You need to add the bot as an admin first

### Sending Messages

1. Go to the "Send Messages" tab
2. Enter chat IDs (one per line) in the text area:
   ```
   123456789
   -1001234567890
   987654321
   ```
3. Type your message
4. (Optional) Choose formatting: Markdown or HTML
5. Click "Test" to send to first ID only, or "Send Message" to send to all

### Message Formatting

**Markdown:**
```
*italic text*
**bold text**
[clickable link](https://example.com)
`code`
```

**HTML:**
```html
<i>italic text</i>
<b>bold text</b>
<a href="https://example.com">clickable link</a>
<code>code</code>
```

## 🎯 Use Cases

- **Company Announcements**: Send updates to multiple team groups
- **Community Management**: Broadcast messages to community members
- **Customer Support**: Send messages to specific customers
- **Event Notifications**: Alert participants about events
- **News Distribution**: Share news with subscribers
- **Personal Assistant**: Send reminders to yourself or family groups

## 🔒 Security Tips

1. **Never share your bot token publicly**
2. **Use Streamlit secrets** - Never hardcode the token in your code
3. **Restrict access**: Consider adding authentication to the Streamlit app
4. **Monitor usage**: Keep track of who's using your bot in the Activity Monitor
5. **Group privacy**: Be cautious when adding bots to groups with sensitive information

## 📝 Advanced Configuration (Optional)

You can restrict who can interact with your bot by adding allowed chat IDs to secrets:

```toml
BOT_TOKEN = "your_bot_token_here"
ALLOWED_CHAT_IDS = [123456789, 987654321]
```

This will make the bot only respond to messages from those specific chat IDs.

## 🛠️ Customization Ideas

### Add Scheduled Messages
Integrate with Streamlit's scheduler to send messages at specific times:
```python
import schedule
schedule.every().day.at("09:00").do(send_morning_update)
```

### Add Database Storage
Store chat IDs and message history in a database:
```python
# Use Streamlit's connection feature
import streamlit as st
conn = st.connection("postgresql", type="sql")
```

### Add Authentication
Protect your Streamlit app:
```python
import streamlit_authenticator as stauth
authenticator = stauth.Authenticate(...)
```

### Add Message Templates
Create reusable message templates:
```python
templates = {
    "welcome": "Welcome to our community! 👋",
    "reminder": "Don't forget about tomorrow's meeting at 10 AM!"
}
```

## 🐛 Troubleshooting

**Issue: Can't see my group's chat ID**
- Solution: Make sure someone has sent a message in the group after adding the bot
- Try sending a message with the bot's username mentioned: `@yourbotname`

**Issue: "Chat not found" error**
- Solution: The bot might have been removed from the group
- For private chats, the user must have started a conversation with the bot first

**Issue: "Bot was blocked by the user"**
- Solution: The user has blocked your bot. They need to unblock it first

**Issue: Message not delivered to group**
- Solution: Check if the bot has permission to send messages in the group
- The bot might need admin privileges in some groups

**Issue: Rate limiting**
- Solution: Telegram limits bots to ~30 messages per second
- The app includes a small delay between messages to avoid this

## 📚 API Reference

### Key Functions

- `send_message(chat_id, text, parse_mode)` - Send a message to a specific chat
- `get_chat_info(chat_id)` - Get information about a chat
- `get_updates(offset)` - Get new messages from Telegram

### Chat ID Format

- **Individuals**: Positive integer (e.g., `123456789`)
- **Groups**: Negative integer starting with `-100` (e.g., `-1001234567890`)
- **Channels**: Similar to groups (e.g., `-1001234567890`)

## 🚀 Next Steps

- **Add a database** to store chat lists persistently
- **Create message templates** for quick sending
- **Add scheduling** for automated messages
- **Implement analytics** to track message delivery
- **Add file uploads** to send images/documents
- **Create subscriber management** system

## 📞 Support

For questions about:
- **Telegram Bot API**: [Telegram Bot Documentation](https://core.telegram.org/bots/api)
- **Streamlit**: [Streamlit Documentation](https://docs.streamlit.io)
- **This project**: Check the code comments or modify as needed!

---

Enjoy broadcasting with your Telegram bot! 🎉
