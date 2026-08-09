# Technical Questions — Day 12

## JWT Authentication

**Q: What is JWT?**
> JSON Web Token — a compact, self-contained token for securely transmitting information. Contains header, payload, and signature. Used for stateless authentication.

**Q: What is the difference between authentication and authorization?**
> Authentication = verifying who you are (login). Authorization = verifying what you can do (permissions).

**Q: Why hash passwords with bcrypt?**
> Bcrypt is a slow hashing algorithm designed for passwords. It adds a salt automatically and is resistant to brute-force attacks. Never store plain text passwords.

**Q: What is OAuth2PasswordBearer in FastAPI?**
> A FastAPI security utility that extracts the JWT token from the `Authorization: Bearer <token>` header and passes it to the dependency.

**Q: What does `Depends(get_current_user)` do?**
> FastAPI dependency injection — automatically calls `get_current_user()` before the route handler, validates the JWT, and injects the user object into the route.

---

## Linked List DSA

**Q: How do you reverse a linked list iteratively?**
> Use three pointers: `prev=None`, `curr=head`. At each step: save `next`, point `curr.next` to `prev`, move `prev` to `curr`, move `curr` to saved `next`.

**Q: How do you find the middle of a linked list?**
> Fast & Slow pointer technique. `slow` moves 1 step, `fast` moves 2 steps. When `fast` reaches end, `slow` is at middle. O(n) time, O(1) space.

**Q: What is the time complexity of linked list operations?**
> Access: O(n), Search: O(n), Insert at head: O(1), Insert at tail: O(n), Delete: O(n).
