# StudyMate AI — Context-Aware Chatbot

StudyMate AI is an AI-powered study assistant built using Python, FastAPI, Google Gemini, HTML, CSS, and JavaScript.

## Features

- Real-time AI responses using Google Gemini
- Multi-turn conversation history
- Separate conversation IDs
- Context management using the latest 10 messages
- System prompt for beginner-friendly educational assistance
- Timeout and API error handling
- Responsive web-based chat interface
- New conversation functionality

## Tech Stack

- **Backend:** Python, FastAPI
- **AI Model:** Google Gemini API
- **Frontend:** HTML, CSS, JavaScript
- **Environment Variables:** python-dotenv

## Project Structure

```text
context-aware-chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── chatbot.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd StudyMate-AI-Context-Aware-Chatbot
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root using `.env.example` as a template.

Add your own Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit your real API key to GitHub.

### 5. Start the backend

```bash
uvicorn backend.main:app --reload
```

Backend: `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open a second terminal and run:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500` in your browser.

## Context Management

The chatbot maintains separate conversation histories and retains the latest 10 messages for context. The system prompt instructs the AI to provide friendly, clear, beginner-friendly educational support.

## Error Handling

The backend handles request timeouts and API failures and returns user-facing error messages.

## Security

API credentials are stored in environment variables and excluded from version control.

## Author

Developed as a context-aware AI chatbot project using Python and Google Gemini.
