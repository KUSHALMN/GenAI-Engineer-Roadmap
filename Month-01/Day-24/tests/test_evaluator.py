import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from templates import PromptTemplate, FewShotPromptTemplate, create_cot_prompt
from evaluator import PromptEvaluator
from app import run_prompt_benchmark

def test_prompt_template_formatting():
    tmpl = PromptTemplate("Translate '{text}' to {lang}.", ["text", "lang"])
    res = tmpl.format(text="Good morning", lang="French")
    assert res == "Translate 'Good morning' to French."

    with pytest.raises(ValueError):
        tmpl.format(text="Only text provided")

def test_few_shot_formatting():
    examples = [{"q": "2+2", "a": "4"}]
    few_shot = FewShotPromptTemplate(
        prefix="Math assistant",
        example_template="Q: {q}\nA: {a}",
        examples=examples,
        suffix="Q: {q}\nA:",
        input_variables=["q"]
    )
    formatted = few_shot.format(q="3+5")
    assert "Math assistant" in formatted
    assert "Q: 2+2\nA: 4" in formatted

def test_metrics():
    exact = PromptEvaluator.exact_match("Positive", "Positive")
    assert exact == 1.0

    bleu = PromptEvaluator.calculate_bleu("the cat on the mat", "the cat is on the mat")
    assert bleu > 0.5

    rouge = PromptEvaluator.calculate_rouge_l("fast automated testing", "automated fast testing")
    assert rouge > 0.5

    cos = PromptEvaluator.cosine_similarity("apple orange banana", "banana apple orange")
    assert cos == 1.0

def test_benchmark_runner():
    bench = run_prompt_benchmark()
    assert "few_shot_eval" in bench
    assert bench["few_shot_eval"]["exact_match"] == 1.0
