/**
 * Binary Tree Construction from Traversal Arrays
 * Solves core FAANG interview problems:
 * 1. Construct Binary Tree from Preorder and Inorder Traversal (LC 105)
 * 2. Construct Binary Tree from Postorder and Inorder Traversal (LC 106)
 * Achieves O(N) time complexity using HashMap lookup for inorder roots.
 */

import java.util.HashMap;
import java.util.Map;

public class ConstructTreeTraversals {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
    }

    // 1. LC 105: Construct from Preorder and Inorder
    public static TreeNode buildTreePreIn(int[] preorder, int[] inorder) {
        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }
        return buildPreIn(preorder, 0, preorder.length - 1, 0, inorder.length - 1, inMap);
    }

    private static TreeNode buildPreIn(int[] pre, int preStart, int preEnd,
                                       int inStart, int inEnd, Map<Integer, Integer> inMap) {
        if (preStart > preEnd || inStart > inEnd) return null;

        int rootVal = pre[preStart];
        TreeNode root = new TreeNode(rootVal);
        int inRootIdx = inMap.get(rootVal);
        int numsLeft = inRootIdx - inStart;

        root.left = buildPreIn(pre, preStart + 1, preStart + numsLeft, inStart, inRootIdx - 1, inMap);
        root.right = buildPreIn(pre, preStart + numsLeft + 1, preEnd, inRootIdx + 1, inEnd, inMap);

        return root;
    }

    // 2. LC 106: Construct from Postorder and Inorder
    public static TreeNode buildTreePostIn(int[] inorder, int[] postorder) {
        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }
        return buildPostIn(postorder, 0, postorder.length - 1, 0, inorder.length - 1, inMap);
    }

    private static TreeNode buildPostIn(int[] post, int postStart, int postEnd,
                                        int inStart, int inEnd, Map<Integer, Integer> inMap) {
        if (postStart > postEnd || inStart > inEnd) return null;

        int rootVal = post[postEnd];
        TreeNode root = new TreeNode(rootVal);
        int inRootIdx = inMap.get(rootVal);
        int numsLeft = inRootIdx - inStart;

        root.left = buildPostIn(post, postStart, postStart + numsLeft - 1, inStart, inRootIdx - 1, inMap);
        root.right = buildPostIn(post, postStart + numsLeft, postEnd - 1, inRootIdx + 1, inEnd, inMap);

        return root;
    }

    public static void main(String[] args) {
        System.out.println("=== Binary Tree Construction Verification ===");

        int[] preorder = {3, 9, 20, 15, 7};
        int[] inorder = {9, 3, 15, 20, 7};
        TreeNode rootPreIn = buildTreePreIn(preorder, inorder);
        assert rootPreIn.val == 3 : "Root should be 3";
        assert rootPreIn.left.val == 9 : "Left should be 9";
        assert rootPreIn.right.val == 20 : "Right should be 20";
        System.out.println("LC 105 (Pre + In): Tree built successfully!");

        int[] postorder = {9, 15, 7, 20, 3};
        TreeNode rootPostIn = buildTreePostIn(inorder, postorder);
        assert rootPostIn.val == 3 && rootPostIn.right.left.val == 15 : "LC 106 failed";
        System.out.println("LC 106 (Post + In): Tree built successfully!");

        System.out.println("All Tree Construction tests passed!");
    }
}
