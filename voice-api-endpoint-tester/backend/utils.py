import base64
import requests


def fetch_audio_as_base64(audio_url: str) -> str:
    response = requests.get(audio_url, timeout=10)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")
