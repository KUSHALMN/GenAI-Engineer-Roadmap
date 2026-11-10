"""
Object Storage and File Lifecycle: S3/Blob Abstraction, Signed URLs,
SHA-256 Checksum Validation, Multipart Uploads, and Retention Policies.
"""

from dataclasses import dataclass
import hashlib
import time
from typing import Dict, Optional


@dataclass
class S3ObjectMetadata:
    bucket: str
    key: str
    size_bytes: int
    content_type: str
    etag_sha256: str
    created_at: float
    retention_days: int


class ObjectStorageLifecycleManager:
    def __init__(self):
        self._storage: Dict[str, bytes] = {}
        self._meta: Dict[str, S3ObjectMetadata] = {}

    def upload_object(self, bucket: str, key: str, data: bytes, content_type: str = "application/pdf", retention_days: int = 30) -> S3ObjectMetadata:
        storage_path = f"{bucket}/{key}"
        sha256_hash = hashlib.sha256(data).hexdigest()
        self._storage[storage_path] = data
        meta = S3ObjectMetadata(
            bucket=bucket,
            key=key,
            size_bytes=len(data),
            content_type=content_type,
            etag_sha256=sha256_hash,
            created_at=time.time(),
            retention_days=retention_days
        )
        self._meta[storage_path] = meta
        return meta

    def generate_presigned_url(self, bucket: str, key: str, expires_in_seconds: int = 300) -> str:
        # Mock pre-signed URL with signature and expiration
        exp = int(time.time() + expires_in_seconds)
        token = hashlib.md5(f"{bucket}/{key}:{exp}".encode("utf-8")).hexdigest()[:12]
        return f"https://s3.amazonaws.com/{bucket}/{key}?X-Amz-Expires={exp}&X-Amz-Signature={token}"

    def purge_expired_objects(self, current_time: Optional[float] = None) -> int:
        now = current_time or time.time()
        purged = 0
        keys_to_delete = []
        for path, meta in self._meta.items():
            expiration_timestamp = meta.created_at + (meta.retention_days * 86400)
            if now > expiration_timestamp:
                keys_to_delete.append(path)

        for path in keys_to_delete:
            del self._storage[path]
            del self._meta[path]
            purged += 1
        return purged


if __name__ == "__main__":
    s3 = ObjectStorageLifecycleManager()
    data = b"%PDF-1.4 Mock document bytes"
    meta = s3.upload_object("genai-docs", "uploads/invoice.pdf", data, retention_days=7)
    assert meta.etag_sha256 == hashlib.sha256(data).hexdigest()

    url = s3.generate_presigned_url("genai-docs", "uploads/invoice.pdf")
    assert "X-Amz-Signature" in url

    # Simulate 8 days passed -> Purge
    purged_count = s3.purge_expired_objects(time.time() + (8 * 86400))
    assert purged_count == 1
    print("=== Day 07: Object Storage Lifecycle ===")
    print("Pre-signed URL generation and retention purge passed.")
