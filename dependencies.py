from fastapi import Header, HTTPException, status
from typing import Annotated

# Статический API ключ
API_KEY = "test-api-key-12345"


async def verify_api_key(x_api_key: Annotated[str, Header()]):
    """
    Проверяет статический API ключ из заголовка X-API-Key
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
    return x_api_key
