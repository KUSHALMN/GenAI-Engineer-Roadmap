from typing import List, Dict, Any, Optional
import re

class PromptTemplate:
    """
    Production-grade Prompt Template supporting variable interpolation,
    few-shot dynamic formatting, and Chain-of-Thought (CoT) system prompt generation.
    """
    def __init__(self, template: str, input_variables: List[str]):
        self.template = template
        self.input_variables = input_variables

    def format(self, **kwargs) -> str:
        for var in self.input_variables:
            if var not in kwargs:
                raise ValueError(f"Missing required prompt variable: '{var}'")
        return self.template.format(**kwargs)

class FewShotPromptTemplate:
    """
    Dynamically injects calibrated few-shot input/output demonstrations
    into the system prompt to guide LLM reasoning.
    """
    def __init__(
        self,
        prefix: str,
        example_template: str,
        examples: List[Dict[str, str]],
        suffix: str,
        input_variables: List[str]
    ):
        self.prefix = prefix
        self.example_template = example_template
        self.examples = examples
        self.suffix = suffix
        self.input_variables = input_variables

    def format(self, **kwargs) -> str:
        formatted_examples = []
        for ex in self.examples:
            formatted_examples.append(self.example_template.format(**ex))
        
        examples_str = "\n\n".join(formatted_examples)
        formatted_suffix = self.suffix.format(**kwargs)
        
        return f"{self.prefix}\n\n{examples_str}\n\n{formatted_suffix}"

def create_cot_prompt(task_instruction: str, user_input: str) -> str:
    """
    Generates a calibrated Chain-of-Thought prompt enforcing step-by-step reasoning
    before reaching a final conclusion.
    """
    return (
        f"System: You are an expert AI reasoning assistant. Solve the user's task step-by-step.\n"
        f"Format your response as follows:\n"
        f"THOUGHT PROCESS:\n"
        f"[Break down the problem, evaluate constraints, verify edge cases]\n"
        f"FINAL ANSWER:\n"
        f"[Concise, definitive final output]\n\n"
        f"Task: {task_instruction}\n"
        f"Input: {user_input}\n"
    )
