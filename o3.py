from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve the API key and strip whitespace
api_key = os.getenv("OPENAI_API_KEY")
api_key = api_key.strip()
    

client = OpenAI(api_key=api_key)

def get_response(prompt, system_prompt= None):
    response = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="medium",
        messages=[
            {
                "role": "system",
                "content": system_prompt  # The system prompt provides context or instructions.
            },
            {
                "role": "user", 
                "content": prompt  # The actual user prompt.
            }
        ]
    )
    return response.choices[0].message.content