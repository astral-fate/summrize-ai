import streamlit as st
import PyPDF2
import openai

# Read the API key from Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in Streamlit secrets.")
    st.stop()

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to call OpenAI API for summarization
def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=150  # Adjust as needed
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred while summarizing: {e}")
        return None

# Streamlit app
def main():
    st.title("PDF Summarizer with OpenAI")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)
        st.write("### Extracted Text")
        st.write(text[:1000] + "...")  # Display first 1000 characters for preview
        
        # Summarize button
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(text)
                if summary:
                    st.write("### Summary")
                    st.write(summary)

if __name__ == "__main__":
    main()
