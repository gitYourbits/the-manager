import streamlit as st
import requests
import json
import re
from theme import create_page_header, create_card, create_action_button

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, ""

def validate_username(username):
    """Validate username"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if not username.replace('_', '').replace('-', '').isalnum():
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, ""

def render():
    create_page_header("Authentication", "Secure access to your AI Manager", "🔐")
    
    # Initialize session state
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check if already authenticated
    if st.session_state.token:
        create_card(
            "Welcome Back! 🎉",
            f"<p style='font-size: 1.2rem; color: #00ff88;'>You are logged in as <strong>{st.session_state.user.get('email', 'User')}</strong></p>",
            "✅"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if create_action_button("Logout", "🚪", "logout_btn"):
                st.session_state.token = None
                st.session_state.user = None
                st.rerun()
        return
    
    # Auth forms in a centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Tabs for Login and Register
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            create_card(
                "Login to Your Account",
                """
                <p style="margin-bottom: 1rem;">Enter your credentials to access your personalized AI Manager dashboard.</p>
                """,
                "🔑"
            )
            
            with st.form("login_form", clear_on_submit=True):
                email = st.text_input("📧 Email Address", placeholder="Enter your email")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if not email or not password:
                        st.error("Please fill in all fields")
                    else:
                        with st.spinner("Authenticating..."):
                            try:
                                response = requests.post(
                                    "http://34.60.140.141:8000/api/login/",
                                    json={"email": email, "password": password}
                                )
                                if response.status_code == 200:
                                    data = response.json()
                                    st.session_state.token = data['access']
                                    st.session_state.user = {"email": email}
                                    st.success("🎉 Login successful! Redirecting...")
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid credentials. Please check your email and password.")
                            except Exception as e:
                                st.error(f"❌ Login failed: {str(e)}")
        
        with tab2:
            create_card(
                "Create New Account",
                """
                <p style="margin-bottom: 1rem;">Join AI Manager to get personalized music career assistance.</p>
                """,
                "📝"
            )
            
            with st.form("register_form", clear_on_submit=True):
                email = st.text_input("📧 Email Address", key="reg_email", placeholder="Enter your email")
                username = st.text_input("👤 Username", key="reg_username", placeholder="Choose a username")
                password = st.text_input("🔒 Password", type="password", key="reg_password", placeholder="Create a strong password (min 8 characters)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                is_artist = st.checkbox("🎵 I am a music artist", key="is_artist_check")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("🚀 Create Account", use_container_width=True)
                
                if submit:
                    # Client-side validation
                    validation_errors = []
                    
                    # Check for empty fields
                    if not email.strip():
                        validation_errors.append("Email is required")
                    elif not validate_email(email):
                        validation_errors.append("Please enter a valid email address")
                    
                    if not username.strip():
                        validation_errors.append("Username is required")
                    else:
                        is_valid, error_msg = validate_username(username)
                        if not is_valid:
                            validation_errors.append(error_msg)
                    
                    if not password:
                        validation_errors.append("Password is required")
                    else:
                        is_valid, error_msg = validate_password(password)
                        if not is_valid:
                            validation_errors.append(error_msg)
                    
                    if validation_errors:
                        st.error("❌ Please fix the following errors:\n" + "\n".join([f"• {error}" for error in validation_errors]))
                    else:
                        with st.spinner("Creating your account..."):
                            try:
                                response = requests.post(
                                    "http://34.60.140.141:8000/api/register/",
                                    json={
                                        "email": email.strip(),
                                        "username": username.strip(),
                                        "password": password,
                                        "is_artist": is_artist
                                    }
                                )
                                if response.status_code == 201:
                                    st.success("🎉 Registration successful! Please login with your new account.")
                                else:
                                    try:
                                        error_data = response.json()
                                        if isinstance(error_data, dict):
                                            # Handle field-specific errors
                                            error_messages = []
                                            for field, errors in error_data.items():
                                                if isinstance(errors, list):
                                                    error_messages.extend([f"{field.title()}: {error}" for error in errors])
                                                else:
                                                    error_messages.append(f"{field.title()}: {errors}")
                                            st.error("❌ " + "\n".join(error_messages))
                                        else:
                                            st.error(f"❌ {error_data}")
                                    except:
                                        st.error("❌ Registration failed. Please try again.")
                            except Exception as e:
                                st.error(f"❌ Registration failed: {str(e)}")
    
    # Footer with additional info
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        create_card(
            "Why AI Manager?",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>🎯 Personalized music career guidance</li>
                <li>📚 Intelligent document management</li>
                <li>💬 AI-powered conversations</li>
                <li>📊 Strategic insights and analytics</li>
                <li>🔒 Secure and private data handling</li>
            </ul>
            """,
            "💡"
        ) 