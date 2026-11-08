# Technical Interview Preparation — Table Extraction & Binary Search

## 1. Why LLMs Hallucinate Table Arithmetic & How to Guard Against It
**Question:** Why do state-of-the-art LLMs frequently make calculation errors when reading financial tables, and what is the production-grade architectural pattern to resolve this?

**Answer:**
- **Why LLMs Fail:**
  - LLMs are autoregressive token predictors, not algebraic solvers. They lack state registers for carry bits and multi-digit column alignment.
  - Multi-token numbers (e.g., `14,250.00`) are split into sub-tokens (`14`, `,`, `250`, `.00`), obscuring numerical magnitude and positional math.
- **Production Guardrail Architecture:**
  1. *Structured Matrix Parser:* Extract table cells into a deterministic 2D matrix rather than plain text.
  2. *Deterministic Verification Layer:* Compute row/column sums programmatically in Python/Java.
  3. *Prompt Injection Guard:* Never allow the LLM to generate summary totals directly from visual inspection. Instead, pass the verified programmatic totals as grounded context variables into the prompt template.

---

## 2. Binary Search Invariants: Boundary Selection
**Question:** Compare `while (low <= high)` with `while (low < high)`. How do you decide which loop condition and midpoint calculation to use?

**Answer:**
- **Template 1 (`while (low <= high)`):**
  - Search space includes both bounds.
  - Used when seeking a specific target value. When `nums[mid] == target`, either return immediately or adjust `high = mid - 1` / `low = mid + 1` for bounds.
  - Terminates when `low > high`.
- **Template 2 (`while (low < high)`):**
  - Search space shrinks to a single candidate element.
  - Used for optimization/slope problems like **Find Peak Element** or **Find Minimum in Rotated Sorted Array**.
  - `mid` is compared with `mid + 1`. If slope is decreasing, `high = mid`; if increasing, `low = mid + 1`.
  - Loop terminates with `low == high`, avoiding out-of-bounds access.
