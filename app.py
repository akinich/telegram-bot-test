import streamlit as st
import requests
import time
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Telegram Bot Monitor", page_icon="🤖")

st.title("🤖 Telegram Bot Monitor")
st.write("Your Telegram bot is running in the background!")

# Get bot token from Streamlit secrets
BOT_TOKEN = st.secrets.get("BOT_TOKEN", "")

if not BOT_TOKEN:
    st.error("⚠️ BOT_TOKEN not found in secrets! Please add it in Streamlit Cloud settings.")
    st.stop()

# Telegram API base URL
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_bot_info():
    """Get information about the bot"""
    try:
        response = requests.get(f"{BASE_URL}/getMe", timeout=10)
        if response.status_code == 200:
            return response.json().get('result', {})
        return None
    except Exception as e:
        st.error(f"Error getting bot info: {e}")
        return None

def send_message(chat_id, text):
    """Send a message to a chat"""
    try:
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(f"{BASE_URL}/sendMessage", json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return False

def get_updates(offset=None):
    """Get updates from Telegram"""
    try:
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        if response.status_code == 200:
            return response.json().get('result', [])
        return []
    except Exception as e:
        st.error(f"Error getting updates: {e}")
        return []

def process_message(message):
    """Process incoming message and send response"""
    chat_id = message['chat']['id']
    text = message.get('text', '')
    
    # Simple command handling
    if text == '/start':
        response = "👋 Hello! I'm your Telegram bot. Send me a message and I'll echo it back!"
    elif text == '/help':
        response = "Available commands:\n/start - Start the bot\n/help - Show this help message\n/time - Get current time"
    elif text == '/time':
        response = f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        response = f"You said: {text}"
    
    send_message(chat_id, response)

# Display bot info
bot_info = get_bot_info()
if bot_info:
    st.success("✅ Bot is connected!")
    st.write(f"**Bot Name:** {bot_info.get('first_name', 'N/A')}")
    st.write(f"**Username:** @{bot_info.get('username', 'N/A')}")
else:
    st.error("❌ Failed to connect to bot. Check your token!")
    st.stop()

# Status display
status_placeholder = st.empty()
messages_placeholder = st.container()

# Initialize session state for offset
if 'offset' not in st.session_state:
    st.session_state.offset = None
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

st.divider()
st.subheader("📊 Bot Activity")

# Main loop
while True:
    status_placeholder.info(f"🔄 Polling for messages... (Messages processed: {st.session_state.message_count})")
    
    # Get updates
    updates = get_updates(st.session_state.offset)
    
    if updates:
        for update in updates:
            # Update offset
            st.session_state.offset = update['update_id'] + 1
            
            # Process message if it exists
            if 'message' in update:
                message = update['message']
                st.session_state.message_count += 1
                
                # Display message info
                with messages_placeholder:
                    st.write(f"**New message #{st.session_state.message_count}:**")
                    st.write(f"- From: {message['from'].get('first_name', 'Unknown')}")
                    st.write(f"- Text: {message.get('text', 'N/A')}")
                    st.write(f"- Time: {datetime.now().strftime('%H:%M:%S')}")
                    st.divider()
                
                # Process the message
                process_message(message)
    
    # Sleep to avoid hammering the API
    time.sleep(2)
