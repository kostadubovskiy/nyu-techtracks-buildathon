from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users, auth, roadmap
from app.core.security import get_current_user, get_current_user_sync
from flask import Flask, render_template, redirect, url_for, request
import os
from app.schemas import UserCreate
from app.database import get_db
from app.models import Roadmap
from app.api.endpoints.roadmap import get_user_roadmaps

# FastAPI app
app = FastAPI(title="TechTracks API")

# Flask app
flask_app = Flask(__name__, 
                 static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                 template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Configure CORS for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI static files and templates
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routers for FastAPI
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(roadmap.router, prefix="/api/v1")

# Flask routes
@flask_app.route('/')
def home():
    token = request.cookies.get('access_token')
    user = None
    if token:
        try:
            user = get_current_user(token=token)
        except HTTPException:
            pass
    return render_template("index.html", user=user)

@flask_app.route('/register', methods=['GET'])
def register_page():
    return render_template("register.html", user=None)

@flask_app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        password = request.form['password']
        # Get database session
        db = next(get_db())
        
        # Use the synchronous create user function
        user = users.create_user_sync(user=UserCreate(email=email, password=password), db=db)
        return redirect(url_for('login_page'))
    except HTTPException as e:
        return render_template("register.html", error=e.detail, user=None), e.status_code
    except Exception as e:
        return render_template("register.html", error=str(e), user=None), 500

@flask_app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html", user=None)

@flask_app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        
        # Get database session
        db = next(get_db())
        
        # Use the synchronous login function
        token_data = auth.login_sync(email=email, password=password, db=db)
        response = redirect(url_for('roadmaps_page'))
        response.set_cookie('access_token', f"Bearer {token_data['access_token']}")
        return response
    except HTTPException as e:
        return render_template("login.html", error=e.detail, user=None), e.status_code
    except Exception as e:
        return render_template("login.html", error=str(e), user=None), 500

@flask_app.route('/roadmaps', methods=['GET'])
def roadmaps_page():
    token = request.cookies.get('access_token')
    if not token:
        return redirect(url_for('login_page'))
    
    try:
        # Get database session
        db = next(get_db())
        current_user = get_current_user_sync(db=db, token=token)
        user_roadmaps = get_user_roadmaps(user=current_user)
        
        return render_template(
            "roadmaps.html",
            roadmaps=user_roadmaps,
            user=current_user
        )
    except HTTPException:
        return redirect(url_for('login_page'))
    except AttributeError as e:
        return render_template("error.html", error=str(e)), 500

@flask_app.route('/roadmaps', methods=['POST'])
def create_roadmap():
    token = request.cookies.get('access_token')
    if not token:
        return redirect(url_for('login_page'))
    
    try:
        current_user = get_current_user(token=token)
        title = request.form['title']
        description = request.form['description']
        
        # Get database session
        db = next(get_db())
        
        # Create roadmap using the model directly
        new_roadmap = Roadmap(
            title=title,
            description=description,
            owner_id=current_user.id
        )
        db.add(new_roadmap)
        db.commit()
        db.refresh(new_roadmap)
        
        return redirect(url_for('roadmaps_page'))
    except HTTPException as e:
        user_roadmaps = roadmap.get_user_roadmaps(current_user)
        return render_template(
            "roadmaps.html",
            roadmaps=user_roadmaps,
            user=current_user,
            error=e.detail
        ), e.status_code

@flask_app.route('/logout')
def logout():
    response = redirect(url_for('home'))
    response.delete_cookie('access_token')
    return response

if __name__ == '__main__':
    flask_app.run(debug=True)
    