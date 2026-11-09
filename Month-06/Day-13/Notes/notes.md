# Engineering Notes — Day 13: Voice Streaming Sessions & BST Deletion Invariants

## 1. WebSocket Streaming State Machine
- States: `CONNECTED` $\rightarrow$ `LISTENING` $\rightarrow$ `USER_SPEAKING` $\rightarrow$ `ENDPOINTING` $\rightarrow$ `AGENT_RESPONDING`.
- Barge-in transition: `AGENT_RESPONDING` $\xrightarrow{\text{VAD on microphone}}$ `INTERRUPTED` $\rightarrow$ `LISTENING`.

## 2. BST Node Deletion Cases
1. Leaf node: Return `null`.
2. One child: Return the non-null child.
3. Two children: Copy inorder successor value and recursively delete successor from right subtree.
