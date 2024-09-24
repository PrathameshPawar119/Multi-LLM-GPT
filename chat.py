from backend import OpenAIService

class ChatBot:
    def __init__(self):
        self.openai_service = OpenAIService()  # Initialize OpenAI service

    def handle_chat(self, prompt, chats):
        if prompt:
            chats.append({"role": "user", "content": prompt})

            assistant_message = self.openai_service.get_openai_response(
                [{"role": "system", "content": "You are brilliant, having a lot of knowledge."}] + chats
            )

            chats.append({"role": "assistant", "content": assistant_message})

        return chats
