# llm_calling.py

import json
import asyncio
import anthropic
from pydantic import BaseModel
from typing import List, Type, TypeVar
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Define a generic type for output models
T = TypeVar("T", bound=BaseModel)

async def create_chat_completions(messages: List[dict], output_model: Type[T], model: str) -> T:
    """
    Performs an asynchronous chat completion call using Anthropic's Claude Messages API,
    instructing the model to return output in a JSON format matching the provided Pydantic model.
    
    This pattern is based on Anthropic's function calling approach (see
    https://docs.anthropic.com/claude/docs/function-calling) where you supply a JSON schema
    to guide the response.
    
    Parameters:
        messages (List[dict]): A list of conversation messages.
        output_model (Type[T]): A Pydantic model defining the expected JSON output.
        model (str): The Anthropic model to use for the completion.
    
    Returns:
        T: An instance of output_model parsed from the model's JSON response.
    """
    # Extract the JSON schema from the provided Pydantic model.
    schema_json = output_model.schema_json(indent=2)
    
    # Build prompt instructions similar to typical function calling examples.
    instructions = (
        "You are a helpful assistant. Please provide the output in a valid JSON format "
        "that conforms exactly to the following JSON schema. Do not include any additional text:\n\n"
        f"{schema_json}\n"
    )
    
    # Combine the instructions with the user's conversation.
    conversation_text = "\n".join(msg.get("content", "") for msg in messages)
    prompt_text = instructions + conversation_text
    
    # Create the Anthropic client.
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    
    # Use the Messages API by sending a single user message with our prompt.
    response = await asyncio.to_thread(
        client.messages.create,
        messages=[{"role": "user", "content": prompt_text}],
        model=model,
        max_tokens=300,  # Required parameter
        stop_sequences=[anthropic.HUMAN_PROMPT]
    )
    
    # Access the text from the first message in the response content.
    response_text = response.content[0].text
    try:
        parsed_output = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nResponse text: {response_text}")
    
    # Parse and validate the result using the provided output_model.
    return output_model.parse_obj(parsed_output)

# A simple test if this script is run directly.
if __name__ == "__main__":
    import asyncio
    from pydantic import Field

    class ListOfStrings(BaseModel):
        output: List[str] = Field(..., description="A list of strings.")

    test_messages = [
        {"role": "user", "content": "Please provide a list of strings using the Anthropic function calling demo."}
    ]

    async def main():
        # Use a model ID that supports the Messages API (e.g. "claude-3-5-sonnet-20241022")
        result = await create_chat_completions(messages=test_messages, output_model=ListOfStrings, model="claude-3-5-sonnet-20241022")
        # Use model_dump_json() for Pydantic v2 compatibility
        print(result)
        print(type(result))
        print(result.model_dump_json(indent=2))
    
    asyncio.run(main())
