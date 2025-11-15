# AI DSA Article Factory

This project is a skeleton for an AI-powered content creation pipeline, inspired by the concepts in the "AI Content Factory" notebook. It uses a series of modular AI agents to automate the process of generating a high-quality, SEO-optimized article from a simple topic idea.

## Project Structure

- `backend/`: Contains the core application logic.
  - `agents/`: Houses the individual AI agents, each responsible for a specific task in the content creation pipeline.
  - `tests/`: Contains unit tests for the backend components.
  - `utils/`: Contains utility functions, such as the Markdown to HTML converter.
  - `app.py`: The main orchestrator that runs the content creation pipeline.
- `docs/`: Contains project documentation.
- `examples/`: Contains sample data and outputs from the pipeline.

## How it Works

The pipeline is orchestrated by `backend/app.py` and follows these steps:

1. **Clarifier Agent**: Asks clarifying questions to refine the user's intent.
2. **Search Agent**: Gathers up-to-date context from the web.
3. **POV Agent**: Forms a thesis and a plan for the article.
4. **SEO Agent**: Recommends keywords for optimization.
5. **Writer Agent**: Drafts the full article.
6. **Editor Agent**: Reviews the article for quality and can approve it or send it back for revision.
7. **Designer Agent**: Generates a feature image for the article.
8. **Web Dev Agent**: Converts the final article into HTML.
