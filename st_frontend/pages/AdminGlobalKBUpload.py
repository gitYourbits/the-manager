import streamlit as st
import requests

st.title('🛡️ Admin: Global KB Upload')
st.markdown('Upload documents to the **Global Knowledge Base**. Only authenticated users can use this page. For production, restrict to admins.')

# File uploader
uploaded_file = st.file_uploader('Upload TXT, PDF, or DOCX file', type=['txt', 'pdf', 'docx'])
file_type = None
if uploaded_file:
    if uploaded_file.type == 'text/plain':
        file_type = 'txt'
    elif uploaded_file.type == 'application/pdf':
        file_type = 'pdf'
    elif uploaded_file.type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
        file_type = 'docx'
    else:
        st.error('Unsupported file type.')

# Auth token (from session)
token = st.session_state.get('token')

if uploaded_file and file_type and token:
    if st.button('Upload to Global KB'):
        with st.spinner('Uploading and ingesting...'):
            files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {'file_type': file_type}
            headers = {'Authorization': f'Bearer {token}'}
            try:
                response = requests.post(
                    'http://34.60.140.141:8000/api/global_kb_upload/',
                    files=files,
                    data=data,
                    headers=headers
                )
                if response.status_code == 200:
                    st.success(f"Upload successful! Chunks created: {response.json().get('num_chunks')}")
                else:
                    st.error(f"Upload failed: {response.json().get('error', response.text)}")
            except Exception as e:
                st.error(f"Request failed: {e}")
else:
    st.info('Please select a file and ensure you are logged in.')
