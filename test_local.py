from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

def load_file_content(file_path):
    """Load content from a text file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def analyze_parking_local(image_path):
    """Local version for testing - takes a file path instead of HTTP upload"""
    
    try:
        # Set up the API client (same as your original script)
        load_dotenv()
        api_key = os.getenv("API_KEY")
        
        if not api_key:
            print("Error: API_KEY not found in environment variables")
            return None
        
        client = genai.Client(api_key=api_key)
        
        # Load the text files
        try:
            system_instruction = load_file_content("system_instructions2.txt")
            prompt = load_file_content("prompt2.txt")
        except FileNotFoundError as e:
            print(f"Error: Required file not found: {e}")
            return None
        
        # Upload the image to Gemini
        gemini_file = client.files.upload(file=image_path)
        
        # Make the API call (identical to Cloud Function)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            ),
            contents=[gemini_file, prompt],
        )
        
        return response.text
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None

# Test it locally
if __name__ == "__main__":
    # Test with a local image file
    image_path = "beach_st_signs/118.jpg"  # or whatever test image you have
    
    print("Testing parking analysis...")
    result = analyze_parking_local(image_path)
    
    if result:
        print("\n" + "="*50)
        print("ANALYSIS RESULT:")
        print("="*50)
        print(result)
    else:
        print("Analysis failed - check the error messages above")