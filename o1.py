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
        model="o1",
        reasoning_effort="high",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content