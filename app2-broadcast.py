import streamlit as st
import requests
import time
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Telegram Bot - Broadcast", page_icon="📢", layout="wide")

st.title("📢 Telegram Bot - Broadcast Manager")

# Get bot token from Streamlit secrets
BOT_TOKEN = st.secrets.get("BOT_TOKEN", "")

if not BOT_TOKEN:
    st.error("⚠️ BOT_TOKEN not found in secrets! Please add it in Streamlit Cloud settings.")
    st.stop()

# Telegram API base URL
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Get allowed chat IDs from secrets (optional - for restricting who can use the bot)
ALLOWED_CHAT_IDS = st.secrets.get("ALLOWED_CHAT_IDS", [])

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

def send_message(chat_id, text, parse_mode=None):
    """Send a message to a chat"""
    try:
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        if parse_mode:
            payload['parse_mode'] = parse_mode
            
        response = requests.post(f"{BASE_URL}/sendMessage", json=payload, timeout=10)
        return response.status_code == 200, response.json()
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return False, None

def get_updates(offset=None):
    """Get updates from Telegram"""
    try:
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        if response.status_code == 200:
            return response.json().get('result', [])
        return []
    except Exception as e:
        return []

def get_chat_info(chat_id):
    """Get information about a chat"""
    try:
        response = requests.get(f"{BASE_URL}/getChat", params={'chat_id': chat_id}, timeout=10)
        if response.status_code == 200:
            return response.json().get('result', {})
        return None
    except Exception as e:
        return None

# Display bot info
bot_info = get_bot_info()
if bot_info:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success("✅ Bot is connected!")
        st.write(f"**Bot Name:** {bot_info.get('first_name', 'N/A')}")
        st.write(f"**Username:** @{bot_info.get('username', 'N/A')}")
else:
    st.error("❌ Failed to connect to bot. Check your token!")
    st.stop()

st.divider()

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📤 Send Messages", "📋 Chat List", "📊 Activity Monitor"])

