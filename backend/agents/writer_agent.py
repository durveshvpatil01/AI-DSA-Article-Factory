# backend/agents/writer_agent.py
import json
import os
import re
from openai import OpenAI

# TODO: Make the article structure more flexible and configurable.
# TODO: Implement a revision loop based on editor feedback.
# TODO: Add more sophisticated error handling for API calls.

def _create_slug(topic: str) -> str:
    """Creates a URL-friendly slug from a topic string."""
    s = topic.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s.strip('-')

def write_article(spec: dict) -> str:
    """
    Generates a full-length article in Markdown format based on a spec.

    Args:
        spec: A dictionary containing the article specification.
              Expected keys: 'topic', 'goal', 'audience', 'word_count',
                             'language', 'selected_examples'.

    Returns:
        A string containing the complete article in Markdown format.

    Raises:
        ValueError: If required keys are missing from the spec dictionary.
    """
    # 1. Validate input
    required_keys = ['topic', 'goal', 'audience', 'word_count', 'language', 'selected_examples']
    for key in required_keys:
        if key not in spec:
            raise ValueError(f"Missing required key in spec: '{key}'")

    client = OpenAI()

    # 2. Construct the detailed prompt
    system_prompt = f"""
You are a professional technical writer specializing in Data Structures and Algorithms (DSA).
Your task is to write a high-quality, educational article in Markdown format.

The article must follow this exact structure:
1.  `# Title`: A compelling title for the article.
2.  `## Introduction`: A brief introduction to the concept.
3.  `## Concept Explanation`: A detailed explanation of the core concept.
4.  `## Example Problems`: Provide 1-3 full code examples for the specified problems. Each example must be in a fenced code block with the correct language identifier.
5.  `## Complexity Analysis`: Analyze the time and space complexity of the solution(s).
6.  `## FAQ`: Include a section with 3 frequently asked questions and their answers.
7.  `## Conclusion`: A summary of the key takeaways.

Adhere to all instructions in the user prompt regarding topic, audience, language, and examples.
Do not include any text or commentary outside of the Markdown article itself.
"""

    user_prompt = f"""
Please write an article based on the following specification:
- **Topic**: {spec['topic']}
- **Goal**: {spec['goal']}
- **Target Audience**: {spec['audience']}
- **Estimated Word Count**: {spec['word_count']}
- **Programming Language for Examples**: {spec['language']}
- **Required Examples**: {', '.join(spec['selected_examples'])}
"""

    # 3. Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    article_md = response.choices[0].message.content.strip()

    # 4. Save a sample to the examples directory
    if article_md:
        topic_slug = _create_slug(spec['topic'])
        example_path = os.path.join('examples', f"{topic_slug}.md")
        os.makedirs('examples', exist_ok=True)
        with open(example_path, "w", encoding="utf-8") as f:
            f.write(article_md)
        print(f"Sample article saved to {example_path}")

    return article_md
