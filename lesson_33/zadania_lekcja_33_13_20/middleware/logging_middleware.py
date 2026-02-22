import os
import uuid
import time
from datetime import datetime
from fastapi import Request
from starlette.responses import Response

LOG_FILE_PATH = "logs/requests.log"


def ensure_log_directory():
    """Upewnia się, że katalog logs istnieje."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


async def logging_middleware(request: Request, call_next):
    """
    Middleware logujący wszystkie requesty.

    Funkcjonalność:
    - Loguje metodę HTTP
    - Loguje ścieżkę requestu
    - Mierzy czas wykonania requestu
    - Dodaje header X-Request-ID do response
    - Zapisuje logi do pliku logs/requests.log
    """

    ensure_log_directory()

    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Process request
    response: Response = await call_next(request)

    process_time = time.time() - start_time

    # Add header
    response.headers["X-Request-ID"] = request_id

    log_entry = (
        f"[{datetime.now().isoformat()}] "
        f"RID={request_id} "
        f"{request.method} {request.url.path} "
        f"TIME={process_time:.6f}s\n"
    )

    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)

    return response