# Tab 1: Send Messages
with tab1:
    st.subheader("Send Message to Specific Chats")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("💡 **How to get Chat IDs:**\n"
                "1. Add your bot to a group or send it a message\n"
                "2. Check the 'Chat List' tab to see all chat IDs\n"
                "3. For groups: Chat ID is negative (e.g., -1001234567890)\n"
                "4. For individuals: Chat ID is positive (e.g., 123456789)")
        
        # Input for chat IDs
        chat_ids_input = st.text_area(
            "Enter Chat IDs (one per line)",
            placeholder="-1001234567890\n123456789\n-1009876543210",
            help="Enter one chat ID per line. For groups, use negative IDs."
        )
        
        # Message input
        message_text = st.text_area(
            "Message",
            placeholder="Enter your message here...",
            height=150
        )
        
        # Parse mode selection
        parse_mode = st.selectbox(
            "Format",
            ["None", "Markdown", "HTML"],
            help="Choose formatting style for your message"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            send_button = st.button("📤 Send Message", type="primary", use_container_width=True)
        
        with col_btn2:
            test_button = st.button("🧪 Test (Send to first ID only)", use_container_width=True)
    
    with col2:
        st.info("**Formatting Examples:**")
        st.markdown("""
        **Markdown:**
        ```
        *italic*
        **bold**
        [link](url)
        ```
        
        **HTML:**
        ```
        <i>italic</i>
        <b>bold</b>
        <a href="url">link</a>
        ```
        """)
    
    # Handle send button
    if send_button or test_button:
        if not message_text.strip():
            st.error("⚠️ Please enter a message!")
        elif not chat_ids_input.strip():
            st.error("⚠️ Please enter at least one chat ID!")
        else:
            # Parse chat IDs
            chat_ids = [cid.strip() for cid in chat_ids_input.strip().split('\n') if cid.strip()]
            
            # If test button, only use first ID
            if test_button:
                chat_ids = chat_ids[:1]
                st.info(f"🧪 Test mode: Sending to {chat_ids[0]} only")
            
            # Send messages
            success_count = 0
            fail_count = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, chat_id in enumerate(chat_ids):
                status_text.text(f"Sending to {chat_id}...")
                
                parse_mode_value = None if parse_mode == "None" else parse_mode
                success, response = send_message(chat_id, message_text, parse_mode_value)
                
                if success:
                    success_count += 1
                    st.success(f"✅ Sent to {chat_id}")
                else:
                    fail_count += 1
                    error_msg = response.get('description', 'Unknown error') if response else 'Unknown error'
                    st.error(f"❌ Failed to send to {chat_id}: {error_msg}")
                
                progress_bar.progress((idx + 1) / len(chat_ids))
                time.sleep(0.5)  # Small delay to avoid rate limiting
            
            status_text.empty()
            progress_bar.empty()
            
            # Summary
            st.divider()
            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("Total Sent", len(chat_ids))
            col_s2.metric("✅ Success", success_count)
            col_s3.metric("❌ Failed", fail_count)

# Tab 2: Chat List
with tab2:
    st.subheader("📋 Discovered Chats")
    st.write("This list shows all chats where someone has interacted with your bot.")
    
    # Initialize session state for chat list
    if 'chat_list' not in st.session_state:
        st.session_state.chat_list = {}
    
    # Button to refresh and discover chats
    if st.button("🔄 Discover New Chats", type="primary"):
        with st.spinner("Checking for new chats..."):
            updates = get_updates()
            new_chats = 0
            
            for update in updates:
                if 'message' in update:
                    message = update['message']
                    chat = message['chat']
                    chat_id = str(chat['id'])
                    
                    if chat_id not in st.session_state.chat_list:
                        new_chats += 1
                        
                        chat_info = {
                            'id': chat_id,
                            'type': chat['type'],
                            'title': chat.get('title', chat.get('first_name', 'Unknown')),
                            'username': chat.get('username', 'N/A'),
                            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        st.session_state.chat_list[chat_id] = chat_info
            
            if new_chats > 0:
                st.success(f"✅ Found {new_chats} new chat(s)!")
            else:
                st.info("No new chats found. Make sure to send a message to your bot first!")
    
    st.divider()
    
    # Display chat list
    if st.session_state.chat_list:
        st.write(f"**Total Chats:** {len(st.session_state.chat_list)}")
        
        # Filter options
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_type = st.selectbox("Filter by type", ["All", "private", "group", "supergroup", "channel"])
        
        for chat_id, chat_info in st.session_state.chat_list.items():
            if filter_type != "All" and chat_info['type'] != filter_type:
                continue
                
            with st.expander(f"💬 {chat_info['title']} ({chat_info['type']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Chat ID:** `{chat_info['id']}`")
                    st.write(f"**Type:** {chat_info['type']}")
                with col2:
                    st.write(f"**Username:** @{chat_info['username']}")
                    st.write(f"**Last Seen:** {chat_info['last_seen']}")
                
                # Quick send button
                if st.button(f"📤 Quick Send", key=f"send_{chat_id}"):
                    st.session_state.quick_send_chat_id = chat_id
                    st.rerun()
    else:
        st.info("👋 No chats discovered yet!\n\n"
                "**To get started:**\n"
                "1. Add your bot to a group or send it a message on Telegram\n"
                "2. Click 'Discover New Chats' button above\n"
                "3. The chat will appear here with its Chat ID")

# Tab 3: Activity Monitor
with tab3:
    st.subheader("📊 Bot Activity Monitor")
    
    # Initialize session state
    if 'offset' not in st.session_state:
        st.session_state.offset = None
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    if 'monitoring' not in st.session_state:
        st.session_state.monitoring = False
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Monitoring" if not st.session_state.monitoring else "⏸️ Stop Monitoring", 
                     type="primary"):
            st.session_state.monitoring = not st.session_state.monitoring
            st.rerun()
    
    with col2:
        st.metric("Messages Processed", st.session_state.message_count)
    
    st.divider()
    
    status_placeholder = st.empty()
    messages_container = st.container()
    
    # Monitoring loop
    if st.session_state.monitoring:
        while st.session_state.monitoring:
            status_placeholder.info(f"🔄 Monitoring... (Messages: {st.session_state.message_count})")
            
            updates = get_updates(st.session_state.offset)
            
            if updates:
                for update in updates:
                    st.session_state.offset = update['update_id'] + 1
                    
                    if 'message' in update:
                        message = update['message']
                        chat = message['chat']
                        
                        # Add to chat list
                        chat_id = str(chat['id'])
                        if 'chat_list' not in st.session_state:
                            st.session_state.chat_list = {}
                        
                        if chat_id not in st.session_state.chat_list:
                            st.session_state.chat_list[chat_id] = {
                                'id': chat_id,
                                'type': chat['type'],
                                'title': chat.get('title', chat.get('first_name', 'Unknown')),
                                'username': chat.get('username', 'N/A'),
                                'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                        
                        st.session_state.message_count += 1
                        
                        with messages_container:
                            st.write(f"**New message #{st.session_state.message_count}:**")
                            st.write(f"- From: {message['from'].get('first_name', 'Unknown')}")
                            st.write(f"- Chat: {chat.get('title', chat.get('first_name', 'N/A'))} (ID: `{chat_id}`)")
                            st.write(f"- Type: {chat['type']}")
                            st.write(f"- Text: {message.get('text', 'N/A')}")
                            st.write(f"- Time: {datetime.now().strftime('%H:%M:%S')}")
                            st.divider()
            
            time.sleep(2)
    else:
        status_placeholder.warning("⏸️ Monitoring paused. Click 'Start Monitoring' to resume.")

# Handle quick send from chat list
if hasattr(st.session_state, 'quick_send_chat_id'):
    st.info(f"Chat ID {st.session_state.quick_send_chat_id} has been copied! Go to 'Send Messages' tab to send.")
    del st.session_state.quick_send_chat_id
