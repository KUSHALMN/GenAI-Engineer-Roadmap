# 🎯 Technical Interview Questions — Day 03: Human Evaluation & Two Pointers

### 1. Why is Pairwise Blind Comparison (Side-by-Side Elo Rating) preferred over absolute Likert scales?
**Answer:**
Absolute Likert scales (e.g., rate 1 to 5) suffer from severe annotator calibration variance (one annotator's "4" is another's "2"). Side-by-side blind comparisons present Model A vs. Model B in randomized order, asking the annotator to simply select the better response or declare a tie. This transforms subjective absolute scoring into rigorous Elo ratings, completely neutralizing individual annotator grading curves.

### 2. How do you prevent duplicate triplets in $O(N^2)$ 3Sum?
**Answer:**
First sort the array. In the outer loop, skip duplicate anchor elements if `nums[i] == nums[i-1]`. In the inner two-pointer loop, after finding a valid triplet summing to zero, advance `left` past identical elements (`nums[left] == nums[left+1]`) and decrement `right` past identical elements (`nums[right] == nums[right-1]`).
