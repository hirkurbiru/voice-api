# AI-Generated Voice Detection API

This project implements a FastAPI-based REST API that detects whether a given voice sample is AI-generated or spoken by a real human.

## Supported Languages
- English
- Tamil
- Hindi
- Telugu
- Malayalam

## API Endpoint

### POST /detect-voice

Analyzes a voice sample and returns whether it is AI-generated or human.

#### Request
- **audio_url** (query parameter): Public URL of an MP3 audio file
- **language** (query parameter): Language code (e.g., en, ta, hi)
- **Authorization header**:

Authorization: Bearer test123

#### Response (JSON)
```json
{
"result": "AI_GENERATED",
"confidence": 0.72,
"language": "en",
"explanation": {
  "signal_consistency": 0.62,
  "spectral_smoothness": 0.72
}
}
