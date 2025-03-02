from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Any, List

from ...core.security import get_current_user
from ...database import get_db
from ... import models, schemas
from llm_utils import text_generation

router = APIRouter(tags=["roadmaps"])

@router.post("/roadmaps", response_model=schemas.Roadmap)
async def create_roadmap(
    roadmap: schemas.RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    # Generate roadmap content using Anthropic
    content = await text_generation.generate_roadmap_content(roadmap.title, roadmap.description)
    
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

@router.get("/roadmaps/{roadmap_id}/lessons", response_model=List[schemas.Lesson])
def list_lessons(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    lessons = db.query(models.Lesson)\
        .filter(models.Lesson.roadmap_parent_id == roadmap_id)\
        .filter(models.Lesson.owner_id == current_user.id)\
        .all()
    return lessons

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

@router.post("/roadmaps/{roadmap_id}/generate-lessons", response_model=List[schemas.Lesson])
async def generate_lessons(
    roadmap_id: int,
    input_data: schemas.LessonInput,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Any:
    # Check if the roadmap exists and belongs to the current user
    roadmap = db.query(models.Roadmap)\
        .filter(models.Roadmap.id == roadmap_id)\
        .first()
    if not roadmap or roadmap.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found or not authorized"
        )

    # Find the maximum lesson ID in the database
    max_id_result = db.query(func.max(models.Lesson.id)).first()
    next_id = 1 if max_id_result[0] is None else max_id_result[0] + 1

    # Find the maximum order for lessons in this roadmap
    max_order_result = db.query(func.max(models.Lesson.order))\
        .filter(models.Lesson.roadmap_parent_id == roadmap_id)\
        .first()
    next_order = 1 if max_order_result[0] is None else max_order_result[0] + 1

    # Generate lesson topics using the input
    topics = [
        f"Introduction to {input_data.topic}",
        f"Basic concepts of {input_data.topic}",
        f"Intermediate {input_data.topic} techniques",
        f"Advanced {input_data.topic} strategies",
        f"Mastering {input_data.topic} and next steps"
    ]

    # Import necessary modules for LLM content generation
    from app.llm_utils import create_chat_completions
    from pydantic import BaseModel, Field
    from typing import List as TypeList

    # Define a Pydantic model for lesson content generation
    class LessonContent(BaseModel):
        title: str = Field(..., description="The title of the lesson")
        objectives: TypeList[str] = Field(..., description="List of learning objectives for the lesson")
        content: str = Field(..., description="The main educational content of the lesson in markdown format")
        summary: str = Field(..., description="A brief summary of what was covered in the lesson")

    # Generate 5 lessons based on the input using LLM
    lessons = []
    for i in range(5):
        # Create a prompt for the LLM based on the current topic
        messages = [
            {
                "role": "user", 
                "content": f"""Please create a comprehensive lesson on "{topics[i]}" for learners interested in finance.
                
                This is lesson {i+1} in a series of 5 lessons about {input_data.topic}.
                
                The lesson should include:
                1. Clear learning objectives
                2. Detailed educational content with examples
                3. A concise summary
                
                Make the content thorough and accurate, focusing on financial concepts and practical applications.
                Ensure the content is well-structured with proper headings using markdown format."""
            }
        ]
        
        try:
            # Use the LLM to generate the lesson content
            lesson_content_model = await create_chat_completions(
                messages=messages,
                output_model=LessonContent,
                model="claude-3-5-sonnet-20240620"  # You may need to adjust the model name
            )
            
            # Format the lesson content in markdown
            formatted_content = f"""## {lesson_content_model.title}

### Objectives
{chr(10).join([f'- {objective}' for objective in lesson_content_model.objectives])}

### Content
{lesson_content_model.content}

### Summary
{lesson_content_model.summary}
"""
        except Exception as e:
            # Fallback content in case of any issues with the LLM
            formatted_content = f"""# {topics[i]}

### Objectives
- Understand the key concepts related to this lesson
- Apply the knowledge in practical scenarios
- Develop skills in {input_data.topic}

### Content
This is a placeholder content for {topics[i]}.
Due to technical limitations, we couldn't generate the full content at this time.
Please try again later or contact support if this issue persists.

### Summary
This lesson would have covered the fundamentals of {topics[i].lower()}.
"""
            
        lesson = models.Lesson(
            id=next_id + i,
            roadmap_parent_id=roadmap_id,
            owner_id=current_user.id,
            unlocked=i == 0,  # Only the first lesson is unlocked initially
            order=next_order + i,
            name=topics[i],
            content=formatted_content
        )
        db.add(lesson)
        lessons.append(lesson)

    db.commit()
    for lesson in lessons:
        db.refresh(lesson)

    return lessons 