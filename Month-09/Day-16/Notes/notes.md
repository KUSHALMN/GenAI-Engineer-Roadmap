# 📝 Notes — Day 16: Collectives & Sliding Window Maximum

- **Bisection Bandwidth:** The minimum network capacity across any cut that splits the network into two equal halves; critical for All-to-All MoE scaling.
- **Deque Index vs Value Storage:** Always store array *indices* in the deque rather than values so expiration checks (`deque.peekFirst() < i - k + 1`) can be evaluated in $O(1)$ time.
