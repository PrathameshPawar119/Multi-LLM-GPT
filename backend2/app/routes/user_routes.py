from flask import Blueprint, jsonify
from app.utils.dbconnect import dbconnect
from bson import ObjectId

bp = Blueprint('user', __name__)

db = dbconnect()

@bp.route('/users', methods=['GET'])
def get_all_users():
    users = db.users.find({}, {"email": 1, "total_api_calls": 1, "total_prompt_tokens": 1, "total_completion_tokens": 1})
    user_list = [
        {
            "id": str(user["_id"]),
            "email": user["email"],
            "total_api_calls": user.get("total_api_calls", 0),
            "total_prompt_tokens": user.get("total_prompt_tokens", 0),
            "total_completion_tokens": user.get("total_completion_tokens", 0)
        } for user in users
    ]
    return jsonify(user_list), 200

@bp.route('/users/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        api_usage = db.api_usage.find({"user_id": ObjectId(user_id)})
        api_usage_list = [
            {
                "id": str(entry["_id"]),  
                "chat_id": str(entry["chat_id"]),  
                "api_response": entry["api_response"],
                "created_at": entry["created_at"]  
            }
            for entry in api_usage
        ]

        stats = {
            "total_api_calls": user.get("total_api_calls", 0),
            "total_prompt_tokens": user.get("total_prompt_tokens", 0),
            "total_completion_tokens": user.get("total_completion_tokens", 0),
            "api_usage": api_usage_list
        }

        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
