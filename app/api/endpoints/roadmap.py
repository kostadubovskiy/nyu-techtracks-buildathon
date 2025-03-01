from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from ...core.security import get_current_user
from ...database import get_db
from ... import models, schemas
from ...services.anthropic import generate_roadmap_content

router = APIRouter(tags=["roadmaps"])

@router.post("/roadmaps", response_model=schemas.Roadmap)
async def create_roadmap(
    roadmap: schemas.RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    # Generate roadmap content using Anthropic
    content = await generate_roadmap_content(roadmap.title, roadmap.description)
    
    db_roadmap = models.Roadmap(
        **roadmap.dict(),
        content=content,
        owner_id=current_user.id
    )
    db.add(db_roadmap)
    db.commit()
    db.refresh(db_roadmap)
    return db_roadmap

@router.get("/roadmaps", response_model=List[schemas.Roadmap])
def list_roadmaps(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    roadmaps = db.query(models.Roadmap)\
        .filter(models.Roadmap.owner_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return roadmaps

@router.get("/roadmaps/{roadmap_id}", response_model=schemas.Roadmap)
def get_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    roadmap = db.query(models.Roadmap)\
        .filter(models.Roadmap.id == roadmap_id)\
        .first()
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found"
        )
    if roadmap.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return roadmap

@router.put("/roadmaps/{roadmap_id}", response_model=schemas.Roadmap)
def update_roadmap(
    roadmap_id: int,
    roadmap_update: schemas.RoadmapUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    roadmap = db.query(models.Roadmap)\
        .filter(models.Roadmap.id == roadmap_id)\
        .first()
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found"
        )
    if roadmap.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    for field, value in roadmap_update.dict(exclude_unset=True).items():
        setattr(roadmap, field, value)
    db.commit()
    db.refresh(roadmap)
    return roadmap

@router.delete("/roadmaps/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a roadmap
    """
    roadmap = db.query(models.Roadmap)\
        .filter(models.Roadmap.id == roadmap_id)\
        .first()
    
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found"
        )
    
    if roadmap.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(roadmap)
    db.commit()
    return None

def get_user_roadmaps(user):
    db = next(get_db())
    return db.query(models.Roadmap).filter(models.Roadmap.owner_id == user.id).all() 