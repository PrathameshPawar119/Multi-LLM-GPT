# MultiLLM Chat Platform

A versatile chat application leveraging multiple Language Learning Models (LLMs) with a Flask backend and Streamlit frontend. This platform offers seamless integration with various LLM providers, user authentication, chat history management, and comprehensive usage analytics.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
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
your_project/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── utils/
├── .env
├── frontend/
│   ├── components/
│   ├── pages/
├── admin/
├── run.py
└── requirements.txt
```

- `app/`: Core backend logic
  - `routes/`: API endpoint definitions
  - `services/`: Business logic and LLM integration
  - `utils/`: Helper functions and utilities
- `frontend/`: Streamlit-based user interface
- `admin/`: Admin dashboard for analytics
- `.env`: Environment variables configuration
- `run.py`: Application entry point

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multillm-chat-platform.git
   cd multillm-chat-platform
   ```

2. Set up a virtual environment:
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
   ```
   Edit `.env` with your API keys and configuration.

## Configuration

1. LLM API Keys:
   Add your API keys to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   GOOGLE_API_KEY=your_google_key
   ```

2. MongoDB Configuration:
   Set your MongoDB URI in the `.env` file:
   ```
   MONGODB_URI=your_mongodb_uri
   ```

## Usage

1. Start the Flask backend:
   ```
   python run.py
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

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/multillm-chat-platform](https://github.com/yourusername/multillm-chat-platform)

