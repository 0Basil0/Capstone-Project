import os
from google import genai


def generate_allergy_description(name: str) -> str:
    # Call the genai client to create a short description for an allergy name.
    
    if not name:
        return ""
    os.environ["GEMINI_API_KEY"] = "AIzaSyBYsuwdWzG5Vm70uJ_AuzKljDES4FpUxyA"
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

    try:
        client = genai.Client()
        prompt = f"Write a concise (1-2 sentence) description of the allergy named '{name}', including typical triggers and a short note on severity." 
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"parts": [{"text": prompt}]}],
        )

        
        text = response.text
        if not text:
            text = str(response)

        return text or ""
    except Exception:
        return ""


