from datetime import datetime
from bson import ObjectId

class StatsService:
    def __init__(self, db):
        self.db = db


    def save_api_usage(self, user_id, chat_id, token_details):
        print("\n serialized_token_details \n", token_details)
        
        usage_entry = {
            "user_id": ObjectId(user_id),
            "chat_id": ObjectId(chat_id),
            "api_response": token_details,
            "created_at": datetime.now()
        }
        self.db.api_usage.insert_one(usage_entry)

    def update_user_stats(self, user_id, token_details):
        update_query = {
            "$inc": {
                "total_api_calls": 1,
                "total_prompt_tokens": token_details['usage']['prompt_tokens'],
                "total_completion_tokens": token_details['usage']['completion_tokens']
            }
        }
        self.db.users.update_one({"_id": ObjectId(user_id)}, update_query)