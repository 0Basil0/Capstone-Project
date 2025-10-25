from datetime import datetime
import os
from google import genai
import requests
from PIL import Image
from io import BytesIO
os.environ["GEMINI_API_KEY"] = "AIzaSyBYsuwdWzG5Vm70uJ_AuzKljDES4FpUxyA"
# os.environ["GEMINI_API_KEY"] = "AIzaSyDWDJ-Ul87SKmcUdmkRWvCzus2vuLtI6KU"


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


def generate_daily_meals(allergy_names=None, meals_today=None):
    """Generate a simple breakfast/lunch/dinner suggestion using the genai client.
    Returns a dict: { 'breakfast': {name, ingredients, description}, 'lunch': {...}, 'dinner': {...} }
    allergy_names: optional list of allergy names to avoid in suggestions.
    """
 

    if allergy_names is None:
        allergy_names = []
    if meals_today is None:
        meals_today = []
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        client = genai.Client()
        avoid = ', '.join(allergy_names) if allergy_names else 'none'
        prompt = (
            f"Generate a STRICT JSON object with three fields: breakfast, lunch, dinner.\n"
            f"Each field must be an object with the keys: name, ingredients, description.\n"
            f"For each of those keys, return a single STRING that contains the English text, then a space, then two slashes `//`, then a space, then the Arabic translation.\n"
            f"Example: \"name\": \"Pancakes // فطائر\" , \"ingredients\": \"flour, milk // دقيق, حليب\"\n"
            f"Ingredients should be a comma-separated list. Descriptions should be one short sentence.\n"
            f"Avoid any ingredients that commonly contain these allergens: {avoid}.\n"
            f"Do not repeat meal names across breakfast, lunch, and dinner.\n"
            f"Do not include any additional text outside the JSON object — RETURN ONLY VALID JSON.\n"
            f"If the user already had meals today: {meals_today}, do not include those meals.\n"
            f"Use the `//` delimiter exactly (space on both sides) to separate English and Arabic in each field.\n"
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
        # Prefer saving generated images to MEDIA_ROOT (user-generated content).
        # This way they are served via /media/ and do not require collectstatic.
        try:
            from django.conf import settings
            media_root = getattr(settings, 'MEDIA_ROOT', None)
        except Exception:
            media_root = None

        if media_root:
            # ensure output_path does not start with a leading slash
            output_path_rel = output_path.lstrip('/\\')
            full_output_path = os.path.join(media_root, output_path_rel)
        else:
            static_dir = os.path.join(base_dir, 'static')
            output_path_rel = output_path.lstrip('/\\')
            full_output_path = os.path.join(static_dir, output_path_rel)

        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        # Format the prompt safely for URL
        prompt = prompt.split(":")[0]
        safe_prompt = prompt.replace(" ", "%20")
        # Use external image generation API
        print(f"Requesting image generation for prompt: {safe_prompt}")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
        response = requests.get(url, timeout=30)
        print(response.status_code, response.headers.get('Content-Type'))
        if response.status_code == 200:
            print("Image generation successful, processing image...")
            img = Image.open(BytesIO(response.content)).convert('RGBA')
            # Crop bottom pixels if requested and image is tall enough
            width, height = img.size
            crop_h = min(crop_bottom_px, height//6)
            cropped_img = img.crop((0, 0, width, max(1, height - crop_h)))
            # Save into the app static folder (so development flow remains unchanged)
            cropped_img.save(full_output_path)
            print(f"Generated image saved to: {full_output_path}")

            # Return URL path suitable for templates: prefer /media/ if we saved to MEDIA_ROOT
            if media_root:
                # return an URL using MEDIA_URL
                try:
                    from django.conf import settings as dj_settings
                    media_url = getattr(dj_settings, 'MEDIA_URL', '/media/')
                except Exception:
                    media_url = '/media/'
                return (media_url + output_path_rel.replace('\\', '/')).replace('//', '/')
            else:
                # fallback to static path
                try:
                    from django.conf import settings
                    static_root = getattr(settings, 'STATIC_ROOT', None)
                    if static_root:
                        # Also copy into STATIC_ROOT so WhiteNoise can serve it (best-effort)
                        target_path = os.path.join(static_root, *output_path_rel.replace('\\', '/').split('/'))
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        cropped_img.save(target_path)
                except Exception:
                    pass
                return '/static/' + output_path_rel.replace('\\', '/')
        return None
    except Exception:
        return None

