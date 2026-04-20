
import os
import json
from datetime import datetime
import asyncio

LOG_DIR = "logs"
DATA_DIR = "data"

EMAIL_LOG_FILE = os.path.join(LOG_DIR, "email_log.txt")
STATISTICS_FILE = os.path.join(DATA_DIR, "statistics.json")


def _ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


async def send_email_log(book_title: str, author_email: str):
    """
    Background task symulujący wysyłkę email (log do pliku).

    Zapisuje informację o "wysłaniu emaila" do pliku logów.

    Format logu:
    [datetime] Email sent
    To: author_email
    Book: book_title
    """

    def write_log():
        _ensure_dirs()

        timestamp = datetime.utcnow().isoformat()

        with open(EMAIL_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Email sent\n")
            f.write(f"To: {author_email}\n")
            f.write(f"Book: {book_title}\n")
            f.write("-" * 40 + "\n")

    await asyncio.to_thread(write_log)


async def update_statistics_after_delete():
    """
    Background task aktualizujący statystyki po usunięciu książki.

    Aktualnie:
    - zwiększa licznik operacji delete
    - zapisuje timestamp aktualizacji
    """

    def update_stats():
        _ensure_dirs()

        stats = {
            "books_total": 0,
            "last_updated": datetime.utcnow().isoformat(),
            "delete_operations": 1
        }

        # jeśli plik istnieje → wczytaj poprzednie dane
        if os.path.exists(STATISTICS_FILE):
            try:
                with open(STATISTICS_FILE, "r", encoding="utf-8") as f:
                    old = json.load(f)
                    stats["delete_operations"] = old.get("delete_operations", 0) + 1
            except Exception:
                pass

        with open(STATISTICS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

    await asyncio.to_thread(update_stats)


# New async function to send comment email log
async def send_comment_email(user_email: str, post_title: str, comment_content: str):
    """
    Background task symulujący wysłanie emaila przy nowym komentarzu.

    Format logu:
    [datetime] Comment Email
    To: user_email
    Post: post_title
    Comment: comment_content
    """

    def write_log():
        _ensure_dirs()

        timestamp = datetime.utcnow().isoformat()

        email_log_file = os.path.join(LOG_DIR, "comment_email_log.txt")

        with open(email_log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Comment Email\n")
            f.write(f"To: {user_email}\n")
            f.write(f"Post: {post_title}\n")
            f.write(f"Comment: {comment_content}\n")
            f.write("-" * 40 + "\n")

    await asyncio.to_thread(write_log)