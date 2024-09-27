from typing import Literal, Any, Dict
from pydantic import BaseModel
import instructor
from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv

LLMProviders = Literal["openai", "anthropic", "ollama"]

class LLMSettings(BaseModel):
    api_key: str
    default_model: str
    temperature: float = 0.0
    max_tokens: int | None = None
    max_retries: int = 3

class LLMService:
    def __init__(self, provider: LLMProviders):
        self.provider = provider
        self.settings = self._load_settings()
        self.client = self._initialize_client()

    def _load_settings(self) -> LLMSettings:
        load_dotenv()
        if self.provider == "openai":
            return LLMSettings(
                api_key=os.getenv("OPENAI_API_KEY", ""),
                default_model="gpt-4o-mini",
                temperature=0.0,
                max_tokens=None,
                max_retries=3
            )
        elif self.provider == "anthropic":
            return LLMSettings(
                api_key=os.getenv("ANTHROPIC_API_KEY", ""),
                default_model="claude-3-5-sonnet-20240620",
                temperature=0.0,
                max_tokens=1024,
                max_retries=3
            )
        elif self.provider == "ollama":
            return LLMSettings(
                api_key="key",  # required, but not used
                default_model="llama3.1",
                temperature=0.0,
                max_tokens=None,
                max_retries=3
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _initialize_client(self):
        if self.provider == "openai":
            client = OpenAI(api_key=self.settings.api_key)
            return instructor.patch(client)
        elif self.provider == "anthropic":
            client = Anthropic(api_key=self.settings.api_key)
            return instructor.patch(client)
        elif self.provider == "ollama":
            client = OpenAI(base_url="http://localhost:11434/v1", api_key=self.settings.api_key)
            return instructor.patch(client)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def get_llm_response(self, messages: list[Dict[str, str]], model: str | None = None, **kwargs: Any) -> Dict[str, Any]:
        completion_params = {
            "model": model or self.settings.default_model,
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "messages": messages,
        }

        response = self.client.chat.completions.create(**completion_params)
        return self._serialize_response(response)

    def _serialize_response(self, response: Any) -> Dict[str, Any]:
        # This is a simplified version and may need to be adapted for each provider
        return {
            "id": getattr(response, "id", None),
            "created": getattr(response, "created", None),
            "model": getattr(response, "model", None),
            "choices": [
                {
                    "finish_reason": getattr(choice, "finish_reason", None),
                    "index": getattr(choice, "index", None),
                    "message": {
                        "role": getattr(choice.message, "role", None),
                        "content": getattr(choice.message, "content", None)
                    }
                }
                for choice in getattr(response, "choices", [])
            ],
            "usage": {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
                "completion_tokens": getattr(response.usage, "completion_tokens", None),
                "total_tokens": getattr(response.usage, "total_tokens", None)
            } if hasattr(response, "usage") else None
        }

    def generate_summary(self, chat_history: list[Dict[str, str]]) -> Dict[str, Any]:
        summary_prompt = "Summarize the following conversation concisely:"
        for message in chat_history:
            summary_prompt += f"\n{message['role']}: {message['content']}"
        
        messages = [{"role": "system", "content": summary_prompt}]
        return self.get_llm_response(messages)

    def update_summary(self, previous_summary: str, new_messages: list[Dict[str, str]]) -> Dict[str, Any]:
        update_prompt = f"Given the following summary of a conversation:\n{previous_summary}\n\nUpdate the summary to include these new messages:"
        for message in new_messages:
            update_prompt += f"\n{message['role']}: {message['content']}"
        
        messages = [{"role": "system", "content": update_prompt}]
        return self.get_llm_response(messages)