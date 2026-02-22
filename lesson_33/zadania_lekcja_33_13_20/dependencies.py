from fastapi import Header, HTTPException, status, Depends

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Weryfikuje poprawność klucza API przesłanego w nagłówku `x-api-key`.
    
    Funkcja jest używana jako zależność (dependency) w FastAPI za pomocą `Depends`.
    Jeśli klucz API jest niepoprawny lub nieobecny, wyrzuca wyjątek HTTP 401 Unauthorized.
    W przeciwnym razie pozwala na kontynuację obsługi żądania.

    Przykład użycia:
    ```
    @app.get("/items/")
    async def read_items(api_key: str = Depends(verify_api_key)):
        ...
    ```

    Dokumentacja FastAPI dotycząca zależności:
    https://fastapi.tiangolo.com/tutorial/dependencies/
    Dokumentacja FastAPI dotycząca nagłówków:
    https://fastapi.tiangolo.com/tutorial/header-params/
    """
    expected_api_key = "secret_api_key"  # tutaj można podstawić właściwy klucz lub pobrać z konfiguracji
    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_api_key
