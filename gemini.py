import google.generativeai as genai
from PIL import Image
import json
import streamlit as st

# Configure the Gemini API (make sure to use your actual API key)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
)

def analyze_image(image: Image.Image) -> str:
    prompt = """
  Analyze the given image and provide a detailed report in JSON format. The JSON should include the following keys:

  1. "ai_analysis": A string containing a detailed description of the environmental issue or situation shown in the image. This should be a paragraph of 3-5 sentences.
  
  2. "priority_score": A float between 0 and 10 indicating the urgency or severity of the environmental issue. (1 being lowest priority, 10 being highest).
  
  3. "tag": A single word or short phrase categorizing the main environmental issue in the image or based on the situation and time or work (e.g., "deforestation", "pollution", "endangered_species", etc.)Also surely try to give a tag related to the image.
  
  4. "harmful": A boolean indicating whether the image contains any harmful or inappropriate content (true if harmful, false if not).

  Ensure that your response is a valid JSON object. Do not include any text outside of the JSON structure.Give appropriate values based on the given image.

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
        
        json_response = json.loads(response.text)
        return json.dumps(json_response)  # Ensure we return a JSON strin

    except Exception as e:
        error_response = {
            "error": f"An error occurred during image analysis: {str(e)}",
            "ai_analysis": "Error occurred during analysis",
            "priority_score": 0,
            "tag": "error",
            "harmful": False
        }
        return json.dumps(error_response)
