from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.orm_models import User
from models.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint do tworzenia użytkownika bloga.
    """
    result = await db.execute(
        select(User).where(
            (User.username == user.username) |
            (User.email == user.email)
        )
    )

    existing = result.scalars().first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with given username or email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------
@router.get("/", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint zwracający listę użytkowników.
    """
    result = await db.execute(select(User))
    return result.scalars().all()


# ---------------------------------------------------------
# GET USER BY ID
# ---------------------------------------------------------
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint zwracający użytkownika po ID.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------------------------------------------------
# UPDATE USER
# ---------------------------------------------------------
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint aktualizujący użytkownika.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_update.username
    user.email = user_update.email

    await db.commit()
    await db.refresh(user)

    return user


# ---------------------------------------------------------
# DELETE USER
# ---------------------------------------------------------
@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint usuwający użytkownika.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted"}