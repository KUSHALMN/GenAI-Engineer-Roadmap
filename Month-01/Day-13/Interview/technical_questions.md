# Technical Questions — Day 13

## Stack DSA

**Q: How does Largest Rectangle in Histogram work?**
Use a monotonic increasing stack of indices. When current height < stack top height, pop and calculate area using the popped height and width = i - stack.peek() - 1.

**Q: What's the difference between monotonic increasing vs decreasing stack?**
- Increasing: pop when current < top → used for "largest area", "next smaller"
- Decreasing: pop when current > top → used for "daily temperatures", "next greater"

**Q: Why append 0 at the end in Largest Rectangle?**
Forces all remaining elements in the stack to be popped and processed.

## RAG + Docker

**Q: Why Dockerize the RAG chatbot?**
Ensures consistent environment across machines — same Python version, same dependencies, no "works on my machine" issues.

**Q: What is the app/ package structure for?**
Separates concerns — each module has one job. Makes testing, debugging, and scaling easier.

**Q: How do you run tests in this project?**
```bash
pytest tests/
```
pytest auto-discovers test files prefixed with `test_`.

**Q: What does .env.example do?**
Documents required environment variables without exposing actual secrets. Developers copy it to `.env` and fill in real values.
