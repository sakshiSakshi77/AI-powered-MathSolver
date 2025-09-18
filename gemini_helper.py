import os
import google.generativeai as genai

def get_gemini_explanation(prompt):
    # Set API key from environment variable if not already set
    if 'GOOGLE_API_KEY' not in os.environ:
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyC-86PllHzqeW4pGl96IbeW99qwENNHNBg'
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Gemini error: {e}" 