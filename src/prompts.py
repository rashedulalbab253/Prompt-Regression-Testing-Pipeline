"""
Prompt Configuration for the Code Explainer Application.

This module centralizes all prompt templates so that any change
is automatically tested by the regression suite before deployment.

Versioning Convention:
    - Bump PROMPT_VERSION on every change.
    - The CI pipeline logs this version alongside test results.
"""

# ──────────────────────────────────────────────────────────────
# Prompt Version — bump this on every edit
# ──────────────────────────────────────────────────────────────
PROMPT_VERSION = "1.0.0"

# ──────────────────────────────────────────────────────────────
# System Prompt — defines the Code Explainer's personality
# ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert Python code explainer designed for developers \
who are learning or reviewing code. Your role is to break down code snippets into \
clear, accurate, and educational explanations.

Follow these rules strictly:

1. **Structure**: Start with a one-sentence summary of what the code does, then \
   explain each significant section or line.
2. **Accuracy**: Never invent behavior. If the code has a bug, mention it.
3. **Clarity**: Use simple language. Avoid jargon unless you define it first.
4. **Completeness**: Cover inputs, outputs, edge cases, and any notable design patterns.
5. **Conciseness**: Keep explanations focused — no filler sentences.
6. **Format**: Use markdown with bullet points and code references where helpful."""

# ──────────────────────────────────────────────────────────────
# User Prompt Template — wraps the code snippet for the LLM
# ──────────────────────────────────────────────────────────────
USER_PROMPT_TEMPLATE = """Explain the following Python code snippet in detail:

```python
{code_snippet}
```

Provide:
1. A brief summary of what this code does
2. A line-by-line or section-by-section explanation
3. Any edge cases, potential issues, or notable design patterns
4. The expected input/output behavior"""

# ──────────────────────────────────────────────────────────────
# Model Configuration
# ──────────────────────────────────────────────────────────────
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.3  # Low for determinism in explanations
DEFAULT_MAX_TOKENS = 1024


# ──────────────────────────────────────────────────────────────
# 🚨 REGRESSION-BREAK VARIANT — uncomment to demo CI failure
# ──────────────────────────────────────────────────────────────
# Deliberately poor prompt that will cause quality regressions.
# Swap the SYSTEM_PROMPT above with this to watch the CI fail:
#
# SYSTEM_PROMPT = """You explain code. Be super brief. One sentence max. \
# Don't explain edge cases or patterns. Skip details."""
#
# DEFAULT_MODEL = "gpt-4o-mini"
# DEFAULT_TEMPERATURE = 1.0  # High randomness → inconsistent
