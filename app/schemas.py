"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class RoadmapBase(BaseModel):
    title: str
    description: Optional[str] = None

class RoadmapCreate(RoadmapBase):
    pass

class RoadmapUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict[str, str]] = None

class Roadmap(RoadmapBase):
    id: int
    owner_id: int
    content: Optional[Dict[str, str]] = None
    created_at: datetime | None = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    name: str
    content: str
    order: int
    unlocked: bool

class LessonCreate(LessonBase):
    roadmap_parent_id: int

class Lesson(LessonBase):
    id: int
    roadmap_parent_id: int
    owner_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LessonInput(BaseModel):
    topic: str