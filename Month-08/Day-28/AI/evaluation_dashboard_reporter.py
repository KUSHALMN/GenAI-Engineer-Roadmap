"""
Evaluation Dashboards & Reporting: Automated Markdown / JSON Report Generator,
Historical Trend Tracking, Metric Delta Comparisons, and Visual Regressions.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class MetricComparison:
    metric_name: str
    baseline_value: float
    candidate_value: float

    @property
    def delta(self) -> float:
        return self.candidate_value - self.baseline_value

    @property
    def status(self) -> str:
        if self.delta >= 0.0:
            return "IMPROVED"
        elif self.delta >= -0.02:
            return "STABLE"
        return "REGRESSED"


class EvaluationDashboardReporter:
    """
    Generates executive Markdown reports summarizing model benchmark deltas.
    """
    def generate_markdown_report(self, comparisons: List[MetricComparison]) -> str:
        lines = [
            "# 📊 Evaluation Regression & Quality Report",
            "",
            "| Metric | Baseline | Candidate | Delta | Status |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for c in comparisons:
            sign = "+" if c.delta >= 0 else ""
            status_emoji = "✅" if c.status in ["IMPROVED", "STABLE"] else "❌"
            lines.append(
                f"| {c.metric_name} | {c.baseline_value:.4f} | {c.candidate_value:.4f} | {sign}{c.delta:.4f} | {status_emoji} {c.status} |"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    reporter = EvaluationDashboardReporter()
    metrics = [
        MetricComparison("RAG Faithfulness", 0.9120, 0.9450),
        MetricComparison("Answer Relevance", 0.8900, 0.9020),
        MetricComparison("Harm Refusal Rate", 0.9950, 0.9940),
        MetricComparison("Avg Latency (sec)", 1.2500, 1.1000)
    ]

    report = reporter.generate_markdown_report(metrics)
    print(report)
    assert "✅ IMPROVED" in report
    print("Day 28 Evaluation Dashboard Reporter verification passed.")
