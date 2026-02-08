import logging
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests

from auth import verify_api_key
from utils import fetch_audio_as_base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-api-endpoint-tester")

app = FastAPI(title="AI Voice Detection API Endpoint Tester")


@app.get("/health")
def health_check():
    return {"status": "ok"}


class EndpointTestRequest(BaseModel):
    endpoint_url: HttpUrl
    api_key: str
    message: str
    audio_url: HttpUrl


class HoneypotTestRequest(BaseModel):
    endpoint_url: HttpUrl
    api_key: str


def validate_final_response(data: dict[str, Any]):
    if "classification" not in data or "confidence" not in data:
        raise HTTPException(400, "Invalid response schema")


@app.post("/test-endpoint", dependencies=[Depends(verify_api_key)])
def test_endpoint(payload: EndpointTestRequest):
    try:
        audio_base64 = fetch_audio_as_base64(payload.audio_url)

        forward_payload = {
            "message": payload.message,
            "audio_base64": audio_base64,
        }

        headers = {
            "Authorization": f"Bearer {payload.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            payload.endpoint_url,
            json=forward_payload,
            headers=headers,
            timeout=15,
        )

        try:
            response_payload = response.json()
        except ValueError as exc:
            logger.warning("Target returned invalid JSON: %s", exc)
            raise HTTPException(status_code=502, detail="Target API returned invalid JSON") from exc

        validate_final_response(response_payload)

        return {
            "target_status_code": response.status_code,
            "target_response": response_payload,
        }

    except requests.exceptions.Timeout as exc:
        raise HTTPException(status_code=504, detail="Target API timeout") from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error testing endpoint")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/test-honeypot", dependencies=[Depends(verify_api_key)])
def test_honeypot(payload: HoneypotTestRequest):
    try:
        response = requests.get(
            payload.endpoint_url,
            headers={"Authorization": f"Bearer {payload.api_key}"},
            timeout=10,
        )

        return {
            "reachable": True,
            "status_code": response.status_code,
            "response": response.text,
        }

    except Exception as exc:
        return {"reachable": False, "error": str(exc)}
