import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=secret_key
)

def generate_roadmap_topics(roadmap_path, previous_topics: list = None, experience_level: int = 1):
    """
    Generate list of topics for a given roadmap

    Args:
        roadmap_path (str): Roadmap name/specialization
        previous_topics (list): List of topics to build on, exclude, or explore in more depth
    Returns:
        list: List of topics for a given roadmap
    """

    # Prompts for generating roadmap topics for first 5 levels
    if not previous_topics:
        prompts = {
            1: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A complete beginner has reached out to you for help learning about {roadmap_path}.
                Please generate a list of five topics that the user should learn about to start their path in {roadmap_path}, keeping in mind
                that they are a beginner, and that the topics should be the ones most relevant to novices.
                Examples of topics can include:
                - The basics of {roadmap_path}
                - The history of {roadmap_path}
                - The importance of {roadmap_path}
                - The different types of {roadmap_path}
                - The benefits of {roadmap_path}
                - The risks of {roadmap_path}
            """,
            2: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A beginner who has some vague background knowledge of finance has reached out to you for help learning about {roadmap_path}.
                Please generate a list of five topics that the user should learn about to start their path in {roadmap_path}, keeping in mind
                that they are a beginner but have some vague background, and that the topics should be the ones most relevant to someone at their skill level.
                Examples of topics can include:
                - The basics of {roadmap_path}
                - The history of {roadmap_path}
                - The importance of {roadmap_path}
                - The different types of {roadmap_path}
                - The benefits of {roadmap_path}
                - The risks of {roadmap_path}
            """,
            3: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                An amateur who has some background knowledge of finance has reached out to you for help learning about {roadmap_path}.
                Please generate a list of five topics that the user should learn about to start their path in {roadmap_path}, keeping in mind
                that they are have some but not significant knowledge of {roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                Examples of topics can include:
                - The basics of {roadmap_path}
                - The history of {roadmap_path}
                - The importance of {roadmap_path}
                - The different types of {roadmap_path}
                - The benefits of {roadmap_path}
                - The risks of {roadmap_path}
            """,
            4: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {roadmap_path}.
                Please generate a list of five topics that the user should learn about to start their path in {roadmap_path}, keeping in mind
                that they are have solid knowledge of {roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                Examples of topics can include:
                - The in-depth history of {roadmap_path}
                - The importance of {roadmap_path}
                - The different types of {roadmap_path}
                - The benefits of {roadmap_path}
                - The risks of {roadmap_path}
            """
        }

    else:
        prompts = {
            1: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A complete beginner has reached out to you for help learning about {roadmap_path}. They have previously learned about the following topics:
                {previous_topics}.
                Please generate a list of five topics that the user should learn about to continue their path in {roadmap_path}, keeping in mind
                that they are a beginner, and that the topics should be the ones most relevant to novices.
                 The topics can build upon/expand on the previous topics.
            """,
            2: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A beginner who has some vague background knowledge of finance has reached out to you for help learning about {roadmap_path}. They have 
                previously learned about the following topics: {previous_topics}.
                Please generate a list of five topics that the user should learn about to continue their path in {roadmap_path}, keeping in mind
                that they are a beginner but have some vague background, and that the topics should be the ones most relevant to someone at their skill level.
                The topics can build upon/expand on the previous topics.
            """,
            3: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                An amateur who has some background knowledge of finance has reached out to you for help learning about {roadmap_path}. They have 
                previously learned about the following topics: {previous_topics}.
                Please generate a list of five topics that the user should learn about to continue their path in {roadmap_path}, keeping in mind
                that they are have some but not significant knowledge of {roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                The topics can build upon/expand on the previous topics.
            """,
            4: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {roadmap_path}. They have 
                previously learned about the following topics: {previous_topics}.
                Please generate a list of five topics that the user should learn about to continue their path in {roadmap_path}, keeping in mind
                that they are have solid knowledge of {roadmap_path}, and that the topics should be the ones most relevant to someone at their skill level.
                The topics can build upon/expand on the previous topics.
            """
        }

    prompt = prompts[experience_level]

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.3,
        system="You are a helpful, accurate financial advisor who explains concepts simply and effectively, to people of all experience levels.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
        