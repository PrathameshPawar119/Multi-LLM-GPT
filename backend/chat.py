from datetime import datetime
from bson import ObjectId
import logging

class ChatService:
    def __init__(self, db):
        self.db = db

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
            "createdAt": datetime.now()
        }
        result = self.db.chats.insert_one(chat)
        print("result", result)
        print(f"Saved chat with id: {result.inserted_id}")
        return str(result.inserted_id)

    def get_user_chats(self, user_id):
        print(f"Fetching chats for user_id: {user_id}")
        chats = list(self.db.chats.find({"user_id": ObjectId(user_id)}).sort("createdAt", -1))
        print(f"Found {len(chats)} chats")
        serialized_chats = [self._serialize_object_id(chat) for chat in chats]
        print("serialized_chats", serialized_chats)
        return serialized_chats

    def get_chat_by_id(self, chat_id):
        chat = self.db.chats.find_one({"_id": ObjectId(chat_id)})
        if chat:
            serialized_chat = self._serialize_object_id(chat)
            print(f"Fetched chat for chat_id: {chat_id}")
            print("serialized_chat", serialized_chat)
            return serialized_chat
        print(f"No chat found for chat_id: {chat_id}")
        return None

    def update_chat(self, chat_id, chat_history):
        print(f"Updating chat for chat_id: {chat_id}")
        self.db.chats.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"chat_history": chat_history}}
        )