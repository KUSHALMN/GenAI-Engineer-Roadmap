# 🎯 Technical Interview Questions — Day 27: Supply Chain & O(1) Data Structures

### 1. How do you defend against dependency confusion and supply chain attacks in Python/pip?
**Answer:**
1. Pin all direct and transitive dependencies with cryptographic hashes using `pip-tools` or `uv.lock`.
2. Configure private enterprise package repositories (e.g., Artifactory, AWS CodeArtifact) with `--extra-index-url` protections to prevent public PyPI package squatting.
3. Integrate automated SBOM generation and container scanning (Trivy, Snyk) into CI.

### 2. Why is swapping with the last element essential for $O(1)$ removal in an ArrayList?
**Answer:**
Removing an arbitrary element from an ArrayList requires shifting all subsequent elements left, taking $O(N)$ time. By swapping the target element with the element at the tail of the array, updating the map index, and calling `nums.remove(nums.size() - 1)`, removal operates in guaranteed $O(1)$ time.
