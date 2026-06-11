import os
import json
import sys


def pytest_sessionfinish(session, exitstatus):
    """
    pytest hook called at the end of the test session.
    Dynamically extracts SCORES from the test module to avoid import conflicts.
    Saves scores to result/scores.json.
    """
    scores = []
    # Print all modules containing 'SCORES' to debug path differences
    for name, module in list(sys.modules.items()):
        if hasattr(module, "SCORES"):
            print(
                f"[DEBUG] Found module with SCORES: {name} (type: {type(module.SCORES)}, len: {len(module.SCORES)})"
            )
            if module.SCORES:
                scores = module.SCORES

    if scores:
        os.makedirs("result", exist_ok=True)
        with open("result/scores.json", "w") as f:
            json.dump(scores, f, indent=2)
        print(f"\nSaved {len(scores)} evaluation scores to result/scores.json")
    else:
        print("\nWarning: No evaluation scores were collected.")
