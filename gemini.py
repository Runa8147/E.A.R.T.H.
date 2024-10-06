import google.generativeai as genai
from PIL import Image
import json
import streamlit as st

# Configure the Gemini API (make sure to use your actual API key)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def analyze_image(image: Image.Image) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = """
    Analyze the given image and provide a detailed report in JSON format. The JSON should include the following keys:

    1. "ai_analysis": A string containing a detailed description of the environmental issue or situation shown in the image. This should be a paragraph of 3-5 sentences.
    
    2. "priority_score": A float between 0 and 10 indicating the urgency or severity of the environmental issue (0 being lowest priority, 10 being highest).
    
    3. "tag": A single word or short phrase categorizing the main environmental issue in the image (e.g., "deforestation", "pollution", "endangered_species", etc.).
    
    4. "harmful": A boolean indicating whether the image contains any harmful or inappropriate content (true if harmful, false if not).

    Ensure that your response is a valid JSON object. Do not include any text outside of the JSON structure.

    Example output format:
    {
        "ai_analysis": "The image shows significant deforestation in a tropical rainforest. Large areas of cleared land are visible, with only a few patches of trees remaining. This level of forest loss can lead to habitat destruction, increased carbon emissions, and potential soil erosion.",
        "priority_score": 8.5,
        "tag": "deforestation",
        "harmful": false
    }
    """

    try:
        response = model.generate_content([prompt, image])
        
        # Attempt to parse the response as JSON
        try:
            json_response = json.loads(response.text)
            return json.dumps(json_response)  # Ensure we return a JSON string
        except json.JSONDecodeError:
            # If parsing fails, attempt to extract JSON from the text
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                try:
                    json_response = json.loads(json_match.group())
                    return json.dumps(json_response)
                except json.JSONDecodeError:
                    pass
            
            # If all else fails, create a structured error response
            error_response = {
                "error": "Failed to parse JSON from Gemini response",
                "raw_response": response.text
            }
            return json.dumps(error_response)

    except Exception as e:
        error_response = {
            "error": f"An error occurred during image analysis: {str(e)}",
            "ai_analysis": "Error occurred during analysis",
            "priority_score": 0,
            "tag": "error",
            "harmful": False
        }
        return json.dumps(error_response)

# Example usage
if __name__ == "__main__":
    # Load an image (replace with your image path)
    image_path = "path/to/your/image.jpg"
    image = Image.open(image_path)
    
    # Analyze the image
    result = analyze_image(image)
    print(result)