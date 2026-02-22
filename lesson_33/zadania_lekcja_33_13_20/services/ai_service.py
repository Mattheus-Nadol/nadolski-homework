import random
import re

BLACKLIST_WORDS = {
    "badword1",
    "badword2",
    "fuck",
    "shit"
}


async def simulate_post_summary(content: str) -> str:
    """
    Symulacja generowania streszczenia AI.
    """

    words = content.split()

    if len(words) <= 10:
        return content

    summary_length = min(50, len(words) // 2)

    summary = " ".join(words[:summary_length])

    return f"AI Summary: {summary}..."


async def simulate_sentiment_analysis(text: str) -> float:
    """
    Symulacja analizy sentymentu komentarza.
    """

    positive_words = {"good", "nice", "great", "love", "excellent"}
    negative_words = {"bad", "terrible", "hate", "ugly"}

    score = 0

    text_lower = text.lower()

    for w in positive_words:
        if w in text_lower:
            score += 1

    for w in negative_words:
        if w in text_lower:
            score -= 1

    return score


async def check_content_moderation(text: str) -> bool:
    """
    Middleware moderation check.

    Returns True if content is safe.
    """

    text_lower = text.lower()

    for word in BLACKLIST_WORDS:
        if word in text_lower:
            return False

    return True