# Coding Questions — Day 12

## Q1: Reverse Linked List (Java)
```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

## Q2: Middle of Linked List (Java)
```java
public ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```

## Q3: Hash Password (Python)
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

## Q4: Create JWT Token (Python)
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, secret: str, expire_minutes: int = 30) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expire_minutes)
    return jwt.encode(to_encode, secret, algorithm="HS256")
```

## Q5: Protected Route with FastAPI (Python)
```python
from fastapi import Depends
from auth import get_current_user

@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['username']}"}
```

## Q6: Reverse Linked List Recursive (Python)
```python
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```
