import json
import random
from pathlib import Path

RAW_SAMPLES = [
    {
        "instruction": "Explain what a RAG pipeline is.",
        "input": "",
        "output": "RAG (Retrieval-Augmented Generation) combines a retriever that fetches relevant documents from a vector store with a generator LLM that produces answers grounded in those documents, reducing hallucinations."
    },
    {
        "instruction": "What is the difference between fine-tuning and prompt engineering?",
        "input": "",
        "output": "Prompt engineering shapes model behavior at inference time without changing weights. Fine-tuning updates model weights on domain-specific data, yielding deeper specialization at the cost of compute and data preparation."
    },
    {
        "instruction": "Summarize the following text.",
        "input": "LangChain is a framework for building applications powered by language models. It provides abstractions for chains, agents, memory, and tool use.",
        "output": "LangChain is a framework that simplifies building LLM-powered apps through abstractions like chains, agents, memory, and tools."
    },
    {
        "instruction": "What is LoRA in the context of LLM fine-tuning?",
        "input": "",
        "output": "LoRA (Low-Rank Adaptation) injects trainable low-rank matrices into transformer layers, allowing efficient fine-tuning with far fewer parameters than full fine-tuning while preserving base model quality."
    },
    {
        "instruction": "How does vector similarity search work?",
        "input": "",
        "output": "Text is embedded into high-dimensional vectors. At query time, the query is embedded and cosine similarity (or dot product) is computed against stored vectors. The top-k nearest vectors are returned as relevant results."
    },
    {
        "instruction": "What is the purpose of a system prompt?",
        "input": "",
        "output": "A system prompt sets the persona, constraints, and behavioral guidelines for the LLM before the user conversation begins, steering tone, format, and safety boundaries."
    },
    {
        "instruction": "Explain temperature in LLM inference.",
        "input": "",
        "output": "Temperature scales the logits before softmax sampling. Low temperature (near 0) makes output deterministic and focused; high temperature increases randomness and creativity."
    },
    {
        "instruction": "What is chunking in document ingestion?",
        "input": "",
        "output": "Chunking splits large documents into smaller overlapping or non-overlapping segments so each chunk fits within the LLM context window and can be individually embedded and retrieved."
    },
]


def format_prompt(sample: dict) -> str:
    if sample["input"]:
        return (
            f"### Instruction:\n{sample['instruction']}\n\n"
            f"### Input:\n{sample['input']}\n\n"
            f"### Response:\n{sample['output']}"
        )
    return (
        f"### Instruction:\n{sample['instruction']}\n\n"
        f"### Response:\n{sample['output']}"
    )


def prepare(
    output_path: str = "fine_tuning/dataset.jsonl",
    val_path: str = "evaluation/test_samples.jsonl",
    val_ratio: float = 0.2,
):
    random.shuffle(RAW_SAMPLES)
    split = int(len(RAW_SAMPLES) * (1 - val_ratio))
    train, val = RAW_SAMPLES[:split], RAW_SAMPLES[split:]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(val_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for s in train:
            f.write(json.dumps({"text": format_prompt(s)}) + "\n")

    with open(val_path, "w") as f:
        for s in val:
            f.write(json.dumps({"text": format_prompt(s), "expected": s["output"]}) + "\n")

    print(f"Train: {len(train)} samples -> {output_path}")
    print(f"Val:   {len(val)} samples -> {val_path}")


if __name__ == "__main__":
    prepare()
