# 🎯 Technical Interview Questions — Day 02: Authentication & Creational Patterns

### 1. What are the security risks of storing JWTs in browser LocalStorage vs. HttpOnly Secure Cookies?
**Answer:**
- **LocalStorage:** Accessible to any JavaScript executing in the page. If the web app has any Cross-Site Scripting (XSS) vulnerability, an attacker can steal the JWT instantly.
- **HttpOnly Secure Cookies:** Cannot be accessed via JavaScript (`document.cookie`), shielding the token from XSS exfiltration. To prevent Cross-Site Request Forgery (CSRF), cookies must be configured with `SameSite=Strict` or `SameSite=Lax` and paired with anti-CSRF tokens.

### 2. Why is the `volatile` keyword mandatory in Java's Double-Checked Locking Singleton?
**Answer:**
Without `volatile`, the JVM compiler and CPU out-of-order execution may reorder the memory allocation and constructor initialization steps. A second thread checking `instance == null` could see a non-null reference before the constructor finishes execution, leading to reading a partially initialized object.
