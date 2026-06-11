#!/usr/bin/env python
"""
Regression Pipeline Runner.

A CLI script to easily run the prompt regression testing suite locally.
Enables developers to quickly toggle between subset validation and full suite
runs, and automatically configures environment parameters.
"""

import sys
import os
import subprocess
import argparse
from dotenv import load_dotenv

# Load env vars
load_dotenv(".env.local")
load_dotenv(".env")


def generate_histogram():
    import json
    scores_path = "result/scores.json"
    if not os.path.exists(scores_path):
        print("Warning: result/scores.json not found. Skipping histogram generation.")
        return

    try:
        with open(scores_path, "r") as f:
            data = json.load(f)

        scores = [item["score"] for item in data]
        if not scores:
            print("Warning: No scores found to plot.")
            return

        # Print text-based ASCII histogram to console
        print("\n--- Scores Distribution Histogram ---")
        bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        counts = [0] * (len(bins) - 1)
        for s in scores:
            for i in range(len(counts)):
                if bins[i] <= s < bins[i+1] or (i == len(counts) - 1 and s == bins[i+1]):
                    counts[i] += 1
                    break

        for i in range(len(counts)):
            bar = "*" * counts[i]
            print(f"{bins[i]:.1f} - {bins[i+1]:.1f}: {bar}")
        print("--------------------------------------")

        # Now try to generate image with matplotlib
        try:
            import matplotlib
            matplotlib.use("Agg")  # Non-interactive backend
            import matplotlib.pyplot as plt

            plt.figure(figsize=(8, 5))
            plt.hist(
                scores,
                bins=bins,
                edgecolor="white",
                color="#4F46E5",
                rwidth=0.85,
            )

            plt.title("Distribution of Prompt Quality Scores", fontsize=14, pad=15, fontweight="bold")
            plt.xlabel("Quality Score", fontsize=11, labelpad=10)
            plt.ylabel("Number of Test Cases", fontsize=11, labelpad=10)
            plt.xlim(0.0, 1.05)
            plt.ylim(bottom=0)
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            threshold = float(os.getenv("CORRECTNESS_THRESHOLD", "0.7"))
            plt.axvline(
                threshold,
                color="#EF4444",
                linestyle="dashed",
                linewidth=1.5,
                label=f"Quality Gate Threshold ({threshold})",
            )
            plt.legend(loc="upper left")

            output_path = "result/scores_histogram.png"
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"Successfully generated scores histogram: {output_path}")

            # Update summary.txt with text-based histogram as well
            summary_path = "result/summary.txt"
            if os.path.exists(summary_path):
                with open(summary_path, "a") as sf:
                    sf.write("\nScores Distribution:\n")
                    for i in range(len(counts)):
                        bar = "*" * counts[i]
                        sf.write(f"{bins[i]:.1f} - {bins[i+1]:.1f}: {bar}\n")

        except ImportError:
            print("Warning: matplotlib is not installed. Image histogram skipped.")
    except Exception as e:
        print(f"Warning: Failed to generate histogram: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Regression Testing Pipeline Runner"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all 50+ golden test cases (default runs a subset of 5 for speed)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Run pytest in verbose mode showing full outputs",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Override model under test (e.g. gpt-4o-mini, gpt-4o, gpt-3.5-turbo)",
    )

    args = parser.parse_args()

    # Configure Environment
    if args.all:
        os.environ["RUN_ALL_TESTS"] = "true"
        print("Running FULL regression suite (50+ cases)...")
    else:
        os.environ["RUN_ALL_TESTS"] = "false"
        print("Running SUBSET regression suite (5 test cases)...")

    if args.model:
        os.environ["CODE_EXPLAINER_MODEL"] = args.model
        print(f"Overriding code explainer model to: {args.model}")

    # Configure Mock Mode if API Key is not set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        os.environ["MOCK_LLM"] = "true"
        print("No OpenAI API Key found. Running pipeline in OFFLINE MOCK MODE.")
    else:
        print("OpenAI API Key detected. Running pipeline with live LLM evaluations.")

    # Ensure result directory exists
    os.makedirs("result", exist_ok=True)
    os.environ["DEEPEVAL_RESULTS_FOLDER"] = "result"

    # Construct and run pytest command
    cmd = ["pytest"]
    if args.verbose:
        cmd.append("-v")
    cmd.extend([
        "--junitxml=result/junit_report.xml",
        "tests/test_prompt_regression.py"
    ])

    print(f"Executing: {' '.join(cmd)}")
    print(f"Outputs will be saved in the 'result/' folder.")
    print("-" * 50)

    try:
        # Run pytest. DeepEval outputs detailed score logs and reasons to the console
        result = subprocess.run(cmd, check=True)
        print("-" * 50)
        print("Pipeline execution completed successfully. Quality gates passed.")
        with open("result/summary.txt", "w") as f:
            f.write("Status: SUCCESS\nAll quality gates passed successfully.\n")
        generate_histogram()
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print("Pipeline execution failed! One or more quality gates fell below threshold.")
        with open("result/summary.txt", "w") as f:
            f.write(f"Status: FAILED\nExit code: {e.returncode}\nQuality gates failed.\n")
        generate_histogram()
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
