from fastapi import Header, HTTPException

VALID_API_KEYS = {"test123", "demo-key"}


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
