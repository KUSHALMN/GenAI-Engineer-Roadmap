import json
from typing import Dict, List, Any
try:
    from .templates import PromptTemplate, FewShotPromptTemplate, create_cot_prompt
    from .evaluator import PromptEvaluator
except ImportError:
    from templates import PromptTemplate, FewShotPromptTemplate, create_cot_prompt
    from evaluator import PromptEvaluator

def run_prompt_benchmark() -> Dict[str, Any]:
    # 1. Baseline Zero-shot prompt
    zero_shot_template = PromptTemplate(
        template="Classify the sentiment of the text as Positive, Negative, or Neutral.\nText: {text}\nSentiment:",
        input_variables=["text"]
    )

    # 2. Production Few-shot calibrated prompt
    examples = [
        {"text": "The battery lasts only 2 hours and the screen flickers.", "sentiment": "Negative"},
        {"text": "Setup was intuitive, customer service answered immediately!", "sentiment": "Positive"},
        {"text": "Package arrived on Tuesday in a cardboard box.", "sentiment": "Neutral"}
    ]
    few_shot = FewShotPromptTemplate(
        prefix="Classify customer review sentiment accurately. Output only the category.",
        example_template="Review: {text}\nSentiment: {sentiment}",
        examples=examples,
        suffix="Review: {text}\nSentiment:",
        input_variables=["text"]
    )

    # Test sample
    test_case = {
        "text": "The camera quality exceeded expectations, though the shipping was delayed 2 days.",
        "ground_truth": "Positive",
        "zero_shot_simulated_output": "The sentiment appears to be mostly positive with a minor negative note.",
        "few_shot_simulated_output": "Positive"
    }

    eval_zero = PromptEvaluator.evaluate_response(
        test_case["zero_shot_simulated_output"], test_case["ground_truth"]
    )
    eval_few = PromptEvaluator.evaluate_response(
        test_case["few_shot_simulated_output"], test_case["ground_truth"]
    )

    return {
        "test_input": test_case["text"],
        "ground_truth": test_case["ground_truth"],
        "zero_shot_eval": eval_zero,
        "few_shot_eval": eval_few,
        "cot_sample_prompt": create_cot_prompt("Extract all financial liabilities", "Quarterly SEC 10-Q filing text")
    }

if __name__ == "__main__":
    results = run_prompt_benchmark()
    print("==================================================")
    print("🧠 Production Prompt Engineering Benchmark")
    print("==================================================")
    print(json.dumps(results, indent=2))
