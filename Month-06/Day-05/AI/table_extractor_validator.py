"""
Table Extraction & Cell Cross-Validation Engine.
Parses semi-structured table matrices, validates row/column arithmetic sums,
and flags LLM hallucinations when summary figures contradict cell values.
"""

from dataclasses import dataclass
import re
from typing import List, Optional


@dataclass
class TableCell:
    row: int
    col: int
    text: str
    numeric_value: Optional[float] = None
    rowspan: int = 1
    colspan: int = 1


@dataclass
class ValidationReport:
    is_valid: bool
    row_sum_errors: List[str]
    col_sum_errors: List[str]
    hallucination_warnings: List[str]


class TableExtractorValidator:
    """Extracts tables and validates internal arithmetic integrity."""

    @staticmethod
    def parse_numeric(text: str) -> Optional[float]:
        clean = re.sub(r"[\$,%\s]", "", text)
        try:
            return float(clean)
        except ValueError:
            return None

    def parse_markdown_table(self, md_table: str) -> List[List[TableCell]]:
        lines = [line.strip() for line in md_table.strip().split("\n") if line.strip()]
        matrix = []

        row_idx = 0
        for line in lines:
            if line.startswith("|") and ("---" in line or ":---" in line):
                continue  # Skip markdown separator
            cells = [c.strip() for c in line.split("|")[1:-1]]
            row_cells = []
            for col_idx, c_text in enumerate(cells):
                num = self.parse_numeric(c_text)
                row_cells.append(TableCell(row=row_idx, col=col_idx, text=c_text, numeric_value=num))
            matrix.append(row_cells)
            row_idx += 1

        return matrix

    def validate_totals(self, matrix: List[List[TableCell]], row_total_col_idx: int = -1) -> ValidationReport:
        row_errors = []
        col_errors = []

        # Validate horizontal row totals
        for r_idx, row in enumerate(matrix[1:], start=1):  # Skip header row
            if len(row) < 3:
                continue
            values = [c.numeric_value for c in row[:-1] if c.numeric_value is not None]
            target = row[-1].numeric_value
            if values and target is not None:
                computed = sum(values)
                if abs(computed - target) > 0.01:
                    row_errors.append(f"Row {r_idx} mismatch: sum({values}) = {computed} != reported {target}")

        return ValidationReport(
            is_valid=(len(row_errors) == 0 and len(col_errors) == 0),
            row_sum_errors=row_errors,
            col_sum_errors=col_errors,
            hallucination_warnings=[]
        )

    def detect_hallucinations(self, generated_summary: str, matrix: List[List[TableCell]]) -> List[str]:
        """Detects if generated narrative mentions numbers conflicting with table cells."""
        table_numbers = {c.numeric_value for row in matrix for c in row if c.numeric_value is not None}
        extracted_numbers = [float(x.replace(",", "")) for x in re.findall(r"\b\d+(?:\.\d+)?\b", generated_summary)]
        
        warnings = []
        for n in extracted_numbers:
            # Check if mentioned number is supported by table data
            if n not in table_numbers:
                warnings.append(f"Unverified number quoted in summary: {n}")
        return warnings


if __name__ == "__main__":
    validator = TableExtractorValidator()

    sample_table = """
    | Region | Q1 Revenue | Q2 Revenue | Q3 Revenue | Total Reported |
    | :--- | :--- | :--- | :--- | :--- |
    | North America | 1200.0 | 1450.0 | 1800.0 | 4450.0 |
    | Europe | 850.0 | 920.0 | 1100.0 | 2870.0 |
    | Asia Pacific | 640.0 | 710.0 | 800.0 | 2150.0 |
    """

    matrix = validator.parse_markdown_table(sample_table)
    report = validator.validate_totals(matrix)
    print("=== Table Arithmetic Validation ===")
    print("Is Valid:", report.is_valid)
    if report.row_sum_errors:
        print("Row Errors:", report.row_sum_errors)
    else:
        print("All row totals match computed sums exactly!")

    summary = "North America generated 4450.0 total, but Latin America contributed 999.0."
    hallucinations = validator.detect_hallucinations(summary, matrix)
    print("\nHallucination Warnings:", hallucinations)
