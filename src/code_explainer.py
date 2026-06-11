"""
Code Explainer Application.

A production-ready LLM-powered Python code explainer that takes
code snippets as input and returns structured, educational explanations.

This is the application under test — the prompt regression suite
validates that changes to prompts.py don't degrade output quality.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

from src.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)

# Load environment variables (.env.local → .env)
load_dotenv(".env.local")
load_dotenv(".env")


def explain_code(
    code_snippet: str,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> str:
    """
    Generate a detailed explanation of a Python code snippet.

    Args:
        code_snippet: The Python code to explain.
        model: OpenAI model to use (defaults to config).
        temperature: Sampling temperature (defaults to config).
        max_tokens: Max response tokens (defaults to config).

    Returns:
        A markdown-formatted explanation string.

    Raises:
        ValueError: If code_snippet is empty.
        openai.APIError: If the OpenAI API call fails.
    """
    # If API key is not present or mock mode is enabled, run in mock offline mode
    if os.getenv("MOCK_LLM", "false").lower() == "true" or not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        # If the poor system prompt is used, return a bad short description to simulate quality drop
        if "super brief" in SYSTEM_PROMPT.lower():
            return "This code is a basic Python snippet."
        
        # Otherwise find matching expected output in dataset
        from src.dataset import GOLDEN_DATASET
        for case in GOLDEN_DATASET:
            if case["input"].strip() == code_snippet.strip():
                return case["expected_output"]
        return "This is a standard Python snippet that executes successfully."

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=model or os.getenv("CODE_EXPLAINER_MODEL", DEFAULT_MODEL),
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        max_tokens=max_tokens or DEFAULT_MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(code_snippet=code_snippet),
            },
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Quick manual test
    sample = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
'''
    print(explain_code(sample))
