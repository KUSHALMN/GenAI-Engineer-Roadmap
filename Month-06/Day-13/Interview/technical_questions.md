# Technical Interview Preparation — Real-Time Voice Sessions & BST Patterns

## 1. Barge-In (Interruption Handling) in Conversational Voice Systems
**Question:** How does a full-duplex conversational voice agent detect user barge-in and cancel in-flight audio playback without introducing echo cancellation artifacts?

**Answer:**
- **Full-Duplex Audio Flow:**
  - The client streams microphone audio frames upstream via WebSockets while simultaneously playing downstream TTS audio frames received from the server.
- **Barge-In Detection:**
  - **Acoustic Echo Cancellation (AEC):** The client subtracts the currently playing loudspeaker signal from the incoming microphone signal.
  - If the residual energy exceeds the VAD speech threshold while the agent is speaking, a **Barge-In Event** is fired immediately.
- **Cancellation Lifecycle:**
  1. The client immediately stops audio buffer playback.
  2. The client transmits a cancel control packet to the server.
  3. The server aborts any pending LLM token generation and purges downstream TTS synthesis queues.
  4. Drops conversational latency to human conversational cadence ($pprox 250$ ms).

---

## 2. BST Deletion: Inorder Successor Invariant
**Question:** When deleting a node with two children in a Binary Search Tree (LC 450), why do we replace it with its inorder successor, and how do we ensure the tree structure remains valid?

**Answer:**
- In a BST, the **inorder successor** is the smallest node in the right subtree (`findMin(node.right)`).
- Because it is the smallest in the right subtree:
  - It is strictly greater than all elements in the left subtree.
  - It is strictly smaller than (or equal to) all other elements in the right subtree.
- Therefore, replacing `node.val` with `successor.val` preserves the BST invariant across the entire tree.
- The successor node itself has at most one child (a right child), making its subsequent deletion trivial.
