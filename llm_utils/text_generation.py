"""
Text generation utilities using llm-utils for roadmap generation.
"""

async def generate_roadmap_content(title, description):
    """
    Generate roadmap content based on title and description.
    
    Args:
        title (str): Roadmap title
        description (str): Roadmap description
        
    Returns:
        str: Generated roadmap content with markdown formatting
    """
    from llm_utils import TextGenerator
    
    # Create the prompt for the roadmap generation
    prompt = f"""
    Create a detailed learning roadmap based on the following:
    
    Title: {title}
    Description: {description}
    
    The roadmap should include:
    1. A brief introduction
    2. 5-7 major steps or milestones
    3. Key resources or skills needed for each step
    4. Expected outcomes or achievements
    
    Format the output in markdown with proper headings, lists, and structure.
    """
    
    # Initialize text generator
    generator = TextGenerator()
    
    # Generate roadmap content (returning a placeholder for now, replace with actual call)
    # In a real implementation, you would call generator.generate_text(prompt) or similar
    generated_content = f"""
# {title}

{description}

## Introduction
This roadmap provides a structured path to mastering {title}.

## Step 1: Fundamentals
- Learn the basic concepts
- Practice with simple exercises
- Resources: Beginner tutorials and documentation

## Step 2: Core Skills Development
- Build small projects
- Understand best practices
- Resources: Intermediate courses and documentation

## Step 3: Advanced Techniques
- Implement complex features
- Optimize performance
- Resources: Advanced tutorials and case studies

## Step 4: Real-world Application
- Work on comprehensive projects
- Integrate with other technologies
- Resources: Project-based learning platforms

## Step 5: Mastery and Specialization
- Contribute to open-source projects
- Develop specialized skills
- Resources: Community forums and advanced documentation

## Expected Outcomes
- Ability to build and deploy production-ready applications
- Understanding of best practices and optimization techniques
- Confidence in tackling complex problems in this domain
"""
    
    return generated_content 