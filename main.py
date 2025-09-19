import functions_framework
import google.generativeai as genai
import os
import tempfile
from flask import jsonify

def load_file_content(file_path):
    """Load content from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        raise
    except Exception as e:
        print(f"ERROR: Failed to read file {file_path}: {str(e)}")
        raise

@functions_framework.http
def analyze_parking(request):
    """HTTP Cloud Function that analyzes parking signs using Gemini AI"""
    
    print("Function called - starting analysis")
    
    # Handle CORS for browser requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    # Set CORS headers for actual request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    if request.method != 'POST':
        return jsonify({'error': 'Only POST method allowed'}), 405, headers
    
    try:
        print("Checking for uploaded file...")
        
        # Get the uploaded image file
        if 'image' not in request.files:
            print("ERROR: No image file in request")
            return jsonify({'error': 'No image file provided'}), 400, headers
        
        uploaded_file = request.files['image']
        
        if uploaded_file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'error': 'No file selected'}), 400, headers
        
        print(f"File uploaded: {uploaded_file.filename}")
        
        # Set up the Gemini API client
        print("Setting up Gemini API client...")
        api_key = os.getenv("API_KEY")
        if not api_key:
            print("ERROR: API_KEY environment variable not found")
            return jsonify({'error': 'API key not configured'}), 500, headers
        
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully")
        
        # Save the uploaded file temporarily
        print("Saving file temporarily...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            uploaded_file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        print(f"File saved to: {temp_file_path}")
        
        try:
            # Load the text files
            print("Loading prompt files...")
            try:
                system_instruction = load_file_content("system_instructions2.txt")
                prompt = load_file_content("prompt2.txt")
                print("Prompt files loaded successfully")
            except FileNotFoundError as e:
                print(f"ERROR: Prompt file not found: {e}")
                return jsonify({
                    'error': f'Required file not found: {str(e)}',
                    'details': 'Make sure system_instructions2.txt and prompt2.txt are in your deployment'
                }), 500, headers
            
            # Upload the image to Gemini
            print("Uploading image to Gemini...")
            gemini_file = genai.upload_file(temp_file_path)
            print("Image uploaded to Gemini successfully")
            
            # Create the model and make the API call
            print("Making Gemini API call...")
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            response = model.generate_content([gemini_file, prompt])
            
            print("Gemini API call successful")
            
            # Return the result as JSON
            result = {
                'result': response.text,
                'status': 'success'
            }
            print(f"Returning result: {result}")
            return jsonify(result), 200, headers
            
        finally:
            # Clean up the temporary file
            print(f"Cleaning up temporary file: {temp_file_path}")
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                print(f"Warning: Failed to delete temp file: {e}")
            
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to analyze image',
            'details': str(e)
        }), 500, headers