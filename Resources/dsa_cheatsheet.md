# DSA Cheatsheet — Month 01

## HashMap Patterns (Java)

```java
// Frequency count
HashMap<Integer, Integer> freq = new HashMap<>();
for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);

// Check complement (Two Sum)
HashMap<Integer, Integer> map = new HashMap<>();
int complement = target - nums[i];
if (map.containsKey(complement)) return new int[]{map.get(complement), i};
map.put(nums[i], i);
```

## HashSet Patterns (Java)

```java
// Detect duplicate
HashSet<Integer> set = new HashSet<>();
if (!set.add(num)) return true; // duplicate found

// Intersection
HashSet<Integer> set = new HashSet<>();
for (int n : nums1) set.add(n);
for (int n : nums2) if (set.remove(n)) result.add(n);
```

## Binary Search Template (Java)

```java
int left = 0, right = nums.length - 1;
while (left <= right) {
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
}
return -1;
```

## Sliding Window Template (Java)

```java
int left = 0, max = 0;
HashSet<Character> set = new HashSet<>();
for (int right = 0; right < s.length(); right++) {
    while (set.contains(s.charAt(right))) set.remove(s.charAt(left++));
    set.add(s.charAt(right));
    max = Math.max(max, right - left + 1);
}
```

## Two Pointers Template (Java)

```java
int left = 0, right = arr.length - 1;
while (left < right) {
    // process
    left++;
    right--;
}
```

## Problems Solved

| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Two Sum | HashMap | Easy |
| 217 | Contains Duplicate | HashSet | Easy |
| 242 | Valid Anagram | Frequency Count | Easy |
| 125 | Valid Palindrome | Two Pointers | Easy |
| 383 | Ransom Note | HashMap | Easy |
| 205 | Isomorphic Strings | Two HashMaps | Easy |
| 3 | Longest Substring | Sliding Window | Medium |
| 121 | Best Time to Buy Stock | Greedy | Easy |
| 14 | Longest Common Prefix | String | Easy |
| 704 | Binary Search | Binary Search | Easy |
| 35 | Search Insert Position | Binary Search | Easy |
| 278 | First Bad Version | Binary Search | Easy |
| 153 | Find Min Rotated Array | Binary Search | Medium |
| 33 | Search Rotated Array | Binary Search | Medium |
| 852 | Peak Index Mountain | Binary Search | Medium |
| 349 | Intersection of Arrays | HashSet | Easy |
| 347 | Top K Frequent | HashMap + Heap | Medium |
| 3 | Longest Substring (Day-07) | Sliding Window | Medium |
| 121 | Best Time to Buy Stock (Day-07) | Greedy | Easy |
| 704 | Binary Search (Day-08) | Binary Search | Easy |
| 35 | Search Insert Position (Day-08) | Binary Search | Easy |
| 125 | Valid Palindrome (Day-09) | Two Pointers | Easy |
| 88 | Merge Sorted Array (Day-09) | Two Pointers | Easy |
| 20 | Valid Parentheses (Day-10) | Stack | Easy |
| 155 | Min Stack (Day-10) | Stack | Easy |

**Total: 23 problems solved**
