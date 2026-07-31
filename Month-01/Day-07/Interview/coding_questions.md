# Coding Interview Questions — Day 7

## Q1: Reverse a String in Python
```python
def reverse_string(s):
    return s[::-1]

print(reverse_string("hello"))  # "olleh"
```

## Q2: Check if a String is a Palindrome
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False
```

## Q3: Find the Most Frequent Element
```python
from collections import Counter

def most_frequent(nums):
    return Counter(nums).most_common(1)[0][0]

print(most_frequent([1, 2, 2, 3, 3, 3]))  # 3
```

## Q4: Two Sum (Java)
```java
public int[] twoSum(int[] nums, int target) {
    HashMap<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement))
            return new int[]{map.get(complement), i};
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

## Q5: FizzBuzz
```python
for i in range(1, 101):
    if i % 15 == 0: print("FizzBuzz")
    elif i % 3 == 0: print("Fizz")
    elif i % 5 == 0: print("Buzz")
    else: print(i)
```

## Q6: Flatten a Nested List
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], 5]))  # [1, 2, 3, 4, 5]
```

## Q7: Count Words in a String
```python
from collections import Counter
import re

def word_count(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return dict(Counter(words))

print(word_count("the cat sat on the mat"))
```
