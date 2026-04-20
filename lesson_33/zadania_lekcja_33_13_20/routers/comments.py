from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.orm_models import Comment, Post, User
from models.schemas import CommentCreate, CommentResponse
from services.background_service import send_comment_email
from services.ai_service import simulate_sentiment_analysis

router = APIRouter(prefix="/comments", tags=["Comments"])


# ---------------------------------------------------------
# CREATE COMMENT + BACKGROUND TASK EMAIL
# ---------------------------------------------------------
@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint do dodawania komentarza do posta.

    Po utworzeniu komentarza uruchamiana jest background task,
    który symuluje wysłanie emaila.
    """

    # Check post exists
    post_result = await db.execute(
        select(Post).where(Post.id == comment.post_id)
    )

    post = post_result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check user exists
    user_result = await db.execute(
        select(User).where(User.id == comment.user_id)
    )

    user = user_result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=comment.user_id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    # AI sentiment analysis simulation
    sentiment = await simulate_sentiment_analysis(comment.content)
    # Optional logging for development/debugging
    print(f"⭐️⭐️⭐️⭐️⭐️ Sentiment score: {sentiment}")
    # Background task - simulate email
    background_tasks.add_task(
        send_comment_email,
        user.email,
        post.title,
        comment.content
    )

    return new_comment


# ---------------------------------------------------------
# GET COMMENTS
# ---------------------------------------------------------
@router.get("/", response_model=list[CommentResponse])
async def get_comments(
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint zwracający listę komentarzy.
    """

    result = await db.execute(select(Comment))

    return result.scalars().all()