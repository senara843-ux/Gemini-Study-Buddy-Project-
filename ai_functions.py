import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

def summarize_notes(notes_text):
    """Generates a key bullet-point summary and study tips from the provided notes."""
    prompt = (
        "You are an expert academic summarizer. Take the following study "
        "material and condense it into a clear, concise summary of 5-7 key "
        "bullet points. Then, based on the summary, provide 3 actionable study tips "
        "and a 3-step action plan for reviewing this material. "
        "Output the result using clear markdown with headings for 'Summary' and 'Action Plan'. "
        f"\n\nSTUDY MATERIAL:\n\n{notes_text}"
    )
    
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"temperature": 0.2}
    )
    return response.text

def generate_flashcards(notes_text, count=10):
    """Generates a specified number of flashcards from the notes."""
    prompt = (
        f"Generate {count} flashcards from the following study material. "
        "Present the output as a two-column Markdown table. "
        "The first column should be 'Question' (a concept or term) and the "
        "second column should be 'Answer' (the definition or explanation). "
        "Do not include any other introductory or concluding text, only the table. "
        f"\n\nSTUDY MATERIAL:\n\n{notes_text}"
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"temperature": 0.5}
    )
    return response.text
