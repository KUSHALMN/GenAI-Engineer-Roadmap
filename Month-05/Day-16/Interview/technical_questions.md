# Day 16: Technical Interview Preparation — Model Artifacts & Token Bucket

### Q1: Why should raw trained model weights NEVER be committed directly to a Git repository?
**Answer:**
Git is a delta-compression VCS optimized for text. Binary weights (multi-gigabyte `.bin` or `.safetensors` files) bloat repository size permanently, cause clone timeouts, and defeat CI/CD pipelines. Model weights should be uploaded to artifact registries (Hugging Face Hub, AWS S3, OCI registry), tracking only cryptographic hashes and metadata in Git.

### Q2: Compare Token Bucket vs Leaky Bucket algorithms for API rate limiting.
**Answer:**
- **Token Bucket:** Tokens accumulate up to capacity. Allows bursts of requests as long as tokens are available, then caps at refill rate.
- **Leaky Bucket:** Requests enter a queue and are processed at a strictly constant rate. Smooths out traffic, but drops or buffers bursts rigidly.
