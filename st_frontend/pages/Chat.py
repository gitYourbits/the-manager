import streamlit as st
import requests
import json
from datetime import datetime
from theme import create_page_header, create_card, create_action_button, create_section_header

def render():
    create_page_header("AI Chat", "Intelligent conversations with your AI assistant", "💬")
    
    # Check authentication
    if not st.session_state.get('token'):
        create_card(
            "Authentication Required",
            "Please login to access the AI chat feature.",
            "🔐"
        )
        return
    
    # Initialize chat state
    if 'conversations' not in st.session_state:
        st.session_state.conversations = []
    if 'current_conversation' not in st.session_state:
        st.session_state.current_conversation = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for conversation management
    with st.sidebar:
        create_section_header("Conversations", "💬")
        
        if create_action_button("New Conversation", "➕", "new_conv"):
            try:
                response = requests.post(
                    "http://localhost:8000/api/chat/conversations/",
                    headers={"Authorization": f"Bearer {st.session_state.token}"},
                    json={"title": f"Chat {datetime.now().strftime('%H:%M')}"}
                )
                if response.status_code == 201:
                    st.session_state.current_conversation = response.json()
                    st.session_state.messages = []
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to create conversation: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Load existing conversations
        try:
            response = requests.get(
                "http://localhost:8000/api/chat/conversations/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if response.status_code == 200:
                conversations = response.json()
                if conversations:
                    st.markdown("**Your Conversations:**")
                    for conv in conversations:
                        # Highlight current conversation
                        if st.session_state.current_conversation and conv['id'] == st.session_state.current_conversation['id']:
                            st.markdown(f"""
                            <div style="background: rgba(255, 68, 68, 0.1); padding: 0.5rem; border-radius: 8px; border-left: 4px solid #ff4444; margin: 0.5rem 0;">
                                <p style="margin: 0; color: #ff4444; font-weight: 600;">📝 {conv.get('title', 'Untitled')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            if st.button(f"📝 {conv.get('title', 'Untitled')}", key=f"conv_{conv['id']}", use_container_width=True):
                                st.session_state.current_conversation = conv
                                st.session_state.messages = conv.get('messages', [])
                                st.rerun()
                else:
                    st.info("No conversations yet. Start your first chat!")
        except Exception as e:
            st.error(f"Failed to load conversations: {str(e)}")
    
    # Main chat area
    if st.session_state.current_conversation:
        # Chat header
        create_card(
            f"💬 {st.session_state.current_conversation.get('title', 'Chat')}",
            f"Started: {st.session_state.current_conversation.get('started_at', 'Unknown')[:10]}",
            "💬"
        )
        
        # Chat messages container
        chat_container = st.container()
        with chat_container:
            if st.session_state.messages:
                for msg in st.session_state.messages:
                    if msg['sender'] == 'user':
                        st.markdown(f"""
                        <div style="background: rgba(255, 68, 68, 0.1); padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border-left: 4px solid #ff4444;">
                            <p style="margin: 0; color: #ffffff;"><strong>You:</strong> {msg['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(0, 255, 136, 0.1); padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border-left: 4px solid #00ff88;">
                            <p style="margin: 0; color: #ffffff;"><strong>AI Assistant:</strong> {msg['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                create_card(
                    "Start Your Conversation",
                    "Type a message below to begin chatting with your AI assistant. Ask about your music career, get advice, or discuss your goals!",
                    "💭"
                )
        
        # Message input
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Chat input with better styling
        with st.container():
            st.markdown("""
            <div style="background: rgba(26, 26, 26, 0.8); padding: 1rem; border-radius: 12px; border: 1px solid #333333;">
                <p style="margin: 0 0 0.5rem 0; color: #cccccc; font-weight: 600;">💬 Send a message:</p>
            </div>
            """, unsafe_allow_html=True)
            
            if prompt := st.chat_input("Type your message here...", key="chat_input"):
                try:
                    # Send message to backend
                    response = requests.post(
                        "http://localhost:8000/api/chat/messages/",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        json={
                            "conversation": st.session_state.current_conversation['id'],
                            "text": prompt,
                            "sender": "user"
                        }
                    )
                    if response.status_code == 201:
                        # Reload conversation to get updated messages
                        conv_response = requests.get(
                            f"http://localhost:8000/api/chat/conversations/{st.session_state.current_conversation['id']}/",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if conv_response.status_code == 200:
                            st.session_state.messages = conv_response.json()['messages']
                            st.rerun()
                except Exception as e:
                    st.error(f"Failed to send message: {str(e)}")
    else:
        # No conversation selected
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            create_card(
                "Welcome to AI Chat! 🎉",
                """
                <p>Start a new conversation to begin chatting with your AI assistant.</p>
                <p>You can ask about:</p>
                <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                    <li>🎵 Music career advice</li>
                    <li>📚 Knowledge from your documents</li>
                    <li>🎯 Strategic planning</li>
                    <li>📊 Industry insights</li>
                    <li>💡 Creative inspiration</li>
                </ul>
                """,
                "💬"
            )
            
            if create_action_button("Start New Conversation", "🚀", "start_new"):
                try:
                    response = requests.post(
                        "http://localhost:8000/api/chat/conversations/",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        json={"title": f"Chat {datetime.now().strftime('%H:%M')}"}
                    )
                    if response.status_code == 201:
                        st.session_state.current_conversation = response.json()
                        st.session_state.messages = []
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to create conversation: {str(e)}")
    
    # Chat tips section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    create_section_header("Chat Tips", "💡")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_card(
            "Getting Better Responses",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>🎯 Be specific about your questions</li>
                <li>📚 Reference your uploaded documents</li>
                <li>🎵 Ask about music industry trends</li>
                <li>📊 Request data-driven insights</li>
            </ul>
            """,
            "🎯"
        )
    
    with col2:
        create_card(
            "Conversation Features",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>💾 Conversations are automatically saved</li>
                <li>🔄 Switch between different chats</li>
                <li>📝 Each conversation has a unique title</li>
                <li>🔍 Search through your chat history</li>
            </ul>
            """,
            "⚡"
        ) 