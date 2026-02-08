# AI Voice API Endpoint Tester

This project provides a FastAPI backend and a lightweight frontend to validate AI-Generated Voice Detection endpoints, honeypot availability, and response schema readiness.

## Project Structure
```
voice-api-endpoint-tester/
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── utils.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

## Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Health check:
```
http://127.0.0.1:8000/health
```

## Frontend
Open the UI directly:
```
frontend/index.html
```

## Endpoints
- `GET /health` — readiness probe.
- `POST /test-endpoint` — forwards audio + message to a target API.
- `POST /test-honeypot` — validates honeypot availability.
