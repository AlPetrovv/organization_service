from fastapi import HTTPException, status, Security, Depends
from fastapi.security import APIKeyHeader

from config import Settings


settings = Settings()
API_KEY = settings.api_key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return api_key


auth_api_key_dep = Depends(get_api_key)
