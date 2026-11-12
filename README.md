# 💬 Kurakani AI Assistant

**Kurakani** (Nepali for *"conversation"*) is a web-based AI chatbot that gives
parenting, child-development and family-wellness advice. It runs entirely on your
own computer using a locally hosted Large Language Model (LLM) through
[Ollama](https://ollama.com), so no conversation data is sent to the cloud.

> Undergraduate project — demonstrates building a REST API with FastAPI, a
> custom LLM persona with an Ollama Modelfile, and a responsive chat interface.

---

## Features

- Clean, responsive chat interface (desktop and mobile)
- Custom AI persona defined in a `Modelfile` (parenting specialist)
- Fully local and private — powered by Llama 3 via Ollama
- REST API with request validation (Pydantic)
- Helpful error messages when the model is not running or not installed
- Auto-generated API docs at `/docs` (Swagger UI)

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | HTML5, CSS3, vanilla JavaScript         |
| Backend   | Python 3.10+, FastAPI, Uvicorn          |
| AI model  | Llama 3 running on Ollama               |
| Other     | httpx, Pydantic, python-dotenv          |

## How It Works

```
 Browser  ──POST /api/chat──▶  FastAPI backend  ──POST /api/chat──▶  Ollama (kurakani model)
    ▲                               │                                     │
    └───────────── JSON reply ◀─────┴───────────────◀─────────────────────┘
```

1. The user types a question in the browser.
2. The frontend sends it to the FastAPI backend (`/api/chat`).
3. The backend forwards it to the local Ollama server running the custom
   `kurakani` model.
4. The model's answer is returned and displayed in the chat window.

## Project Structure

```
kurakani/
├── app/
│   ├── main.py               # FastAPI app and routes
│   ├── config.py             # Settings from environment variables
│   └── services/
│       └── ai_service.py     # Communication with Ollama
├── static/
│   ├── index.html            # Chat page
│   ├── css/style.css
│   ├── js/chat.js
│   └── images/logo.png
├── Modelfile                 # Custom Ollama model (persona + parameters)
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Prerequisites

- Python 3.10 or newer
- [Ollama](https://ollama.com/download) installed and running

### 2. Create the custom model

```bash
ollama pull llama3
```

```bash
ollama create kurakani -f Modelfile
```

### 3. Install the Python dependencies

```bash
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure

```bash
cp .env.example .env
```

| Variable          | Default                  | Description                     |
|-------------------|--------------------------|---------------------------------|
| `HOST`            | `127.0.0.1`              | Address the server listens on   |
| `PORT`            | `8000`                   | Port the server listens on      |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Where Ollama is running         |
| `OLLAMA_MODEL`    | `kurakani`               | Model name to use               |
| `OLLAMA_TIMEOUT`  | `120`                    | Seconds to wait for a reply     |

### 5. Run the app

```bash
python -m app.main
```

Open **http://127.0.0.1:8000** in your browser.
Interactive API documentation is available at **http://127.0.0.1:8000/docs**.

> The page also works if you open `static/index.html` directly or with VS Code
> Live Server, as long as the backend from step 5 is running on port 8000.

### Checklist if the chat does not reply

1. Is Ollama running? → `ollama list` should work without an error
2. Does the model exist? → `kurakani` must appear in `ollama list`
   (if not: `ollama create kurakani -f Modelfile`)
3. Is the backend running? → http://127.0.0.1:8000/api/health should show `"status": "ok"`
4. Run commands from the **project root** (the folder that contains `app/`),
   not from inside `app/`

## API Reference

| Method | Endpoint      | Body                       | Response              |
|--------|---------------|----------------------------|-----------------------|
| GET    | `/api/health` | –                          | `{ "status", "model" }` |
| POST   | `/api/chat`   | `{ "message": "..." }`     | `{ "reply": "..." }`  |

Errors are returned as `{ "detail": "..." }` — `400`/`422` for invalid input and
`503` when the AI model is unavailable.

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I help my toddler sleep better?"}'
```

## Troubleshooting

| Message | Fix |
|---------|-----|
| *Could not reach Ollama…* | Start Ollama (open the app or run `ollama serve`) |
| *Model 'kurakani' was not found…* | Run `ollama create kurakani -f Modelfile` |
| Replies are slow | Normal on CPU-only machines; the first reply also loads the model |

## Limitations & Future Work

- No conversation memory yet — each message is answered independently
- Add streaming responses so text appears word-by-word
- Save chat history in a database
- Support for the Nepali language
- Docker setup for one-command deployment

## Disclaimer

Kurakani provides general information only and is **not** a substitute for advice
from doctors or other qualified professionals.

## Author

**Mrsaroj646** — Undergraduate project

## License

Released under the [MIT License](LICENSE).
