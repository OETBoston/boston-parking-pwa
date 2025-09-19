import google.generativeai as genai
from dotenv import load_dotenv
import os

def load_file_content(file_path):
    """Load content from a text file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def analyze_parking_local(image_path):
    """Local version for testing - takes a file path instead of HTTP upload"""
    
    try:
        # Set up the API client
        load_dotenv()
        api_key = os.getenv("API_KEY")
        
        if not api_key:
            print("Error: API_KEY not found in environment variables")
            return None
        
        # Configure the API (modern way)
        genai.configure(api_key=api_key)
        print("API configured successfully")
        
        # Load the text files
        try:
            system_instruction = load_file_content("system_instructions2.txt")
            prompt = load_file_content("prompt2.txt")
            print("Prompt files loaded successfully")
        except FileNotFoundError as e:
            print(f"Error: Required file not found: {e}")
            return None
        
        # Upload the image to Gemini
        print(f"Uploading image: {image_path}")
        gemini_file = genai.upload_file(image_path)
        print("Image uploaded successfully")
        
        # Create the model and make the API call
        print("Creating model and making API call...")
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content([gemini_file, prompt])
        print("API call successful")
        
        return response.text
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

# Test it locally
if __name__ == "__main__":
    # Test with a local image file
    image_path = "beach_st_signs/118.jpg"  # or whatever test image you have
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        print("Please update the image_path variable to point to a real image file.")
    else:
        print("Testing parking analysis...")
        result = analyze_parking_local(image_path)
        
        if result:
            print("\n" + "="*50)
            print("ANALYSIS RESULT:")
            print("="*50)
            print(result)
        else:
            print("Analysis failed - check the error messages above")