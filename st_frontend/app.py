import streamlit as st
from pages import Auth, Chat, Knowledgebase, Consultancy, Dashboard

st.set_page_config(page_title="AI Manager", page_icon="🎵", layout="wide")

# Custom CSS for modern, soothing UI
def set_custom_theme():
    st.markdown(
        """
        <style>
        body { background: linear-gradient(135deg, #e0e7ff 0%, #f0f4ff 100%) !important; }
        .stApp { background: transparent !important; }
        .block-container { padding-top: 2rem; }
        .sidebar .sidebar-content { background: #312e81 !important; color: #fff; }
        .sidebar .sidebar-content a { color: #a5b4fc !important; }
        .sidebar .sidebar-content a:hover { color: #fff !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
set_custom_theme()

st.sidebar.title("🎵 AI Manager")
page = st.sidebar.radio(
    "Go to",
    ("Dashboard", "Chat", "Knowledgebase", "Consultancy", "Auth"),
    index=0
)

if page == "Dashboard":
    Dashboard.render()
elif page == "Chat":
    Chat.render()
elif page == "Knowledgebase":
    Knowledgebase.render()
elif page == "Consultancy":
    Consultancy.render()
else:
    Auth.render() 