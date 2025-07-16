import streamlit as st

def apply_custom_theme():
    """Apply custom black and red theme to Streamlit"""
    st.set_page_config(
        page_title="AI Manager",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for modern black and red theme
    st.markdown("""
    <style>
    /* Global Theme Variables */
    :root {
        --primary-color: #ff4444;
        --primary-dark: #cc3333;
        --secondary-color: #1a1a1a;
        --background-dark: #0d0d0d;
        --surface-dark: #1a1a1a;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
        --accent-red: #ff6666;
        --border-color: #333333;
        --success-color: #00ff88;
        --warning-color: #ffaa00;
        --error-color: #ff4444;
    }
    
    /* Main Background */
    .main .block-container {
        background-color: var(--background-dark);
        color: var(--text-primary);
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--surface-dark);
    }
    
    .css-1d391kg .css-1lcbmhc {
        background-color: var(--surface-dark);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    h1 {
        color: var(--primary-color) !important;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 0 10px rgba(255, 68, 68, 0.3);
    }
    
    h2 {
        color: var(--accent-red) !important;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: var(--text-primary) !important;
        font-size: 1.4rem;
        margin-bottom: 0.8rem;
    }
    
    /* Text Elements */
    p, div, span {
        color: var(--text-secondary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 68, 68, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 68, 68, 0.4);
    }
    
    /* Primary Button */
    .stButton > button[data-baseweb="button"] {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    }
    
    /* Secondary Buttons */
    .stButton > button:not([data-baseweb="button"]) {
        background: linear-gradient(135deg, var(--surface-dark), var(--secondary-color));
        border: 1px solid var(--border-color);
    }
    
    /* Form Elements */
    .stTextInput > div > div > input {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(255, 68, 68, 0.2);
    }
    
    /* File Uploader */
    .stFileUploader > div {
        background-color: var(--surface-dark);
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 2rem;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-color);
    }
    
    /* Tabs */
    .stTabs > div > div > div > div {
        background-color: var(--surface-dark);
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs > div > div > div > div > button {
        background-color: transparent;
        color: var(--text-secondary);
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs > div > div > div > div > button[aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: var(--surface-dark);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary-color);
    }
    
    .stChatMessage[data-testid="chatMessage"] {
        background-color: var(--surface-dark);
    }
    
    /* Metrics */
    .stMetric > div > div {
        background-color: var(--surface-dark);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    
    .stMetric > div > div > div[data-testid="metric-container"] > div[data-testid="metric-value"] {
        color: var(--primary-color);
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stMetric > div > div > div[data-testid="metric-container"] > div[data-testid="metric-label"] {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stAlert[data-testid="stAlert"] {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
    }
    
    /* Info Boxes */
    .stAlert[data-testid="stAlert"] > div[data-testid="stAlert"] {
        background-color: rgba(255, 68, 68, 0.1);
        border-left: 4px solid var(--primary-color);
    }
    
    /* Sidebar Navigation */
    .css-1d391kg .css-1lcbmhc .css-1lcbmhc {
        background-color: var(--surface-dark);
    }
    
    /* Container Styling */
    .stContainer {
        background-color: var(--surface-dark);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Form Styling */
    .stForm {
        background-color: var(--surface-dark);
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid var(--border-color);
    }
    
    /* Checkbox Styling */
    .stCheckbox > div > div {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
        border-radius: 4px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div > div {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Spinner */
    .stSpinner > div > div {
        border-color: var(--primary-color);
        border-top-color: transparent;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background-color: var(--surface-dark);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--surface-dark);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Custom Card Styling */
    .custom-card {
        background: linear-gradient(135deg, var(--surface-dark), var(--secondary-color));
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .custom-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Custom Button Variants */
    .btn-primary {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 68, 68, 0.3) !important;
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, var(--surface-dark), var(--secondary-color)) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1rem;
        }
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
    </style>
    """, unsafe_allow_html=True)

def create_page_header(title, subtitle=None, icon="🎵"):
    """Create a consistent page header with the theme"""
    st.markdown(f"""
    <div class="fade-in" style="text-align: center; margin-bottom: 2rem;">
        <h1>{icon} {title}</h1>
        {f'<p style="color: var(--text-secondary); font-size: 1.1rem; margin-top: -1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_card(title, content, icon="📋"):
    """Create a themed card component"""
    st.markdown(f"""
    <div class="custom-card fade-in">
        <h3 style="color: var(--primary-color); margin-bottom: 1rem;">{icon} {title}</h3>
        <div style="color: var(--text-secondary);">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, icon="📊"):
    """Create a themed metric card"""
    st.markdown(f"""
    <div class="custom-card fade-in" style="text-align: center;">
        <div style="font-size: 2rem; color: var(--primary-color); margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">{value}</div>
        <div style="color: var(--text-secondary);">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def create_action_button(text, icon="⚡", key=None):
    """Create a themed action button"""
    return st.button(f"{icon} {text}", key=key, use_container_width=True)

def create_section_header(title, icon="📋"):
    """Create a consistent section header"""
    st.markdown(f"""
    <div class="slide-in">
        <h2 style="color: var(--accent-red); margin-bottom: 1.5rem;">{icon} {title}</h2>
    </div>
    """, unsafe_allow_html=True) 