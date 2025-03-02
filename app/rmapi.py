from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
import roadmap
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Roadmap API",
    description="API for accessing financial education roadmap content",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class RoadmapRequest(BaseModel):
    roadmap_path: str
    experience_level: int
    user_id: Optional[str] = None

class TopicRequest(BaseModel):
    topic: str
    roadmap_path: str
    experience_level: int
    user_id: Optional[str] = None

class RoadmapResponse(BaseModel):
    roadmap_path: str
    experience_level: int
    topics: List[str]
    
class TopicResponse(BaseModel):
    topic: str
    content: str
    roadmap_path: str
    experience_level: int

# Create a cache for roadmap instances to improve performance
roadmap_cache = {}

def get_roadmap(roadmap_path: str, experience_level: int) -> roadmap.Roadmap:
    """Helper function to get or create a Roadmap instance"""
    cache_key = f"{roadmap_path}_{experience_level}"
    
    if cache_key not in roadmap_cache:
        roadmap_cache[cache_key] = roadmap.Roadmap(
            roadmap_path=roadmap_path,
            experience_level=experience_level
        )
    
    return roadmap_cache[cache_key]

# API Endpoints
@app.post("/roadmap/", response_model=RoadmapResponse)
async def create_roadmap(request: RoadmapRequest):
    """Create a new roadmap for a user"""
    try:
        rm = get_roadmap(request.roadmap_path, request.experience_level)
        
        # In a real application, you might want to store the user's roadmap 
        # information in a database here using the user_id
        
        # For this example, we'll just return the roadmap details
        return {
            "roadmap_path": request.roadmap_path,
            "experience_level": request.experience_level,
            "topics": rm.get_topics() if hasattr(rm, 'get_topics') else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating roadmap: {str(e)}")

@app.get("/roadmap/{roadmap_path}")
async def get_roadmap_details(
    roadmap_path: str,
    experience_level: int = Query(1, description="User experience level (1=beginner, etc.)")
):
    """Get roadmap details including available topics"""
    try:
        rm = get_roadmap(roadmap_path, experience_level)
        
        # Assuming there's a method to get topics, if not, modify accordingly
        topics = rm.get_topics() if hasattr(rm, 'get_topics') else []
        
        return {
            "roadmap_path": roadmap_path,
            "experience_level": experience_level,
            "topics": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving roadmap: {str(e)}")

@app.post("/topic/", response_model=TopicResponse)
async def generate_topic_content(request: TopicRequest):
    """Generate content for a specific topic"""
    try:
        rm = get_roadmap(request.roadmap_path, request.experience_level)
        
        # Generate the topic content
        topic_content = rm.generate_topic(request.topic)
        
        # In a real application, you might want to store the generated content
        # or track the user's progress through topics
        
        return {
            "topic": request.topic,
            "content": topic_content,
            "roadmap_path": request.roadmap_path,
            "experience_level": request.experience_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating topic: {str(e)}")

@app.get("/topic/{topic}")
async def get_topic_content(
    topic: str,
    roadmap_path: str = Query(..., description="The roadmap path"),
    experience_level: int = Query(1, description="User experience level")
):
    """Get content for a specific topic via GET request"""
    try:
        rm = get_roadmap(roadmap_path, experience_level)
        topic_content = rm.generate_topic(topic)
        
        return {
            "topic": topic,
            "content": topic_content,
            "roadmap_path": roadmap_path,
            "experience_level": experience_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving topic: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 