from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

API_KEY = "test123"


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/detect-voice")
def detect_voice(
    audio_url: str,
    language: str = "en",
    authorization: str = Header(None)
):
    # Check API key
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Download audio
    try:
        response = requests.get(audio_url)
        if response.status_code != 200:
            raise Exception()
    except:
        raise HTTPException(status_code=400, detail="Invalid audio URL")

    # Temporary logic
    size = len(response.content)
    confidence = min(0.95, max(0.3, size / 1_000_000))
    result = "AI_GENERATED" if confidence > 0.6 else "HUMAN"

    return {
        "result": result,
        "confidence": round(confidence, 2),
        "language": language,
        "explanation": {
            "signal_consistency": round(confidence - 0.1, 2),
            "spectral_smoothness": round(confidence, 2)
        }
    }
