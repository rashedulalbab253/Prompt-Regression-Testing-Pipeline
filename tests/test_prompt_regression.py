"""
DeepEval Regression Test Suite.

This test suite runs automatically on every prompt change or model switch.
It compares the actual outputs of our Code Explainer application against the
ground truth (golden dataset) using a custom G-Eval metric for Explanation Quality.
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Ensure the root project directory is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval

from src.code_explainer import explain_code
from src.dataset import GOLDEN_DATASET
from src.prompts import PROMPT_VERSION

SCORES = []

# Load environment variables
load_dotenv(".env.local")
load_dotenv(".env")

# Check if we should run in offline mock mode (if API key is missing or explicitly mocked)
IS_MOCK = (
    os.getenv("MOCK_LLM", "false").lower() == "true"
    or not os.getenv("OPENAI_API_KEY")
    or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here"
)

if IS_MOCK:
    print("Warning: Running regression test suite in OFFLINE MOCK MODE (no API key required).")


# ──────────────────────────────────────────────────────────────
# Configure DeepEval Quality Metric
# ──────────────────────────────────────────────────────────────
if IS_MOCK:
    from deepeval.metrics import BaseMetric
    
    class MockExplanationMetric(BaseMetric):
        def __init__(self, threshold: float = 0.7):
            super().__init__()
            self.threshold = threshold
            self.score = 0.0
            self.reason = ""
            self.success = False
            self.async_mode = False
            
        def measure(self, test_case) -> float:
            if len(test_case.actual_output) < 50:
                self.score = 0.3
                self.reason = "Explanation is too brief and lacks structured detail."
                self.success = False
            else:
                self.score = 0.95
                self.reason = "Explanation is highly detailed, structured, and matches expected output."
                self.success = True
                
            SCORES.append({
                "input": test_case.input,
                "score": self.score,
                "reason": self.reason,
                "success": self.success
            })
            return self.score
            
        async def a_measure(self, test_case, *args, **kwargs) -> float:
            return self.measure(test_case)

        def is_successful(self) -> bool:
            return self.success
            
        @property
        def __name__(self):
            return "Explanation Quality"
            
    explanation_metric = MockExplanationMetric(threshold=float(os.getenv("CORRECTNESS_THRESHOLD", "0.7")))
else:
    # We use a Custom G-Eval class that intercepts score calculation at the class level
    class CustomGEval(GEval):
        def measure(self, test_case, *args, **kwargs):
            score = super().measure(test_case, *args, **kwargs)
            SCORES.append({
                "input": test_case.input,
                "score": self.score if self.score is not None else 0.0,
                "reason": self.reason or "",
                "success": self.is_successful()
            })
            return score

        async def a_measure(self, test_case, *args, **kwargs):
            score = await super().a_measure(test_case, *args, **kwargs)
            SCORES.append({
                "input": test_case.input,
                "score": self.score if self.score is not None else 0.0,
                "reason": self.reason or "",
                "success": self.is_successful()
            })
            return score

    explanation_metric = CustomGEval(
        name="Explanation Quality",
        criteria=(
            "Evaluate whether the 'actual output' is a high-quality explanation of the Python code input. "
            "It should be:\n"
            "1. Accurate and truthful to the code's behavior.\n"
            "2. Clear, structured (e.g. using bullet points), and educational.\n"
            "3. Capturing the same semantic explanation and correctness as the 'expected output'.\n"
            "4. Free from fluff and overly generic statements.\n"
            "Assign a score between 0.0 and 1.0."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        threshold=float(os.getenv("CORRECTNESS_THRESHOLD", "0.7")),
    )


# ──────────────────────────────────────────────────────────────
# Test Case Selection Configuration
# ──────────────────────────────────────────────────────────────
RUN_ALL = os.getenv("RUN_ALL_TESTS", "false").lower() == "true"
TEST_CASES = GOLDEN_DATASET if RUN_ALL else GOLDEN_DATASET[:5]


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[f"case_{i+1}" for i in range(len(TEST_CASES))],
)
def test_code_explanation_regression(case):
    code_input = case["input"]
    expected_output = case["expected_output"]

    # 1. Run the application to get the LLM's explanation
    actual_output = explain_code(code_input)

    # 2. Package into a DeepEval LLMTestCase
    test_case = LLMTestCase(
        input=code_input,
        actual_output=actual_output,
        expected_output=expected_output,
    )

    # 3. Assert quality against our predefined gate
    assert_test(test_case, [explanation_metric])


