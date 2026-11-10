# 🎯 Technical Interview Questions — Day 01: Production API Architecture & SOLID

### 1. Explain the 3-Tier Layered Architecture (Routers, Services, Repositories). Why is direct database access from HTTP route handlers an anti-pattern?
**Answer:**
Direct DB calls inside route handlers tightly couple transport concerns (HTTP headers, query parsing, status codes) with data persistence. Layered architecture divides responsibilities:
- **Routers/Controllers:** Handle HTTP serialization, path parameters, dependency injection, and status code translation.
- **Service Layer:** Houses domain logic, business invariants, cross-model transactions, and authorization checks.
- **Repositories:** Abstract DB queries, indexing, and ORM schemas. This enables mocking the data tier during unit tests and swapping the underlying database without modifying business logic.

### 2. How does the Dependency Inversion Principle (DIP) enhance unit testing in large-scale systems?
**Answer:**
High-level policy modules should not import low-level I/O details; both should depend on abstractions (interfaces). In unit tests, real dependencies (e.g., Stripe API, PostgreSQL, Redis) can be replaced with lightweight in-memory fakes or mocks without needing Docker containers or active network connections.
