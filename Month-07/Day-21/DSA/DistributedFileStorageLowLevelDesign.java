package Month07.Day21;

import java.util.HashMap;
import java.util.Map;

/**
 * Low-Level Design (LLD): Distributed Object Storage Node
 * Models Buckets, Blob storage by SHA key, and Metadata registry.
 */
public class DistributedFileStorageLowLevelDesign {

    public record BlobMetadata(String key, int sizeBytes, String contentType) {}

    public static class StorageNode {
        private final Map<String, byte[]> blobStore = new HashMap<>();
        private final Map<String, BlobMetadata> metaRegistry = new HashMap<>();

        public void putObject(String key, byte[] content, String contentType) {
            blobStore.put(key, content);
            metaRegistry.put(key, new BlobMetadata(key, content.length, contentType));
        }

        public byte[] getObject(String key) { return blobStore.get(key); }
        public BlobMetadata getMetadata(String key) { return metaRegistry.get(key); }
    }

    public static void main(String[] args) {
        StorageNode node = new StorageNode();
        byte[] payload = "PDF Document Data".getBytes();
        node.putObject("doc-1", payload, "application/pdf");

        assert node.getObject("doc-1") != null;
        assert node.getMetadata("doc-1").sizeBytes() == payload.length;

        System.out.println("Day 21 Distributed File Storage LLD verification passed.");
    }
}
