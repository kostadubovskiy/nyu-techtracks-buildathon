from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from ...core.security import get_current_user, get_password_hash
from ...database import get_db
from ... import models, schemas

router = APIRouter(tags=["users"])

@router.post("/users", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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

"""
# Create a user
curl -X POST "http://localhost:8000/api/v1/users" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "yourpassword"}'

# Log in to get a token
curl -X POST "http://localhost:8000/api/v1/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@example.com&password=yourpassword"

# Use the token to access protected endpoints
curl -X GET "http://localhost:8000/api/v1/roadmaps" -H "Authorization: Bearer <your_token_here>"
"""