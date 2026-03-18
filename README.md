# 📄 AI PDF Insight Extractor

A smart, Streamlit-based web application that uses Google's Gemini AI to automatically read and extract key insights from PDF documents. 

Whether it's a hotel brochure, an invoice, or a product manual, this tool instantly pulls out the most important details (like room service times, pricing, or instructions) and allows you to ask specific questions about the document.

## 🌟 Features
- **Fast PDF Parsing:** Extracts text directly from multi-page PDFs using `PyMuPDF`.
- **Dynamic AI Analysis:** Automatically detects and utilizes the best available Gemini model via the Google Generative AI API.
- **Custom Queries:** Ask specific questions about the uploaded document.
- **Save Insights:** Download the AI's analysis locally as a text file.

## 🚀 How to Run Locally

### Prerequisites
1. Python 3.9+ installed.
2. A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation
1. Clone this repository to your local machine:
   ```bash
   git clone <your-github-repo-url>
   cd pdf_analyzer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   streamlit run app.py
   ```
5. Open your web browser and go to `http://localhost:8501`. Provide your Gemini API key in the configuration sidebar to get started!

## 🛠️ Built With...
- [Streamlit](https://streamlit.io/) - For the interactive Web UI
- [PyMuPDF](https://pymupdf.readthedocs.io/) - For lightning-fast PDF text extraction
- [Google Generative AI](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models) - For the brain powering the document analysis
