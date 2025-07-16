import streamlit as st
from theme import apply_custom_theme, create_page_header
from pages import Auth, Chat, Knowledgebase, Consultancy, Dashboard

# Apply custom theme
apply_custom_theme()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #ff4444; margin-bottom: 0;">🎵 AI Manager</h2>
        <p style="color: #cccccc; font-size: 0.9rem;">Music Artist Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation menu
    menu_items = {
        'Dashboard': ('📊', 'Overview & Analytics'),
        'Chat': ('💬', 'AI Conversations'),
        'Knowledgebase': ('📚', 'Document Management'),
        'Consultancy': ('💡', 'AI Recommendations'),
        'Auth': ('🔐', 'Authentication')
    }
    
    for page_name, (icon, description) in menu_items.items():
        if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    st.markdown("---")
    
    # User info
    if st.session_state.get('user'):
        st.markdown(f"""
        <div style="background: rgba(255, 68, 68, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ff4444;">
            <p style="color: #ffffff; margin: 0; font-weight: 600;">👤 {st.session_state.user.get('email', 'User')}</p>
            <p style="color: #cccccc; margin: 0; font-size: 0.8rem;">Logged In</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.current_page = 'Auth'
            st.rerun()
    else:
        st.markdown("""
        <div style="background: rgba(255, 170, 0, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ffaa00;">
            <p style="color: #ffffff; margin: 0; font-weight: 600;">⚠️ Not Authenticated</p>
            <p style="color: #cccccc; margin: 0; font-size: 0.8rem;">Please login to continue</p>
        </div>
        """, unsafe_allow_html=True)

# Main content area
def main():
    # Page routing
    if st.session_state.current_page == 'Dashboard':
        Dashboard.render()
    elif st.session_state.current_page == 'Chat':
        Chat.render()
    elif st.session_state.current_page == 'Knowledgebase':
        Knowledgebase.render()
    elif st.session_state.current_page == 'Consultancy':
        Consultancy.render()
    elif st.session_state.current_page == 'Auth':
        Auth.render()
    else:
        Dashboard.render()

if __name__ == "__main__":
    main()