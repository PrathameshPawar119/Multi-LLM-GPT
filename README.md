# MultiLLM Chat Platform

A versatile chat application leveraging multiple Language Learning Models (LLMs) (Using Factory Pattern) with a Flask backend and Streamlit frontend. This platform offers seamless integration with various LLM providers, user authentication, chat history management, and comprehensive usage analytics.

https://github.com/user-attachments/assets/73817e40-9526-49d9-bb1c-93dd3071c1df


## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Installation](#installation)
- [Contact](#contact)

## Features

- **Multi-LLM Support**: Seamlessly integrate with OpenAI, Anthropic, Ollama, and Gemini.
- **User Authentication**: Secure login and registration system.
- **Chat History Management**: Store and retrieve user chat sessions.
- **API Usage Tracking**: Monitor and analyze API calls and token usage.
- **Admin Dashboard**: Visualize user statistics and platform usage.

## Technology Stack

- **Backend**: Flask, Python
- **Frontend**: Streamlit
- **Database**: MongoDB
- **LLM Providers**: OpenAI, Anthropic, Ollama, Gemini

## Project Structure

```
ChatGPT/
├── Admin/
│   ├── app.py
│   └── requirements.txt
├── backend2/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── chat_routes.py
│   │   │   └── user_routes.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── llm_service.py
│   │   │   └── stat_service.py
│   │   └── utils/
│   ├── init.py
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── components/
│   │   ├── auth.py
│   │   ├── chats.py
│   │   └── sidebar.py
│   ├── app.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

- `app/`: Core backend logic
  - `routes/`: API endpoint definitions
  - `services/`: Business logic and LLM integration
  - `utils/`: Helper functions and utilities
- `frontend/`: Streamlit-based user interface
- `admin/`: Admin dashboard for analytics
- `.env`: Environment variables configuration
- 

## Configuration

1. LLM API Keys:
   Add your API keys to the backend/ `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   GOOGLE_API_KEY=your_google_key
   MONGODB_URI=your_mongodb_uri
   ```
   

## Usage

1. Start the Flask backend:
   ```
   flask run
   ```

2. Launch the Streamlit frontend:
   ```
   cd frontend
   streamlit run app.py
   ```

3. Access the admin dashboard:
   ```
   cd admin
   streamlit run admin.py
   ```

## API Endpoints

- Authentication:
  - `POST /auth/register`: Register a new user
  - `POST /auth/login`: User login

- Chat:
  - `POST /chats`: Retrieve user's chat history
  - `POST /createchat`: Start a new chat session
  - `GET /chats/<chat_id>`: Get specific chat details
  - `POST /chats/<chat_id>/messages`: Add a message to a chat

- User:
  - `GET /users`: Retrieve all users (admin only)
  - `GET /users/<user_id>/stats`: Get user statistics

## Contributing

We welcome contributions to the MultiLLM Chat Platform!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## Installation and Running

Each component (backend2, frontend, and Admin) has its own `requirements.txt` file and can be run independently. Note that you can run either the frontend or Admin component at a time on your local machine, alongside the backend.

### Backend

1. Navigate to the backend2 directory:
   ```
   cd backend2
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the Flask server:
   ```
   flask run
   ```

### Frontend

1. Open a new terminal and navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### Admin Dashboard

1. Open a new terminal and navigate to the Admin directory:
   ```
   cd Admin
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Admin Streamlit app:
   ```
   streamlit run app.py
   ```

## Contact

Prathamesh Pawar - prathameshpawar28788@gmail.com

Project Link: https://github.com/PrathameshPawar119/Multi-LLM-GPT

