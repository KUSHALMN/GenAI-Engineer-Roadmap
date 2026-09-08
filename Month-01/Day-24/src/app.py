import json
from typing import Dict, Any

try:
    from .templates import PromptTemplate, FewShotPromptTemplate, create_cot_prompt
    from .evaluator import PromptEvaluator
except ImportError:
    from templates import PromptTemplate, FewShotPromptTemplate, create_cot_prompt
    from evaluator import PromptEvaluator

def run_prompt_benchmark() -> Dict[str, Any]:
    examples = [
        {"text": "The battery lasts only 2 hours and the screen flickers.", "sentiment": "Negative"},
        {"text": "Setup was intuitive, customer service answered immediately!", "sentiment": "Positive"}
    ]
    few_shot = FewShotPromptTemplate(
        prefix="Classify review sentiment.",
        example_template="Review: {text}\nSentiment: {sentiment}",
        examples=examples,
        suffix="Review: {text}\nSentiment:",
        input_variables=["text"]
    )
    test_case = {
        "text": "The camera quality exceeded expectations.",
        "ground_truth": "Positive",
        "simulated_output": "Positive"
    }
    eval_few = PromptEvaluator.evaluate_response(
        test_case["simulated_output"], test_case["ground_truth"]
    )
    return {
        "test_input": test_case["text"],
        "few_shot_eval": eval_few,
        "cot_prompt": create_cot_prompt("Classify intent", "Book a flight to NYC")
    }

if __name__ == "__main__":
    print(json.dumps(run_prompt_benchmark(), indent=2))
