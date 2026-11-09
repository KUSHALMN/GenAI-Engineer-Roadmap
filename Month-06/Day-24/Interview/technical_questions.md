# Technical Interview Preparation — Cost Profiling & String DP
1. Multimodal Cost Trade-Offs: Image tokens dominate prompt budgets ($1,105$ tokens per image vs $50$ tokens per query). Cropping to bounding boxes cuts cost by $70\%$.
2. Edit Distance Recurrence: Three choices on mismatch: Insert ($dp[i][j-1]$), Delete ($dp[i-1][j]$), Replace ($dp[i-1][j-1]$).
