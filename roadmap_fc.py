import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=secret_key
)

class Roadmap:
    def __init__(self, roadmap_path: str, experience_level: int = 1):
        self.roadmap_path = roadmap_path
        self.previous_topics = []
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
            model="claude-3-haiku-20240307",
            max_tokens=10000,
            temperature=0.3,
            system="You are a helpful, accurate financial advisor who explains concepts simply and effectively, to people of all experience levels.",
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
            """,
            2: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A beginner who has some vague background knowledge of finance has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate an overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to a beginner who has some vague background knowledge of finance.
            """,
            3: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                An amateur who has some background knowledge of finance has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate an overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to an amateur who has some background knowledge of finance.
            """,
            4: f"""
                You are an experienced financial advisor who has helped many people learn about finance.
                A person with sound knowledge looking to learn in more depth has reached out to you for help learning about {self.roadmap_path}, in particular
                about the topic: {topic}.
                Please generate a detailed overview of the topic, and provide a list of resources that the user can use to learn more about the topic.
                These resources should be ones that are most relevant to a person with sound knowledge looking to learn in more depth.
            """
        }

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10000,
            temperature=0.3,
            system="You are a helpful, accurate financial advisor who explains concepts simply and effectively, to people of all experience levels.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
