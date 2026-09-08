# 💻 Day 25 Coding Interview Questions: Trapping Rain Water

### Problem: Trapping Rain Water (LeetCode 42 - Hard / High-Frequency)
**Key Insight (Two Pointers)**:
Water trapped at any index $i$ depends on $\min(\maxLeft, \maxRight) - \text{height}[i]$.
By scanning inward from both ends with `left` and `right`:
- If `height[left] <= height[right]`, the bottleneck for `left` is guaranteed to be `maxLeft`, because whatever `maxRight` is, it is at least `height[right] >= height[left]`. Hence we can process `left` safely in $O(1)$ space.
- Vice-versa if `height[right] < height[left]`.

```java
while (left < right) {
    if (height[left] <= height[right]) {
        if (height[left] >= maxLeft) maxLeft = height[left];
        else totalWater += maxLeft - height[left];
        left++;
    } else {
        if (height[right] >= maxRight) maxRight = height[right];
        else totalWater += maxRight - height[right];
        right--;
    }
}
```

**Alternative: Monotonic Stack**:
Stores indices of decreasing heights. When a taller bar is seen, it pops the bottom of the basin, calculates bounded height and distance, and accumulates volume horizontally in layers.
