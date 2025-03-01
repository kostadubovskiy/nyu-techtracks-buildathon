from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from ...core.security import get_current_user, get_password_hash
from ...database import get_db
from ... import models, schemas

router = APIRouter(tags=["users"])

def create_user_sync(user: schemas.UserCreate, db: Session) -> models.User:
    """
    Synchronous function to create a user, can be called from Flask routes
    """
    email = user.email
    password = user.password
    
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(password)
    db_user = models.User(
        email=email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/users", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    return create_user_sync(user.email, user.password, db)

@router.get("/users/me", response_model=schemas.User)
def read_current_user(
    current_user: models.User = Depends(get_current_user)
) -> Any:
    return current_user

@router.put("/users/me", response_model=schemas.User)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user 