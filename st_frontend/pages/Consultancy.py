import streamlit as st
import requests
import json
from theme import create_page_header, create_card, create_action_button, create_section_header, create_metric_card

def render():
    create_page_header("AI Consultancy", "Get personalized strategic recommendations", "💡")
    
    # Check authentication
    if not st.session_state.get('token'):
        create_card(
            "Authentication Required",
            "Please login to access AI consultancy features.",
            "🔐"
        )
        return
    
    # Introduction section
    create_card(
        "AI-Powered Music Career Guidance",
        """
        <p>Based on your personal knowledgebase and activity patterns, our AI will analyze your data and provide strategic recommendations for your music career.</p>
        <p>The AI considers your uploaded documents, chat history, and industry best practices to generate personalized suggestions.</p>
        """,
        "🎯"
    )
    
    # Main suggestion button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if create_action_button("Get AI Recommendations", "🎯", "get_suggestions"):
            with st.spinner("🤖 Analyzing your data and generating recommendations..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/api/consultancy/suggest/",
                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Success message
                        st.success("✨ AI Recommendations Generated Successfully!")
                        
                        # Suggestions section
                        if data.get('suggestions'):
                            create_section_header("Strategic Recommendations", "🎯")
                            
                            for i, suggestion in enumerate(data['suggestions'], 1):
                                create_card(
                                    f"Recommendation {i}",
                                    f"<p style='font-size: 1.1rem; color: #ffffff;'>{suggestion}</p>",
                                    "💡"
                                )
                        
                        # Recent documents section
                        if data.get('recent_docs'):
                            create_section_header("Recent Activity Analysis", "📚")
                            
                            create_card(
                                "Documents Analyzed",
                                "".join([f"<p>📄 {doc}</p>" for doc in data['recent_docs']]),
                                "📚"
                            )
                        
                        # Action items section
                        create_section_header("Recommended Next Steps", "🚀")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            create_card(
                                "Immediate Actions",
                                """
                                <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                                    <li>📋 Review your recent uploads for insights</li>
                                    <li>🎯 Set specific weekly goals</li>
                                    <li>📅 Plan your next release timeline</li>
                                    <li>🤝 Connect with industry contacts</li>
                                </ul>
                                """,
                                "⚡"
                            )
                        
                        with col2:
                            create_card(
                                "Strategic Planning",
                                """
                                <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                                    <li>📊 Analyze your current position</li>
                                    <li>🎵 Identify growth opportunities</li>
                                    <li>📈 Track progress over time</li>
                                    <li>🔄 Adapt strategies based on results</li>
                                </ul>
                                """,
                                "📈"
                            )
                        
                        # Metrics/insights section
                        create_section_header("Analysis Insights", "📊")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            create_metric_card("Documents Analyzed", len(data.get('recent_docs', [])), "📚")
                        
                        with col2:
                            create_metric_card("Suggestions Generated", len(data.get('suggestions', [])), "💡")
                        
                        with col3:
                            activity_level = "Active" if data.get('recent_docs') else "New User"
                            create_metric_card("Activity Level", activity_level, "📈")
                        
                    else:
                        st.error("❌ Failed to generate suggestions. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error generating suggestions: {str(e)}")
    
    # Additional features section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    create_section_header("Additional Features", "⚡")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if create_action_button("View Career Progress", "📈", "career_progress"):
            create_card(
                "Career Progress Tracking",
                "Track your music career milestones, achievements, and growth over time. This feature is coming soon!",
                "📈"
            )
    
    with col2:
        if create_action_button("Music Industry Trends", "🎵", "industry_trends"):
            create_card(
                "Industry Trend Analysis",
                "Get insights into current music industry trends, market analysis, and emerging opportunities. This feature is coming soon!",
                "🎵"
            )
    
    # Pro tips section
    create_section_header("Pro Tips for Better Results", "💡")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_card(
            "Optimize Your Data",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>📁 Upload documents regularly to keep insights fresh</li>
                <li>📝 Include detailed information about your goals</li>
                <li>🎯 Be specific about your challenges and aspirations</li>
                <li>📊 Share both successes and areas for improvement</li>
            </ul>
            """,
            "📁"
        )
    
    with col2:
        create_card(
            "Maximize AI Benefits",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>🤔 Reflect on suggestions before implementing</li>
                <li>📈 Track how following advice impacts your career</li>
                <li>🔄 Provide feedback to improve future recommendations</li>
                <li>💬 Use chat feature to discuss recommendations</li>
            </ul>
            """,
            "🤖"
        )
    
    # How it works section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    create_section_header("How AI Consultancy Works", "🔬")
    
    create_card(
        "The AI Analysis Process",
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2rem; color: #ff4444; margin-bottom: 0.5rem;">📚</div>
                <p style="color: #cccccc; margin: 0;"><strong>1. Data Collection</strong></p>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Analyzes your documents</p>
            </div>
            <div style="font-size: 1.5rem; color: #ff4444; margin: 0 1rem;">→</div>
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2rem; color: #ff4444; margin-bottom: 0.5rem;">🧠</div>
                <p style="color: #cccccc; margin: 0;"><strong>2. AI Processing</strong></p>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Identifies patterns & insights</p>
            </div>
            <div style="font-size: 1.5rem; color: #ff4444; margin: 0 1rem;">→</div>
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2rem; color: #ff4444; margin-bottom: 0.5rem;">💡</div>
                <p style="color: #cccccc; margin: 0;"><strong>3. Recommendations</strong></p>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Generates personalized advice</p>
            </div>
        </div>
        """,
        "🔬"
    ) 