import streamlit as st
import fitz # PyMuPDF
from ai_functions import summarize_notes, generate_flashcards, client # Import the functions and client

# --- Configuration and Title ---
st.set_page_config(page_title="Gemini AI Study Buddy", layout="wide")
st.title("📚 Gemini AI Study Buddy")
st.markdown("---")

# --- Function to Extract Text from PDF ---
def extract_text_from_pdf(uploaded_file):
    """Uses PyMuPDF to extract text from an uploaded PDF file."""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return ""

# --- Content Input Section (Sidebar) ---
notes_text = ""
with st.sidebar:
    st.header("1. Input Your Material")
    
    input_method = st.radio("Choose Input Method:", ("Paste Text", "Upload File (PDF/TXT)"), index=0)
    
    if input_method == "Paste Text":
        notes_text = st.text_area("Paste your notes here:", height=300)
        
    elif input_method == "Upload File (PDF/TXT)":
        uploaded_file = st.file_uploader("Upload a document (.pdf or .txt)", type=["pdf", "txt"])
        
        if uploaded_file is not None:
            # Handle PDF Upload
            if uploaded_file.type == "application/pdf":
                notes_text = extract_text_from_pdf(uploaded_file)
                if notes_text:
                    st.success(f"PDF content loaded ({len(notes_text)} characters).")
            # Handle TXT Upload
            elif uploaded_file.type == "text/plain":
                 notes_text = uploaded_file.read().decode("utf-8")
                 st.success(f"Text file content loaded ({len(notes_text)} characters).")
            else:
                 st.warning("Please upload a supported file type (.pdf or .txt).")
            

# --- Main App Logic (After Content is Loaded) ---
if notes_text:
    
    st.header("2. Study Tools Powered by Gemini")
    
    # Tabbed interface for different tools
    tab1, tab2 = st.tabs(["📝 Summary & Action Plan", "🗂️ Flashcards"])
    
    with tab1:
        st.subheader("Key Takeaways and Study Strategy")
        if st.button("Generate Summary & Study Tips", key="summary_btn"):
            with st.spinner("Gemini is analyzing and summarizing your notes..."):
                try:
                    # Call the combined summarization function
                    result_markdown = summarize_notes(notes_text)
                    st.markdown("---")
                    st.markdown(result_markdown)
                except Exception as e:
                    st.error(f"An error occurred with the Gemini API. Check your key and context length. Error: {e}")

    with tab2:
        st.subheader("Custom Flashcard Deck Generator")
        card_count = st.slider("Number of Flashcards to Generate", 5, 20, 10)
        if st.button("Generate Flashcards", key="flashcard_btn"):
            with st.spinner(f"Gemini is generating {card_count} flashcards..."):
                try:
                    # Call the flashcard function
                    flashcards_markdown = generate_flashcards(notes_text, count=card_count)
                    
                    st.markdown("---")
                    st.markdown("### Generated Flashcards (Question : Answer)")
                    st.markdown(flashcards_markdown)
                    st.success("Flashcards ready! Use the table for active recall.")
                except Exception as e:
                    st.error(f"An error occurred with the Gemini API. Error: {e}")

else:
    st.info("Please paste your study notes or upload a file in the left sidebar to activate the study tools.")
    