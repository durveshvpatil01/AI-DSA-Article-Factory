# backend/agents/seo_agent.py

# TODO: Implement the SEO Agent
#
# Expected Function Signature:
# def generate_seo_keywords(project_path: str, topic: str, clarifications: dict, pov_plan: dict) -> dict:
#
# Expected Payload (Input):
# - project_path: str - The path to the current article's project folder.
# - topic: str - The article topic.
# - clarifications: dict - The user's answers to the clarifying questions.
# - pov_plan: dict - The POV plan from the POV Agent.
#
# Expected Payload (Output):
# A dictionary with primary and secondary keywords, a meta description, and a suggested SEO title.
# {
#   "primary_keywords": ["...", "..."],
#   "secondary_keywords": ["...", "..."],
#   "meta_description": "...",
#   "suggested_seo_title": "..."
# }
