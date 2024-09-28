from datetime import datetime
from bson import ObjectId

class ChatService:
    SUMMARY_THRESHOLD = 3

    def __init__(self, db, llm_service, stats_service):
        self.db = db
        self.llm_service = llm_service
        self.stats_service = stats_service

    def _serialize_object_id(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, dict):
            return {k: self._serialize_object_id(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._serialize_object_id(item) for item in obj]
        return obj

    def save_chat(self, user_id, chat_history):
        chat = {
            "user_id": ObjectId(user_id),
            "chat_history": chat_history,
            "summary": "",
            "message_count": len(chat_history),
            "createdAt": datetime.now()
        }
        result = self.db.chats.insert_one(chat)
        return str(result.inserted_id)

    def get_user_chats(self, user_id):
        chats = list(self.db.chats.find({"user_id": ObjectId(user_id)}).sort("createdAt", -1))
        return [self._serialize_object_id(chat) for chat in chats]

    def get_chat_by_id(self, chat_id):
        chat = self.db.chats.find_one({"_id": ObjectId(chat_id)})
        return self._serialize_object_id(chat) if chat else None

    def update_chat(self, chat_id, new_user_message, new_assistant_message, user_id, token_details):
        chat = self.get_chat_by_id(chat_id)
        if not chat:
            return None, None

        chat_history = chat['chat_history']
        chat_history.extend([new_user_message, new_assistant_message])
        message_count = len(chat_history)
        summary = chat.get('summary', '')

        # Update summary after every SUMMARY_THRESHOLD interactions
        if message_count == self.SUMMARY_THRESHOLD * 2:  # each interaction has 2 messages
            summary_response = self.llm_service.generate_summary(chat_history)
            if 'error' in summary_response:
                print(f"Error generating summary: {summary_response['error']}")
                summary = "Error generating summary"
            else:
                summary = summary_response['choices'][0]['message']['content']
        elif message_count > self.SUMMARY_THRESHOLD * 2:
            summary_response = self.llm_service.update_summary(summary, [new_user_message, new_assistant_message])
            if 'error' in summary_response:
                print(f"Error updating summary: {summary_response['error']}")
                # Keep the old summary if there's an error
            else:
                summary = summary_response['choices'][0]['message']['content']

        self.db.chats.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {
                "chat_history": chat_history,
                "summary": summary,
                "message_count": message_count
            }}
        )

        if isinstance(token_details, dict) and 'error' not in token_details:
            self.stats_service.update_user_stats(user_id, token_details)
        else:
            print(f"Skipping stats update due to error in token_details: {token_details}")

        return summary, chat_history

    def get_context_for_chat(self, chat_id):
        chat = self.get_chat_by_id(chat_id)
        if not chat:
            return None

        if chat['message_count'] <= self.SUMMARY_THRESHOLD * 2:
            return chat['chat_history']
        else:
            # After threshold is met, return summary + last two interactions
            return [{"role": "system", "content": chat['summary']}] + chat['chat_history'][-4:]