from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import AuthService
from chat import ChatService
from openaipy import OpenAIService
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
chat_service = ChatService(db)
openai_service = OpenAIService()

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
    print(f"Retrieved {len(chats)} chats")
    
    return jsonify(chats)

@app.route('/createchat', methods=['POST'])
def create_chat():
    data = request.json
    user_id = data.get('user_id')
    print(f"Creating new chat for user_id: {user_id}")
    messages = [{"role": "user", "content": data['prompt']}]
    assistant_response = openai_service.get_openai_response(messages)
    
    chat_history = [
        {"role": "user", "content": data['prompt']},
        {"role": "assistant", "content": assistant_response}
    ]
    
    chat_id = chat_service.save_chat(user_id, chat_history)
    print(f"Created new chat with id: {chat_id}")
    
    return jsonify({"chat_id": str(chat_id), "assistant_message": assistant_response}), 201

@app.route('/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = chat_service.get_chat_by_id(chat_id)
    return jsonify(chat)

@app.route('/chats/<chat_id>/messages', methods=['POST'])
def add_message(chat_id):
    data = request.json
    user_id = data.get('user_id')
    
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404
    
    chat_history = chat['chat_history']
    chat_history.append({"role": "user", "content": data['prompt']})
    
    assistant_response = openai_service.get_openai_response(chat_history)
    chat_history.append({"role": "assistant", "content": assistant_response})
    
    chat_service.update_chat(chat_id, chat_history)
    
    return jsonify({"chat_id": chat_id, "assistant_message": assistant_response}), 200

if __name__ == '__main__':
    app.run(debug=True)