import os
from google import genai
import requests
from PIL import Image
from io import BytesIO
os.environ["GEMINI_API_KEY"] = "AIzaSyBYsuwdWzG5Vm70uJ_AuzKljDES4FpUxyA"

def generate_allergy_description(name: str) -> str:
    # Call the genai client to create a short description for an allergy name.
    
    if not name:
        return ""
    
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


def generate_daily_meals(allergy_names=None):
    """Generate a simple breakfast/lunch/dinner suggestion using the genai client.
    Returns a dict: { 'breakfast': {name, ingredients, description}, 'lunch': {...}, 'dinner': {...} }
    allergy_names: optional list of allergy names to avoid in suggestions.
    """
    import os
    from google import genai
    if allergy_names is None:
        allergy_names = []
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        client = genai.Client()
        avoid = ', '.join(allergy_names) if allergy_names else 'none'
        prompt = (
            f"Generate a JSON object with three fields: breakfast, lunch, dinner. "
            f"Each field should contain an object with name, ingredients (comma-separated), and a one-sentence description. "
            f"Avoid any ingredients that commonly contain these allergens: {avoid}. "
            f"Return ONLY valid JSON. Keep names short and ingredients concise."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"parts": [{"text": prompt}]}],
        )
        text = response.text or str(response)

        # Try to extract JSON from the model output
        import json
        try:
            data = json.loads(text)
        except Exception:
            # If model returned non-strict JSON (surrounding text), try to find JSON substring
            import re
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                try:
                    data = json.loads(m.group(0))
                except Exception:
                    return {}
            else:
                return {}

        return data
    except Exception:
        return {}



def generate_image(prompt, output_path="output.png", crop_bottom_px=50):
    # This implementation saves the generated image into the app's static folder
    # output_path is treated as a relative path under main_app/static/, e.g. 'images/generated/user/day_breakfast.png'
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # path to main_app
        static_dir = os.path.join(base_dir, 'static')
        full_output_path = os.path.join(static_dir, output_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        # Format the prompt safely for URL
        safe_prompt = prompt.replace(" ", "%20")
        # Use external image generation API
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model=sdxl"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert('RGBA')
            # Crop bottom pixels if requested and image is tall enough
            width, height = img.size
            crop_h = min(crop_bottom_px, height//6)
            cropped_img = img.crop((0, 0, width, max(1, height - crop_h)))
            cropped_img.save(full_output_path)
            # Return URL path suitable for templates: /static/<output_path>
            return '/static/' + output_path.replace('\\', '/')
        return None
    except Exception:
        return None

generate_image("image for human ")
