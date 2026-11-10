# 📝 Notes — Day 01: Production API Architecture & SOLID Principles

## 1. RESTful Design Best Practices
- **Standardized Response Envelope:** Every API endpoint returns a predictable JSON structure (`success`, `data`, `error`, `meta`).
- **Pagination Contracts:** Use cursor-based or limit-offset pagination with total count and current page metadata.
- **HTTP Status Code Precision:** `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity`, `429 Too Many Requests`.

## 2. SOLID OOP Design Summary
- **Single Responsibility (SRP):** A class should have only one reason to change.
- **Open/Closed (OCP):** Software entities should be open for extension, but closed for modification.
- **Liskov Substitution (LSP):** Subtypes must be substitutable for their base types without altering program correctness.
- **Interface Segregation (ISP):** Clients should not be forced to depend upon interfaces that they do not use.
- **Dependency Inversion (DIP):** Depend on abstractions, not concretions.
