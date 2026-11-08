"""
Chart QA & Visual Data Fact Extraction Engine.
Identifies chart types, extracts axes and series data, and strictly
separates directly observed facts from inferred explanations.
"""

from dataclasses import dataclass, field
from enum import Enum
import json
import time
from typing import Any, Dict, List, Optional, Tuple


class ChartType(Enum):
    BAR = "bar_chart"
    LINE = "line_chart"
    SCATTER = "scatter_plot"
    PIE = "pie_chart"


@dataclass
class ChartAxis:
    name: str
    unit: str
    min_val: float
    max_val: float


@dataclass
class DataSeriesPoint:
    label: str
    x_val: Any
    y_val: float


@dataclass
class ChartAnalysisResult:
    chart_type: ChartType
    title: str
    axes: Dict[str, ChartAxis]
    data_points: List[DataSeriesPoint]
    observed_facts: List[str]
    inferred_explanations: List[str]


class ChartQAExtractor:
    """Parses chart visual elements into structured data with fact verification."""

    def analyze_chart(self, image_path: str) -> ChartAnalysisResult:
        # Simulated high-fidelity chart parsing
        axes = {
            "x_axis": ChartAxis(name="Quarter", unit="Quarter Year", min_val=1.0, max_val=4.0),
            "y_axis": ChartAxis(name="Throughput", unit="req/sec", min_val=0.0, max_val=5000.0)
        }
        points = [
            DataSeriesPoint(label="vLLM PagedAttention", x_val="Q1", y_val=2100.0),
            DataSeriesPoint(label="vLLM PagedAttention", x_val="Q2", y_val=3400.0),
            DataSeriesPoint(label="vLLM PagedAttention", x_val="Q3", y_val=4200.0),
            DataSeriesPoint(label="vLLM PagedAttention", x_val="Q4", y_val=4850.0),
            DataSeriesPoint(label="HuggingFace Baseline", x_val="Q1", y_val=620.0),
            DataSeriesPoint(label="HuggingFace Baseline", x_val="Q2", y_val=710.0),
            DataSeriesPoint(label="HuggingFace Baseline", x_val="Q3", y_val=750.0),
            DataSeriesPoint(label="HuggingFace Baseline", x_val="Q4", y_val=810.0)
        ]
        
        # Grounded facts directly measurable from visual pixels
        facts = [
            "vLLM throughput increased monotonically from 2,100 req/sec in Q1 to 4,850 req/sec in Q4.",
            "HuggingFace baseline throughput grew from 620 req/sec to 810 req/sec over the same interval.",
            "In Q4, vLLM throughput is approximately 5.98x higher than the HuggingFace baseline."
        ]
        
        # Inferred explanations (clearly tagged as speculative hypothesis)
        inferences = [
            "The performance gap is likely attributable to dynamic continuous batching and virtual paged memory management.",
            "The leveling off between Q3 and Q4 may suggest GPU compute saturation or memory bandwidth bottlenecks."
        ]

        return ChartAnalysisResult(
            chart_type=ChartType.LINE,
            title="Model Serving Engine Throughput Comparison (2026)",
            axes=axes,
            data_points=points,
            observed_facts=facts,
            inferred_explanations=inferences
        )


if __name__ == "__main__":
    extractor = ChartQAExtractor()
    res = extractor.analyze_chart("benchmark_chart.png")

    print(f"=== {res.title} ===")
    print(f"Chart Type: {res.chart_type.value}")
    print("\nObserved Visual Facts:")
    for f in res.observed_facts:
        print(f"  [FACT] {f}")
    print("\nInferred Explanations:")
    for inf in res.inferred_explanations:
        print(f"  [INFERENCE] {inf}")
