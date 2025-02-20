from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_response(prompt, system_prompt=None):
    # Combine the system prompt and user prompt as a single string.
    
        # You can format this string as needed.
    full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"

    
    # Note: The API expects a string (or list with a string element),
    # so we wrap the full_prompt in a list.
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[full_prompt],
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                google_search=types.GoogleSearchRetrieval(
                    dynamic_retrieval_config=types.DynamicRetrievalConfig(
                        dynamic_threshold=0.6))
            )]
        )
    )
    return response.candidates[0].content.parts[0].text
