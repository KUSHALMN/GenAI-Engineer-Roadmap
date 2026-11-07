"""
Day 01: Fine-Tuning Decision Framework
Evaluates task requirements (domain adaptation, style consistency, latency, cost,
data availability) to recommend Prompting vs RAG vs SFT vs Preference Optimization.
"""

from typing import Dict, Any, List

class AdaptationDecisionEngine:
    def evaluate_strategy(self,
                          needs_fresh_knowledge: bool,
                          needs_custom_format_style: bool,
                          has_labeled_dataset: bool,
                          latency_budget_ms: int,
                          privacy_on_prem_required: bool) -> Dict[str, Any]:
        """
        Recommends adaptation method based on constraints.
        """
        score_rag = 0
        score_prompt = 0
        score_sft = 0

        # RAG is primary for fresh, factual, cite-able data
        if needs_fresh_knowledge:
            score_rag += 4
        else:
            score_prompt += 1

        # SFT is essential for hard syntax/style constraints or latency minimization
        if needs_custom_format_style:
            score_sft += 3
        
        if not has_labeled_dataset:
            score_sft -= 4
            score_prompt += 2

        if latency_budget_ms < 150: # Ultra low latency demands smaller fine-tuned models
            score_sft += 2
            score_rag -= 1

        if privacy_on_prem_required:
            score_sft += 2

        # Recommendation logic
        scores = {"Prompting / Few-Shot": score_prompt, "Retrieval-Augmented Generation (RAG)": score_rag, "Supervised Fine-Tuning (SFT)": score_sft}
        sorted_strat = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommended = sorted_strat[0][0]

        return {
            "recommended_strategy": recommended,
            "scores": scores,
            "decision_rule": "RAG for factual recall; SFT for syntax/behavior adherence; Prompting for low-effort baselines."
        }

if __name__ == "__main__":
    engine = AdaptationDecisionEngine()

    # Scenario A: Customer Support bot needing latest policy docs
    resA = engine.evaluate_strategy(needs_fresh_knowledge=True, needs_custom_format_style=False, has_labeled_dataset=False, latency_budget_ms=800, privacy_on_prem_required=False)
    assert resA["recommended_strategy"] == "Retrieval-Augmented Generation (RAG)"

    # Scenario B: Domain SQL generator needing strict JSON output and ultra low latency
    resB = engine.evaluate_strategy(needs_fresh_knowledge=False, needs_custom_format_style=True, has_labeled_dataset=True, latency_budget_ms=100, privacy_on_prem_required=True)
    assert resB["recommended_strategy"] == "Supervised Fine-Tuning (SFT)"

    print("Day 01 AI Decision Framework verified successfully:")
    print(f"Scenario A -> {resA['recommended_strategy']}")
    print(f"Scenario B -> {resB['recommended_strategy']}")
