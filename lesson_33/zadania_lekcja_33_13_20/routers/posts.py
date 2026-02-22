from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm_models import Post, User, Comment
from models.schemas import PostCreate, PostUpdate, PostResponse, CommentResponse
from services.ai_service import simulate_post_summary

router = APIRouter(prefix="/posts", tags=["Posts"])


# ---------------------------------------------------------
# CREATE POST (async ORM safe eager loading)
# ---------------------------------------------------------
@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint do tworzenia posta blogowego.
    """

    # Check author exists
    result = await db.execute(
        select(User).where(User.id == post.author_id)
    )

    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id
    )

    db.add(new_post)
    await db.commit()
    # Reload post with eager loading to avoid MissingGreenlet async ORM crash
    await db.flush()

    result_post = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments).selectinload(Comment.user)
        )
        .where(Post.id == new_post.id)
    )

    return result_post.scalars().first()


# ---------------------------------------------------------
# GET ALL POSTS
# ---------------------------------------------------------
@router.get("/", response_model=list[PostResponse])
async def get_posts(
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint zwracający listę postów.
    """

    result = await db.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.comments).selectinload(Comment.user)
        )
    )

    return result.scalars().all()


# ---------------------------------------------------------
# GET POST WITH COMMENTS (EAGER LOADING)
# ---------------------------------------------------------
@router.get("/{post_id}/with-comments", response_model=PostResponse)
async def get_post_with_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint zwracający post wraz z komentarzami (eager loading).
    """

    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments).selectinload(Comment.user)
        )
        .where(Post.id == post_id)
    )

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# ---------------------------------------------------------
# UPDATE POST (only author can edit)
# ---------------------------------------------------------
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    author_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint aktualizujący post.

    Zasada biznesowa:
    - Tylko autor posta może go edytować.
    """

    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != author_id:
        raise HTTPException(
            status_code=403,
            detail="Only author can edit this post"
        )

    if post_update.title is not None:
        post.title = post_update.title

    if post_update.content is not None:
        post.content = post_update.content

    await db.commit()
    # Reload post with eager loading to avoid MissingGreenlet async ORM crash
    result_post = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments).selectinload(Comment.user)
        )
        .where(Post.id == post_id)
    )

    return result_post.scalars().first()


# ---------------------------------------------------------
# DELETE POST (only author can delete)
# ---------------------------------------------------------
@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    author_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint usuwający post.

    Zasada biznesowa:
    - Tylko autor może usuwać post.
    """

    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != author_id:
        raise HTTPException(
            status_code=403,
            detail="Only author can delete this post"
        )

    await db.delete(post)
    await db.commit()

    return {"message": "Post deleted"}

# ---------------------------------------------------------
# POST Summary (AI simulation)
# ---------------------------------------------------------
@router.post("/{post_id}/summarize")
async def summarize_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    summary = await simulate_post_summary(post.content)

    return {
        "post_id": post_id,
        "summary": summary
    }