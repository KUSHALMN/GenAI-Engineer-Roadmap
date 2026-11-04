# Notes: Citation Attribution & Grounding Verification

## 1. Why Citation Validation is Critical
In enterprise RAG, users and auditors require verifiable answers. LLMs commonly suffer from **Citation Hallucination**:
1. Inventing fictitious document citations (`[Doc 99]` when only 3 docs were provided).
2. Attaching valid citation brackets to claims that are completely unsupported by the cited source (citation spoofing).

## 2. Automated Citation Audit Workflow
1. **Extraction**: Parse all citation markers (`[Doc X]`, `[Ref Y]`) using regex.
2. **Existence Verification**: Check if $X \in \{1, \dots, K\}$ where $K$ is the number of provided context passages.
3. **Grounding Alignment**: Measure token overlap, entity alignment, or NLI (Natural Language Inference) entailment between the cited statement and the source chunk.
4. **Rejection Policy**: If ungrounded statements or hallucinated citations exceed a threshold, reject the response or flag with a warning badge.
