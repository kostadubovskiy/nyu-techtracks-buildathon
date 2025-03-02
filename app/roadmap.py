import anthropic
import os
from dotenv import load_dotenv
from flask import (
    Blueprint, request, render_template, g, flash, redirect, url_for, session
)

# Import database models - adjust imports according to your actual database models
from .models import User, UserRoadmap
from .database import get_db

load_dotenv()

client = anthropic.Anthropic(
       api_key=os.environ.get("ANTHROPIC_API_KEY")
   )

bp = Blueprint('lesson', __name__, url_prefix='/lesson')

class Roadmap:
    def __init__(self, roadmap_path: str, previous_topics: list[str] = [], experience_level: int = 1):
        self.roadmap_path = roadmap_path
        self.previous_topics = previous_topics
        self.experience_level = experience_level
        

    def generate__levels(self):
        """Generate list of topics for a given roadmap"""

        # Prompts for generating roadmap topics for first 5 levels
        if len(self.previous_topics) == 0:
            prompts = {
                1: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A complete beginner has reached out to you for help learning about {self.roadmap_path}.
                    Please generate a list of five topics that the user should learn about to start their path in {self.roadmap_path}, keeping in mind
                    that they are a beginner, and that the topics should be the ones most relevant to novices.
                    Examples of topics can include:
                    - The basics of {self.roadmap_path}
                    - The history of {self.roadmap_path}
                    - The importance of {self.roadmap_path}
                    - The different types of {self.roadmap_path}
                    - The benefits of {self.roadmap_path}
                    - The risks of {self.roadmap_path}
                """,
                2: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A beginner who has some vague background knowledge of finance has reached out to you for help learning about {self.roadmap_path}.
                    Please generate a list of five topics that the user should learn about to start their path in {self.roadmap_path}, keeping in mind
                    that they are a beginner but have some vague background, and that the topics should be the ones most relevant to someone at their skill level.
                    Examples of topics can include:
                    - The basics of {self.roadmap_path}
                    - The history of {self.roadmap_path}
                    - The importance of {self.roadmap_path}
                    - The different types of {self.roadmap_path}
                    - The benefits of {self.roadmap_path}
                    - The risks of {self.roadmap_path}
                """,
                3: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    An amateur who has some background knowledge of finance has reached out to you for help learning about {self.roadmap_path}.
                    Please generate a list of five topics that the user should learn about to start their path in {self.roadmap_path}, keeping in mind
                    that they are have some but not significant knowledge of {self.roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                    Examples of topics can include:
                    - The basics of {self.roadmap_path}
                    - The history of {self.roadmap_path}
                    - The importance of {self.roadmap_path}
                    - The different types of {self.roadmap_path}
                    - The benefits of {self.roadmap_path}
                    - The risks of {self.roadmap_path}
                """,
                4: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {self.roadmap_path}.
                    Please generate a list of five topics that the user should learn about to start their path in {self.roadmap_path}, keeping in mind
                    that they are have solid knowledge of {self.roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                    Examples of topics can include:
                    - The in-depth history of {self.roadmap_path}
                    - The importance of {self.roadmap_path}
                    - The different types of {self.roadmap_path}
                    - The benefits of {self.roadmap_path}
                    - The risks of {self.roadmap_path}
                """
            }

        else:
            prompts = {
                1: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A complete beginner has reached out to you for help learning about {self.roadmap_path}. They have previously learned about the following topics:
                    {self.previous_topics}.
                    Please generate a list of five topics that the user should learn about to continue their path in {self.roadmap_path}, keeping in mind
                    that they are a beginner, and that the topics should be the ones most relevant to novices.
                    The topics can build upon/expand on the previous topics.
                """,
                2: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A beginner who has some vague background knowledge of finance has reached out to you for help learning about {self.roadmap_path}. They have 
                    previously learned about the following topics: {self.previous_topics}.
                    Please generate a list of five topics that the user should learn about to continue their path in {self.roadmap_path}, keeping in mind
                    that they are a beginner but have some vague background, and that the topics should be the ones most relevant to someone at their skill level.
                    The topics can build upon/expand on the previous topics.
                """,
                3: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    An amateur who has some background knowledge of finance has reached out to you for help learning about {self.roadmap_path}. They have 
                    previously learned about the following topics: {self.previous_topics}.
                    Please generate a list of five topics that the user should learn about to continue their path in {self.roadmap_path}, keeping in mind
                    that they are have some but not significant knowledge of {self.roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                    The topics can build upon/expand on the previous topics.
                """,
                4: f"""
                    You are an experienced financial advisor who has helped many people learn about finance.
                    A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {self.roadmap_path}. They have 
                    previously learned about the following topics: {self.previous_topics}.
                    Please generate a list of five topics that the user should learn about to continue their path in {self.roadmap_path}, keeping in mind
                    that they are have solid knowledge of {self.roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                    The topics can build upon/expand on the previous topics.
                """
            }

        prompt = prompts[self.experience_level]

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            temperature=0.3,
            system="You are a helpful, accurate financial advisor who explains concepts simply and effectively, to people of all experience levels. You generate only bullet point lists of topics.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text


    def generate_topic(self, topic: str):
        """Generates topic summary and resources for a given roadmap level"""

        prompt = {
            1: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A complete beginner has reached out to you for help learning about {self.roadmap_path}, in particular about the topic: {topic}.
                Please generate an overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to a complete beginner. 
                Provide at most 3, well reviewed, and reputable resources.
            """,
            2: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A beginner who has some vague background knowledge of finance has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate an overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to a beginner who has some vague background knowledge of finance.
                Provide at most 3, well reviewed, and reputable resources.
            """,
            3: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                An amateur who has some background knowledge of finance has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate an overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to an amateur who has some background knowledge of finance. 
                Provide at most 3, well reviewed, and reputable resources.
            """,
            4: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate a detailed overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to a person with sound knowledge looking to learn in more depth.
                Provide at most 3, well reviewed, and reputable resources.
            """
        }

        prompt = prompt[self.experience_level]

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            temperature=0.3,
            system="You are a helpful, accurate financial advisor who explains concepts simply and effectively, to people of all experience levels." +
                "You accurately and intelligently provide resources according to the user's experience level, and verify their quality and existence." + 
                "You prioritize free resources, and provide links to the online resources, books or courses you suggest.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
    
<<<<<<< Updated upstream

# Add lesson route directly to the roadmap blueprint
@bp.route('/<string:topic>')
def show_lesson(topic):
    """Display a lesson for the given topic.
    
    Retrieves the user's roadmap info from the database and
    generates content for the requested topic.
    """
    # Get the current user ID from session
    user_id = session.get('user_id')
    if not user_id:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))
    
    # Get database connection
    db = get_db()
    
    # Query the database for user's roadmap information
    user_roadmap = db.execute(
        """
        SELECT ur.roadmap_path, ur.experience_level, ur.previous_topics
        FROM user_roadmap ur
        WHERE ur.user_id = ?
        """,
        (user_id,)
    ).fetchone()
    
    if not user_roadmap:
        # If no roadmap exists for the user, create a default one or redirect
        # This is just an example - modify according to your application logic
        flash("No roadmap found. Please select one first.")
        return redirect(url_for('select_roadmap'))
    
    # Create a Roadmap instance using the data from the database
    roadmap_path = user_roadmap['roadmap_path']
    experience_level = user_roadmap['experience_level']
    # Add this topic to the user's previous topics if not already there
    previous_topics = user_roadmap['previous_topics'].split(',') if user_roadmap['previous_topics'] else []
    
    # Create the Roadmap instance
    rm = Roadmap(roadmap_path=roadmap_path, previous_topics=previous_topics, experience_level=experience_level)
    
    # Generate content for the topic
    topic_content = rm.generate_topic(topic)
    
    # Render the template with the generated content
    return render_template('roadmap/lesson.html',
                          topic=topic,
                          content=topic_content)
=======
>>>>>>> Stashed changes

def main():
    rmp = Roadmap("Value Investing", 1)
    print(rmp.generate__levels())
    print(rmp.generate_topic("Financial Statements"))

if __name__ == "__main__":
    main()