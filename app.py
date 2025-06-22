import streamlit as st
import requests
import os

# Configure the app
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("Document Question Answering System")

# API configuration
# Use service name when running in Docker, localhost when running locally
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

# Main document QA form
with st.form("qa_form"):
    uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt", "csv"])
    question = st.text_area("Enter your question")
    submitted = st.form_submit_button("Send")

if submitted:
    if not uploaded_file or not question:
        st.error("Please upload a document and enter a question")
    else:
        with st.spinner("Processing your request..."):
            try:
                # Save file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Send to API
                with open(temp_path, "rb") as f:
                    response = requests.post(
                        f"{API_URL}/process",
                        files={"file": (uploaded_file.name, f)},
                        data={"question": question}
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Processing complete!")
                    
                    st.subheader("Answer")
                    st.write(result.get("answer", "No answer found"))
                    
                    st.subheader("Supporting Context")
                    st.write(result.get("context", "No context available"))
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to process request: {str(e)}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)