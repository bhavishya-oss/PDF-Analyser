import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="PDF Insight Extractor", page_icon="📄", layout="centered")

# Custom CSS for a better UI
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 8px;
    }
    .header-style {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header-style">📄 AI PDF Insight Extractor</p>', unsafe_allow_html=True)
st.write("Upload a PDF document (e.g., a hotel brochure, menu, or manual) and let AI extract the most important details for you.")

# Configure Gemini from .env
env_key = os.getenv("GEMINI_API_KEY", "")
if env_key and env_key != "your_api_key_here":
    genai.configure(api_key=env_key)
else:
    st.warning("⚠️ Please ensure your Gemini API Key is set in the .env file!")

# Functions
def extract_text_from_pdf(pdf_bytes):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    # Open the PDF from bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(min(doc.page_count, 20)): # limit to first 20 pages for safety
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def analyze_document_with_ai(text, custom_prompt=""):
    """Uses Gemini API to extract important details from the text."""
    try:
        # Dynamically find a suitable text generation model available to this API key
        available_models = [m.name.replace("models/", "") for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        
        model_id = None
        # Preferred models in order of fallback
        for preferred in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro", "gemini-1.0-pro"]:
            if preferred in available_models:
                model_id = preferred
                break
                
        if not model_id and available_models:
            model_id = available_models[0] # Grab whatever is available
            
        if not model_id:
            return "Could not find any supported Models for this API Key."

        model = genai.GenerativeModel(model_id)
        
        base_prompt = "You are an AI assistant tasked with analyzing a document. Extract all important details in a well-structured, easy-to-read markdown format. For example, if it's a hotel PDF, extract room service details, food timings, amenities, rules, etc. Be concise but comprehensive."
        
        if custom_prompt:
            prompt = f"Here is a document:\n\n{text}\n\nTask: {custom_prompt}"
        else:
            prompt = f"Here is a document:\n\n{text}\n\n{base_prompt}"

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the AI: {str(e)}"

# Main UI
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

custom_query = st.text_input("Specific question (optional)", placeholder="e.g., What are the breakfast timings?")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if st.button("Analyze PDF"):
        env_key = os.getenv("GEMINI_API_KEY", "")
        if not env_key or env_key == "your_api_key_here":
             st.error("⚠️ Please provide a valid Gemini API Key in the .env file.")
        else:
            with st.spinner("Extracting text and analyzing with AI... This might take a few seconds."):
                # 1. Extract text
                pdf_bytes = uploaded_file.read()
                extracted_text = extract_text_from_pdf(pdf_bytes)
                
                if not extracted_text.strip():
                    st.error("Could not extract any text from the PDF. It might be an image-based PDF without OCR.")
                else:
                    # 2. Analyze with AI
                    insights = analyze_document_with_ai(extracted_text, custom_query)
                    
                    st.subheader("💡 Extracted Insights")
                    st.markdown(insights)
                    
                    # Option to download results
                    st.download_button(
                        label="Download Analysis as TXT",
                        data=insights,
                        file_name="pdf_analysis.txt",
                        mime="text/plain"
                    )
