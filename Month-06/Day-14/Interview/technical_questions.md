# Technical Interview Preparation — VAD Turn-Taking & Tree Construction

## 1. Conversational Voice Endpointing & False-Termination Traps
**Question:** Why does naive silence thresholding cause voice assistants to interrupt human speakers prematurely, and what algorithmic strategies prevent this?

**Answer:**
- **The Problem:** Natural human speech contains mid-sentence cognitive pauses ($200 - 500$ ms) where the speaker formulates thoughts while retaining the floor.
- **Premature Endpointing Trap:** A rigid $400$ ms silence threshold cuts off the speaker mid-sentence, causing severe user frustration.
- **Production Solutions:**
  1. *Adaptive Pause Threshold:* Scale silence threshold based on syntactic completion: if the partial transcript ends with an incomplete clause (e.g. "I would like to order a..."), increase the threshold to $1,000$ ms; if it ends with a complete grammatical question, trigger endpoint at $600$ ms.
  2. *Dual-Threshold Hysteresis:* Require speech energy to cross a high threshold to start turn ($120$ ms sustain), but tolerate lower energy before declaring silence.

---

## 2. Tree Construction: Inorder Index Mapping
**Question:** Why is a HashMap essential for constructing a binary tree from Preorder and Inorder traversals in $O(N)$ time instead of $O(N^2)$?

**Answer:**
- In preorder traversal, the root is always `preorder[preStart]`.
- We must find the position of `rootVal` in `inorder` to determine the size of the left subtree ($numsLeft = inRootIdx - inStart$).
- Linear search for `rootVal` in `inorder` takes $O(N)$ per node, yielding $T(N) = 2T(N/2) + O(N) = O(N^2)$ worst-case for skewed trees.
- Precomputing `Map<Integer, Integer> inMap` achieves $O(1)$ lookup for `inRootIdx`, reducing overall complexity to strictly $O(N)$ time and $O(N)$ auxiliary space.
