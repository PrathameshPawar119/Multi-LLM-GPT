import os
from dotenv import load_dotenv
import openai

class OpenAIService:
    def __init__(self):
        self.api_key = self.load_api_key() 
        openai.api_key = self.api_key 

    def load_api_key(self):
        load_dotenv() 
        return os.getenv("OPENAI_API_KEY")  
    
    def get_openai_response(self, messages, model="gpt-4o-mini"):
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages
            )
            print(response)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"