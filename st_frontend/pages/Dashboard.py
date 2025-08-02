import streamlit as st
import requests
import json
from datetime import datetime
from theme import create_page_header, create_card, create_metric_card, create_action_button, create_section_header

def render():
    create_page_header("Dashboard", "Your AI Manager Overview", "📊")
    
    # Check authentication
    if not st.session_state.get('token'):
        create_card(
            "Authentication Required",
            "Please login to access your personalized dashboard.",
            "🔐"
        )
        return
    
    # Welcome message
    user_email = st.session_state.user.get('email', 'User') if st.session_state.user else 'User'
    create_card(
        f"Welcome back, {user_email}! 🎵",
        "Your AI-powered music career assistant is ready to help you succeed.",
        "👋"
    )
    
    # Main metrics section
    create_section_header("Activity Overview", "📈")
    
    try:
        # Get user stats from backend
        col1, col2, col3, col4 = st.columns(4)
        
        # Personal documents count
        try:
            kb_response = requests.get(
                "https://the-manager-emyz.onrender.com/api/personal-kb/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if kb_response.status_code == 200:
                personal_docs = len(kb_response.json())
            else:
                personal_docs = 0
        except:
            personal_docs = 0
        
        # Conversations count
        try:
            chat_response = requests.get(
                "https://the-manager-emyz.onrender.com/api/chat/conversations/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if chat_response.status_code == 200:
                conversations = len(chat_response.json())
            else:
                conversations = 0
        except:
            conversations = 0
        
        with col1:
            create_metric_card("Personal Documents", personal_docs, "📚")
        with col2:
            create_metric_card("Chat Conversations", conversations, "💬")
        with col3:
            create_metric_card("Suggestions Used", "Coming Soon", "🎯")
        with col4:
            create_metric_card("Days Active", "1", "📅")
            
    except Exception as e:
        st.error(f"Failed to load metrics: {str(e)}")
    
    # Quick actions section
    create_section_header("Quick Actions", "⚡")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if create_action_button("Start New Chat", "💬", "quick_chat"):
            st.session_state.current_page = 'Chat'
            st.rerun()
    
    with col2:
        if create_action_button("Upload Document", "📁", "quick_upload"):
            st.session_state.current_page = 'Knowledgebase'
            st.rerun()
    
    with col3:
        if create_action_button("Get Suggestions", "💡", "quick_suggest"):
            st.session_state.current_page = 'Consultancy'
            st.rerun()
    
    # Recent activity section
    create_section_header("Recent Activity", "🕒")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Recent documents
            kb_response = requests.get(
                "https://the-manager-emyz.onrender.com/api/personal-kb/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if kb_response.status_code == 200:
                recent_docs = kb_response.json()[:5]  # Last 5 documents
                if recent_docs:
                    create_card(
                        "Recent Documents",
                        "".join([f"<p>📄 {doc['title']} ({doc['file_type']}) - {doc['uploaded_at'][:10]}</p>" for doc in recent_docs]),
                        "📚"
                    )
                else:
                    create_card(
                        "Recent Documents",
                        "No documents uploaded yet. Start by uploading your first document!",
                        "📚"
                    )
        except Exception as e:
            create_card(
                "Recent Documents",
                f"Unable to load documents: {str(e)}",
                "❌"
            )
    
    with col2:
        try:
            # Recent conversations
            chat_response = requests.get(
                "https://the-manager-emyz.onrender.com/api/chat/conversations/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if chat_response.status_code == 200:
                recent_chats = chat_response.json()[:3]  # Last 3 conversations
                if recent_chats:
                    create_card(
                        "Recent Conversations",
                        "".join([f"<p>💬 {chat.get('title', 'Untitled')} - {chat['started_at'][:10]}</p>" for chat in recent_chats]),
                        "💬"
                    )
                else:
                    create_card(
                        "Recent Conversations",
                        "No conversations yet. Start your first AI chat!",
                        "💬"
                    )
        except Exception as e:
            create_card(
                "Recent Conversations",
                f"Unable to load conversations: {str(e)}",
                "❌"
            )
    
    # Tips and insights section
    create_section_header("Tips for Success", "💡")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_card(
            "Getting Started",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>📁 Upload your first document to build your knowledgebase</li>
                <li>💬 Start a conversation with AI for personalized advice</li>
                <li>💡 Check consultancy for strategic recommendations</li>
                <li>📊 Monitor your progress in this dashboard</li>
            </ul>
            """,
            "🚀"
        )
    
    with col2:
        create_card(
            "Best Practices",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>📚 Upload regularly to keep your knowledgebase updated</li>
                <li>🎯 Be specific in your AI conversations for better advice</li>
                <li>📈 Review suggestions before implementing them</li>
                <li>🔄 Track how following AI advice impacts your career</li>
            </ul>
            """,
            "⭐"
        )
    
    # System status section
    create_section_header("System Status", "🔧")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_card(
            "Backend Status",
            "<p style='color: #00ff88; font-weight: 600;'>✅ Connected</p>",
            "🔗"
        )
    
    with col2:
        create_card(
            "Authentication",
            "<p style='color: #00ff88; font-weight: 600;'>✅ Active</p>",
            "🔐"
        )
    
    with col3:
        create_card(
            "Vector Database",
            "<p style='color: #ffaa00; font-weight: 600;'>ℹ️ Qdrant</p>",
            "🗄️"
        )
    
    with col4:
        create_card(
            "AI Integration",
            "<p style='color: #ffaa00; font-weight: 600;'>ℹ️ OpenAI</p>",
            "🤖"
        ) 