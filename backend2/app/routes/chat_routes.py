from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.stat_service import StatsService
from app.utils.dbconnect import dbconnect

bp = Blueprint('chat', __name__)

db = dbconnect()
llm_service = LLMService(provider="openai")
stats_service = StatsService(db)
chat_service = ChatService(db, llm_service=llm_service, stats_service=stats_service)

@bp.route('/chats', methods=['POST'])
def get_chats():
    data = request.json
    user_id = data.get('user_id')
    
    print(f"Retrieving chats for user_id: {user_id}")
    chats = chat_service.get_user_chats(user_id)
    print(f"Retrieved {len(chats)} chats", chats)
    
    return jsonify(chats)

@bp.route('/createchat', methods=['POST'])
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

@bp.route('/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = chat_service.get_chat_by_id(chat_id)
    return jsonify(chat)

@bp.route('/chats/<chat_id>/messages', methods=['POST'])
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