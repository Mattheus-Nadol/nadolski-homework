# Standard library imports
from datetime import datetime
import random
from contextlib import asynccontextmanager

# FastAPI imports
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

from routers import books, authors, users, posts, comments

# Middleware logging (Zadanie 16)
from middleware.logging_middleware import logging_middleware

# AI Moderation Service import (Zadanie 20)
from services.ai_service import check_content_moderation
import json

# Dependency
from dependencies import verify_api_key

from database import lifespan_db

app = FastAPI(
    title="LearnIT FastAPI Exercises",
    description="API do zadań z lekcji 33",
    lifespan=lifespan_db
)

# Routers
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
# Jeśli w przyszłości chcesz włączyć globalną weryfikację API key:
# app.include_router(books.router, dependencies=[Depends(verify_api_key)])
# app.include_router(authors.router, dependencies=[Depends(verify_api_key)])

# Rejestracja middleware
app.middleware("http")(logging_middleware)

# ---------------------------------------------------------
# AI Moderation Middleware (Zadanie 20)
# ---------------------------------------------------------
@app.middleware("http")
async def moderation_middleware(request, call_next):
    """
    Middleware auto-moderacji treści.

    Sprawdza JSON body requestu i blokuje wulgaryzmy w:
    - title
    - content
    - nested JSON structures
    """

    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()

            if body:
                try:
                    data = json.loads(body.decode("utf-8", errors="ignore"))

                    # Collect ALL strings recursively
                    def collect_strings(obj):
                        texts = []

                        if isinstance(obj, str):
                            texts.append(obj)

                        elif isinstance(obj, dict):
                            for v in obj.values():
                                texts.extend(collect_strings(v))

                        elif isinstance(obj, list):
                            for item in obj:
                                texts.extend(collect_strings(item))

                        return texts

                    all_texts = collect_strings(data)

                    # Check moderation for each text field
                    for text in all_texts:
                        safe = await check_content_moderation(text)

                        if not safe:
                            import fastapi.responses as responses

                            return responses.JSONResponse(
                                status_code=400,
                                content={"detail": "Content rejected by AI moderation"}
                            )

                except json.JSONDecodeError:
                    pass

        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Moderation middleware error: {e}")

            import fastapi.responses as responses
            return responses.JSONResponse(
                status_code=500,
                content={"detail": "Moderation middleware internal error"}
            )

    response = await call_next(request)
    return response