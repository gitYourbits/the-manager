import streamlit as st
import requests
import json
import os
from theme import create_page_header, create_card, create_action_button, create_section_header

def render():
    create_page_header("Knowledgebase", "Manage your documents and search your knowledge", "📚")
    
    # Check authentication
    if not st.session_state.get('token'):
        create_card(
            "Authentication Required",
            "Please login to access your knowledgebase.",
            "🔐"
        )
        return
    
    # Tabs for Global and Personal KB
    tab1, tab2 = st.tabs(["📁 Personal Knowledgebase", "🌍 Global Knowledgebase"])
    
    with tab1:
        create_section_header("Personal Documents", "📁")
        
        # File upload section
        create_card(
            "Upload New Document",
            "Upload your documents to build your personal knowledgebase. Supported formats: TXT, PDF, DOCX",
            "📤"
        )
        
        uploaded_file = st.file_uploader(
            "Choose a file to upload",
            type=['txt', 'pdf', 'docx'],
            key="personal_upload",
            help="Select a document to add to your personal knowledgebase"
        )
        
        if uploaded_file is not None:
            st.markdown(f"""
            <div style="background: rgba(0, 255, 136, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #00ff88; margin: 1rem 0;">
                <p style="margin: 0; color: #00ff88;"><strong>Selected:</strong> {uploaded_file.name}</p>
                <p style="margin: 0.5rem 0 0 0; color: #cccccc; font-size: 0.9rem;">Size: {uploaded_file.size} bytes | Type: {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if create_action_button("Upload to Personal KB", "🚀", "upload_personal"):
                try:
                    with st.spinner("Uploading and processing document..."):
                        files = {'file': uploaded_file}
                        data = {
                            'title': uploaded_file.name,
                            'file_type': uploaded_file.name.split('.')[-1]
                        }
                        response = requests.post(
                            "http://34.60.140.141:8000/api/personal-kb/",
                            headers={"Authorization": f"Bearer {st.session_state.token}"},
                            files=files,
                            data=data
                        )
                        if response.status_code == 201:
                            st.success("🎉 Document uploaded and processed successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Upload failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Upload failed: {str(e)}")
        
        # List personal documents
        create_section_header("Your Documents", "📋")
        
        try:
            response = requests.get(
                "http://34.60.140.141:8000/api/personal-kb/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if response.status_code == 200:
                documents = response.json()
                if documents:
                    for doc in documents:
                        create_card(
                            f"📄 {doc['title']}",
                            f"""
                            <p><strong>Type:</strong> {doc['file_type'].upper()}</p>
                            <p><strong>Uploaded:</strong> {doc['uploaded_at'][:10]}</p>
                            <p><strong>Status:</strong> <span style="color: #00ff88;">✅ Processed</span></p>
                            """,
                            "📄"
                        )
                        
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            if create_action_button("Delete", "🗑️", f"del_personal_{doc['id']}"):
                                try:
                                    del_response = requests.delete(
                                        f"http://34.60.140.141:8000/api/personal-kb/{doc['id']}/",
                                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                                    )
                                    if del_response.status_code == 204:
                                        st.success("🗑️ Document deleted successfully!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Delete failed: {str(e)}")
                else:
                    create_card(
                        "No Documents Yet",
                        "Upload your first document to start building your personal knowledgebase. This will help the AI provide more personalized recommendations.",
                        "📝"
                    )
        except Exception as e:
            create_card(
                "Error Loading Documents",
                f"Unable to load your documents: {str(e)}",
                "❌"
            )
        
        # Semantic search section
        create_section_header("Search Personal Knowledgebase", "🔍")
        
        create_card(
            "Search Your Documents",
            "Search through your uploaded documents using natural language queries. The AI will find relevant information from your personal knowledgebase.",
            "🔍"
        )
        
        search_query = st.text_input("Enter your search query", key="personal_search", placeholder="e.g., music marketing strategies, release planning...")
        
        if create_action_button("Search Personal KB", "🔍", "search_personal"):
            if search_query:
                try:
                    with st.spinner("Searching your knowledgebase..."):
                        response = requests.post(
                            "http://34.60.140.141:8000/api/personal-kb/search/",
                            headers={"Authorization": f"Bearer {st.session_state.token}"},
                            json={"query": search_query}
                        )
                        if response.status_code == 200:
                            results = response.json()
                            if results.get('result'):
                                create_card(
                                    "Search Results",
                                    "".join([f"<p style='margin-bottom: 1rem; padding: 0.5rem; background: rgba(255, 68, 68, 0.1); border-radius: 8px;'>{result['payload'].get('chunk', 'No content')}</p>" for result in results.get('result', [])]),
                                    "📄"
                                )
                            else:
                                st.info("No results found in your personal knowledgebase.")
                        else:
                            st.error("❌ Search failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Search failed: {str(e)}")
            else:
                st.warning("Please enter a search query.")
    
    with tab2:
        create_section_header("Global Knowledgebase", "🌍")
        
        create_card(
            "Global Documents",
            "Access shared knowledge from the global knowledgebase. This contains industry-wide information and best practices.",
            "🌍"
        )
        
        # List global documents (read-only for regular users)
        try:
            response = requests.get(
                "http://34.60.140.141:8000/api/global-kb/",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if response.status_code == 200:
                documents = response.json()
                if documents:
                    for doc in documents:
                        create_card(
                            f"📄 {doc['title']}",
                            f"""
                            <p><strong>Type:</strong> {doc['file_type'].upper()}</p>
                            <p><strong>Added:</strong> {doc['uploaded_at'][:10]}</p>
                            <p><strong>Access:</strong> <span style="color: #ffaa00;">🌍 Global</span></p>
                            """,
                            "📄"
                        )
                else:
                    create_card(
                        "No Global Documents",
                        "No global documents are currently available.",
                        "📝"
                    )
        except Exception as e:
            create_card(
                "Error Loading Global Documents",
                f"Unable to load global documents: {str(e)}",
                "❌"
            )
        
        # Global semantic search
        create_section_header("Search Global Knowledgebase", "🔍")
        
        create_card(
            "Search Global Documents",
            "Search through the global knowledgebase for industry insights and best practices.",
            "🔍"
        )
        
        global_search_query = st.text_input("Enter your search query", key="global_search", placeholder="e.g., music industry trends, artist development...")
        
        if create_action_button("Search Global KB", "🔍", "search_global"):
            if global_search_query:
                try:
                    with st.spinner("Searching global knowledgebase..."):
                        response = requests.post(
                            "http://34.60.140.141:8000/api/global-kb/search/",
                            json={"query": global_search_query}
                        )
                        if response.status_code == 200:
                            results = response.json()
                            if results.get('result'):
                                create_card(
                                    "Global Search Results",
                                    "".join([f"<p style='margin-bottom: 1rem; padding: 0.5rem; background: rgba(255, 68, 68, 0.1); border-radius: 8px;'>{result['payload'].get('chunk', 'No content')}</p>" for result in results.get('result', [])]),
                                    "📄"
                                )
                            else:
                                st.info("No results found in the global knowledgebase.")
                        else:
                            st.error("❌ Global search failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Global search failed: {str(e)}")
            else:
                st.warning("Please enter a search query.")
    
    # Knowledgebase tips section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    create_section_header("Knowledgebase Tips", "💡")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_card(
            "Document Management",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>📁 Upload various document types (TXT, PDF, DOCX)</li>
                <li>📚 Organize documents by category or purpose</li>
                <li>🔄 Keep your knowledgebase updated regularly</li>
                <li>🗑️ Remove outdated or irrelevant documents</li>
            </ul>
            """,
            "📁"
        )
    
    with col2:
        create_card(
            "Effective Searching",
            """
            <ul style="color: #cccccc; margin: 0; padding-left: 1.5rem;">
                <li>🎯 Use specific, descriptive search terms</li>
                <li>📖 Ask questions in natural language</li>
                <li>🔍 Combine personal and global searches</li>
                <li>💡 Use search results to inform your decisions</li>
            </ul>
            """,
            "🔍"
        ) 