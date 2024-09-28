import os
from dotenv import load_dotenv
import openai

class OpenAIService:
    def __init__(self):
        self.api_key = self.load_api_key()
        openai.api_key = self.api_key
    
    def _serialize_openai_response(self, response):
        # Ensure all parts of the response are converted to serializable dictionaries
        return {
            "id": response.id,
            "created": response.created,
            "model": response.model,
            "object": response.object,
            "choices": [
                {
                    "finish_reason": choice.finish_reason,
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    }
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }


    def load_api_key(self):
        load_dotenv()
        return os.getenv("OPENAI_API_KEY")
        
    def get_openai_response(self, messages, model="gpt-4o-mini"):
        try:
            print("\n Making openai request: ", messages)
            print("\n Data to be sent len(messages) = ", len(messages))

            response = openai.chat.completions.create(
                model=model,
                messages=messages
            )
            print("\n Before Serielize \n", response)

            response = self._serialize_openai_response(response)

            print("\n Response After Serielize \n", response)
            return response
        except Exception as e:
            return f"Error: {str(e)}", None

    def generate_summary(self, chat_history):
        # Build a summary prompt using the complete chat history
        summary_prompt = "Summarize the following conversation concisely:"
        for message in chat_history:
            summary_prompt += f"\n{message['role']}: {message['content']}"
        
        messages = [{"role": "system", "content": summary_prompt}]
        return self.get_openai_response(messages)

    def update_summary(self, previous_summary, new_messages):
        update_prompt = f"Given the following summary of a conversation:\n{previous_summary}\n\nUpdate the summary to include these new messages:"
        for message in new_messages:
            update_prompt += f"\n{message['role']}: {message['content']}"
        
        messages = [{"role": "system", "content": update_prompt}]
        return self.get_openai_response(messages)
