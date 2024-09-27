from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import AuthService
from chat import ChatService
from LLMServices import LLMService
from StatService import StatsService
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import json
import logging


# logging.basicConfig(level=print)


load_dotenv()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
app.json_encoder = JSONEncoder
CORS(app)
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chat_app"]
auth_service = AuthService(db)
llm_service = LLMService(provider="gemini")
stats_service = StatsService(db)
chat_service = ChatService(db, llm_service=llm_service, stats_service=stats_service)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status_code = auth_service.create_user(data['email'], data['password'])
    return jsonify(response), status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    token, user_id = auth_service.login_user(data['email'], data['password'])
    if token:
        return jsonify({"token": token, "user_id": str(user_id)}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/chats', methods=['POST'])  # Change to POST
def get_chats():
    data = request.json
    user_id = data.get('user_id')
    
    print(f"Retrieving chats for user_id: {user_id}")
    chats = chat_service.get_user_chats(user_id)
    print(f"Retrieved {len(chats)} chats", chats)
    
    return jsonify(chats)

@app.route('/createchat', methods=['POST'])
def create_chat():
    data = request.json
    user_id = data.get('user_id')
    print(f"Creating new chat for user_id: {user_id}")
    messages = [{"role": "user", "content": data['prompt']}]
    response = llm_service.get_llm_response(messages)
    
    assistant_message = response['choices'][0]['message']['content']
    chat_history = [
        {"role": "user", "content": data['prompt']},
        {"role": "assistant", "content": assistant_message}
    ]
    
    chat_id = chat_service.save_chat(user_id, chat_history)
    stats_service.save_api_usage(user_id, chat_id, response)
    stats_service.update_user_stats(user_id, response)
    print(f"Created new chat with id: {chat_id}")
    
    return jsonify({"chat_id": str(chat_id), "assistant_message": assistant_message}), 201

@app.route('/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = chat_service.get_chat_by_id(chat_id)
    return jsonify(chat)

@app.route('/chats/<chat_id>/messages', methods=['POST'])
def add_message(chat_id):
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('prompt')
    
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404
    
    # Get chat context, which may be full chat history or summary + recent messages
    context = chat_service.get_context_for_chat(chat_id)
    context.append({"role": "user", "content": user_message})

    response = llm_service.get_llm_response(context)
    print("\n Token details from add_message: ", response)
    
    if isinstance(response, tuple) and response[1] is None:
        # This means there was an error
        return jsonify({"error": response[0]}), 500
    
    assistant_message = response['choices'][0]['message']['content']

    new_user_message = {"role": "user", "content": user_message}
    new_assistant_message = {"role": "assistant", "content": assistant_message}

    # Update chat with new messages and, if applicable, update the summary
    summary, updated_chat_history = chat_service.update_chat(chat_id, new_user_message, new_assistant_message, user_id=user_id, token_details=response)
    stats_service.save_api_usage(user_id, chat_id, response)

    return jsonify({
        "chat_id": chat_id,
        "assistant_message": assistant_message,
        "summary": summary,
        "chat_history": updated_chat_history
    }), 200


if __name__ == '__main__':
    app.run(debug=True)