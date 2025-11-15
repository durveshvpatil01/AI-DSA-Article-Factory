# backend/agents/clarifier.py
import json
from openai import OpenAI
import os

# TODO: Add more robust error handling and input validation.
# TODO: Allow for more flexible input schemas.
# TODO: Use a more specific model version for reproducibility.

def clarify(job_json: dict) -> dict:
    """
    Takes a job dictionary and generates a normalized specification for an article.

    Args:
        job_json: A dictionary containing the job details.
                  Expected keys: 'topic', 'level', 'language', 'examples'.

    Returns:
        A dictionary containing the normalized specification.

    Raises:
        ValueError: If required keys are missing from the input dictionary.
        json.JSONDecodeError: If the model output is not valid JSON.
    """
    # 1. Validate input
    required_keys = ['topic', 'level', 'language', 'examples']
    for key in required_keys:
        if key not in job_json:
            raise ValueError(f"Missing required key in job_json: '{key}'")

    client = OpenAI()

    # 2. Create the prompt from the job dictionary
    system_prompt = """
You are a helpful content planning assistant for an educational platform that teaches Data Structures and Algorithms (DSA).
Your task is to take a raw article request and convert it into a structured, normalized specification.
The output must be a single JSON object with the following keys:
- "audience": A description of the target audience (e.g., "Beginner or intermediate DSA learners").
- "goal": A clear, concise goal for the article (e.g., "Explain the concept of recursion clearly").
- "word_count": An estimated integer word count for the article (e.g., 1500).
- "selected_examples": A list of specific, relevant code examples to include.
- "angles": A list of 2-3 alternative or creative ways to teach the topic.

Do not include any text outside of the JSON object.
"""

    user_prompt = f"""
Here is the article request:
Topic: {job_json['topic']}
Level: {job_json['level']}
Programming Language: {job_json['language']}
Suggested Examples: {', '.join(job_json['examples'])}
"""

    # 3. Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7
    )

    reply_text = response.choices[0].message.content.strip()

    # 4. Parse the JSON response
    try:
        normalized_spec = json.loads(reply_text)
        return normalized_spec
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from model response: {e}")
        print(f"Raw response: {reply_text}")
        raise
